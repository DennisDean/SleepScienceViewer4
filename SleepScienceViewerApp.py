from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsTextItem
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import QEvent, Qt, QObject

import sys
import logging
from AnnotationXmlClass import AnnotationXml, SignalAnnotations, SleepStages
from edfFile import EdfHeader, EdfSignalHeader, EdfSignalsStats, EdfSignal, EdfSignalAnalysis, EdfFile
import math

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("SleepScienceViewer.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Import your Ui_MainWindow from the generated module
# from your_ui_module import Ui_MainWindow  # Replace this with your actual import if in a separate file
from SleepScienceViewer import Ui_MainWindow

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
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setWindowTitle("Sleep Science Viewer")
        self.ui.setupUi(self)

        # Initialize control variables
        self.max_epoch: int                         = 1
        self.current_epoch: int                     = 1
        self.current_epoch_width_index:int          = 0
        self.signal_length_seconds:int              = 1
        self.edf_file_obj:EdfFile                   = None
        self.annotation_xml_obj: AnnotationXmlClass = None
        self.epoch_display_options_text             = ['30 s', '1 min', '5 min', '10 min', '1 hr']
        self.epoch_display_options_width_sec        = [ 30,     60,      300,     600,      3600]
        self.epoch_display_axis_grid                = [ [5,1],  [10,2],  [60, 10], [120, 30],[600, 50] ]

        # Visualization Controls
        # Assign the annotation list widget to a fixed width font
        all_families = QFontDatabase.families()
        monospace_fonts = [f for f in all_families if QFontDatabase.isFixedPitch(f)]
        selected_font = monospace_fonts[0] if monospace_fonts else "Courier"
        font = QFont(selected_font, 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.ui.annotation_listWidget.setFont(font)

        # Save sleep stage mappings when annotations are loaded
        self.sleep_stage_mappings = None

        # Enable updating the annotation list based on user selection
        self.ui.annotation_comboBox.currentTextChanged.connect(self.on_annotation_combobox_text_changed)
        self.annotations_list:str= None

        # Load Buttons
        self.ui.load_edf_pushButton.clicked.connect(self.load_edf_file)
        self.ui.load_annotation_pushButton.clicked.connect(self.load_xml_file)

        # Spectrogram Buttons
        self.ui.compute_spectrogram_pushButton.clicked.connect(self.compute_and_display_spectrogram)

        # Epoch Buttons
        time_str = self.return_time_string(self.current_epoch, self.epoch_display_options_width_sec[0])
        self.ui.epochs_label.setText(f"of {self.max_epoch} epochs ({time_str})")
        self.ui.epochs_textEdit.setText(f"{self.current_epoch}")
        self.ui.epochs_textEdit.setAlignment(Qt.AlignRight)
        self.ui.first_pushButton.clicked.connect(self.set_epoch_to_first)
        self.ui.next_epoch_pushButton.clicked.connect(self.set_epoch_to_next)
        self.ui.update_epoch_pushButton.clicked.connect(self.set_epoch_from_text)
        self.ui.previous_pushButton.clicked.connect(self.set_epoch_to_prev)
        self.ui.last_epoch_pushButton.clicked.connect(self.set_epoch_to_last)
        self.ui.epoch_comboBox.addItems(self.epoch_display_options_text)
        self.ui.epoch_comboBox.setStyleSheet("color: black; background-color: white;")

        # Signal Buttons
        self.ui.color_1_pushButton.clicked.connect(self.set_signal_color)
        self.ui.color_2_pushButton.clicked.connect(self.set_signal_color)
        self.ui.color_3_pushButton.clicked.connect(self.set_signal_color)
        self.ui.color_4_pushButton.clicked.connect(self.set_signal_color)
        self.ui.color_5_pushButton.clicked.connect(self.set_signal_color)
        self.ui.color_6_pushButton.clicked.connect(self.set_signal_color)
        self.ui.color_7_pushButton.clicked.connect(self.set_signal_color)
        self.ui.color_8_pushButton.clicked.connect(self.set_signal_color)
        self.ui.color_9_pushButton.clicked.connect(self.set_signal_color)
        self.ui.color_10_pushButton.clicked.connect(self.set_signal_color)
        self.ui.color_11_pushButton.clicked.connect(self.set_signal_color)

        # Combo Box Action
        self.ui.hypnogram_comboBox.currentIndexChanged.connect(self.on_hypnogram_changed)

        # Edit Box Actions
        self.numeric_filter = NumericTextEditFilter(self)
        self.ui.epochs_textEdit.installEventFilter(self.numeric_filter)
        self.ui.epoch_comboBox.currentIndexChanged.connect(self.on_epoch_width_change)

        # Signal Selection Boxes
        self.ui.signal_1_comboBox.currentTextChanged.connect(self.signal_1_change)
        self.ui.signal_2_comboBox.currentTextChanged.connect(self.signal_2_change)
        self.ui.signal_3_comboBox.currentTextChanged.connect(self.signal_3_change)
        self.ui.signal_4_comboBox.currentTextChanged.connect(self.signal_4_change)
        self.ui.signal_5_comboBox.currentTextChanged.connect(self.signal_5_change)
        self.ui.signal_6_comboBox.currentTextChanged.connect(self.signal_6_change)
        self.ui.signal_7_comboBox.currentTextChanged.connect(self.signal_7_change)
        self.ui.signal_8_comboBox.currentTextChanged.connect(self.signal_8_change)
        self.ui.signal_9_comboBox.currentTextChanged.connect(self.signal_9_change)
        self.ui.signal_10_comboBox.currentTextChanged.connect(self.signal_10_change)
        self.ui.signal_11_comboBox.currentTextChanged.connect(self.signal_11_change)

        # Set Up list widget
        self.ui.annotation_listWidget.itemDoubleClicked.connect(self.annotation_list_widget_double_click)

        # Store multi-taper results
        self.multitaper_spectrogram_obj:MultitaperSpectrogram = None
    # Initialize Annotations
    def load_xml_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml)")

        try:
            # Create XML Object
            self.annotation_xml_obj = AnnotationXml(file_path)
            self.annotation_xml_obj.load()

            # Update interface
            self.ui.load_annotation_textEdit.setText(f"{file_path}")
            #QMessageBox.information(self, "XML Loaded", f"Loaded: {file_path}")
            logger.info(f"Loaded XML: {file_path}")
        except:
            logger.error('SleepScienceViewer: Error loading XML file.')

        if file_path:
            # Set Sleep Stage Labels
            sleep_stage_labels = self.annotation_xml_obj.sleep_stages_obj.return_sleep_stage_labels()
            sleep_stage_labels.remove(sleep_stage_labels[0])
            self.ui.hypnogram_comboBox.clear()
            self.ui.hypnogram_comboBox.addItems(sleep_stage_labels)

            # Get Sleep Stage Mappings
            self.sleep_stage_mappings = self.annotation_xml_obj.sleep_stages_obj.return_sleep_stage_mappings()

            # Set annotation types
            annotations_type_list = self.annotation_xml_obj.scored_event_obj.scored_event_unique_names
            annotations_type_list.insert(0, 'All')
            self.ui.annotation_comboBox.clear()
            self.ui.annotation_comboBox.addItems(annotations_type_list)
            self.ui.annotation_listWidget.clear()
            annotations_list = self.annotation_xml_obj.scored_event_obj.scored_event_name_source_time_list
            for item in annotations_list:
                self.ui.annotation_listWidget.addItem(item)
            self.annotations_list = annotations_list

            # Plot Hypnogram
            # self.draw_hypnogram_in_view(self.annotation_xml_obj.sleep_stages_obj, self.ui.hypnogram_graphicsView)
            self.annotation_xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.hypnogram_graphicsView)
    def on_hypnogram_changed(self, index):
        # Update Variables
        selected_text = self.ui.hypnogram_comboBox.itemText(index)
        self.hypnogram_combobox_selection = index
        logger.info(f"Combo box changed to index {index}: {selected_text}")

        # Update Hypnogram
        if self.sleep_stage_mappings != None:
            stage_map = index
            self.annotation_xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.hypnogram_graphicsView,
                                                                stage_index=stage_map)
    def on_annotation_combobox_text_changed(self,text):
        logger.info(f'Annotation combobox text changed to {text}')

        if self.annotations_list:
            # Clear the current list in the widget
            self.ui.annotation_listWidget.clear()

            # Always keep the header (assumed to be the first line)
            header = self.annotations_list[0]
            self.ui.annotation_listWidget.addItem(header)

            # If 'All' is selected, show everything
            if text == 'All':
                for item in self.annotations_list[1:]:  # Skip header (already added)
                    self.ui.annotation_listWidget.addItem(item)
            else:
                # Filter items that contain the selected text
                for item in self.annotations_list[1:]:
                    if text in item:
                        self.ui.annotation_listWidget.addItem(item)
    # Initialize EDF
    def load_edf_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open EDF File", "", "EDF Files (*.edf)")
        try:
            # Create XML Object
            self.edf_file_obj = EdfFile(file_path)
            self.edf_file_obj.load()

            # Update interface
            self.ui.load_edf_textEdit.setText(f"{file_path}")

            #QMessageBox.information(self, "XML Loaded", f"Loaded: {file_path}")
            logger.info(f"Loaded EDF: {file_path}")
        except:
            logger.error('SleepScienceViewer: Error loading XML file.')

        if file_path:
            # Set epoch display options
            # Spectrogram Signal Labels
            signal_labels = self.edf_file_obj.edf_signals.signal_labels
            eeg_labels = self.edf_file_obj.edf_signals.eeg_signal_labels # Will want a new one with stepped signals
            stepped_signal_list = self.edf_file_obj.edf_signals.return_stepped_signals_from_list(signal_labels)
            continuous_signal_list = self.edf_file_obj.edf_signals.return_continuous_signals_from_list(signal_labels)
            self.ui.spectrogram_comboBox.clear()
            self.ui.spectrogram_comboBox.addItems(continuous_signal_list)

            # Determine length of signal
            epoch_width    = self.epoch_display_options_width_sec[self.ui.epoch_comboBox.currentIndex()]
            max_num_epochs = self.edf_file_obj.edf_signals.return_num_epochs(eeg_labels[0], epoch_width)
            self.max_epoch = max_num_epochs
            self.signal_length_seconds = self.edf_file_obj.edf_signals.return_signal_length_seconds(signal_labels[0], epoch_width)

            # Update epoch label
            time_str = self.return_time_string(self.current_epoch, epoch_width)
            self.ui.epochs_label.setText(f" of {max_num_epochs} epochs ({time_str})")

            # Draw Signals
            self.set_signal_combo_boxes()
    def set_signal_combo_boxes(self):
        # Get signal labels
        signal_labels = self.edf_file_obj.edf_signals.signal_labels
        signal_labels.insert(0, '')
        num_available_signals = len(signal_labels)

        # Load signal pop up box
        signal_combo_boxes = [self.ui.signal_1_comboBox,  self.ui.signal_2_comboBox, self.ui.signal_3_comboBox,
                              self.ui.signal_4_comboBox,  self.ui.signal_5_comboBox, self.ui.signal_6_comboBox,
                              self.ui.signal_7_comboBox,  self.ui.signal_8_comboBox, self.ui.signal_9_comboBox,
                              self.ui.signal_10_comboBox, self.ui.signal_11_comboBox]

        # add signal list to all comboboxes
        for combo in signal_combo_boxes:
            combo.clear()
            combo.addItems(signal_labels)

        for i, combo in enumerate(signal_combo_boxes):
            if i + 1 < len(signal_labels):  # +1 to skip the inserted empty string
                combo.setCurrentIndex(i + 1)  # Set to the i-th signal
            else:
                combo.setCurrentIndex(0)  # Default to the empty string if no signal available
    def compute_and_display_spectrogram(self):
        # Check before starting long computation

        if self.edf_file_obj != None:
            process_eeg = self.show_ok_cancel_dialog()
        else:
            self.show_missing_eeg_warning()

        if process_eeg == True:
            # Get EEG Signal
            eeg_label = self.ui.spectrogram_comboBox.currentText()
            signal_type = 'EEG'
            eeg_signal_obj = self.edf_file_obj.edf_signals.return_edf_signal(eeg_label, signal_type)
            edf_signal_analysis_obj = EdfSignalAnalysis(eeg_signal_obj)

            logger.info(f'Computing spectrogram ({eeg_label}): computation may be time consuming')
            multitaper_spectrogram_obj = edf_signal_analysis_obj.multitapper_spectrogram()
            multitaper_spectrogram_obj.plot(self.ui.spectrogram_graphicsView)
            self.multitaper_spectrogram_obj = multitaper_spectrogram_obj
            logger.info('Computing spectrogram: Computation completed')
    def draw_signals_in_graphic_views(self):

        signal_combo_boxes = [self.ui.signal_1_comboBox, self.ui.signal_2_comboBox, self.ui.signal_3_comboBox,
                              self.ui.signal_4_comboBox, self.ui.signal_5_comboBox, self.ui.signal_6_comboBox,
                              self.ui.signal_7_comboBox, self.ui.signal_8_comboBox, self.ui.signal_9_comboBox,
                              self.ui.signal_10_comboBox, self.ui.signal_11_comboBox]

        graphic_views = [ self.ui.signal_1_graphicsView,  self.ui.signal_2_graphicsView,  self.ui.signal_3_graphicsView,
                          self.ui.signal_4_graphicsView,  self.ui.signal_5_graphicsView,  self.ui.signal_6_graphicsView,
                          self.ui.signal_7_graphicsView,  self.ui.signal_8_graphicsView,  self.ui.signal_9_graphicsView,
                          self.ui.signal_10_graphicsView, self.ui.signal_11_graphicsView]

        # get combo boxes labels
        combo_box_signal_labels = [combo_box.currentText() for combo_box in signal_combo_boxes]
        graphic_views_to_update_id = []
        for i, label in enumerate(combo_box_signal_labels): # not needed since plot in EDF handles no signal key present
            graphic_views_to_update_id.append(i)

        # Set variables
        current_epoch = int(self.ui.epochs_textEdit.toPlainText())

        # Update graphic view
        epoch_num               = current_epoch - 1  # function expect zero indexing, reset epoch to signal start
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]
        signal_type             = ""
        for i in graphic_views_to_update_id:
            signal_label            = combo_box_signal_labels[i]
            graphic_view            = graphic_views[i]

            self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                 signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)

        # Update epoch label string
        # combo_box_signal_labels = [ label for label in combo_box_signal_labels if label != '']
        # print(combo_box_signal_labels)
        # if len(combo_box_signal_labels) > 0:
        # signal_label = combo_box_signal_labels[0]
        # max_num_epochs = self.edf_file_obj.edf_signals.return_num_epochs(signal_label, epoch_width)
        epoch_width    = self.epoch_display_options_width_sec[self.ui.epoch_comboBox.currentIndex()]
        self.max_epoch = self.edf_file_obj.edf_signals.return_num_epochs_from_width(epoch_width)
        time_str       = self.return_time_string(current_epoch, epoch_width)
        self.ui.epochs_label.setText(f" of {self.max_epoch } epochs ({time_str})")
    def show_ok_cancel_dialog(parent=None):
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Confirm Action")
        msg_box.setText("Computing a multitaper spectrogram can be time consuming. Future versions will include a less computational alternative. \n\nDo you want to proceed?")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Ok)

        result = msg_box.exec()

        if result == QMessageBox.Ok:
            logger.info("OK clicked: Will continue ")
            return True
        else:
            logger.info(f"Message Dialog Box - Cancel clicked, Msg: {'Computing a multitaper spectrogram can be time consuming. Do you want to proceed?'} ")
            return False
    def show_missing_eeg_warning(self):
        QMessageBox.warning(
            self,
            "Missing EEG Signal",
            "Please load an EDF file with an EEG signal."
        )
    # Epochs
    def set_epoch_to_first(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """
        # Example: Set an internal index
        self.current_epoch = 1
        self.ui.epochs_textEdit.setText(f"{self.current_epoch}")
        self.ui.epochs_textEdit.setAlignment(Qt.AlignRight)

        # update Signals
        self.draw_signals_in_graphic_views()

        # You can now update views, annotations, etc.
        logger.info("Epoch set to first (0)")
    def set_epoch_to_next(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """
        # Example: Set an internal index
        if self.current_epoch < self.max_epoch:
            self.current_epoch += 1
            self.ui.epochs_textEdit.setText(f"{self.current_epoch}")
            self.ui.epochs_textEdit.setAlignment(Qt.AlignRight)

            # update Signals
            self.draw_signals_in_graphic_views()

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to next ({self.current_epoch})")
    def set_epoch_from_text(self):
        self.ui.update_epoch_pushButton.setEnabled(False)
        logger.info(f'User entered a new epoch')
        if self.edf_file_obj:
            new_epoch = int(self.ui.epochs_textEdit.toPlainText())
            if new_epoch < 1:
                new_epoch = 1
            elif new_epoch > self.max_epoch:
                new_epoch = self.max_epoch
            self.ui.epochs_textEdit.setText(f"{new_epoch}")
            self.ui.epochs_textEdit.setAlignment(Qt.AlignRight)

            # update Signals
            self.draw_signals_in_graphic_views()
        self.ui.update_epoch_pushButton.setEnabled(True)
    def set_epoch_to_prev(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """
        # Example: Set an internal index
        if self.current_epoch > 1:
            self.current_epoch -= 1
            self.ui.epochs_textEdit.setText(f"{self.current_epoch}")
            self.ui.epochs_textEdit.setAlignment(Qt.AlignRight)

            # update Signals
            self.draw_signals_in_graphic_views()

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to prev ({self.current_epoch})")
    def set_epoch_to_last(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """
        # Example: Set an internal index
        self.current_epoch = self.max_epoch
        self.ui.epochs_textEdit.setText(f"{self.max_epoch}")
        self.ui.epochs_textEdit.setAlignment(Qt.AlignRight)

        # update Signals
        self.draw_signals_in_graphic_views()

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to last ({self.max_epoch})")
    def on_epoch_width_change(self):
        # Adjust epoch number to new width
        old_epoch_width_index = self.current_epoch_width_index
        old_epoch_width       = self.epoch_display_options_width_sec[old_epoch_width_index]
        new_epoch_width_index = int(self.ui.epoch_comboBox.currentIndex())
        new_epoch_width       = self.epoch_display_options_width_sec[new_epoch_width_index]

        # Get new maximum epochs
        signal_keys            = [label for label in self.edf_file_obj.edf_signals.signal_labels if label != '']
        new_maximum_epochs    = self.edf_file_obj.edf_signals.return_num_epochs(signal_keys[0], new_epoch_width)
        self.max_epoch        = new_maximum_epochs
        self.ui.epochs_label.setText(f' of {new_maximum_epochs} epochs')

        # Compute new epoch number
        current_epoch         = int(self.ui.epochs_textEdit.toPlainText())
        current_time_in_sec   = current_epoch*old_epoch_width - old_epoch_width
        new_epoch             = current_time_in_sec / new_epoch_width + 1
        if new_epoch <  1 :
            new_epoch = int(math.ceil(new_epoch))
        else:
            new_epoch = int(math.floor(new_epoch))

        # Update epoch textEdit widget
        self.ui.epochs_textEdit.setText(str(new_epoch))

        # Update signal plots
        self.draw_signals_in_graphic_views()

        # Update current width
        self.current_epoch_width_index = new_epoch_width_index
    # Signals
    def signal_1_change(self, text):
        logger.info(f"Signal 1 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_1_graphicsView
        signal_type             = ""
        epoch_num               = int(self.ui.epochs_textEdit.toPlainText()) - 1 # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                    signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
        if text == '':
            text = "''"
        logger.info(f"Signal 1 combo box changed to {text}")
    def signal_2_change(self, text):
        logger.info(f"Signal 2 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_2_graphicsView
        signal_type             = ""
        epoch_num               = int(self.ui.epochs_textEdit.toPlainText()) - 1  # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                        signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
    def signal_3_change(self, text):
        logger.info(f"Signal 3 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_3_graphicsView
        signal_type             = ""
        epoch_num               = int(self.ui.epochs_textEdit.toPlainText()) - 1 # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                       signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
    def signal_4_change(self, text):
        pass
        logger.info(f"Signal 4 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_4_graphicsView
        signal_type             = ""
        epoch_num               = int(self.ui.epochs_textEdit.toPlainText()) - 1 # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                       signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
    def signal_5_change(self, text):
        logger.info(f"Signal 5 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_5_graphicsView
        signal_type             = ""
        epoch_num               = int(self.ui.epochs_textEdit.toPlainText()) - 1  # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                        signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
    def signal_6_change(self, text):
        logger.info(f"Signal 6 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_6_graphicsView
        signal_type             = ""
        epoch_num               =  int(self.ui.epochs_textEdit.toPlainText()) - 1  # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                        signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
    def signal_7_change(self, text):
        # Update Variables
        logger.info(f"Signal 7 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_7_graphicsView
        signal_type             = ""
        epoch_num               = int(self.ui.epochs_textEdit.toPlainText()) - 1  # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                        signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
    def signal_8_change(self, text):
        logger.info(f"Signal 8 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_8_graphicsView
        signal_type             = ""
        epoch_num               = int(self.ui.epochs_textEdit.toPlainText()) - 1  # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                    signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
    def signal_9_change(self, text):
        logger.info(f"Signal 9 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_9_graphicsView
        signal_type             = ""
        epoch_num               = int(self.ui.epochs_textEdit.toPlainText()) - 1  # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                     signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
    def signal_10_change(self, text):
        logger.info(f"Signal 10 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_10_graphicsView
        signal_type             = ""
        epoch_num               = int(self.ui.epochs_textEdit.toPlainText()) - 1  # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                     signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
    def signal_11_change(self, text):
        logger.info(f"Signal 11 combo box changed to {text}")
        signal_label            = text
        graphic_view            = self.ui.signal_11_graphicsView
        signal_type             = ""
        epoch_num               = int(self.ui.epochs_textEdit.toPlainText()) - 1  # function expect zero indexing
        epoch_width_index       = self.ui.epoch_comboBox.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]

        self.edf_file_obj.edf_signals.plot_signal_segment(signal_label,
                    signal_type, epoch_num, epoch_width, graphic_view, x_tick_settings = epoch_display_axis_grid)
    def set_signal_color(self):
        pass
    def annotation_list_widget_double_click(self, item):
        # Slot to handle double-click events on QListWidget items.
        logger.info(f"Annotation list double-clicked: {item.text()}")
        if self.edf_file_obj == None:
            return

        # Parse text
        self.ui.annotation_listWidget.currentItem()
        text_list       = item.text()
        text_list       = text_list.split()

        # Parse text list
        starttime       = text_list[0]
        annotation_type = text_list[1]
        signal_label    = text_list[-1]
        if len(text_list) > 3:
            annotation_type = text_list[2:-1]
            annotation_type = ' '.join(annotation_type)

        # Compute start time
        time_list              = starttime.split(':')
        annotation_time_in_sec = int(time_list[0])*3600 + int(time_list[1])*60 + int(time_list[2])

        # Change Current epoch
        new_epoch = float(annotation_time_in_sec)/self.epoch_display_options_width_sec[self.ui.epoch_comboBox.currentIndex()]
        new_epoch = math.floor(new_epoch) + 1
        self.ui.epochs_textEdit.setText(str(new_epoch))

        # Update signal graphic views to annotation epoch
        self.draw_signals_in_graphic_views()

        logger.info(f"Jumped to new signal epoch ({new_epoch})")
    # Utilities
    def return_time_string(self, epoch:int, epoch_width:int):
        val     = float((epoch-1)*epoch_width)
        seconds = val
        hours   = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds) % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"
def show_main_window():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()

# Only run if this script is executed directly
if __name__ == "__main__":
    show_main_window()# -*- coding: utf-8 -*-