"""
Sleep Science Viewer

Overview:
A python native edf-annotation viewed with corresponding EDF and Annotation loaders.
Nearly all the work is done in the loaders with the goal of developing tools to
support interactive analysis and future development.

Author:
Dennis A. Dean, II, PhD
Sleep Science

Completion Date: July 31, 2025

Acknowledgement:
The python code models previous Matlab versions of the code written by Case Western Reserve
University and by Matlab code I wrote when I was at Brigham and Women's Hospital. The previously
authored Matlab code benefited from feedback received following public release of the MATLAB
code on MATLAB central.

Copyright 2025 Dennis A. Dean II
This file is part of the SleepScienceViewer project.

This source code is licensed under the GNU Affero General Public License v3.0.
See the LICENSE file in the root directory of this source tree or visit
https://www.gnu.org/licenses/agpl-3.0.html for full terms.
"""

# To Do List
# TODO: Support for changing signal color
# TODO: clean up video

# PySide6 imports
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsTextItem
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtCore import QEvent, Qt, QObject
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QListWidgetItem

# System Imports
import os
import sys
import logging
import math
from functools import partial

# Utilites
import pyrsdameraulevenshtein as dl

# EDF and Annotation Classes
from AnnotationXmlClass import AnnotationXml, SignalAnnotations, SleepStages
from EdfFileClass import EdfHeader, EdfSignalHeader, EdfSignalsStats, EdfSignal, EdfSignalAnalysis, EdfFile

# Configure the logger
from logging_config import logger

# Import your Ui_MainWindow from the generated module
from SleepScienceViewer import Ui_MainWindow

# Dialog Boxes
class EDFInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About EDF Format")
        self.setMinimumSize(500, 300)

        description = (
            "<b>European Data Format (EDF)</b> is a standard file format "
            "designed for exchange and storage of time-series physiological data such as EEG, EMG, or ECG.<br><br>"
            "<i>Kemp B, Zwinderman AH, Tuk B, Kamphuisen HA, Oberye JJ. "
            "Analysis of a sleep-dependent neuronal feedback loop: the slow-wave microcontinuity of the EEG. "
            "Clin Neurophysiol. 1992;82(2):145-150.</i><br><br>"
            "<a href='https://www.edfplus.info/' style='color:#0077cc;'>https://www.edfplus.info/</a>"
        )

        label = QLabel(description)
        label.setWordWrap(True)
        label.setOpenExternalLinks(True)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)
class SleepXMLInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sleep Annotation XML Standard")
        self.setMinimumSize(500, 300)

        description = (
            "<b>Sleep Annotation XML Standard</b> is a structured format designed for "
            "encoding events and annotations in sleep recordings, such as arousals, "
            "apneas, and sleep stages. This format supports interoperability and consistent "
            "data sharing across research studies and clinical applications.<br><br>"
            "It is widely used by large-scale sleep research initiatives, including the "
            "<a href='https://sleepdata.org/' style='color:#0077cc;'>National Sleep Research Resource (NSRR)</a>, "
            "to facilitate analysis and reproducibility.<br><br>"
            "<a href='https://github.com/nsrr/edf-editor-translator/wiki/Compumedics-Annotation-Format' style='color:#0077cc;'>Learn more about Sleep XML Annotations</a>"
        )

        label = QLabel(description)
        label.setWordWrap(True)
        label.setOpenExternalLinks(True)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Sleep Science Viewer")
        self.setMinimumSize(400, 250)

        layout = QVBoxLayout(self)

        about_text = """
        <h3>Sleep Science Viewer</h3>
        <p>Application provides access to EDF and XML file used in sleep research and includes summary/report exports.
         The applications demonstrates features made available in an EDF and Annotation class. </p>
        <p><b>Developer:</b> Dennis A. Dean, II, PhD</p>
        <p>&copy; 2025 Dennis A. Dean, II, PhD. All rights reserved.</p>
        """

        text_browser = QTextBrowser(self)
        text_browser.setHtml(about_text)
        text_browser.setReadOnly(True)
        text_browser.setOpenExternalLinks(True)

        layout.addWidget(text_browser)

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

