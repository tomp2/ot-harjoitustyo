import os
from contextlib import contextmanager
from os import PathLike
from typing import Generator, Any


@contextmanager
def as_working_dir(working_dir: PathLike[str]) -> Generator[PathLike[str], Any, None]:
    previous_working_dir = os.getcwd()
    os.chdir(working_dir)
    try:
        yield working_dir
    finally:
        os.chdir(previous_working_dir)
