from __future__ import annotations

from typing import TypeVar, Generic, Callable

T = TypeVar("T")


class ObjectRegistry(Generic[T]):
    """Handles registering and providing instances.

    Registry is a global central store for instances which should be
    accessible widely between modules, for example Database, Settings,
    or any Repository objects.

    Using registry avoids re-creating objects needlessly or passing them
    around a lot. Also, global constants or singletons for these
    types of objects could be harder to test and manage.
    """

    def __init__(
        self,
        default_instance_factory: Callable[[], T],
        default_name: str = "default",
    ):
        self.default_name = default_name
        self._registry: dict[str, T] = {}
        self._default_instance_factory = default_instance_factory

    def register(self, name: str, instance: T) -> T:
        """Register an instance with the given name.

        Args:
            name: name for the instance. Used to access it later with `get`.
            instance: instance to register.

        Returns:
            T: the registered instance.

        Raises:
            KeyError: If the name is already taken.
        """
        if name in self._registry:
            raise KeyError(f'Instance with name "{name}" is already registered.')
        return self._registry.setdefault(name, instance)

    def get(self, name: str | None = None) -> T:
        """Return instance with the given name form the registry.

        Args:
            name: name for the instance. Leave empty for default.

        Returns:
            T: from the registry.

        Notes:
            If name isn't given, the default instance is created and/or
            returned.
        """
        if name is not None:
            return self._registry[name]

        default = self._registry.get(self.default_name)
        if default is not None:
            return default

        default = self._default_instance_factory()
        return self.register(self.default_name, default)

    def clear(self) -> None:
        """Unregister everything, including default."""
        self._registry.clear()

    def list(self) -> list[str]:
        """Return a list of all registered names."""
        return list(self._registry.keys())

    def unregister(self, name: str) -> None:
        """Remove the instance with the given name from the registry.

        Args:
            name: name for the instance to remove.

        Raises:
            KeyError: If the name isn't in the register.
        """
        del self._registry[name]
