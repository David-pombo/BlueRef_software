from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QTabWidget, QDialog,
    QVBoxLayout, QLabel, QWidget, QMessageBox, QToolBar, QToolButton, QPushButton
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from ui.dialogs import NewTabDialog
from core.tool_manager import ToolType, ToolManager

# load canvas into each tab
from canvas.graphics_scene import Graphic_Scene
from canvas.graphics_view import Graphic_View



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BlueRef")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(1000, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_menu_bar()
        
        self.tool_manager = ToolManager()
        self.create_toolbar()

        
        
    def create_toolbar(self):
        toolbar = QToolBar("Tools")
        self.addToolBar(toolbar)
        
        select_button = QPushButton("Select", self.tool_manager, ToolType.SELECT)
        scale_button = QPushButton("Scale", self.tool_manager, ToolType.SCALE)
        rotate_button = QPushButton("Rotate", self.tool_manager, ToolType.ROTATE)
        
        select_button.clicked.connect(lambda: self.tool_manager.set_tool(ToolType.SELECT))
        scale_button.clicked.connect(lambda: self.tool_manager.set_tool(ToolType.SCALE))
        rotate_button.clicked.connect(lambda: self.tool_manager.set_tool(ToolType.ROTATE))
        
        toolbar.addWidget(select_button)
        toolbar.addWidget(scale_button)
        toolbar.addWidget(rotate_button)
    

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("File")

        new_tab_action = QAction("New", self)
        new_tab_action.triggered.connect(self.create_tab_widget)
        
        delete_tab_action = QAction("Delete WorkSpace Tab", self)
        delete_tab_action.triggered.connect(self.delete_tabs)
        delete_tab_action.setShortcut("Ctrl+W")

        save_action = QAction("Save", self)
        open_action = QAction("Open", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addActions([new_tab_action, delete_tab_action, save_action, open_action, exit_action])

        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        fullscreen_action = QAction("Full Screen", self)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        edit_menu.addAction(fullscreen_action)
        
        reset_view_action = QAction("Reset View", self)
        reset_view_action.setShortcut("Ctrl+0")
        reset_view_action.triggered.connect(lambda: self.get_current_view() and self.get_current_view().reset_view())

        center_selected_action = QAction("Center on Selection", self)
        center_selected_action.setShortcut("F")
        center_selected_action.triggered.connect(lambda: self.get_current_view() and self.get_current_view().center_on_selected())


        edit_menu.addAction(reset_view_action)
        edit_menu.addAction(center_selected_action)

        

    def create_tab_widget(self):
        dialog = NewTabDialog(self)
        #dialog.setWindowModality(Qt.ApplicationModal)
        dialog.raise_()
        dialog.activateWindow()

        if dialog.exec():
            tab_name = dialog.get_tab_name()
            
            if not tab_name:
                QMessageBox.warning(self, "Warning", "Please enter a atab name.")
                return
            
            print(f"[DEBUG] Creating tab with name: {tab_name}")
            
            scene = Graphic_Scene()
            view = Graphic_View(scene)

            container = QWidget()
            
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f"Tab: {tab_name}"))  # Add a label for the tab name
            layout.addWidget(view)
            container.setLayout(layout)

            self.tabs.addTab(container, tab_name)
    
    def delete_tabs(self):
        current_index = self.tabs.currentIndex()
        print(f"[DEBUG] Current tab index: {current_index}")

        if current_index == -1:
            QMessageBox.information(self, "Warning", "No tab selected to delete.")
            return

        tab_name = self.tabs.tabText(current_index)
        print(f"[DEBUG] Tab to delete: {tab_name}")
        
        confirm = QMessageBox.question(
            self,
            "Delete Tab",
            f"You are about to delete:\nTab: '{tab_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.tabs.removeTab(current_index)
            print(f"[DEBUG] Tab '{tab_name}' deleted")



    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def get_current_view(self):
        current_widget = self.tabs.currentWidget()
        if current_widget:
            views = current_widget.findChildren(Graphic_View)
            if views:
                return views[0]
        return None