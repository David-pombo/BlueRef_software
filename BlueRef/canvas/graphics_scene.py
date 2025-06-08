from PySide6.QtWidgets import (QGraphicsScene, QGraphicsPixmapItem)
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QMouseEvent, QTransform
from PySide6.QtCore import Qt, QUrl
import os

class Graphic_Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, 5000, 5000) 
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    event.acceptProposedAction()
                    return
        event.ignore()
    
    def dragMoveEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    pixmap = QPixmap(file_path)
                    if not pixmap.isNull():
                        item = QGraphicsPixmapItem(pixmap)
                        item.setFlags(QGraphicsPixmapItem.ItemIsMovable | QGraphicsPixmapItem.ItemIsSelectable)
                        item.setPos(event.scenePos())
                        self.addItem(item)
        event.acceptProposedAction()