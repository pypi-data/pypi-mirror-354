"""Student Management System GUI to manage student data.

Provides a student management solution where you can add, edit, delete, and serch students.
"""
from PyQt6.QtWidgets import QApplication
import sys
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.load_data()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()