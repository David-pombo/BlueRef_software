from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton)
from PySide6.QtCore import Qt

class NewTabDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New WorkSpace Tab")
        self.setMinimumSize(130, 70)
        self.setWindowModality(Qt.ApplicationModal)

        self.layout = QVBoxLayout()
        
        self.label = QLabel("Enter the name of the new WorkSpace:")
        self.line_edit = QLineEdit()
        self.ok_button = QPushButton("Create New WorkSpace")
        self.ok_button.clicked.connect(self.accept)
        
        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.ok_button)
        self.setLayout(self.layout)

        self.raise_()
        self.activateWindow()

        # Center on parent
        if parent:
            geo = parent.geometry()
            self.move(
                geo.center().x() - self.width() // 2,
                geo.center().y() - self.height() // 2
            )

    def get_tab_name(self):
        return self.line_edit.text().strip()
