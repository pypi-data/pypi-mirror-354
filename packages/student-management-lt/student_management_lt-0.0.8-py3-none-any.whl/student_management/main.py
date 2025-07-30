"""Student Management System GUI to manage student data.

Provides a student management solution where you can add, edit, delete, and serch students.
"""
from PyQt6.QtWidgets import QApplication
import sys
from student_management.main_window import MainWindow
import argparse


def main():
    parser = argparse.ArgumentParser(description="Student Management System GUI")
    parser.add_argument(
        "--database",
        help="Path to the database file",
        default=None,
    )
    args = parser.parse_args()
    app = QApplication(sys.argv)
    main_window = MainWindow(database_file=args.database)
    main_window.show()
    main_window.load_data()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()