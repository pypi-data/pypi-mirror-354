import os
import yaml

config_name_key = "name"
config_desc_key = "description"
settings_key = "settings"
bump_type_key = "bump_type"
files_key = "files"

change_log_file_key = "change_log_file"


def open_config_file(config_path: os.PathLike) -> dict:
    """
    Open a yaml configuration file and return as a dict
    Args:
        config_path(os.PathLike): path to config file
    Returns:
        dict: app config in dict structure
    Raises:
        FileNotFoundError: config file is not found
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Config file {config_path} was not found")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def write_config_file(config_path, config):
    with open(config_path, "w") as f:
        yaml.dump(config, f, sort_keys=False)


def validate_config(config: dict) -> bool:
    """
    Checks if the config dict contains
    all required fields in the expected format
    Returns:
        bool
    """
    return True


def parse_config_arguments(
    config_path: os.PathLike,
) -> tuple[list[str], bool, bool, bool, bool]:
    """
    Parse the arguments in the config file
    Args:
        config(os.PathLike): path to the config file
    Returns:
        tuple(list[str], bool, bool, bool, bool):
        list of paths to files with version numbers and boolean flags for bump version type
    Raises:
        ValueError: config file is invalid
        ValueError: major bump type provided in config file
    """
    is_dry_run = False
    config = open_config_file(config_path)
    ### if config not complete, raise error
    if not validate_config(config):
        raise ValueError("Config file is invalid")
    bump_type: str = config[settings_key][bump_type_key]
    if bump_type == "major":
        raise ValueError(
            "Major version bumping is not supported with a config file. Use CLI instead"
        )
    is_minor, is_patch = get_bump_flags(bump_type)
    is_major = False
    files = config[settings_key][files_key]

    return files, is_major, is_minor, is_patch, is_dry_run


def get_bump_flags(bump_type: str) -> tuple[bool, bool]:
    """
    Convert string bump type to boolean flags.
    If the version type is not recognized, set to patch
    Args:
        bump_type(str): bump type (major, minor, patch)
    Returns:
        list(bool, bool):
        List of boolean flags. Only one is true
    """
    is_minor = False
    is_patch = False

    if bump_type == "minor":
        is_minor = True
    elif bump_type == "patch":
        is_patch = True
    else:
        # Default to patch if unrecognized
        is_patch = True

    return is_minor, is_patch


def get_change_log_file(config_path):
    config = open_config_file(config_path)
    change_log_file = config[settings_key][change_log_file_key]
    return change_log_file


def set_change_log_file(config_path, new_name):
    config = open_config_file(config_path)
    config[settings_key][change_log_file_key] = new_name
    write_config_file(config_path, config)


if __name__ == "__main__":
    conf_dir = "/home/wsl/projects/forks/bump_version/bump_config.yml"
    f = get_change_log_file(conf_dir)
    print(f)
    set_change_log_file(conf_dir, "new_config.md")
    f = get_change_log_file(conf_dir)
    print(f)
