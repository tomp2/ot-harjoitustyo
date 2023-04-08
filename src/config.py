import os
from pathlib import Path
from typing import Final
from dotenv import load_dotenv
import utils

SOURCES_ROOT: Final[Path] = Path(__file__).parent
REPOSITORY_ROOT: Final[Path] = SOURCES_ROOT.parent
INCLUDED_DATA_DIR_PATH: Final[Path] = SOURCES_ROOT / "data"

APP_DEFAULT_DOTENV_PATH: Final[Path] = INCLUDED_DATA_DIR_PATH / ".env"

load_dotenv(APP_DEFAULT_DOTENV_PATH)

with utils.as_working_dir(REPOSITORY_ROOT):
    APP_DATA_DIR_PATH = Path(os.getenv("APP_DATA_DIR_PATH")).resolve()
    APP_DATA_DIR_PATH.mkdir(exist_ok=True, parents=True)
    DATABASE_FILEPATH = Path(os.getenv("DATABASE_FILEPATH")).resolve()
