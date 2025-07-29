import hashlib
import re
import stat
from pathlib import Path
from textwrap import dedent

from dblocks_core import exc
from dblocks_core.config.config import logger
from dblocks_core.deployer import fsequencer
from dblocks_core.model import plugin_model

from dblocks_plugin.jahero_plugin import plug_config, plug_model


class Dpl(plugin_model.PluginWalker):
    def __init__(self):
        self.batch: fsequencer.DeploymentBatch | None = None

    def before(
        self,
        path: Path,
        environment: str | None,
        **kwargs,
    ):
        """
        Prepare the deployment process before the walk starts.

        This method initializes the deployment batch, creates necessary directories,
        and generates deployment scripts based on the steps defined in the batch.

        Args:
            path (Path): The root path of the deployment package.
            environment (str | None): The target environment for the deployment.
            **kwargs: Additional keyword arguments.

        Raises:
            exc.DOperationsError: If required directories or steps are missing.
        """
        # get plugin config
        plug_cfg = plug_config.load_config(path)
        checkpoint_table = plug_cfg.checkpoint_table
        root_dir = self._get_root_dir(path)

        # sanity check
        if not root_dir.is_dir():
            raise exc.DOperationsError(f"directory not found: {root_dir}")

        # get a log directory in the package
        log_dir = path / "log"
        log_dir.mkdir(exist_ok=True)

        self.batch = fsequencer.create_batch(root_dir=root_dir, tgr=None)
        if len(self.batch.steps) == 0:
            raise exc.DOperationsError("Empty batch.")

        exec_scripts = []
        deployment_dir = root_dir.parent / "_deployment"
        log_dir = path / "log"

        deployment_dir.mkdir(exist_ok=True, parents=True)
        log_dir.mkdir(exist_ok=True, parents=True)

        batch_name = path.absolute().as_posix()
        for step in self.batch.steps:
            logger.info(f"creating step: {step.name}")
            statements, prev_db = [], None

            # skip empty steps
            if len(step.files) == 0:
                logger.error(f"empty step: {step.name}")
                continue

            bteq_file = deployment_dir / (step.name + ".bteq")
            exec_scripts.append(_get_bteq_call(bteq_file, log_dir))

            for f in step.files:
                db = f.default_db

                if db is not None and db != prev_db:
                    statements.append(f"\ndatabase {_get_database(db, plug_cfg)};")

                deployed_script = f.file.absolute().as_posix()
                checkpoint_label = _get_checkpoint_label(deployed_script)

                # test if the checkpoint exists
                statements.append(
                    _checkpoint_achieved(
                        checkpoint_table,
                        checkpoint_label,
                    )
                )
                # run the file and create the checkpoint
                statements.append(f".run file = '{deployed_script}'")
                statements.append(
                    _get_checkpoint_insert(
                        checkpoint_table,
                        deployed_script,
                        checkpoint_label,
                        batch_name,
                    )
                )
                statements.append(f".LABEL {checkpoint_label}")
                statements.append("")

                prev_db = db

            if statements:
                script = _get_header() + "\n".join(statements) + _get_footer()
                bteq_file.write_text(script, encoding="utf-8")
            else:
                logger.error(f"EMPTY STEP: {step.name}")

        # prepare checkpoint table creation
        sql = _create_checkpoint_table(plug_cfg)
        create_bteq = deployment_dir / ("__cc_checkpoint__.bteq")
        create_bteq.write_text(sql, encoding="utf-8")

        # prepare cleanup
        sql = (
            _get_header()
            + "\n\n"
            + f"delete from {checkpoint_table} where batch_name = '{batch_name}'\n;"
        )
        commit_bteq = deployment_dir / ("__commit__.bteq")
        commit_bteq.write_text(sql, encoding="utf-8")

        # inject checkpoint table creation and cleanup bteq to the exec
        exec_scripts.insert(0, _get_bteq_call(create_bteq, log_dir))
        exec_scripts.append(_get_bteq_call(commit_bteq, log_dir))

        # prepare exec shell
        runme_file = deployment_dir / "runme.sh"
        script = "#!/bin/bash\n\n" + "\n\n".join(exec_scripts)
        runme_file.write_text(script, encoding="utf-8")
        runme_file.chmod(runme_file.stat().st_mode | stat.S_IEXEC)

    def walker(
        self,
        path: Path,
        environment: str | None,
        **kwargs,
    ):
        pass

    def _get_root_dir(self, path: Path) -> Path:
        pkg_cfg = self.cfg.packager
        if pkg_cfg.case_insensitive_dirs:
            logger.info("case insensitive search")
            subdirs = case_insensitive_search(path, pkg_cfg.steps_subdir)

            if subdirs is None:
                raise exc.DOperationsError(
                    f"subdir not found: {pkg_cfg.steps_subdir}: in {path}"
                )
            root_dir = path / subdirs
        else:
            logger.warning("case SENSITIVE search")
            root_dir = path / pkg_cfg.steps_subdir
        return root_dir

    def after(
        self,
        path: Path,
        environment: str | None,
        **kwargs,
    ):
        pass


