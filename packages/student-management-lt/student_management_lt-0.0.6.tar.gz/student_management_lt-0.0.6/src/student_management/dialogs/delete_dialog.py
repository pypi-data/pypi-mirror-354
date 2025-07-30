from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QDialog, QMessageBox
from db.connection import DatabaseConnection


class DeleteDialog(QDialog):
    """Window showing an option to delete a student record."""

    def __init__(self, main_window) -> None:
        """Initializes the Delete window for deletion of student record.

        Returns:
            None
        """
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()

        index = self.main_window.table.currentRow()
        self.student_id = self.main_window.table.item(index, 0).text()

        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.delete_student)
        
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

    def delete_student(self) -> None:
        """Deletes a student record to the database.

        Returns:
            None
        """
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (self.student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully.")
        confirmation_widget.exec()