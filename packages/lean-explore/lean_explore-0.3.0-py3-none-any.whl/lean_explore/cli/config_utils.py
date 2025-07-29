# src/lean_explore/cli/config_utils.py

"""Utilities for managing CLI user configurations, such as API keys.

This module provides functions to save and load user-specific settings,
such as API keys for Lean Explore and OpenAI, from a configuration
file stored in the user's home directory. It handles file creation,
parsing, and sets secure permissions for files containing sensitive
information. It also supports loading API keys from environment
variables as a fallback if they are not found in the configuration file.
"""

import logging
import os
import pathlib
from typing import Any, Dict, Optional

import toml

logger = logging.getLogger(__name__)

# Define the application's configuration directory and file name
_APP_CONFIG_DIR_NAME: str = "leanexplore"
_CONFIG_FILENAME: str = "config.toml"

# Define keys for Lean Explore API section
_LEAN_EXPLORE_API_SECTION_NAME: str = "lean_explore_api"
_LEAN_EXPLORE_API_KEY_NAME: str = "key"
_LEAN_EXPLORE_API_KEY_ENV_VAR: str = "LEANEXPLORE_API_KEY"

# Define keys for OpenAI API section
_OPENAI_API_SECTION_NAME: str = "openai"
_OPENAI_API_KEY_NAME: str = "api_key"
_OPENAI_API_KEY_ENV_VAR: str = "OPENAI_API_KEY"


def get_config_file_path() -> pathlib.Path:
    """Constructs and returns the absolute path to the configuration file.

    The path is typically ~/.config/leanexplore/config.toml.

    Returns:
        pathlib.Path: The absolute path to the configuration file.
    """
    config_dir = (
        pathlib.Path(os.path.expanduser("~")) / ".config" / _APP_CONFIG_DIR_NAME
    )
    return config_dir / _CONFIG_FILENAME


def _ensure_config_dir_exists() -> None:
    """Ensures that the configuration directory exists.

    Creates the directory if it's not already present.

    Raises:
        OSError: If the directory cannot be created due to permission issues
                 or other OS-level errors.
    """
    config_file_path = get_config_file_path()
    config_dir = config_file_path.parent
    try:
        config_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Failed to create configuration directory {config_dir}: {e}")
        raise


def _load_config_data(config_file_path: pathlib.Path) -> Dict[str, Any]:
    """Loads configuration data from a TOML file.

    Args:
        config_file_path: Path to the configuration file.

    Returns:
        A dictionary containing the configuration data. Returns an empty
        dictionary if the file does not exist or is corrupted.
    """
    config_data: Dict[str, Any] = {}
    if config_file_path.exists() and config_file_path.is_file():
        try:
            with open(config_file_path, encoding="utf-8") as f:
                config_data = toml.load(f)
        except toml.TomlDecodeError:
            logger.warning(
                "Configuration file %s is corrupted. Treating as empty.",
                config_file_path,
            )
        except Exception as e:
            logger.error(
                "Error reading existing config file %s: %s",
                config_file_path,
                e,
                exc_info=True,
            )
    return config_data


def _save_config_data(
    config_file_path: pathlib.Path, config_data: Dict[str, Any]
) -> bool:
    """Saves configuration data to a TOML file with secure permissions.

    Args:
        config_file_path: Path to the configuration file.
        config_data: Dictionary containing the configuration data to save.

    Returns:
        True if saving was successful, False otherwise.
    """
    try:
        with open(config_file_path, "w", encoding="utf-8") as f:
            toml.dump(config_data, f)
        os.chmod(config_file_path, 0o600)  # Set user read/write only
        return True
    except OSError as e:
        logger.error(
            "OS error saving configuration to %s: %s",
            config_file_path,
            e,
            exc_info=True,
        )
    except Exception as e:
        logger.error(
            "Unexpected error saving configuration to %s: %s",
            config_file_path,
            e,
            exc_info=True,
        )
    return False


# --- Lean Explore API Key Management ---


def save_api_key(api_key: str) -> bool:
    """Saves the Lean Explore API key to the user's configuration file.

    Args:
        api_key: The Lean Explore API key string to save.

    Returns:
        bool: True if the API key was saved successfully, False otherwise.
    """
    if not api_key or not isinstance(api_key, str):
        logger.error("Attempted to save an invalid or empty Lean Explore API key.")
        return False

    config_file_path = get_config_file_path()
    try:
        _ensure_config_dir_exists()
        config_data = _load_config_data(config_file_path)

        if _LEAN_EXPLORE_API_SECTION_NAME not in config_data or not isinstance(
            config_data[_LEAN_EXPLORE_API_SECTION_NAME], dict
        ):
            config_data[_LEAN_EXPLORE_API_SECTION_NAME] = {}

        config_data[_LEAN_EXPLORE_API_SECTION_NAME][_LEAN_EXPLORE_API_KEY_NAME] = (
            api_key
        )

        if _save_config_data(config_file_path, config_data):
            logger.info("Lean Explore API key saved to %s", config_file_path)
            return True
    except Exception as e:
        logger.error(
            "General error during Lean Explore API key saving process: %s",
            e,
            exc_info=True,
        )
    return False


