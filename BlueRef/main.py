from PySide6.QtWidgets import (QApplication)
from ui.main_window import MainWindow
import sys

def main_app():
    blueref_software = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(blueref_software.exec())

if __name__ == "__main__":
    main_app()