# Signal Window Class
# Generates and independent window with a copy of the edf and xml object loaded by the Sleep Science Window.
#

# Modules
import logging

# Sleep Science Classes
from EdfFileClass import EdfHeader, EdfSignalHeader, EdfSignals, EdfSignal, EdfFile
from AnnotationXmlClass import AnnotationXml, SignalAnnotations, SleepStages

# Interface packages and modules
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QEvent, Qt, QObject

# GUI Interface
from SignalViewer import Ui_SignalWindow  # the generated file from your .ui

# Set up a module-level logger
logger = logging.getLogger(__name__)

# To Do List
# TODO: Setup epoch buttons
# TODO" Load Signal for drawing
# TODO: Draw signals
# TODO: Respond to epoch change
# TODO: Add Epoch Number to Signals
# TODO: Push Button update name does not conform with other buttons

# Utilities
class NumericTextEditFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
                return False  # Allow backspace and delete
            if event.text().isdigit():
                return False  # Allow digits
            else:
                return True  # Filter out non-numeric input
        return False

# GUI Classes
class SignalWindow(QMainWindow):
    # Initialize
    def __init__(self, edf_obj:EdfFile=None, xml_obj:AnnotationXml=None, signal_combobox_index:int = None, parent=None):
        super().__init__(parent)
        # Signal Window Features
        self.number_of_epochs_on_screen = 15

        # Setup and Draw Window
        self.ui = Ui_SignalWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Signal Viewer")

        # Make a copy of the edf and xml information
        self.edf_obj = edf_obj
        self.xml_obj = xml_obj

        # Set signal labels
        self.signal_labels = self.edf_obj.edf_signals.signal_labels
        self.ui.comboBox_signals.addItems(self.signal_labels )
        signal_combobox_index = signal_combobox_index if signal_combobox_index!=None else 0
        self.signal_label = self.signal_labels[signal_combobox_index]
        self.ui.comboBox_signals.setCurrentIndex(signal_combobox_index)

        # Time Unit Converstions
        s_to_min = lambda s: int(s / 60)
        s_to_s = lambda s: int(s)

        # Set up epoch controls
        self.epoch_display_options_text:List       = ['30 s', '1 min', '4 min', '8 min', '1 hr']
        self.epoch_display_options_width_sec:List  = [ 30,     60,      240,     480,      3600]
        self.epoch_display_axis_grid:List          = [ [5,1],  [10,2],  [60, 10], [120, 30],[600, 50] ]
        self.epoch_axis_units:List                 = ['s', 's', 'm', 'm', 'm']
        self.time_convert_f:List                   = [s_to_s, s_to_s, s_to_min, s_to_min, s_to_min]

        # Initialize epoch variables
        self.max_epoch: int                 = None
        self.current_epoch: int             = None
        self.current_epoch_width_index: int = None
        self.signal_length_seconds: int     = None
        self.automatic_histogram_redraw     = True
        self.automatic_signal_redraw        = True

        # Setup epoch widgets
        self.ui.pushButton_first.clicked.connect(self.set_epoch_to_first)
        self.ui.pushButton__next.clicked.connect(self.set_epoch_to_next)
        self.ui.pushButton_update.clicked.connect(self.set_epoch_from_text)
        self.ui.pushButton_previous.clicked.connect(self.set_epoch_to_prev)
        self.ui.pushButton_last.clicked.connect(self.set_epoch_to_last)
        self.initialize_epoch_variables()

        # Set up signal
        self.signal        = self.edf_obj.edf_signals.signals_dict[self.signal_label]
        self.signal_units  = self.edf_obj.edf_signals.signal_units_dict[self.signal_label]
        self.sampling_time = self.edf_obj.edf_signals.signal_sampling_time_dict[self.signal_label]

        # Initialize epoch variables and widget
        self.initialize_epoch_variables()
    # Setup
    def initialize_epoch_variables(self, combobox_index:int = None):
        # Reset class epoch variable upon loading a new file
        self.max_epoch = 1
        self.current_epoch = 1
        self.current_epoch_width_index = 0
        self.signal_length_seconds = 1

        # Set maximum number of epochs
        epoch_width     = self.epoch_display_options_width_sec[self.ui.comboBox_epoch.currentIndex()]
        self.max_epoch  = self.edf_obj.edf_signals.return_num_epochs(self.signal_label, epoch_width)

        # Set up epic combobox
        self.ui.comboBox_epoch.addItems(self.epoch_display_options_text)

        # Set epoch edit box to 1
        self.ui.textEdit_epoch.setText(f"{self.current_epoch}")
        self.ui.textEdit_epoch.setAlignment(Qt.AlignRight)

        # Set epoch string
        time_str = self.return_time_string(self.current_epoch, epoch_width)
        self.ui.label_page.setText(f'of {self.max_epoch} epochs, ({time_str})')

        # Set epoch combo box to 30 second window
        self.ui.comboBox_epoch.setCurrentIndex(self.current_epoch_width_index)

        # Edit Box Actions
        self.numeric_filter = NumericTextEditFilter(self)
        self.ui.textEdit_epoch.installEventFilter(self.numeric_filter)
    # Epoch Buttons
    def set_epoch_to_first(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """
        # Example: Set an internal index
        self.current_epoch = 1
        self.ui.textEdit_epoch.setText(f"{self.current_epoch}")
        self.ui.textEdit_epoch.setAlignment(Qt.AlignRight)

        # update Signals
        # self.draw_signals_in_graphic_views()

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to first ({self.current_epoch})")
    def set_epoch_to_next(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """
        # Example: Set an internal index
        if self.current_epoch + self.number_of_epochs_on_screen < self.max_epoch:
            self.current_epoch += self.number_of_epochs_on_screen
            self.ui.textEdit_epoch.setText(f"{self.current_epoch}")
            self.ui.textEdit_epoch.setAlignment(Qt.AlignRight)

            # update Signals
            # self.draw_signals_in_graphic_views()

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to next ({self.current_epoch})")
    def set_epoch_from_text(self):
        self.ui.pushButton_update.setEnabled(False)
        logger.info(f'User entered a new epoch')
        if self.edf_obj:
            new_epoch = int(self.ui.textEdit_epoch.toPlainText())
            if new_epoch < 1:
                new_epoch = 1
            elif new_epoch > self.max_epoch:
                new_epoch = self.max_epoch
            self.ui.textEdit_epoch.setText(f"{new_epoch}")
            self.ui.textEdit_epoch.setAlignment(Qt.AlignRight)
            self.current_epoch = new_epoch

            # update Signals
            # self.draw_signals_in_graphic_views()
        self.ui.pushButton_update.setEnabled(True)
    def set_epoch_to_prev(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """
        # Example: Set an internal index
        if self.current_epoch - self.number_of_epochs_on_screen  >= 1:
            self.current_epoch -= self.number_of_epochs_on_screen
            self.ui.textEdit_epoch.setText(f"{self.current_epoch}")
            self.ui.textEdit_epoch.setAlignment(Qt.AlignRight)
        else:
            self.set_epoch_to_first()

            # update Signals
            # self.draw_signals_in_graphic_views()

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to prev ({self.current_epoch})")
    def set_epoch_to_last(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """
        # Example: Set an internal index
        max_num_pages = self.max_epoch//self.number_of_epochs_on_screen
        self.current_epoch = int(max_num_pages*self.number_of_epochs_on_screen)+1
        self.ui.textEdit_epoch.setText(f"{self.current_epoch }")
        self.ui.textEdit_epoch.setAlignment(Qt.AlignRight)

        # update Signals
        #self.draw_signals_in_graphic_views()

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to page ({self.current_epoch})")
    # Update Signal Change
    def update_signal_combobox (self):
        pass
    # Utilities
    def return_time_string(self, epoch:int, epoch_width:int):
        val     = float((epoch-1)*epoch_width)
        seconds = val
        hours   = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds) % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"

