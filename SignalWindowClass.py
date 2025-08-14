from PySide6.QtWidgets import QMainWindow
from SignalViewer import Ui_SignalWindow  # the generated file from your .ui

class SignalWindow(QMainWindow):
    def __init__(self, signal_data=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_SignalWindow()
        self.ui.setupUi(self)

        self.signal_data = signal_data
        self.setWindowTitle("Signal Viewer")