# Application
def clear_spectrogram_plot(parent_widget = None):
    layout = parent_widget.layout()
    if layout:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
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

        # Time Unit Converstions
        s_to_hr  = lambda s:int(s/3600)
        s_to_min = lambda s:int(s/60)
        s_to_s   = lambda s:int(s)

        # Initialize control variables
        self.edf_file_obj:EdfFile                   = None
        self.annotation_xml_obj: AnnotationXmlClass = None
        self.epoch_display_options_text: List       = ['30 s', '1 min', '5 min', '10 min', '1 hr']
        self.epoch_display_options_width_sec: List  = [ 30,     60,      300,     600,      3600]
        self.epoch_display_axis_grid: List          = [ [5,1],  [10,2],  [60, 10], [120, 30],[600, 50] ]
        self.epoch_axis_units: List                 = ['s', 's', 'm', 'm', 'm']
        self.time_convert_f: List                   = [s_to_s, s_to_s, s_to_min, s_to_min, s_to_min]
        self.text_similarity_threshold             = 0.9
        self.listBoxFontSize                       = 9

        # Initialize epoch variables
        self.max_epoch: int                 = None
        self.current_epoch: int             = None
        self.current_epoch_width_index: int = None
        self.signal_length_seconds: int     = None
        self.automatic_histogram_redraw     = True
        self.automatic_signal_redraw        = True
        self.initialize_epoch_variables()

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

        # Combo Box Action
        self.ui.hypnogram_comboBox.currentIndexChanged.connect(self.on_hypnogram_changed)

        # Edit Box Actions
        self.numeric_filter = NumericTextEditFilter(self)
        self.ui.epochs_textEdit.installEventFilter(self.numeric_filter)
        self.ui.epoch_comboBox.currentIndexChanged.connect(self.on_epoch_width_change)

        # Set up for a single function combobox change
        self.signal_views = [
            self.ui.signal_1_graphicsView,
            self.ui.signal_2_graphicsView,
            self.ui.signal_3_graphicsView,
            self.ui.signal_4_graphicsView,
            self.ui.signal_5_graphicsView,
            self.ui.signal_6_graphicsView,
            self.ui.signal_7_graphicsView,
            self.ui.signal_8_graphicsView,
            self.ui.signal_9_graphicsView,
            self.ui.signal_10_graphicsView,
        ]

        self.signal_comboboxes = [
            self.ui.signal_1_comboBox,
            self.ui.signal_2_comboBox,
            self.ui.signal_3_comboBox,
            self.ui.signal_4_comboBox,
            self.ui.signal_5_comboBox,
            self.ui.signal_6_comboBox,
            self.ui.signal_7_comboBox,
            self.ui.signal_8_comboBox,
            self.ui.signal_9_comboBox,
            self.ui.signal_10_comboBox,
        ]

        # Connect Combo Box Change
        for i, cb in enumerate(self.signal_comboboxes):
            cb.currentTextChanged.connect(partial(self.on_signal_combobox_changed, i))

        # Set Up list widget
        font = self.ui.annotation_listWidget.font()
        font.setPointSize(self.listBoxFontSize)
        self.ui.annotation_listWidget.setFont(font)
        self.ui.annotation_listWidget.itemDoubleClicked.connect(self.annotation_list_widget_double_click)

        # Store multi-taper results
        self.multitaper_spectrogram_obj:MultitaperSpectrogram = None

        # Turn on menu buttons
        self.ui.actionOpen_Edf.triggered.connect(self.open_edf_menu_item)
        self.ui.actionOpen_XML.triggered.connect(self.open_xml_menu_item)
        self.ui.actionSettings.triggered.connect(self.settings_menu_item)

        self.ui.actionEDF_Summary.triggered.connect(self.edf_summary_menu_item)
        self.ui.actionEDF_Signal_Export_2.triggered.connect(self.edf_signal_export_menu_item)
        self.ui.actionAnnotation_Summary.triggered.connect(self.annotation_summary_menu_item)
        self.ui.actionAnnotation_Export.triggered.connect(self.annotation_export_menu_item)
        self.ui.actionSleep_Stages_Export.triggered.connect(self.sleep_stages_export_menu_item)

        self.ui.actionEDF_Standard.triggered.connect(self.edf_standard_menu_item)
        self.ui.actionAnnotation_Standard.triggered.connect(self.xml_standard_menu_item)
        self.ui.actionAbout.triggered.connect(self.about_menu_item)

        # Turn Off Epoch Buttons
        self.turn_off_edf_signal_pushbuttons()
    # Initialize EDF
    def load_edf_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open EDF File", "", "EDF Files (*.edf)")
        try:
            # Create XML Object
            self.edf_file_obj = EdfFile(file_path)
            self.edf_file_obj.load()

            # Update interface
            self.ui.load_edf_textEdit.setText(f"{file_path}")

            # QMessageBox.information(self, "XML Loaded", f"Loaded: {file_path}")
            logger.info(f"Loaded EDF: {file_path}")
        except:
            logger.error('SleepScienceViewer: Error loading XML file.')

        if file_path:
            # Set epoch display options
            self.initialize_epoch_variables()
            if self.annotation_xml_obj != None:
                self.clear_annotation_widgets()
            clear_spectrogram_plot(parent_widget=self.ui.spectrogram_graphicsView)

            # Set Spectrogram Signal Labels
            signal_labels = self.edf_file_obj.edf_signals.signal_labels
            eeg_labels = self.edf_file_obj.edf_signals.eeg_signal_labels  # Will want a new one with stepped signals
            stepped_signal_list = self.edf_file_obj.edf_signals.return_stepped_signals_from_list(signal_labels)
            continuous_signal_list = self.edf_file_obj.edf_signals.return_continuous_signals_from_list(
                signal_labels)
            self.ui.spectrogram_comboBox.clear()
            self.ui.spectrogram_comboBox.addItems(continuous_signal_list)

            # Determine length of signal
            epoch_width = self.epoch_display_options_width_sec[self.ui.epoch_comboBox.currentIndex()]
            max_num_epochs = self.edf_file_obj.edf_signals.return_num_epochs(eeg_labels[0], epoch_width)
            self.max_epoch = max_num_epochs
            self.signal_length_seconds = self.edf_file_obj.edf_signals.return_signal_length_seconds(
                signal_labels[0], epoch_width)

            # Update epoch label
            time_str = self.return_time_string(self.current_epoch, epoch_width)
            self.ui.epochs_label.setText(f" of {max_num_epochs} epochs ({time_str})")

            # Draw Signals
            self.set_signal_combo_boxes()

            # Turn on signal related buttons
            self.turn_on_edf_signal_pushbuttons()
    def initialize_epoch_variables(self):
        # Reset class epoch variable upon loading a new file
        self.max_epoch = 1
        self.current_epoch = 1
        self.current_epoch_width_index = 0
        self.signal_length_seconds = 1

        # Set epoch edit box to 1
        self.ui.epochs_textEdit.setText(f"{self.current_epoch}")
        self.ui.epochs_textEdit.setAlignment(Qt.AlignRight)

        # Set epoch combo box to 30 second window
        self.ui.epoch_comboBox.setCurrentIndex(self.current_epoch_width_index)
    def turn_off_edf_signal_pushbuttons(self):
        # Turn off edf signal related widgets
        self.ui.compute_spectrogram_pushButton.setEnabled(False)
        self.ui.first_pushButton.setEnabled(False)
        self.ui.next_epoch_pushButton.setEnabled(False)
        self.ui.update_epoch_pushButton.setEnabled(False)
        self.ui.epochs_textEdit.setEnabled(False)
        self.ui.previous_pushButton.setEnabled(False)
        self.ui.last_epoch_pushButton.setEnabled(False)
        self.ui.epoch_comboBox.setEnabled(False)
        self.ui.load_annotation_pushButton.setEnabled(False)
    def turn_on_edf_signal_pushbuttons(self):
        # Turn off edf signal related widgets
        self.ui.compute_spectrogram_pushButton.setEnabled(True)
        self.ui.first_pushButton.setEnabled(True)
        self.ui.next_epoch_pushButton.setEnabled(True)
        self.ui.update_epoch_pushButton.setEnabled(True)
        self.ui.epochs_textEdit.setEnabled(True)
        self.ui.previous_pushButton.setEnabled(True)
        self.ui.last_epoch_pushButton.setEnabled(True)
        self.ui.epoch_comboBox.setEnabled(True)
        self.ui.load_annotation_pushButton.setEnabled(True)
    def set_signal_combo_boxes(self):
        # Turn off signal plot update
        self.automatic_signal_redraw = False

        # Get signal labels
        signal_labels = self.edf_file_obj.edf_signals.signal_labels
        signal_labels.insert(0, '')
        num_available_signals = len(signal_labels)

        # Load signal pop up box
        signal_combo_boxes = [self.ui.signal_1_comboBox, self.ui.signal_2_comboBox, self.ui.signal_3_comboBox,
                              self.ui.signal_4_comboBox, self.ui.signal_5_comboBox, self.ui.signal_6_comboBox,
                              self.ui.signal_7_comboBox, self.ui.signal_8_comboBox, self.ui.signal_9_comboBox,
                              self.ui.signal_10_comboBox]

        # Turn off change signal while updating combobox list following selection of a new edf file
        for combo_box in signal_combo_boxes:
            combo_box.blockSignals(True)

        # add signal list to all comboboxes
        for combo in signal_combo_boxes:
            combo.clear()
            combo.addItems(signal_labels)

        # Turn combo change signals on
        for combo_box in signal_combo_boxes:
            combo_box.blockSignals(False)

        # Turn on signal plot update. Using the label list set the combobox sequentially to different labels.
        for i, combo in enumerate(signal_combo_boxes):
            if i + 1 < len(signal_labels):  # +1 to skip the inserted empty string
                combo.setCurrentIndex(i + 1)  # Set to the i-th signal
            else:
                combo.setCurrentIndex(0)  # Default to the empty string if no signal available
        # Turn auto redraw back on
        self.automatic_signal_redraw = True
    def compute_and_display_spectrogram(self):
        # Check before starting long computation

        if self.edf_file_obj != None:
            process_eeg = self.show_ok_cancel_dialog()
        else:
            self.show_missing_eeg_warning()

        if process_eeg == True:
            # Make sure figures are not inadvertenly generated
            self.automatic_signal_redraw = False

            # Get Continuous Signals
            signal_label = self.ui.spectrogram_comboBox.currentText()
            signal_type = 'continuous'
            signal_obj = self.edf_file_obj.edf_signals.return_edf_signal(signal_label, signal_type)
            signal_analysis_obj = EdfSignalAnalysis(signal_obj)

            # Compute Spectrogram
            logger.info(f'Computing spectrogram ({signal_label}): computation may be time consuming')
            multitaper_spectrogram_obj = signal_analysis_obj.multitapper_spectrogram()
            multitaper_spectrogram_obj.plot(self.ui.spectrogram_graphicsView)
            self.multitaper_spectrogram_obj = multitaper_spectrogram_obj

            # Record Spectrogram Completions
            self.ui.spectrogram_label.setText(f'Multitaper Spectrogram - {signal_label}')
            logger.info('Computing spectrogram: Computation completed')

            # Turn on signal update
            self.automatic_signal_redraw = True
    def draw_signals_in_graphic_views(self, annotation_marker=None):

        if self.automatic_signal_redraw == False:
            return

        signal_combo_boxes = [self.ui.signal_1_comboBox, self.ui.signal_2_comboBox, self.ui.signal_3_comboBox,
                              self.ui.signal_4_comboBox, self.ui.signal_5_comboBox, self.ui.signal_6_comboBox,
                              self.ui.signal_7_comboBox, self.ui.signal_8_comboBox, self.ui.signal_9_comboBox,
                              self.ui.signal_10_comboBox]

        graphic_views = [self.ui.signal_1_graphicsView, self.ui.signal_2_graphicsView,
                         self.ui.signal_3_graphicsView,
                         self.ui.signal_4_graphicsView, self.ui.signal_5_graphicsView,
                         self.ui.signal_6_graphicsView,
                         self.ui.signal_7_graphicsView, self.ui.signal_8_graphicsView,
                         self.ui.signal_9_graphicsView,
                         self.ui.signal_10_graphicsView]

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
    def show_ok_cancel_dialog(parent=None):
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Confirm Action")
        msg_box.setText(
            "Computing a multitaper spectrogram can be time consuming. Future versions will include a less computational alternative. \n\nDo you want to proceed?")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Ok)

        result = msg_box.exec()

        if result == QMessageBox.Ok:
            logger.info("OK clicked: Will continue ")
            return True
        else:
            logger.info(
                f"Message Dialog Box - Cancel clicked, Msg: {'Computing a multitaper spectrogram can be time consuming. Do you want to proceed?'} ")
            return False
    def show_signal_export_ok_cancel_dialog(parent=None):
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Confirm Action")
        msg_box.setText(
            "Writing signals to disk may take a while. \n\nDo you want to proceed?")
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Ok)

        result = msg_box.exec()

        if result == QMessageBox.Ok:
            logger.info("OK clicked: Will continue ")
            return True
        else:
            logger.info(
                f"Message Dialog Box - Cancel clicked, Msg: {'Writing signals to disk may take a while. \n\nDo you want to proceed?'} ")
            return False
    def show_missing_eeg_warning(self):
        QMessageBox.warning(
            self,
            "Missing EEG Signal",
            "Please load an EDF file with an EEG signal."
        )
    # Initialize Annotations
    def load_xml_file(self):
        # Write to log
        logger.info(f'Preparing to loading annotation file.')

        # Initiate annotation file selection
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
            self.ui.hypnogram_comboBox.blockSignals(True)
            self.ui.hypnogram_comboBox.clear()
            self.ui.hypnogram_comboBox.addItems(sleep_stage_labels)
            self.ui.hypnogram_comboBox.blockSignals(False)

            # Get Sleep Stage Mappings
            self.sleep_stage_mappings = self.annotation_xml_obj.sleep_stages_obj.return_sleep_stage_mappings()

            # Set annotation types
            annotations_type_list = self.annotation_xml_obj.scored_event_obj.scored_event_unique_names
            annotations_type_list.insert(0, 'All')
            self.ui.annotation_comboBox.clear()
            self.ui.annotation_comboBox.addItems(annotations_type_list)
            self.ui.annotation_listWidget.clear()
            annotations_list = self.annotation_xml_obj.scored_event_obj.scored_event_name_source_time_list
            t_start, t_end = self.extract_event_indexes(annotations_list[0])
            color_dict = self.annotation_xml_obj.scored_event_obj.scored_event_color_dict
            for item_text in annotations_list:
                item = QListWidgetItem(item_text)
                event_type = item_text[t_start:t_end].strip()
                # item.setBackground(QBrush(QColor("black")))
                if event_type in color_dict.keys():
                    text_color = self.invert_color(color_dict[event_type])
                else:
                    text_color = 'black'
                item.setForeground(QBrush(QColor(text_color)))
                self.ui.annotation_listWidget.addItem(item)
            self.annotations_list = annotations_list

            # Plot Hypnogram
            # self.draw_hypnogram_in_view(self.annotation_xml_obj.sleep_stages_obj, self.ui.hypnogram_graphicsView)
            self.annotation_xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.hypnogram_graphicsView)

            # Annotation File Loaded
            logger.info(f'Annotation file loaded {file_path}')

            # Copy stepped information into edf object if available
            if self.edf_file_obj != None:
                # Check if file names differ by extension
                edf_filename_basename = os.path.basename(self.edf_file_obj.file_name)
                xml_filename_basename = os.path.basename(self.annotation_xml_obj.file_name)
                edf_filename_basename = os.path.splitext(edf_filename_basename)[0]
                xml_filename_basename = os.path.splitext(xml_filename_basename)[0]
                text_distance = dl.distance_unicode(edf_filename_basename, xml_filename_basename)
                xmltext_contains_edftext = edf_filename_basename in xml_filename_basename
                logger.info(f'Checking if EDF and Annotation files names are aligned: text distance ({text_distance}), subset = {xmltext_contains_edftext}, {edf_filename_basename}, {xml_filename_basename}')
            # Turn on hypnogram combobox
            self.ui.hypnogram_comboBox.setEnabled(True)
            self.automatic_histogram_redraw = True
    def on_hypnogram_changed(self, index):
        # Update Variables
        if self.automatic_histogram_redraw:
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
    def clear_annotation_widgets(self):
        # Clear annotation histogram and object
        self.automatic_histogram_redraw = False
        # self.ui.annotation_comboBox.currentTextChanged.disconnect()
        self.ui.hypnogram_comboBox.setEnabled(False)
        self.ui.hypnogram_comboBox.clear()
        self.annotation_xml_obj.sleep_stages_obj.clear_hypnogram_plot(self.ui.hypnogram_graphicsView)
        self.annotation_xml_obj = None
        self.ui.load_annotation_textEdit.clear()
        # self.ui.epoch_comboBox.setEnabled(False)
        # self.ui.epoch_comboBox.clear()

        # Clear annotation lists
        self.ui.annotation_comboBox.clear()
        self.ui.annotation_listWidget.clear()

        # Clear spectrogram
    def extract_event_indexes(self, entry_text):
        index_start = entry_text.find('Name')
        index_end   = entry_text.find('Input')
        return (index_start, index_end)
    def invert_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        i_rgb     = tuple(255 - c for c in rgb_color)
        brightness = 0.299*i_rgb[0] + 0.587*i_rgb[1] + 0.114*i_rgb[2]
        if brightness > 100:
            factor = 100 / brightness
            i_rgb  =  tuple(int(c * factor) for c in i_rgb)
        return "#{:02X}{:02X}{:02X}".format(*i_rgb)
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
        logger.info(f"Epoch set to first ({self.current_epoch})")
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
    def on_signal_combobox_changed(self, index, text):
        logger.info(f"Signal {index + 1} combo box changed to {text}")

        signal_label = text
        graphic_view = self.signal_views[index]

        signal_type = ""
        epoch_num = int(self.ui.epochs_textEdit.toPlainText()) - 1
        epoch_width_index = self.ui.epoch_comboBox.currentIndex()
        epoch_width = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]
        convert_time_f = self.time_convert_f[epoch_width_index]
        time_axis_units = self.epoch_axis_units[epoch_width_index]

        # Check for stepped channels if annotation file is available
        is_signal_stepped = False
        stepped_dict = {}
        if self.annotation_xml_obj is not None:
            is_signal_stepped = signal_label in self.annotation_xml_obj.steppedChannels
            if is_signal_stepped:
                stepped_dict = self.annotation_xml_obj.steppedChannels[signal_label]

        # Plot signal
        self.edf_file_obj.edf_signals.plot_signal_segment(
            signal_label,
            signal_type,
            epoch_num,
            epoch_width,
            graphic_view,
            x_tick_settings=epoch_display_axis_grid,
            is_signal_stepped=is_signal_stepped,
            stepped_dict=stepped_dict,
            convert_time_f=convert_time_f,
            time_axis_units=time_axis_units
        )

        if text == '':
            text = "''"
        logger.info(f"Signal {index + 1} combo box changed to {text}")
    # Annotation
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
        epoch_window_in_seconds = self.epoch_display_options_width_sec[self.ui.epoch_comboBox.currentIndex()]
        new_epoch = float(annotation_time_in_sec)/epoch_window_in_seconds
        annotation_epoch_offset_start = (new_epoch - math.floor(new_epoch))*epoch_window_in_seconds
        new_epoch = math.floor(new_epoch) + 1
        self.ui.epochs_textEdit.setText(str(new_epoch))



        # Update signal graphic views to annotation epoch
        self.draw_signals_in_graphic_views(annotation_marker = annotation_epoch_offset_start)

        logger.info(f"Jumped to new signal epoch ({new_epoch}, epoch offset {int(annotation_epoch_offset_start)})")
    # Menu Item
    def open_edf_menu_item(self):
        self.load_edf_file()
    def open_xml_menu_item(self):
        self.load_xml_file()
    def settings_menu_item(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Info")
        msg_box.setText("Settings item is not implemented yet")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec()
    def edf_summary_menu_item(self):
        logger.info(f'EDF Summary Menu Item selected')
        if self.edf_file_obj != None:
            """
                Prompts the user to select a file path to save the EDF summary.
                Displays a message box if the user cancels the dialog.

                Parameters:
                    parent (QWidget): The parent widget for the dialog.

                Returns:
                    str or None: The selected file path or None if canceled.
                """
            # Compute Signal Statistics
            self.edf_file_obj.edf_signals = self.edf_file_obj.edf_signals.calc_edf_signal_stats()

            # Generate a suggested file name
            directory           = os.path.dirname(self.edf_file_obj.file_name)  # -> "/home/dennis/data"
            filename            = os.path.basename(self.edf_file_obj.file_name)
            suggested_file_name = os.path.splitext(filename)[0]
            suggested_file_name = suggested_file_name + '_edf_summary.json'

            # Query user file location pation
            file_path, _ = QFileDialog.getSaveFileName(self,"Save EDF Summary",
                suggested_file_name,"Text Files (*.json);;All Files (*)")

            if not file_path:
                logger.info("EDF Summary Save Canceled: No file selected for saving the EDF summary.")
                return None

            # Here you'd write your summary to the selected file path.
            # Example placeholder:
            try:
                self.edf_file_obj.export_summary_to_json(file_path)
                logger.info(f'EDF Summary Menu Item: File written to {file_path}')
            except Exception as e:
                QMessageBox.critical(parent, "Error", f"Failed to save EDF summary:\n{str(e)}")
                return None
        else:
            logger.info(f'EDF Summary Menu Item: EDF File not loaded. Summary not created')
    def edf_signal_export_menu_item(self):
        logger.info(f'EDF Signal Export Menu Item Selected')
        if self.edf_file_obj != None:
            """
                Prompts the user to select a file path to save the EDF summary.
                Displays a message box if the user cancels the dialog.

                Parameters:
                    parent (QWidget): The parent widget for the dialog.

                Returns:
                    str or None: The selected file path or None if canceled.
                """


            # Select folder
            dialog_title       = 'Select a signal export folder.'
            starting_directory = os.getcwd()
            folder_path = QFileDialog.getExistingDirectory(self, dialog_title,
                starting_directory, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

            if folder_path:
                # Verify to proceed
                proceed_flag = self.show_signal_export_ok_cancel_dialog()

                if proceed_flag:
                    self.edf_file_obj.edf_signals.export_signals_to_txt(folder_path, self.edf_file_obj.file_name)
                    logger.info(f'Signals written to folder: {folder_path}')
            else:
                logger.info(f'Folder not selected for signal export.')
                return
        else:
            logger.info(f'EDF Signal Export Menu Item: EDF File not loaded. Export not created not created')
    def annotation_summary_menu_item(self):
        if self.annotation_xml_obj != None:
            """
                Prompts the user to select a file path to save the Annotation summary.
                Displays a message box if the user cancels the dialog.

                Parameters:
                    parent (QWidget): The parent widget for the dialog.

                Returns:
                    str or None: The selected file path or None if canceled.
                """
            # Generate a suggested file name
            directory           = os.path.dirname(self.annotation_xml_obj.annotationFile)  # -> "/home/dennis/data"
            filename            = os.path.basename(self.annotation_xml_obj.annotationFile)
            suggested_file_name = os.path.splitext(filename)[0]
            suggested_file_name = suggested_file_name + '_annotation_summary.json'

            # Query user file location pation
            file_path, _ = QFileDialog.getSaveFileName(self,"Save Annotation Summary",
                suggested_file_name,"Text Files (*.json);;All Files (*)")

            if not file_path:
                logger.info("Annotation Summary Save Canceled: No file selected for saving the EDF summary.")
                return None

            # Here you'd write your summary to the selected file path.
            # Example placeholder:
            try:
                self.annotation_xml_obj.export_summary(filename = file_path)
                logger.info(f'Annotation Summary Menu Item: File written to {file_path}')
            except Exception as e:
                QMessageBox.critical(parent, "Error", f"Failed to save EDF summary:\n{str(e)}")
                return None
        else:
            logger.info(f'EDF Annotation Menu Item: Annotation File not loaded. Summary not created')
    def annotation_export_menu_item(self):
        pass
        if self.annotation_xml_obj != None:
            """
                Prompts the user to select a file path to save the Annotation Export.
                Displays a message box if the user cancels the dialog.

                Parameters:
                    parent (QWidget): The parent widget for the dialog.

                Returns:
                    str or None: The selected file path or None if canceled.
                """
            # Generate a suggested file name
            directory           = os.path.dirname(self.annotation_xml_obj.annotationFile)  # -> "/home/dennis/data"
            filename            = os.path.basename(self.annotation_xml_obj.annotationFile)
            suggested_file_name = os.path.splitext(filename)[0]
            suggested_file_name = suggested_file_name + '_annotation_export.xlsx'

            # Query user file location pation
            file_path, _ = QFileDialog.getSaveFileName(self,"Save Annotation Export",
                suggested_file_name,"Text Files (*.json);;All Files (*)")

            if not file_path:
                logger.info("Annotation Export Save Canceled: No file selected.")
                return None

            # Here you'd write your summary to the selected file path.
            # Example placeholder:
            try:
                self.annotation_xml_obj.scored_event_obj.export_event(filename = file_path)
                logger.info(f'Annotation Export Menu Item: File written to {file_path}')
            except Exception as e:
                QMessageBox.critical(parent, "Error", f"Failed to save EDF summary:\n{str(e)}")
                return None
        else:
            logger.info(f'EDF Annotation Export Item: Annotation File not loaded. Export not created')
    def sleep_stages_export_menu_item(self):
        if self.annotation_xml_obj != None:
            """
                Prompts the user to select a file path to export sleep stages.
                Displays a message box if the user cancels the dialog.

                Parameters:
                    parent (QWidget): The parent widget for the dialog.

                Returns:
                    str or None: The selected file path or None if canceled.
                """
            # Generate a suggested file name
            directory           = os.path.dirname(self.annotation_xml_obj.annotationFile)  # -> "/home/dennis/data"
            filename            = os.path.basename(self.annotation_xml_obj.annotationFile)
            suggested_file_name = os.path.splitext(filename)[0]
            suggested_file_name = suggested_file_name + '_sleep_stages.txt'

            # Query user file location pation
            file_path, _ = QFileDialog.getSaveFileName(self,"Save Sleep Stages",
                suggested_file_name,"Text Files (*.txt);;All Files (*)")

            if not file_path:
                logger.info("Sleep Stages Save Canceled: No file selected for saving the sleep stages to a file.")
                return None

            # Here you'd write your summary to the selected file path.
            # Example placeholder:
            try:
                self.annotation_xml_obj.sleep_stages_obj.set_output_dir(directory)
                self.annotation_xml_obj.sleep_stages_obj.export_sleep_stages(file_path)
                self.annotation_xml_obj.sleep_stages_obj.summary_scored_sleep_stages()
                logger.info(f'Sleep Stages Export Menu Item: File written to {file_path}')
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save Sleep Stages File:\n{str(e)}")
                return None
        else:
            logger.info(f'Sleep Stages Export Menu Item: Annotation File not loaded. Summary not created')
    def xml_standard_menu_item(self):
        dlg = SleepXMLInfoDialog(self)
        dlg.exec()
    def edf_standard_menu_item(self):
        dlg = EDFInfoDialog(self)
        dlg.exec()
    def about_menu_item(self):
        dlg = AboutDialog(self)
        dlg.exec()
    # Utilities
    def return_time_string(self, epoch:int, epoch_width:int):
        val     = float((epoch-1)*epoch_width)
        seconds = val
        hours   = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds) % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"
# Start Application
def show_main_window():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()
if __name__ == "__main__":
    show_main_window()# -*- coding: utf-8 -*-