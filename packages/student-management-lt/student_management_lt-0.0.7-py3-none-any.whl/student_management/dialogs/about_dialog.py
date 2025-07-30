from PyQt6.QtWidgets import QMessageBox


class AboutDialog(QMessageBox):
    """Window showing information about the application."""

    def __init__(self) -> None:
        """Initializes the About window with application information.

        Returns:
            None
        """
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created the course "The Python Mega Course".
        Feel free to modify and reuse this app.
        """
        self.setText(content)