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
        self.ui.pushButton_next.clicked.connect(self.set_epoch_to_next)
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

        # Draw signals in graphic view
        self.automatic_signal_redraw = True
        # self.draw_signal_in_graphic_views()

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
    def draw_signal_in_graphic_views(self, annotation_marker=None):

        if self.automatic_signal_redraw == False:
            return

        signal_combo_boxes = [self.ui.graphicsView_signal_1,  self.ui.graphicsView_signal_2,  self.ui.graphicsView_signal_3,
                              self.ui.graphicsView_signal_4,   self.ui.graphicsView_signal_5,  self.ui.graphicsView_signal_6,
                              self.ui.graphicsView_signal_7,  self.ui.graphicsView_signal_8,  self.ui.graphicsView_signal_9,
                              self.ui.graphicsView_signal_10, self.ui.graphicsView_signal_11, self.ui.graphicsView_signal_12,
                              self.ui.graphicsView_signal_13, self.ui.graphicsView_signal_14, self.ui.graphicsView_signal_14]

        graphic_views = [self.ui.graphicsView_signal_1,  self.ui.graphicsView_signal_2,  self.ui.graphicsView_signal_3,
                              self.ui.graphicsView_signal_4,   self.ui.graphicsView_signal_5,  self.ui.graphicsView_signal_6,
                              self.ui.graphicsView_signal_7,  self.ui.graphicsView_signal_8,  self.ui.graphicsView_signal_9,
                              self.ui.graphicsView_signal_10, self.ui.graphicsView_signal_11, self.ui.graphicsView_signal_12,
                              self.ui.graphicsView_signal_13, self.ui.graphicsView_signal_14, self.ui.graphicsView_signal_14]

        # Turn off change signal while updating combobox list following selection of a new edf file
        for combo_box in signal_combo_boxes:
            combo_box.blockSignals(True)

        # get combo boxes labels
        combo_box_signal_labels = [combo_box.currentText() for combo_box in signal_combo_boxes]
        graphic_views_to_update_id = []
        for i, label in enumerate(
                combo_box_signal_labels):  # not needed since plot in EDF handles no signal key present
            graphic_views_to_update_id.append(i)

        # Set variables
        current_epoch = int(self.ui.epochs_textEdit.toPlainText())

        # Update graphic view
        epoch_num               = current_epoch - 1  # function expect zero indexing, reset epoch to signal start
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]
        convert_time_f          = self.time_convert_f[epoch_width_index]
        time_axis_units         = self.epoch_axis_units[epoch_width_index]
        signal_type = ""

        for i in graphic_views_to_update_id:
            # Select graphic view
            signal_label = combo_box_signal_labels[i]
            graphic_view = graphic_views[i]

            # Set stepped variables
            stepped_dict      = {}
            is_signal_stepped = False
            if self.annotation_xml_obj != None:
                is_signal_stepped = signal_label in self.annotation_xml_obj.steppedChannels.keys()
                if is_signal_stepped:
                    stepped_dict = self.annotation_xml_obj.steppedChannels[signal_label]

            # Plot signal segment
            self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                                                              signal_type, epoch_num, epoch_width, graphic_view,
                                                              x_tick_settings   = epoch_display_axis_grid,
                                                              annotation_marker = annotation_marker,
                                                              convert_time_f    = convert_time_f,
                                                              time_axis_units   = time_axis_units,
                                                              is_signal_stepped = is_signal_stepped,
                                                              stepped_dict      = stepped_dict )

        # Turn on combo box signal change
        for combo_box in signal_combo_boxes:
            combo_box.blockSignals(False)

        # Update epoch label string
        epoch_width    = self.epoch_display_options_width_sec[self.ui.epoch_comboBox.currentIndex()]
        self.max_epoch = self.edf_file_obj.edf_signals.return_num_epochs_from_width(epoch_width)
        time_str       = self.return_time_string(current_epoch, epoch_width)
        self.ui.epochs_label.setText(f" of {self.max_epoch} epochs ({time_str})")
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

