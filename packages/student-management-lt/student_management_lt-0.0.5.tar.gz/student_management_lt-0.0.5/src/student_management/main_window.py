from PyQt6.QtWidgets import QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, \
    QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
from db.connection import DatabaseConnection
from dialogs.about_dialog import AboutDialog
from dialogs.delete_dialog import DeleteDialog
from dialogs.edit_dialog import EditDialog
from dialogs.insert_dialog import InsertDialog
from dialogs.search_dialog import SearchDialog


class MainWindow(QMainWindow):
    """Main application window of the Student Management System.
    """

    def __init__(self) -> None:
        """Initializes the main application window.

        This contains the different menu bar and displays the table of student.

        Returns:
            None
        """
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("resources/icons/add.png"),"Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("resources/icons/search.png"),"Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self) -> None:
        """Handles the click event to show edit and delete options.

        Returns:
            None
        """
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self) -> None:
        """Retrieves the database data and diplays the table.

        Returns:
            None
        """
        connection = DatabaseConnection().connect()
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self) -> None:
        """Display the insert dialog box to add new student.

        Returns:
            None
        """
        dialog = InsertDialog(self)
        dialog.exec()
    
    def search(self) -> None:
        """Display the search dialog box to find student.

        Returns:
            None
        """
        dialog = SearchDialog(self)
        dialog.exec()

    def edit(self) -> None:
        """Display the edit dialog box to update student.

        Returns:
            None
        """
        dialog = EditDialog(self)
        dialog.exec()

    def delete(self) -> None:
        """Display the delete dialog box to remove student.

        Returns:
            None
        """
        dialog = DeleteDialog(self)
        dialog.exec()

    def about(self) -> None:
        """Display the about dialog box to show application information.

        Returns:
            None
        """
        dialog = AboutDialog()
        dialog.exec()