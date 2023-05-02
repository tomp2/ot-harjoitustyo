import sqlite3
import unittest
from pathlib import Path

from skilltracker.database import Database
from skilltracker.settings import SettingRegistry

TESTS_DIR = Path(__file__).parent


class TestDatabase(unittest.TestCase):
    setup_class_db_file = TESTS_DIR / "setup_class_tests.db"
    setup_db_file = TESTS_DIR / "setup_tests.db"

    @classmethod
    def setUpClass(cls):
        database = Database(database_path=cls.temp_test_db_file)
        database.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.setup_class_db_file.unlink()

    def setUp(self):
        self.database = Database(database_path=self.temp_test_db_file)

    def test_instance_creation(self):
        assert self.setup_database._database_path == self.setup_db_file
        assert (
            self.setup_database._init_sqlite_script
            == SettingRegistry.get().database_schema_file
        )

    def test_initialize_creates_file(self):
        database_path = TESTS_DIR / "test_temp.sqlite"
        Database(database_path=database_path).initialize()
        assert database_path.exists() is True

    def test_initialize_creates_tables(self):
        """Test that all the tables are created correctly"""
        with Database(database_path=self.temp_test_db_file).get_cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
        self.assertEqual(tables, ["users"])

    def test_get_connection(self):
        with Database(database_path=self.temp_test_db_file).get_connection() as conn:
            self.assertIsInstance(conn, sqlite3.Connection)

    def test_get_cursor(self):
        with Database(database_path=self.temp_test_db_file).get_cursor() as cursor:
            self.assertIsInstance(cursor, sqlite3.Cursor)


if __name__ == "__main__":
    unittest.main()
