import sys
import tomllib
from pathlib import Path

import cattr
import tomlkit
from dblocks_core import exc
from dblocks_core.config.config import logger
from rich import console, prompt

from dblocks_plugin.jahero_plugin import plug_model

CONFIG_FILE_NAME = "dblocks-jahero-plugin.toml"


def load_config(from_dir: Path) -> plug_model.PluginConfig:
    """
    Load the plugin configuration from a specified directory.

    This function checks if the configuration file exists in the given directory.
    If the file does not exist, it writes a default configuration file and raises
    a `DConfigError`. If the file exists, it reads and parses the configuration
    file into a `PluginConfig` object.

    Args:
        from_dir (Path): The directory where the configuration file is expected to be located.

    Returns:
        plug_model.PluginConfig: The parsed configuration object.

    Raises:
        exc.DConfigError: If the configuration file is not found in the specified directory.
    """
    # check that the file exists
    config_file = from_dir / CONFIG_FILE_NAME
    if not config_file.is_file():
        msg = f"config file not found: {config_file.as_posix()}"
        logger.warning(msg)
        write_default_config(config_file)
        raise exc.DOperationsError(f"config file not found: {config_file.as_posix()}")

    # load it
    logger.info(f"read config from {config_file}")
    data = tomllib.loads(config_file.read_text(encoding="utf-8"))
    cfg = cattr.structure(data, plug_model.PluginConfig)
    return cfg


def write_default_config(file: Path):
    """
    Create a default configuration file if it does not exist.

    This function prompts the user to confirm whether they want to create a default
    configuration file. If the user agrees, it generates a default configuration,
    serializes it to TOML format, and writes it to the specified file.

    Args:
        file (Path): The path where the default configuration file will be created.

    Returns:
        None
    """
    cnsl = console.Console()
    cnsl.print(file.as_posix(), style="green")
    answer = ""

    while answer not in ("Y", "n"):
        cnsl.print("We will create default config to file: ", style="bold blue", end="")
        cnsl.print(file.as_posix())
        answer = prompt.Prompt().ask(
            "Do you want to create file with default config? [Y/n]",
            default="Y",
        )
    if answer != "Y":
        cnsl.print("Canceled.", style="bold red")
        raise exc.DConfigError("missing plugin config")

    cfg = make_default_config()
    data = cattr.unstructure(cfg)
    string = tomlkit.dumps(data, sort_keys=True)
    cns = console.Console()
    cns.print(f"Write to file: {file.as_posix()}")
    file.parent.mkdir(exist_ok=True, parents=True)
    file.write_text(string, encoding="utf-8")
    raise exc.DConfigError("plugin config was just created, please try again")


def make_default_config() -> plug_model.PluginConfig:
    """
    Generate a default plugin configuration.

    This function creates a default `PluginConfig` object with predefined
    replacements and conditional creation settings. The configuration includes
    rules for replacing patterns in strings and conditions for creating files
    in specific paths.

    Returns:
        plug_model.PluginConfig: The default plugin configuration object.
    """
    return plug_model.PluginConfig(
        replacements=[
            plug_model.Replacement(
                replace_from="^EP_CVM(.*)$",
                replace_to=(r"ED1_CVM\1"),
            ),
            plug_model.Replacement(replace_from="^EP_(.*)$", replace_to=(r"ED0_\1")),
            plug_model.Replacement(replace_from="^AP_(.*)$", replace_to=(r"AD0_\1")),
            plug_model.Replacement(replace_from="^VP_(.*)$", replace_to=(r"VD0_\1")),
        ],
        cc=plug_model.ConditionalCreate(
            max_files=50,
            conditionals=[
                plug_model.ConditionalCreatePath(
                    path=Path("DB/Teradata/01-copy-source-ddl-tbl"),
                    scenario=plug_model.DROP,
                    input_encoding="utf-8",
                    output_encoding="utf-8",
                )
            ],
        ),
        checkpoint_table=plug_model.CHECKPOINT_TABLE,
    )
