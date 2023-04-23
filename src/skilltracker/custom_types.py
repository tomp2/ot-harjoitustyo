import sys
from typing import TypeAlias, Union

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

DpgTag: TypeAlias = Union[int, str]

__all__ = ["DpgTag", "Self"]