def load_api_key() -> Optional[str]:
    """Loads the Lean Explore API key.

    It first checks the user's configuration file (typically
    ~/.config/leanexplore/config.toml under the section
    `lean_explore_api` with key `key`). If a valid, non-empty API key
    is found there, it is returned.

    If the API key is not found in the configuration file, is empty,
    or is not a string, this function then checks the environment
    variable `LEAN_EXPLORE_API_KEY`. If this environment variable is
    set to a non-empty string, its value is returned.

    If the API key is not found or is invalid in both locations,
    None is returned.

    Returns:
        Optional[str]: The Lean Explore API key string if found and valid,
            otherwise None.
    """
    config_file_path = get_config_file_path()

    # 1. Try loading from config file
    if config_file_path.exists() and config_file_path.is_file():
        try:
            config_data = _load_config_data(config_file_path)
            key_value = config_data.get(_LEAN_EXPLORE_API_SECTION_NAME, {}).get(
                _LEAN_EXPLORE_API_KEY_NAME
            )

            if isinstance(key_value, str) and key_value:  # Non-empty string
                logger.debug(
                    "Lean Explore API key loaded from configuration file %s",
                    config_file_path,
                )
                return key_value
            elif key_value is not None:  # Present but not a valid non-empty string
                logger.warning(
                    "Lean Explore API key found in %s but is not a valid "
                    "non-empty string. "
                    "Will check environment variable %s.",
                    config_file_path,
                    _LEAN_EXPLORE_API_KEY_ENV_VAR,
                )
        except Exception as e:  # Catch unexpected errors during config processing
            logger.error(
                "Error processing configuration file %s for Lean Explore API key: %s. "
                "Will check environment variable %s.",
                config_file_path,
                e,
                _LEAN_EXPLORE_API_KEY_ENV_VAR,
                exc_info=True,
            )
    else:
        logger.debug(
            "Configuration file %s not found. Will check environment "
            "variable %s for Lean Explore API key.",
            config_file_path,
            _LEAN_EXPLORE_API_KEY_ENV_VAR,
        )

    # 2. Try loading from environment variable
    api_key_from_env = os.getenv(_LEAN_EXPLORE_API_KEY_ENV_VAR)

    if isinstance(api_key_from_env, str) and api_key_from_env:  # Non-empty string
        logger.debug(
            "Lean Explore API key loaded from environment variable %s",
            _LEAN_EXPLORE_API_KEY_ENV_VAR,
        )
        return api_key_from_env
    elif api_key_from_env is not None:  # Env var exists but is empty string
        logger.debug(
            "Environment variable %s for Lean Explore API key is set but empty.",
            _LEAN_EXPLORE_API_KEY_ENV_VAR,
        )

    logger.debug(
        "Lean Explore API key not found in configuration file or "
        "valid in environment variable %s.",
        _LEAN_EXPLORE_API_KEY_ENV_VAR,
    )
    return None


def delete_api_key() -> bool:
    """Deletes the Lean Explore API key from the user's configuration file.

    Returns:
        bool: True if the API key was successfully removed or if it did not exist;
              False if an error occurred.
    """
    config_file_path = get_config_file_path()
    if not config_file_path.exists():
        logger.info(
            "No Lean Explore API key to delete: configuration file does not exist."
        )
        return True

    try:
        config_data = _load_config_data(config_file_path)
        api_section = config_data.get(_LEAN_EXPLORE_API_SECTION_NAME)

        if (
            api_section
            and isinstance(api_section, dict)
            and _LEAN_EXPLORE_API_KEY_NAME in api_section
        ):
            del api_section[_LEAN_EXPLORE_API_KEY_NAME]
            logger.info("Lean Explore API key removed from configuration data.")

            if not api_section:  # If the section is now empty
                del config_data[_LEAN_EXPLORE_API_SECTION_NAME]
                logger.info(
                    "Empty '%s' section removed.", _LEAN_EXPLORE_API_SECTION_NAME
                )

            if _save_config_data(config_file_path, config_data):
                logger.info("Lean Explore API key deleted from %s", config_file_path)
                return True
            return False  # Save failed
        else:
            logger.info(
                "Lean Explore API key not found in %s, no deletion performed.",
                config_file_path,
            )
            return True

    except Exception as e:
        logger.error(
            "Unexpected error deleting Lean Explore API key from %s: %s",
            config_file_path,
            e,
            exc_info=True,
        )
    return False


# --- OpenAI API Key Management ---


