from __future__ import annotations

from pathlib import Path
from typing import Final, Literal

from pydantic import (
    BaseSettings,
    FilePath,
    DirectoryPath,
    PositiveInt,
)

PACKAGE_ROOT: Final[Path] = Path(__file__).parent


class Settings(BaseSettings):
    # App auto login
    login: None | tuple[str, str] = None

    # App files and directories
    user_data_folder: DirectoryPath = PACKAGE_ROOT / "user_data/"
    database_file: FilePath = PACKAGE_ROOT / "user_data/user_data.sqlite"
    icons_folder: DirectoryPath = PACKAGE_ROOT / "resources/icons"
    database_schema_file: FilePath = PACKAGE_ROOT / "resources/create_tables.sql"
    font_file: FilePath = PACKAGE_ROOT / "resources/Roboto.ttf"

    # User interface
    viewport_shape: tuple[PositiveInt, PositiveInt] = (1100, 800)

    # Debugging
    custom_render_loop: bool = False
    log_level: Literal["debug", "info", "warning", "error", "critical"] = "info"


class SettingRegistry:
    """Handles registering and providing Settings instances."""

    DEFAULT_NAME: Final[str] = "default"
    _registry: dict[str, Settings] = {}

    @classmethod
    def register(cls, name: str, settings: Settings) -> Settings:
        """Register a Settings instance with the given name.

        Args:
            name: name for the instance. Used to access it later with `get`.
            settings: Settings instance to register.

        Returns:
            Settings: the registered Settings instance.

        Raises:
            ValueError: If the name is already taken.
        """
        if name in cls._registry:
            raise ValueError(f'Settings with name "{name}" is already registered.')
        if name == cls.DEFAULT_NAME and cls.DEFAULT_NAME in cls._registry:
            raise ValueError(
                'Name "default" is reserved for registry\'s default Settings instance.'
            )

        cls._registry[name] = settings
        return settings

    @classmethod
    def get(cls, name: str = DEFAULT_NAME) -> Settings:
        """Return Settings instance with the given name form the registry.

        Args:
            name: name for the instance. Defaults to "default".

        Returns:
            Settings: from the registry.
        """
        return cls._registry[name]


# Register default settings on module load
SettingRegistry.register(SettingRegistry.DEFAULT_NAME, Settings())

if __name__ == "__main__":
    # Print the parsed default settings when this module is run as __main__
    print(SettingRegistry.get().json(indent=2))
