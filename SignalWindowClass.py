# Signal Window Class
# Generates and independent window with a copy of the edf and xml object loaded by the Sleep Science Window.
#

# Sleep Science Classes
from EdfFileClass import EdfHeader, EdfSignalHeader, EdfSignals, EdfSignal, EdfFile
from AnnotationXmlClass import AnnotationXml, SignalAnnotations, SleepStages

# Interface packages and modules
from PySide6.QtWidgets import QMainWindow
from SignalViewer import Ui_SignalWindow  # the generated file from your .ui

class SignalWindow(QMainWindow):
    def __init__(self, edf_obj:EdfFile=None, xml_obj:AnnotationXml=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_SignalWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Signal Viewer")

        # Make a copy of the edf and xml information
        self.edf_obj = edf_obj
        self.xml_obj = xml_obj

        self.signal_labels = self.edf_obj.edf_signals.signal_labels
        self.ui.comboBox_signals.addItems(self.signal_labels )


    def initialize_window_widgets(self):
        # Set up window widgets

        self.ui.comboBox_signals.connect(update_signal_combobox)

    def update_signal_combobox (self):
        pass

