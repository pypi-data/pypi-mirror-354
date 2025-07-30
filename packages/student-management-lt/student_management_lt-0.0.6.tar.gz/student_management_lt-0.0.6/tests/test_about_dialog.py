import unittest
from PyQt6.QtWidgets import QApplication
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/student_management')))
from dialogs.about_dialog import AboutDialog

# Required for QApplication instance
app = QApplication(sys.argv)

class TestAboutDialog(unittest.TestCase):
    def setUp(self):
        """Create an instance of the AboutDialog before each test."""
        self.dialog = AboutDialog()

    def test_window_title(self):
        """Test if the window title is set correctly."""
        self.assertEqual(self.dialog.windowTitle(), "About")

    def test_content_text(self):
        """Test if the dialog text is set correctly."""
        expected_text = """
        This app was created the course "The Python Mega Course".
        Feel free to modify and reuse this app.
        """
        self.assertEqual(self.dialog.text(), expected_text)

    def tearDown(self):
        """Clean up after each test."""
        self.dialog.close()

if __name__ == "__main__":
    unittest.main()