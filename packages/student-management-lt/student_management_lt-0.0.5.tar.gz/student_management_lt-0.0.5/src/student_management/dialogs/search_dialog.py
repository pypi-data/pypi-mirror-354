from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, \
    QLineEdit, QPushButton, QDialog
from db.connection import DatabaseConnection


class SearchDialog(QDialog):
    """Window showing an option to search a student record."""

    def __init__(self, main_window) -> None:
        """Initializes the Search window for searching of student record.

        Returns:
            None
        """
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        
        # Add student name field
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add search button
        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)
    
    def search(self) -> None:
        """Search a student record to the database.

        Returns:
            None
        """
        name = self.student_name.text()
        connection = DatabaseConnection().connect()
        cursor =  connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?",
            (name,))
        rows = list(result)
        print(rows)
        items = self.main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            self.main_window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()