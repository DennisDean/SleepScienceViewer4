

# GUI Interface
from CreateBatchFileClass import Ui_MainWindow

class BatchWindowClass(QMainWindow)
    def init(self):

        # Setup and Draw Window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Create Batch File")

