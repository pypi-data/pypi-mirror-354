from PyQt6.QtWidgets import QVBoxLayout, QLabel, \
    QLineEdit, QPushButton, QDialog, QComboBox
from student_management.db.connection import DatabaseConnection


class InsertDialog(QDialog):
    """Window showing an option to insert a student record."""

    def __init__(self, main_window) -> None:
        """Initializes the Insert window for inserting of student record.

        Returns:
            None
        """
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        
        # Add student name field
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add courses field
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile field
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)
    
    def add_student(self) -> None:
        """Inserts a student record to the database.

        Returns:
            None
        """
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = DatabaseConnection().connect()
        cursor =  connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
            (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_window.load_data()