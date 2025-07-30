import os
import sqlite3
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/student_management')))
from db.connection import DatabaseConnection

class TestDatabaseConnection(unittest.TestCase):
    """Test cases for database connection
    """
    def test_connect_returns_sqlite_connection(self) -> None:
        """Tests that `connect()` returns an instance of sqlite3.Connection.
        """
        test_db = "test_database.db"

        db = DatabaseConnection(test_db)
        connection = db.connect()

        self.assertIsInstance(connection, sqlite3.Connection)
        connection.close()
        if os.path.exists(test_db):
            os.remove(test_db)

if __name__ == "__main__":
    unittest.main()
