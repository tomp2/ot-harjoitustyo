import unittest

import pytest

from skilltracker.object_registry import ObjectRegistry


class TestObjectRegistry(unittest.TestCase):
    def setUp(self):
        self.object_registry = ObjectRegistry(default_instance_factory=list)

    def test_register(self):
        obj = ["testing"]
        self.object_registry.register("test_name", obj)
        assert self.object_registry.get("test_name") == obj

        with pytest.raises(KeyError):
            self.object_registry.register("test_name", obj)

    def test_get_default(self):
        obj = []

        def test_factory():
            obj.append("called")
            return obj

        object_registry = ObjectRegistry(default_instance_factory=test_factory)
        assert object_registry.get() == ["called"]
        assert object_registry.get() == ["called"]

    def test_get_registered_name(self):
        obj = ["testing"]
        self.object_registry.register("test_name", obj)
        assert self.object_registry.get("test_name") == obj

    def test_get_unregistered_name(self):
        with pytest.raises(KeyError):
            self.object_registry.get("unregistered_name")

    def test_clear(self):
        obj = [1, 2, 3, 4]
        self.object_registry.register("test_name", obj)
        self.object_registry.clear()
        with pytest.raises(KeyError):
            self.object_registry.get("test_name")

    def test_list(self):
        obj_1 = ["testing_1"]
        obj_2 = ["testing_2"]
        self.object_registry.register("object_1", obj_1)
        self.object_registry.register("object_2", obj_2)
        assert self.object_registry.list() == ["object_1", "object_2"]

    def test_unregister(self):
        obj = ["testing_1"]
        self.object_registry.register("test_name", obj)
        self.object_registry.unregister("test_name")
        with pytest.raises(KeyError):
            self.object_registry.get("test_name")
