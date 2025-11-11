from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtCore import Qt, QPoint

class CustomFigureCanvas(FigureCanvasQTAgg):
    def __init__(self, figure, parent_view):
        super().__init__(figure)
        self.parent_view = parent_view

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # Translate local position to global for the menu
            global_pos = self.mapToGlobal(event.pos())
            self.parent_view.show_context_menu(self.parent_view.mapFromGlobal(global_pos))
        else:
            super().mousePressEvent(event)

