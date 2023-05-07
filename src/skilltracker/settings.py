from __future__ import annotations

from pathlib import Path
from typing import Final, Literal

from pydantic import (
    BaseSettings,
    FilePath,
    DirectoryPath,
    PositiveInt,
)

from skilltracker.object_registry import ObjectRegistry

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


SETTINGS_REGISTRY = ObjectRegistry(default_instance_factory=Settings)

if __name__ == "__main__":
    # Print the parsed default settings when this module is run as __main__
    print(SETTINGS_REGISTRY.get().json(indent=2))
