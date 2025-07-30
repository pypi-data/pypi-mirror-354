from PyQt6.QtWidgets import QVBoxLayout, QLabel, \
    QLineEdit, QPushButton, QDialog, QComboBox
from db.connection import DatabaseConnection


class EditDialog(QDialog):
    """Window showing an option to edit a student record."""

    def __init__(self, main_window) -> None:
        """Initializes the Edit window for updating of student record.

        Returns:
            None
        """
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        # Get stdent name from selected row
        index = self.main_window.table.currentRow()
        student_name = self.main_window.table.item(index, 1).text()
        self.student_id = self.main_window.table.item(index, 0).text()
        # Add student name field
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        course_name = self.main_window.table.item(index, 2).text()
        # Add courses field
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        mobile = self.main_window.table.item(index, 3).text()
        # Add mobile field
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add update button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)
    
    def update_student(self) -> None:
        """Updates a student record to the database.

        Returns:
            None
        """
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?", 
            (self.student_name.text(),
            self.course_name.itemText(self.course_name.currentIndex()),
            self.mobile.text(), 
            self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_window.load_data()