import sqlite3
import student_management.config.cfg as cfg


class DatabaseConnection:
    """Handles database connection
    """

    def __init__(self, database_file: str = None) -> None:
        """Initializes the database connection object.

        Args:
            database_file: The path to the database file.

        Returns:
            None
        """
        self.database_file = database_file or cfg.database_file

    def connect(self) -> sqlite3.Connection:
        """Connects to the database.

        Returns:
            sqlite3.Connection: The database connection object.
        """
        connection = sqlite3.connect(self.database_file)
        return connection