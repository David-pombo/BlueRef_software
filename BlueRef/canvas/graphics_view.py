from PySide6.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent, QMouseEvent, QPainter, QDragEnterEvent, QDropEvent, QDragMoveEvent, QPixmap
from canvas.items.image_item import ImageItem

import os


class Graphic_View(QGraphicsView):
    
    def __init__(self, scene, tool_manager, parent=None):
        super().__init__(scene, parent)
        
        self.setAcceptDrops(True)
        self.setScene(scene)
        
        self.tool_manager = tool_manager
        


        self.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform
        )
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setMouseTracking(True)
        self.zoom_factor = 1.5
        print(f"[DEBUG] Scene set in view: {self.scene() is not None}")

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_factor, self.zoom_factor)
        else:
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton and event.modifiers() & Qt.ControlModifier:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.NoDrag)
        super().mouseReleaseEvent(event)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    pixmap = QPixmap(file_path)
                    if not pixmap.isNull():
                        item = ImageItem(pixmap)
                        self.scene().addItem(item)
                        item.setPos(self.mapToScene(event.pos()))  # ✅ fixed
        event.acceptProposedAction()


    def reset_view(self):
        self.resetTransform()
        self.centerOn(0, 0)
    
    def center_on_selected(self):
        selected_items = self.scene().selectedItems()
        if selected_items:
            self.centerOn(selected_items[0])