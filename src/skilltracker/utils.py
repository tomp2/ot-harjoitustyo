from __future__ import annotations

import os
from collections import abc
from contextlib import contextmanager
from os import PathLike
from typing import Generator, Any, Iterator


@contextmanager
def as_working_dir(working_dir: PathLike[str]) -> Generator[PathLike[str], Any, None]:
    previous_working_dir = os.getcwd()
    os.chdir(working_dir)
    try:
        yield working_dir
    finally:
        os.chdir(previous_working_dir)


def walk_nested_mapping(
    mapping: abc.MutableMapping, max_depth: int = 10, _keys: None | list | tuple = ()
) -> Iterator[tuple[list[Any], abc.MutableMapping, Any]]:
    """Recursively walk mapping, yielding current key-list, parent mapping and value."""
    for key, value in mapping.items():
        if isinstance(value, abc.MutableMapping):
            if max_depth == 0:
                return
            yield from walk_nested_mapping(value, max_depth - 1, [*_keys, key])
        else:
            yield [*_keys, key], mapping, value


def mapping_nested_access(mapping: abc.Mapping, keys):
    """Access nested values in a mapping with"""
    for key in keys:
        mapping = mapping[key]
    return mapping