def case_insensitive_search(root: Path, subdir: Path) -> Path | None:
    """
    Perform a case-insensitive search for a subdirectory within a root directory.

    This function attempts to locate a subdirectory path within the given root
    directory, ignoring case sensitivity. It traverses the directory structure
    step by step, matching each part of the subdirectory path against the
    available directories in a case-insensitive manner.

    Args:
        root (Path): The root directory where the search begins.
        subdir (Path): The subdirectory path to search for.

    Returns:
        Path | None: The resolved path to the subdirectory if found, or None if
        the subdirectory does not exist.

    Logs:
        Logs the search process, including the directories being searched and
        the target subdirectory path.
    """
    wanted = _path_to_directories(subdir)
    wanted = [s.lower() for s in wanted]
    logger.info(f"searching in: {root}")
    logger.info(f"searching for: {wanted}")
    found_dirs = []

    for i in range(len(wanted)):
        children_dir_names = [
            (d.name.lower(), d.name) for d in root.glob("*") if d.is_dir
        ]
        found = False
        for name_lower, name in children_dir_names:
            if name_lower == wanted[i]:
                found = True
                found_dirs.append(name)
                root = root / name
                break
        if not found:
            return None

    return Path(*found_dirs)


def _path_to_directories(path: Path) -> list[str]:
    elements = []
    curr: Path = path
    prev: Path | None = None

    while curr != prev:
        if curr.name:
            elements.insert(0, curr.name)
        prev = curr
        curr = curr.parent

    return elements


def _get_header() -> str:
    return dedent(
        """
        -----------------------------------------------------------
        .SET SESSION CHARSET 'UTF8'
        .SET WIDTH 256
        .SET ERRORLEVEL UNKNOWN SEVERITY 8;
        .SET ERROROUT STDOUT;
        .SET MAXERROR 1
        -----------------------------------------------------------
        .RUN FILE='/home/jan/Vaults/o2/logon_prod.sql'
        -----------------------------------------------------------
        SET SESSION DATEFORM=ANSIDATE;
        .SET ERRORLEVEL 3624 SEVERITY 0;            -- collect stats - pro neex. stat - projde
        --.SET ERRORLEVEL 3803 SEVERITY 0;          -- projde create tabulky ktera existuje
        --.SET ERRORLEVEL 3807 SEVERITY 0;          -- projde drop tabulky ktera neexistuje
    """
    )


def _get_footer() -> str:
    return ""


def _get_bteq_call(f: Path, log_dir: Path) -> str:
    stem = f.stem
    log_file = log_dir / f"{stem}.log"
    return dedent(
        f"""
        echo "running {stem}"
        bteq < {f.absolute().as_posix()} &>>{log_file.absolute().as_posix()}
        retval=$?
        if [ $retval -ne 0 ]; then
            echo "===============ERROR================="
            echo "====================================="
            exit $retval
        fi
    """
    )


def _create_checkpoint_table(plug_cfg: plug_model.PluginConfig) -> str:
    checkpoint_table = plug_cfg.checkpoint_table
    db, nm = checkpoint_table.split(".")
    sql = _get_header() + dedent(
        f"""

        select count(*) from dbc.tablesV
        where tablename='{nm}' and databasename= '{db}'
        having count(*) > 0
        ;

        .IF ERRORCODE <> 0 THEN .QUIT 10;
        .IF ACTIVITYCOUNT > 0 THEN .GOTO _CHECKPOINT_EXISTS_;

        CREATE TABLE {checkpoint_table} (
            checkpoint_name varchar(1024) CHARACTER SET unicode,
            checkpoint_label varchar(256) CHARACTER SET latin,
            batch_name varchar(1024) CHARACTER SET unicode,
            achieved_dttm timestamp(6) WITH time zone
        ) 
        PRIMARY INDEX (checkpoint_name)
        ;
        .LABEL _CHECKPOINT_EXISTS_
    """
    )
    return sql


def _get_checkpoint_insert(
    checkpoint_table: str,
    checkpoint: str,
    label: str,
    batch_name: str,
) -> str:
    return (
        f"""insert into {checkpoint_table} ( checkpoint_name, batch_name, """
        """checkpoint_label, achieved_dttm) values ("""
        f"""'{checkpoint}', '{batch_name}', '{label}', current_timestamp);"""
    )


def _checkpoint_achieved(checkpoint_table: str, label: str) -> str:
    return "\n".join(
        (
            "select count(1) "
            f"from {checkpoint_table} "
            f"where checkpoint_label = '{label}' "
            "having count(1) > 0;",
            f".IF ACTIVITYCOUNT > 0 THEN .GOTO {label};",
        )
    )


def _get_checkpoint_label(checkpoint: str) -> str:
    # calculate a md5 hash of the checkpoint name, encode it in hex, and take the first 30 characters
    md5 = hashlib.md5(checkpoint.encode("utf-8")).hexdigest()
    return md5[:30]  # bteq only uses first 30 characters of the label


def _get_database(db: str, cfg: plug_model.PluginConfig) -> str:
    for replacement in cfg.replacements:
        db = re.sub(
            replacement.replace_from,
            replacement.replace_to,
            db,
            flags=re.I | re.X,
        )
    return db