def save_openai_api_key(api_key: str) -> bool:
    """Saves the OpenAI API key to the user's configuration file.

    The API key is stored in the same TOML formatted file as other configurations,
    under a distinct section. File permissions are set securely.

    Args:
        api_key: The OpenAI API key string to save.

    Returns:
        bool: True if the API key was saved successfully, False otherwise.
    """
    if not api_key or not isinstance(api_key, str):
        logger.error("Attempted to save an invalid or empty OpenAI API key.")
        return False

    config_file_path = get_config_file_path()
    try:
        _ensure_config_dir_exists()
        config_data = _load_config_data(config_file_path)

        if _OPENAI_API_SECTION_NAME not in config_data or not isinstance(
            config_data[_OPENAI_API_SECTION_NAME], dict
        ):
            config_data[_OPENAI_API_SECTION_NAME] = {}

        config_data[_OPENAI_API_SECTION_NAME][_OPENAI_API_KEY_NAME] = api_key

        if _save_config_data(config_file_path, config_data):
            logger.info("OpenAI API key saved to %s", config_file_path)
            return True
    except Exception as e:
        logger.error(
            "General error during OpenAI API key saving process: %s", e, exc_info=True
        )
    return False


def load_openai_api_key() -> Optional[str]:
    """Loads the OpenAI API key.

    It first checks the user's configuration file (typically
    ~/.config/leanexplore/config.toml under the section
    `openai` with key `api_key`). If a valid, non-empty API key
    is found there, it is returned.

    If the API key is not found in the configuration file, is empty,
    or is not a string, this function then checks the environment
    variable `OPENAI_API_KEY`. If this environment variable is
    set to a non-empty string, its value is returned.

    If the API key is not found or is invalid in both locations,
    None is returned.

    Returns:
        Optional[str]: The OpenAI API key string if found and valid, otherwise None.
    """
    config_file_path = get_config_file_path()

    # 1. Try loading from config file
    if config_file_path.exists() and config_file_path.is_file():
        try:
            config_data = _load_config_data(config_file_path)
            key_value = config_data.get(_OPENAI_API_SECTION_NAME, {}).get(
                _OPENAI_API_KEY_NAME
            )

            if isinstance(key_value, str) and key_value:  # Non-empty string
                logger.debug(
                    "OpenAI API key loaded from configuration file %s",
                    config_file_path,
                )
                return key_value
            elif key_value is not None:  # Present but not a valid non-empty string
                logger.warning(
                    "OpenAI API key found in %s but is not a valid non-empty string. "
                    "Will check environment variable %s.",
                    config_file_path,
                    _OPENAI_API_KEY_ENV_VAR,
                )
        except Exception as e:  # Catch unexpected errors during config processing
            logger.error(
                "Error processing configuration file %s for OpenAI API key: %s. "
                "Will check environment variable %s.",
                config_file_path,
                e,
                _OPENAI_API_KEY_ENV_VAR,
                exc_info=True,
            )
    else:
        logger.debug(
            "Configuration file %s not found. Will check environment "
            "variable %s for OpenAI API key.",
            config_file_path,
            _OPENAI_API_KEY_ENV_VAR,
        )

    # 2. Try loading from environment variable
    api_key_from_env = os.getenv(_OPENAI_API_KEY_ENV_VAR)

    if isinstance(api_key_from_env, str) and api_key_from_env:  # Non-empty string
        logger.debug(
            "OpenAI API key loaded from environment variable %s",
            _OPENAI_API_KEY_ENV_VAR,
        )
        return api_key_from_env
    elif api_key_from_env is not None:  # Env var exists but is empty string
        logger.debug(
            "Environment variable %s for OpenAI API key is set but empty.",
            _OPENAI_API_KEY_ENV_VAR,
        )

    logger.debug(
        "OpenAI API key not found in configuration file or valid in "
        "environment variable %s.",
        _OPENAI_API_KEY_ENV_VAR,
    )
    return None


def delete_openai_api_key() -> bool:
    """Deletes the OpenAI API key from the user's configuration file.

    Returns:
        bool: True if the API key was successfully removed or if it did not exist;
              False if an error occurred.
    """
    config_file_path = get_config_file_path()
    if not config_file_path.exists():
        logger.info("No OpenAI API key to delete: configuration file does not exist.")
        return True

    try:
        config_data = _load_config_data(config_file_path)
        api_section = config_data.get(_OPENAI_API_SECTION_NAME)

        if (
            api_section
            and isinstance(api_section, dict)
            and _OPENAI_API_KEY_NAME in api_section
        ):
            del api_section[_OPENAI_API_KEY_NAME]
            logger.info("OpenAI API key removed from configuration data.")

            if not api_section:  # If the section is now empty
                del config_data[_OPENAI_API_SECTION_NAME]
                logger.info("Empty '%s' section removed.", _OPENAI_API_SECTION_NAME)

            if _save_config_data(config_file_path, config_data):
                logger.info("OpenAI API key deleted from %s", config_file_path)
                return True
            return False  # Save failed
        else:
            logger.info(
                "OpenAI API key not found in %s, no deletion performed.",
                config_file_path,
            )
            return True

    except Exception as e:
        logger.error(
            "Unexpected error deleting OpenAI API key from %s: %s",
            config_file_path,
            e,
            exc_info=True,
        )
    return False
