import os
from pathlib import Path
from typing import Final
from dotenv import load_dotenv
from skilltracker import utils

PACKAGE_ROOT: Final[Path] = Path(__file__).parent
SRC_ROOT: Final[Path] = PACKAGE_ROOT.parent
REPOSITORY_ROOT: Final[Path] = SRC_ROOT.parent
INCLUDED_DATA_DIR_PATH: Final[Path] = PACKAGE_ROOT / "data"

APP_DEFAULT_DOTENV_PATH: Final[Path] = INCLUDED_DATA_DIR_PATH / ".env"
load_dotenv(APP_DEFAULT_DOTENV_PATH)

DATABASE_CREATE_SCRIPT: Final[Path] = INCLUDED_DATA_DIR_PATH / "create_tables.sql"

with utils.as_working_dir(REPOSITORY_ROOT):
    APP_DATA_DIR_PATH: Final[Path] = Path(os.getenv("APP_DATA_DIR_PATH")).resolve()
    APP_DATA_DIR_PATH.mkdir(exist_ok=True, parents=True)
    DATABASE_FILEPATH: Final[Path] = Path(os.getenv("DATABASE_FILEPATH")).resolve()
