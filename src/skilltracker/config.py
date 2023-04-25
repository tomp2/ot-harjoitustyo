from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import tomli

from skilltracker.utils import walk_nested_mapping

PACKAGE_ROOT: Final[Path] = Path(__file__).parent


@dataclass
class _ConfigPaths:
    package_root: Path
    user_data: Path
    icons: Path
    database_schema: Path
    database_file: Path


class Config:
    """Class that handles reading, parsing, and providing config values from file."""

    CONFIG_PATH = PACKAGE_ROOT / "resources" / "app_config.toml"

    def __init__(self, config_path: Path = CONFIG_PATH):
        self._config_path = config_path
        self._toml_dict: dict | None = None
        self._paths: _ConfigPaths | None = None

    def _substitute_config_file_variables(self):
        paths_section = self.dict["paths"]
        if paths_section["package_root"] == "":
            paths_section["package_root"] = str(PACKAGE_ROOT)

        path_variable_regex = re.compile(paths_section["path_variable_regex"])

        for keys, mapping, path_string in walk_nested_mapping(paths_section):
            if not isinstance(path_string, str):
                continue
            if keys[-1] == "path_variable_regex":
                continue

            # Fix possible unnecessary path separators
            mapping[keys[-1]] = str(Path(path_string))

            path_variables = list(path_variable_regex.finditer(path_string))
            if not path_variables:
                continue

            for match in path_variables:
                match_str, varname = match.group(0), match.group(1)
                mapping[keys[-1]] = path_string.replace(match_str, paths_section[varname])

    def _resolve_paths(self):
        paths_section = self.dict["paths"]
        for keys, mapping, path_string in walk_nested_mapping(paths_section):
            if not isinstance(path_string, str):
                continue
            if keys[-1] == "path_variable_regex":
                continue
            mapping[keys[-1]] = Path(path_string).expanduser().resolve()

    def initialize(self):
        """Read and parse the config file."""
        self._toml_dict = tomli.load(self._config_path.open("rb"))
        self._substitute_config_file_variables()
        self._resolve_paths()
        self.dict["paths"]["user_data"].mkdir(parents=True, exist_ok=True)

    @property
    def dict(self) -> dict:
        """Get all configs as a dictionary."""
        if self._toml_dict is None:
            self.initialize()
        return self._toml_dict

    def __getitem__(self, item):
        return self.dict[item]


DEFAULT_CONFIG: Final[Config] = Config()


if __name__ == "__main__":
    import json

    print(json.dumps(DEFAULT_CONFIG.dict, indent=2, default=repr))
