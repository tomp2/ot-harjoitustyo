import tempfile
import unittest
import sqlite3
from pathlib import Path
from unittest.mock import patch

from skilltracker.config import DEFAULT_CONFIG
from skilltracker.database import Database, get_default_database

TESTS_DIR = Path(__file__).parent


class TestDatabase(unittest.TestCase):
    temp_test_db_file = TESTS_DIR / "tests.db"

    @classmethod
    def setUpClass(cls):
        database = Database(database_path=cls.temp_test_db_file)
        database.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.temp_test_db_file.unlink()

    def setUp(self):
        self.database = Database(database_path=self.temp_test_db_file)

    def test_get_default_database_initializes(self):
        with patch("skilltracker.database.Database.initialize") as initialize_mock:
            get_default_database()
            self.assertTrue(initialize_mock.called)

    def test_instance_creation(self):
        default_db = Database()
        assert default_db._database_path == DEFAULT_CONFIG["paths"]["database_file"]
        assert (
            default_db._init_sqlite_script == DEFAULT_CONFIG["paths"]["database_schema"]
        )

        database_path = Path("testpath")
        database_script = Path("testscript")
        custom_db = Database(database_path=database_path, schema_script=database_script)
        assert custom_db._database_path == database_path
        assert custom_db._init_sqlite_script == database_script

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
