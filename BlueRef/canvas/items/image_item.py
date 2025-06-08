from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF
from core.tool_manager import ToolManager


class ImageItem(QGraphicsPixmapItem):
    def __init__(self, pixmap: QPixmap):
        super().__init__(pixmap)
        self.original_pixmap = pixmap
        
        self.setPixmap(pixmap)
        self.setScale(1.0)
        
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self._resizing = False
        self._resize_handle_size = 10
        self._original_rect = QRectF()
        
        self.tool_manager = None
        

    def boundingRect(self):
        rect = super().boundingRect()
        return rect.adjusted(-5, -5, 5, 5)

    def paint(self, painter: QPainter, option, widget):
        super().paint(painter, option, widget)
        if self.isSelected():
            pen = QPen(Qt.DashLine)
            pen.setColor(Qt.blue)
            painter.setPen(pen)
            painter.drawRect(self.pixmap().rect())

            # Draw resize handle in bottom-right
            painter.setBrush(QColor(0, 120, 255))
            painter.setPen(Qt.NoPen)
            handle_size = self._resize_handle_size
            handle_pos = self.boundingRect().bottomRight() - QPointF(handle_size, handle_size)
            painter.drawRect(QRectF(handle_pos, QSizeF(handle_size, handle_size)))

    def mousePressEvent(self, event):
        if self.tool_manager and self.tool_manager.get_tool() == ToolManager.SCALE:
            #self.setCursor(Qt.SizeFDiagCursor)
            self._resizing = True
            #self._original_rect = self.pixmap().rect()
            self._resize_start_pos = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._resizing:
            delta = event.pos() - self._resize_start_pos

            original_width = self._original_rect.width()
            original_height = self._original_rect.height()

            new_width = max(10, original_width + delta.x())
            new_height = max(10, original_height + delta.y())

             # '''Compute uniform scale based on dominant axis'''
            x_scale = new_width / original_width
            y_scale = new_height / original_height
            scale_factor = max(x_scale, y_scale)  # Choose larger to avoid shrink override

            # '''Clamp scale'''
            scale_factor = max(0.1, min(10.0, scale_factor))

            self.setScale(scale_factor)
        else:
            super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if self._resizing:
            self._resizing = False
        else:
            super().mouseReleaseEvent(event)

    def _on_resize_handle(self, pos):
        handle_size = self._resize_handle_size
        handle_rect = QRectF(
            self.boundingRect().bottomRight() - QPointF(handle_size, handle_size),
            QSizeF(handle_size, handle_size)
        )
        return handle_rect.contains(pos)
