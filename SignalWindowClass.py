# Signal Window Class
# Generates and independent window with a copy of the edf and xml object loaded by the Sleep Science Window.
#

# To Do:
#TODO: Check why sleep stages do not align with histrogram when increasing epoch width then reducting epoch width

# Modules
import logging
import math
import numpy as np

# Interface packages and modules
from PySide6.QtWidgets import QMainWindow, QSizePolicy, QListWidgetItem, QApplication, QMessageBox
from PySide6.QtCore import QEvent, Qt, QObject,Signal, QTimer
from PySide6.QtGui import QColor, QBrush, QFont, QFontDatabase
from PySide6.QtGui import QKeyEvent

# Sleep Science Classes
from EdfFileClass import EdfFile, EdfSignalAnalysis
from AnnotationXmlClass import AnnotationXml

# GUI Interface
from SignalViewer import Ui_SignalWindow  # the generated file from your .ui

# Set up a module-level logger
logger = logging.getLogger(__name__)

# To Do List


# Utilities
def clear_spectrogram_plot(parent_widget = None):
    layout = parent_widget.layout()
    if layout:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
def set_layout_visible(layout, visible: bool):
    """
    Recursively set visibility for all widgets in a layout and its nested layouts.

    Args:
        layout: QLayout object to process
        visible: Boolean indicating whether to show (True) or hide (False) widgets
    """
    for i in range(layout.count()):
        item = layout.itemAt(i)

        # Check if the item is a widget
        widget = item.widget()
        if widget:
            widget.setVisible(visible)

        # Check if the item is a nested layout
        nested_layout = item.layout()
        if nested_layout:
            # Recursively process the nested layout
            set_layout_visible(nested_layout, visible)
class NumericTextEditFilter(QObject):
    enterPressed = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and isinstance(event, QKeyEvent):
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:  # Qt.Key.Key_Return in PySide6
                self.enterPressed.emit()  # Emit signal when Enter is pressed
                return True  # Consume the event so it doesn't insert a newline
            if event.key() == Qt.Key.Key_Backspace or event.key() == Qt.Key.Key_Delete:
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

        # Initialize epoch variables
        self.max_epoch = 1
        self.current_epoch = 1
        self.current_epoch_width_index = 0
        self.signal_length_seconds = 1

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
        signal_combobox_index = signal_combobox_index if signal_combobox_index is not None else 0
        self.signal_label = self.signal_labels[signal_combobox_index]
        self.ui.comboBox_signals.setCurrentIndex(signal_combobox_index)

        # Time Unit Converstions
        s_to_min = lambda s: int(s / 60)
        s_to_s   = lambda s: int(s)

        # Set up epoch controls
        self.epoch_display_options_text:list        = ['30 s', '1 min', '2 min', '4 min', '5 min','8 min', '10 min', '1 hr']
        self.epoch_display_options_width_sec:list  = [ 30,     60,    120,    240,   300,  480,   600,   3600]
        self.epoch_display_axis_grid:list           = [ [5,1],  [10,2], [60,10],  [60, 10], [60, 10], [120, 30],[120, 30], [600, 50] ]
        self.epoch_axis_units:list                  = ['s', 's', 'm', 'm', 'm', 'm' , 'm', 'm']
        self.time_convert_f:list                    = [s_to_s, s_to_s, s_to_min, s_to_min, s_to_min, s_to_min, s_to_min, s_to_min]

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
        self.ui.pushButton_epoch_show_stages.toggled.connect(self.show_signal_stages)

        # Set up signal
        self.signal        = self.edf_obj.edf_signals.signals_dict[self.signal_label]
        self.signal_units  = self.edf_obj.edf_signals.signal_units_dict[self.signal_label]
        self.sampling_time = self.edf_obj.edf_signals.signal_sampling_time_dict[self.signal_label]

        # Initialize epoch variables
        self.initialize_epoch_variables()

        # Initialize Filter
        self.numeric_filter = None

        # Define filter combo box entries
        self.filter_low_menu_text = ['', '0.1 Hz', '0.5 Hz', '1.0 Hz', '10 Hz']
        self.filter_high_menu_text = ['', '50 Hz', '60 Hz', '70 Hz']
        self.filter_notch_text = ['', '50 Hz', '60 Hz']

        # Define filter combo box values
        self.filter_low_menu_val = [-1, 0.1, 0.5, 1.0, 10.0]
        self.filter_high_menu_val = [-1, 50.0, 60.0, 70.0]
        self.filter_notch_val = [-1, 50.0, 60.0]
        self.initialize_filter_variables()
        self.ui.pushButton_filter.toggled.connect(self.filter_button_toggled)
        self.ui.pushButton_notch.toggled.connect(self.notch_button_toggled)
        self.filter_param = [-1, -1, -1]  # Setting filtering off

        # Draw signals in graphic view
        self.automatic_signal_redraw = True
        self.draw_signal_in_graphic_views()

        # Connect change in combo box
        self.ui.comboBox_signals.currentTextChanged[str].connect(self.update_signal_combobox)
        self.ui.comboBox_epoch.currentTextChanged[str].connect(self.update_epoch_combobox)

        # Connect sync push button to response
        self.ui.pushButton_sync_y.clicked.connect(self.sync_y_pushbutton_response)

        # Spectrogram Buttons
        self.ui.pushButton_show_spectrogram.clicked.connect(self.compute_and_display_spectrogram)
        self.ui.pushButton_spectrogram_legend.clicked.connect(self.show_spectrogram_legend)
        self.ui.pushButton_heatmap.clicked.connect(self.show_heatmap)
        self.ui.pushButton_heat_legend.clicked.connect(self.show_heapmap_legend)

        # State Control
        self.combo_boxes_mark = [self.ui.comboBox_mark_1,  self.ui.comboBox_mark_2,  self.ui.comboBox_mark_3,
                                 self.ui.comboBox_mark_4,  self.ui.comboBox_mark_5,  self.ui.comboBox_mark_6,
                                 self.ui.comboBox_mark_7,  self.ui.comboBox_mark_8,  self.ui.comboBox_mark_9,
                                 self.ui.comboBox_mark_10, self.ui.comboBox_mark_11, self.ui.comboBox_mark_12,
                                 self.ui.comboBox_mark_13, self.ui.comboBox_mark_14, self.ui.comboBox_mark_15]
        self.hide_mark_combo_boxes()
        self.ui.pushButton_mark.toggled.connect(self.pushbutton_mark_toggled)

        # Section show/hide buttons
        self.ui.pushButton_show_spectrogram_plot.clicked.connect(self.show_spectrogram_push)
        self.ui.pushButton_show_hypnogram.clicked.connect(self.show_hypnogram_push)
        self.ui.pushButton_show_annotation_panel.clicked.connect(self.show_annotation_push)
        self.ui.pushButton_hypnogram_legend.clicked.connect(self.show_hypnogram_legend)

        # Set up hypnogram and annotation list
        self.sleep_stage_mappings = None
        self.annotations_list     = None
        self.ui.listWidget_annotation.clear()
        self.initialize_hypnogram_and_annotations()

        # Assign the annotation list widget to a fixed width font
        all_families = QFontDatabase.families()
        monospace_fonts = [f for f in all_families if QFontDatabase.isFixedPitch(f)]
        selected_font = monospace_fonts[0] if monospace_fonts else "Courier"
        font = QFont(selected_font, 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.ui.listWidget_annotation.setFont(font)

        # Hypnogram
        self.hypnogram_combobox_selection = None
        self.ui.comboBox_hypnogram.currentIndexChanged.connect(self.on_hypnogram_changed)

        # Setuo Interface

        # Store Spectrogram Object
        self.multitaper_spectrogram_obj = None

    # Setup Interface
    def initialize_epoch_variables(self):
        # Reset class epoch variable upon loading a new file
        self.max_epoch = 1
        self.current_epoch = 1
        self.current_epoch_width_index = 0
        self.signal_length_seconds = 1
        epoch_start_index = 0

        # Set up epic combobox
        self.ui.comboBox_epoch.clear()
        self.ui.comboBox_epoch.addItems(self.epoch_display_options_text)
        self.ui.comboBox_epoch.setCurrentIndex(epoch_start_index)

        # Set maximum number of epochs
        epoch_width     = self.epoch_display_options_width_sec[self.ui.comboBox_epoch.currentIndex()]
        self.max_epoch  = self.edf_obj.edf_signals.return_num_epochs(self.signal_label, epoch_width)

        # Set up epic combobox
        self.ui.comboBox_epoch.clear()
        self.ui.comboBox_epoch.addItems(self.epoch_display_options_text)

        # Set epoch edit box to 1
        self.ui.textEdit_epoch.setText(f"{self.current_epoch}")
        self.ui.textEdit_epoch.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Set epoch string
        time_str = self.return_time_string(self.current_epoch, epoch_width)
        self.ui.label_page.setText(f'of {self.max_epoch} epochs, ({time_str})')

        # Edit Box Actions
        self.numeric_filter = NumericTextEditFilter(self)
        self.ui.textEdit_epoch.installEventFilter(self.numeric_filter)
        self.numeric_filter.enterPressed.connect(self.enter_pressed_epoch_edit)
    def initialize_filter_variables(self):
        # Define filter combo box entries
        self.filter_low_menu_text  = ['', '0.1 Hz', '0.5 Hz', '1.0 Hz', '10 Hz']
        self.filter_high_menu_text = ['', '50 Hz', '60 Hz', '70 Hz']
        self.filter_notch_text     = ['', '50 Hz', '60 Hz']

        # Define filter combo box values
        self.filter_low_menu_val   = [-1, 0.1 , 0.5, 1.0, 10.0]
        self.filter_high_menu_val  = [-1, 50.0, 60.0, 70.0]
        self.filter_notch_val      = [-1, 50.0, 60.0]

        # Set filter combo box values
        self.ui.comboBox_filter_low.addItems(self.filter_low_menu_text)
        self.ui.comboBox_filter_high.addItems(self.filter_high_menu_text)
        self.ui.comboBox_filter_notch.addItems(self.filter_notch_text)
    def initialize_hypnogram_and_annotations(self):
        # Set Sleep Stage Labels
        sleep_stage_labels = self.xml_obj.sleep_stages_obj.return_sleep_stage_labels()
        sleep_stage_labels.remove(sleep_stage_labels[0])
        self.ui.comboBox_hypnogram.blockSignals(True)
        self.ui.comboBox_hypnogram.clear()
        self.ui.comboBox_hypnogram.addItems(sleep_stage_labels)
        self.ui.comboBox_hypnogram.blockSignals(False)

        # Get Sleep Stage Mappings
        self.sleep_stage_mappings = self.xml_obj.sleep_stages_obj.return_sleep_stage_mappings()

        # Set annotation types
        annotations_type_list = self.xml_obj.scored_event_obj.scored_event_unique_names
        #annotations_type_list.insert(0, 'All')

        # Update annotation marker
        self.ui.comboBox_annotation.setEnabled(False)
        self.ui.comboBox_annotation.blockSignals(True)
        self.ui.comboBox_annotation.clear()
        self.ui.comboBox_annotation.addItems(annotations_type_list)

        # Update Annotation Text in List Widget
        self.ui.listWidget_annotation.clear()
        annotations_list = self.xml_obj.scored_event_obj.scored_event_name_source_time_list
        t_start, t_end = self.extract_event_indexes(annotations_list[0])
        color_dict = self.xml_obj.scored_event_obj.scored_event_color_dict
        for item_text in annotations_list:
            item = QListWidgetItem(item_text)
            event_type = item_text[t_start:t_end].strip()
            # item.setBackground(QBrush(QColor("black")))
            if event_type in color_dict.keys():
                text_color = 'black'
            else:
                text_color = 'black'
            item.setForeground(QBrush(QColor(text_color)))
            self.ui.listWidget_annotation.addItem(item)
        self.annotations_list = annotations_list

        # Connect annotation combo box to a response
        self.ui.comboBox_annotation.currentTextChanged.connect(self.on_annotation_combobox_text_changed)

        # Plot Hypnogram
        hypnogram_marker = 0

        # Determine whether to show colored staged rectangles
        show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()

        # Plot Hypnogram
        self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                     hypnogram_marker=hypnogram_marker,
                                                     double_click_callback=self.on_hypnogram_double_click,
                                                     show_stage_colors = show_stage_colors)

        # Set up show stages button
        self.ui.pushButton_show_hypnogram_stages_in_color.clicked.connect(self.show_stages_on_hypnogram)

        # Plot annotations
        total_time_in_seconds = self.xml_obj.sleep_stages_obj.time_seconds
        cur_annotation_setting = self.ui.comboBox_annotation.currentText()
        # print(f'cur_annotation_setting = "{cur_annotation_setting}"')
        self.xml_obj.scored_event_obj.plot_annotation(total_time_in_seconds,
                                                                 self.ui.graphicsView_annotation_plot,
                                                                 annotation_filter=cur_annotation_setting,
                                                                 double_click_callback=self.on_annotation_double_click)
        # Set up plot legend
        self.ui.pushButton_annotation_legend.clicked.connect(self.show_annotation_legend_popup)
        self.ui.listWidget_annotation.itemDoubleClicked.connect(self.annotation_list_widget_double_click)

        # Turn on annotations
        self.ui.comboBox_annotation.setEnabled(True)
        self.ui.comboBox_annotation.blockSignals(False)

    # Interface
    def show_spectrogram_push(self,checked: bool):
        logger.info('Show/Hide  spectrogram')
        # Recursively show/hide widgets in layouts
        self.set_layout_visible(self.ui.horizontalLayout_spectrogam,checked)
        self.set_layout_visible(self.ui.verticalLayout_spectrogram_commands, checked)
        self.set_layout_visible(self.ui.horizontalLayout_spectrogram_label, checked)
    def show_hypnogram_push(self,checked: bool):
        logger.info('Show/Hide  hypnogram')
        # Recursively show/hide widgets in layouts
        self.set_layout_visible(self.ui.horizontalLayout_hypnogram,checked)
        self.set_layout_visible(self.ui.verticalLayout_hypnogram_commands , checked)
    def show_annotation_push(self,checked: bool):
        logger.info('Show/Hide  annotation')
        # Recursively show/hide widgets in layouts
        self.set_layout_visible(self.ui.horizontalLayout_annotation_plot, checked)
        self.set_layout_visible(self.ui.verticalLayout_annotation_list_widget, checked)
    @staticmethod
    def set_layout_visible(layout, visible: bool):
        """
        Recursively set visibility for all widgets in a layout and its nested layouts.

        Args:
            layout: QLayout object to process
            visible: Boolean indicating whether to show (True) or hide (False) widgets
        """
        for i in range(layout.count()):
            item = layout.itemAt(i)

            # Check if the item is a widget
            widget = item.widget()
            if widget:
                widget.setVisible(visible)

            # Check if the item is a nested layout
            nested_layout = item.layout()
            if nested_layout:
                # Recursively process the nested layout
                set_layout_visible(nested_layout, visible)

    # Visualization
    def draw_signal_in_graphic_views(self, annotation_marker:float=None,
                                     epochs_to_draw:int=None):

        if not self.automatic_signal_redraw:
            return

        # Turn off combo box signal change
        self.ui.comboBox_signals.blockSignals(True)

        epochs_to_draw = self.number_of_epochs_on_screen if epochs_to_draw is None else epochs_to_draw

        epoch_labels  = [self.ui.label_signal_1,  self.ui.label_signal_2,  self.ui.label_signal_3,
                         self.ui.label_signal_4,  self.ui.label_signal_5,  self.ui.label_signal_6,
                         self.ui.label_signal_7,  self.ui.label_signal_8,  self.ui.label_signal_9,
                         self.ui.label_signal_10, self.ui.label_signal_11, self.ui.label_signal_12,
                         self.ui.label_signal_13, self.ui.label_signal_14, self.ui.label_signal_15]
        graphic_views = [self.ui.graphicsView_signal_1,  self.ui.graphicsView_signal_2,  self.ui.graphicsView_signal_3,
                         self.ui.graphicsView_signal_4,  self.ui.graphicsView_signal_5,  self.ui.graphicsView_signal_6,
                         self.ui.graphicsView_signal_7,  self.ui.graphicsView_signal_8,  self.ui.graphicsView_signal_9,
                         self.ui.graphicsView_signal_10, self.ui.graphicsView_signal_11, self.ui.graphicsView_signal_12,
                         self.ui.graphicsView_signal_13, self.ui.graphicsView_signal_14, self.ui.graphicsView_signal_15]

        # Set epoch numbers on interface to correspond to graphic view
        current_epoch = int(self.ui.textEdit_epoch.toPlainText())
        for i, label in enumerate(epoch_labels):
            if current_epoch+i <= self.max_epoch:
                label.setText(str(current_epoch+i))
            else:
                label.setText(" ")


        # Update graphic view
        epoch_num               = current_epoch - 1  # function expect zero indexing, reset epoch to signal start
        epoch_width_index       = self.ui.comboBox_epoch.currentIndex()
        epoch_width             = float(self.epoch_display_options_width_sec[epoch_width_index])
        epoch_display_axis_grid = self.epoch_display_axis_grid[epoch_width_index]
        convert_time_f          = self.time_convert_f[epoch_width_index]
        time_axis_units         = self.epoch_axis_units[epoch_width_index]
        signal_type             = ""

        print(f'epoch_width_index = {epoch_width_index}, epoch_width = {epoch_width}')

        # Set signal label
        signal_label = self.ui.comboBox_signals.currentText()

        # Get filtering parameters
        filter_param = self.filter_param

        print(f'filter_param = {filter_param} ')

        # Determine y limits
        if self.ui.pushButton_sync_y.isChecked():
            page_signals = self.edf_obj.edf_signals.return_signal_segments(
                signal_label, "not implemented", current_epoch, current_epoch+epochs_to_draw-1, epoch_width)
            print(f'page_signals = {page_signals}')
            y_page_min   = np.min(page_signals)
            y_page_max   = np.max(page_signals)
            y_axis_page_limits = [y_page_min, y_page_max]
        else:
            y_axis_page_limits = None

        # Get units
        signal_units = self.edf_obj.edf_signals.signal_units_dict[signal_label]
        signal_units.strip()
        if signal_units == "":
            signal_units = None

        stepped_dict = {}  # Initialize to remove warning
        for i, graphic_view in enumerate(graphic_views):
            # Select graphic view
            signal_label = signal_label
            graphic_view = graphic_view

            # Set stepped variables
            stepped_dict      = {}
            is_signal_stepped = False
            if self.xml_obj is not None:
                is_signal_stepped = signal_label in self.xml_obj.steppedChannels.keys()
                if is_signal_stepped:
                    stepped_dict = self.xml_obj.steppedChannels[signal_label]

            # Check if this is an edge case
            if i >= epochs_to_draw:
                # force zero signal
                signal_label = ""

            # Get sleep stages
            sleep_stage_dict_list = None
            if self.ui.pushButton_epoch_show_stages.isChecked():
                epoch_start = epoch_num + i
                # epoch_end = epoch_start + int(epoch_num + epoch_width / self.xml_obj.epochLength)
                # epoch_end   = epoch_start + int(epoch_num+epoch_width/self.xml_obj.epochLength)
                #print(f'draw signal in graphic view: epoch_start = {epoch_start}, epoch_end = {epoch_end}')
                stage_epoch_start = round(epoch_start*epoch_width/self.xml_obj.epochLength)
                stage_epoch_end   = stage_epoch_start + round(epoch_width/self.xml_obj.epochLength)
                #print(f'draw signal in graphic view: stage_epoch_start = {stage_epoch_start}, stage_epoch_end = {stage_epoch_end}')
                sleep_stage_dict_list = self.xml_obj.sleep_stages_obj.return_zeroed_sleep_stage_time_dictionary(
                    stage_epoch_start, stage_epoch_end)
                #print(f'sleep_stage_dict_list = {sleep_stage_dict_list}')

            # Plot signal segment
            if epoch_num+i >= self.max_epoch:
                signal_label = ""

            # Assume annotation is in the first marker
            if annotation_marker is not None and i == 0:
                annotation_time_in_sec = annotation_marker
                annotation_epoch = float(annotation_time_in_sec) / epoch_width
                epoch_annotation_marker = (annotation_epoch - math.floor(annotation_epoch)) * epoch_width
            else:
                epoch_annotation_marker = None

            # Plot current epoch
            self.edf_obj.edf_signals.plot_signal_segment(signal_label,
                                                              signal_type, epoch_num+i, epoch_width, graphic_view,
                                                              x_tick_settings       = epoch_display_axis_grid,
                                                              annotation_marker     = epoch_annotation_marker,
                                                              convert_time_f        = convert_time_f,
                                                              time_axis_units       = time_axis_units,
                                                              is_signal_stepped     = is_signal_stepped,
                                                              stepped_dict          = stepped_dict,
                                                              turn_xaxis_labels_off = True,
                                                              filter_param          = filter_param,
                                                              y_limits              = y_axis_page_limits,
                                                              y_axis_units          = signal_units,
                                                              sleep_stages          = sleep_stage_dict_list)

        # Create x-axis for reference
        signal_label = "" # force no signal
        graphic_view = self.ui.graphicsView_signal_axis
        is_signal_stepped = False
        self.edf_obj.edf_signals.plot_signal_segment(signal_label,
                                                     signal_type, epoch_num, epoch_width, graphic_view,
                                                     x_tick_settings       = epoch_display_axis_grid,
                                                     annotation_marker     = annotation_marker,
                                                     convert_time_f        = convert_time_f,
                                                     time_axis_units       = time_axis_units,
                                                     is_signal_stepped     = is_signal_stepped,
                                                     stepped_dict          = stepped_dict,
                                                     turn_xaxis_labels_off = False,
                                                     filter_param          = filter_param)

        #Turn on combo box signal change
        self.ui.comboBox_signals.blockSignals(False)

        # Update epoch label string
        epoch_width    = self.epoch_display_options_width_sec[self.ui.comboBox_epoch.currentIndex()]
        self.max_epoch = self.edf_obj.edf_signals.return_num_epochs_from_width(epoch_width)
        time_str       = self.return_time_string(current_epoch, epoch_width)
        self.ui.label_page.setText(f" of {self.max_epoch} epochs ({time_str})")

    # State Control
    def hide_mark_combo_boxes(self):
        for cb in self.combo_boxes_mark:
            cb.hide()
        self.ui.horizonatal_spacer_signal_combo_mark.changeSize(0, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    def show_mark_combo_boxes(self):
        for cb in self.combo_boxes_mark:
            cb.show()
        self.ui.horizonatal_spacer_signal_combo_mark.changeSize(75, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ui.horizontalLayout_signal_time.update()
    def pushbutton_mark_toggled(self, checked):
        if checked:
            self.show_mark_combo_boxes()
        else:
            self.hide_mark_combo_boxes()

    # Signal Actions
    def update_signal_combobox (self, signal_label):
        # turn off update signal combobox
        self.ui.comboBox_signals.blockSignals(True)

        # Update signal graphic views
        self.draw_signal_in_graphic_views()

        # Clear Spectrogram
        clear_spectrogram_plot(parent_widget=self.ui.graphicsView_spectrogram)
        self.multitaper_spectrogram_obj.clear_data_heatmap_variables()

        # turn off update signal combobox
        self.ui.comboBox_signals.blockSignals(False)

        # log action
        logger.info(f'Signal combobox changed to {signal_label}')
    def filter_button_toggled(self, checked:bool):
        if checked:
            lowcut = self.filter_low_menu_val[self.ui.comboBox_filter_low.currentIndex()]
            highcut = self.filter_high_menu_val[self.ui.comboBox_filter_high.currentIndex()]
            self.filter_param = [lowcut, highcut, self.filter_param[2]]
            logger.info(f'Setting filtering parameters: lowcut = {lowcut}, highcut  = {highcut}')
        else:
            self.filter_param = [-1, -1, self.filter_param[2]]
            logger.info(f'Turning filter Setting Off')
    def notch_button_toggled(self, checked:bool):
        if checked:
            notch = self.filter_notch_val[self.ui.comboBox_filter_notch.currentIndex()]
            self.filter_param = [self.filter_param[0], self.filter_param[1], notch]
            logger.info(f'Setting notch parameter: notch = {notch}')
        else:
            self.filter_param = [-1, -1, self.filter_param[2]]
            logger.info(f'Turning Notch Setting Off')
    def sync_y_pushbutton_response(self):
        self.draw_signal_in_graphic_views()

    # Hypnogram
    def on_hypnogram_double_click(self, x_value, _y_value):
        # print(f'Sleep Science Viewer: x_value = {x_value}, y_value = {y_value}')
        # Slot to handle double-click events on QListWidget items.
        logger.info(f"Hypnogram plot double-clicked: time in seconds {x_value}")
        if self.edf_obj is None:
            return

        # Change cursor to busy
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        # Get double click x value
        annotation_time_in_sec = x_value

        # Change Current epoch
        epoch_window_in_seconds = self.epoch_display_options_width_sec[self.ui.comboBox_epoch.currentIndex()]
        new_epoch = float(annotation_time_in_sec) / epoch_window_in_seconds
        annotation_epoch_offset_start = (new_epoch - math.floor(new_epoch)) * epoch_window_in_seconds
        new_epoch = math.floor(new_epoch) + 1
        self.ui.textEdit_epoch.setText(str(new_epoch))
        self.current_epoch = new_epoch

        # Update signal graphic views to annotation epoch
        # self.draw_signals_in_graphic_views(annotation_marker=annotation_epoch_offset_start)

        # Plot Hypnogram
        hypnogram_marker = annotation_time_in_sec
        show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()
        self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                     hypnogram_marker=hypnogram_marker,
                                                     double_click_callback=self.on_hypnogram_double_click,
                                                     show_stage_colors = show_stage_colors
                                                     )

        # Update Signals
        self.draw_signal_in_graphic_views()


        # Revert cursor to pointer
        QApplication.restoreOverrideCursor()

        logger.info(f"Jumped to new signal epoch ({new_epoch}, epoch offset {int(annotation_epoch_offset_start)})")
    def on_hypnogram_changed(self, index):
        # Update Variables
        if self.automatic_histogram_redraw:
            selected_text = self.ui.comboBox_hypnogram.itemText(index)
            self.hypnogram_combobox_selection = index
            logger.info(f"Combo box changed to index {index}: {selected_text}")

            # Determine whether to show colored staged rectangles
            show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()

            # Update Hypnogram
            if self.sleep_stage_mappings is not None:
                # Get time
                current_epoch = int(self.ui.textEdit_epoch.toPlainText())
                window_width_sec = self.epoch_display_options_width_sec[self.ui.comboBox_epoch.currentIndex()]
                hypnogram_marker = (current_epoch -1)*window_width_sec # zero referenced epoch

                stage_map = index
                self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                            stage_index=stage_map,
                                                            hypnogram_marker=hypnogram_marker,
                                                            double_click_callback=self.on_hypnogram_double_click,
                                                            show_stage_colors = show_stage_colors)
    def show_stages_on_hypnogram(self):
        # Pretend hypnogram combobox change to update
        if self.automatic_histogram_redraw:
            index = self.ui.comboBox_hypnogram.currentIndex()
            self.on_hypnogram_changed(index)
    def show_hypnogram_legend(self):
        self.xml_obj.sleep_stages_obj.show_sleep_stages_legend()

    # Spectrogram
    def compute_and_display_spectrogram(self):
        # Check before starting long computation

        process_eeg = False
        if self.edf_obj is not None:
            process_eeg = self.show_ok_cancel_dialog()
        else:
            logger.info(f'EDF file not loaded. Can not compute spectrogram.')

        if process_eeg:
            # Turn on busy cursor
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

            # Make sure figures are not inadvertenly generated
            self.automatic_signal_redraw = False

            # Get Continuous Signals
            signal_label = self.ui.comboBox_signals.currentText()
            signal_type = 'continuous'
            signal_obj = self.edf_obj.edf_signals.return_edf_signal(signal_label, signal_type)
            signal_analysis_obj = EdfSignalAnalysis(signal_obj)

            # Compute Spectrogram
            logger.info(f'Computing spectrogram ({signal_label}): computation may be time consuming')
            multitaper_spectrogram_obj = signal_analysis_obj.multitapper_spectrogram()
            if multitaper_spectrogram_obj.spectrogram_computed:
                # Plot spectrogram if computer
                multitaper_spectrogram_obj.plot(self.ui.graphicsView_spectrogram,
                                                double_click_callback=self.on_spectrogram_double_click)
                # Update log
                logger.info(f'Spectrogram plotted')
            else:
                # Plot signal heatmap
                multitaper_spectrogram_obj.plot_data(self.ui.graphicsView_spectrogram,
                                                     double_click_callback=self.on_spectrogram_double_click)
                logger.info(f'Plotted heatmap instead')

            self.multitaper_spectrogram_obj = multitaper_spectrogram_obj

            # Record Spectrogram Completions
            if self.multitaper_spectrogram_obj.spectrogram_computed:
                self.multitaper_spectrogram_obj = multitaper_spectrogram_obj
                self.ui.label_spectrogram.setText(f'Multitaper Spectrogram - {signal_label}')
                logger.info('Computing spectrogram: Computation completed')
            else:
                self.multitaper_spectrogram_obj = multitaper_spectrogram_obj
                self.ui.label_spectrogram.setText(f'Data Heatmap - {signal_label}')
                logger.info('Computing spectrogram: Computation completed')

            # Turn off busy cursor
            QApplication.restoreOverrideCursor()

            # Turn on signal update
            self.automatic_signal_redraw = True

            # Turn on Legend Pushbutton
            self.ui.pushButton_spectrogram_legend.setEnabled(True)
    def on_spectrogram_double_click(self, x_value, _y_value):
        # print(f'Sleep Science Viewer: x_value = {x_value}, y_value = {y_value}')
        # Slot to handle double-click events on QListWidget items.
        logger.info(f"Annotation plot double-clicked: time in seconds {x_value}")
        if self.edf_obj is None:
            return

        # Change cursor to busy
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        # Get double click x value
        annotation_time_in_sec = x_value

        # Change Current epoch
        epoch_window_in_seconds = self.epoch_display_options_width_sec[self.ui.comboBox_epoch.currentIndex()]
        new_epoch = float(annotation_time_in_sec) / epoch_window_in_seconds
        annotation_epoch_offset_start = (new_epoch - math.floor(new_epoch)) * epoch_window_in_seconds
        new_epoch = math.floor(new_epoch) + 1
        self.ui.textEdit_epoch.setText(str(new_epoch))
        self.current_epoch = new_epoch

        # Update signal graphic views to annotation epoch
        # self.draw_signals_in_graphic_views(annotation_marker=annotation_epoch_offset_start)

        # Plot Hypnogram
        hypnogram_marker = annotation_time_in_sec
        show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()
        self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                     hypnogram_marker=hypnogram_marker,
                                                     double_click_callback=self.on_hypnogram_double_click,
                                                     show_stage_colors=show_stage_colors
                                                     )

        # Update Signals
        self.draw_signal_in_graphic_views()

        # Revert cursor to pointer
        QApplication.restoreOverrideCursor()

        logger.info(f"Jumped to new signal epoch ({new_epoch}, epoch offset {int(annotation_epoch_offset_start)})")
    def show_spectrogram_legend(self):
        if not hasattr(self, 'multitaper_spectrogram_obj') or self.multitaper_spectrogram_obj is None:
            logger.info("Error: Spectrogram data not available. Generate spectrogram first.")
            return

        # Display legend dialog
        if self.multitaper_spectrogram_obj.spectrogram_computed:
            self.multitaper_spectrogram_obj.show_colorbar_legend_dialog()
            logger.info('Sleep Science Signal Viewer: Spectrogram dialog plotted')
        else:
            self.multitaper_spectrogram_obj.show_heatmap_legend_dialog()
            logger.info('Sleep Science Signal Viewer: Data heatmap plotted')
    def show_heatmap(self):
        # Check before starting long computation

        # Turn on busy cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        # Make sure figures are not inadvertenly generated
        self.automatic_signal_redraw = False

        # Get Continuous Signals
        signal_label = self.ui.comboBox_signals.currentText()
        signal_type = 'continuous'
        signal_obj = self.edf_obj.edf_signals.return_edf_signal(signal_label, signal_type)
        signal_analysis_obj = EdfSignalAnalysis(signal_obj)

        # Compute Spectrogram
        logger.info(f'Plotting heatmap: ({signal_label})')
        multitaper_spectrogram_obj = signal_analysis_obj.multitapper_spectrogram()

        # Plot signal heatmap
        multitaper_spectrogram_obj.plot_data(self.ui.graphicsView_spectrogram,
                                        double_click_callback=self.on_spectrogram_double_click)
        self.multitaper_spectrogram_obj = multitaper_spectrogram_obj

        # print(self.multitaper_spectrogram_obj.heatmap_fs)

        # Record Spectrogram Completions
        self.ui.label_spectrogram.setText(f'Data Heatmap - {signal_label}')
        logger.info('Computing spectrogram: Computation completed')

        # Turn off busy cursor
        QApplication.restoreOverrideCursor()

        # Turn on signal update
        self.automatic_signal_redraw = True

        # Turn on Legend Pushbutton
        self.ui.pushButton_spectrogram_legend.setEnabled(True)
    def show_heapmap_legend(self):
        if not hasattr(self, 'multitaper_spectrogram_obj') or self.multitaper_spectrogram_obj is None:
            logger.info(f"Signal Window Error: Heapmap data not available.")
            return

        # Display legend dialog
        self.multitaper_spectrogram_obj.show_heatmap_legend_dialog()
        logger.info('Sleep Science Signal Viewer: Data heatmap plotted')

    # Annotation
    def on_annotation_double_click(self, x_value, _y_value):
        # print(f'Sleep Science Viewer: x_value = {x_value}, y_value = {y_value}')
        # Slot to handle double-click events on QListWidget items.
        logger.info(f"Hypnogram plot double-clicked: time in seconds {x_value}")
        if self.edf_obj is None:
            return

        # Change cursor to busy
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        # Get double click x value
        annotation_time_in_sec = x_value

        # Change Current epoch
        epoch_window_in_seconds = self.epoch_display_options_width_sec[self.ui.comboBox_epoch.currentIndex()]
        new_epoch = float(annotation_time_in_sec) / epoch_window_in_seconds
        annotation_epoch_offset_start = (new_epoch - math.floor(new_epoch)) * epoch_window_in_seconds
        new_epoch = math.floor(new_epoch) + 1
        self.ui.textEdit_epoch.setText(str(new_epoch))
        self.current_epoch = new_epoch

        # Update signal graphic views to annotation epoch
        # self.draw_signals_in_graphic_views(annotation_marker=annotation_epoch_offset_start)

        # Plot Hypnogram
        hypnogram_marker = annotation_time_in_sec
        show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()
        self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                     hypnogram_marker=hypnogram_marker,
                                                     double_click_callback=self.on_hypnogram_double_click,
                                                     show_stage_colors = show_stage_colors
                                                     )

        # Update Signals
        self.draw_signal_in_graphic_views()


        # Revert cursor to pointer
        QApplication.restoreOverrideCursor()

        logger.info(f"Jumped to new signal epoch ({new_epoch}, epoch offset {int(annotation_epoch_offset_start)})")
    def on_annotation_combobox_text_changed(self,text):
        logger.info(f'Annotation combobox text changed to {text}')

        # Text Update
        if self.annotations_list:
            # Clear the current list in the widget
            self.ui.listWidget_annotation.clear()

            # Always keep the header (assumed to be the first line)
            header = self.annotations_list[0]
            self.ui.listWidget_annotation.addItem(header)

            # If 'All' is selected, show everything
            if text == 'All':
                for item in self.annotations_list[1:]:  # Skip header (already added)
                    self.ui.listWidget_annotation.addItem(item)
            else:
                # Filter items that contain the selected text
                for item in self.annotations_list[1:]:
                    if text in item:
                        self.ui.listWidget_annotation.addItem(item)


            # Update annotations plot - Need to add
            total_time_in_seconds = self.xml_obj.sleep_stages_obj.time_seconds
            cur_annotation_setting = self.ui.comboBox_annotation.currentText()
            # print(f'cur_annotation_setting = "{cur_annotation_setting}"')
            self.xml_obj.scored_event_obj.plot_annotation(total_time_in_seconds,
                                                        self.ui.graphicsView_annotation_plot,
                                                        annotation_filter = cur_annotation_setting,
                                                        double_click_callback = self.on_annotation_double_click)
    def show_annotation_legend_popup(self):
        if self.xml_obj is not None:
            self.xml_obj.scored_event_obj.show_annotation_legend()
    def annotation_list_widget_double_click(self, item):
        # Slot to handle double-click events on QListWidget items.
        logger.info(f"Annotation list double-clicked: {item.text()}")
        if self.xml_obj is None:
            return

        # Set busy cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        # Parse text
        self.ui.listWidget_annotation.currentItem()
        text_list = item.text()
        text_list = text_list.split()

        # Parse text list
        starttime = text_list[0]
        # if len(text_list) > 3:
        #    annotation_type = text_list[2:-1]
        #    annotation_type = ' '.join(annotation_type)

        # Compute start time
        time_list = starttime.split(':')
        annotation_time_in_sec = int(time_list[0]) * 3600 + int(time_list[1]) * 60 + int(time_list[2])

        # Change Current epoch
        epoch_window_in_seconds = self.epoch_display_options_width_sec[self.ui.comboBox_epoch.currentIndex()]
        new_epoch = float(annotation_time_in_sec) / epoch_window_in_seconds
        annotation_epoch_offset_start = (new_epoch - math.floor(new_epoch)) * epoch_window_in_seconds
        new_epoch = math.floor(new_epoch) + 1
        self.ui.textEdit_epoch.setText(str(new_epoch))
        self.current_epoch = new_epoch

        # Update signal graphic views to annotation epoch
        annotation_marker = annotation_time_in_sec
        self.draw_signal_in_graphic_views(annotation_marker = annotation_marker)
        #draw_signal_in_graphic_views(self, annotation_marker: float = None,
        #epochs_to_draw:int = None)


        # Plot Hypnogram
        hypnogram_marker = annotation_time_in_sec
        show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()
        self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                                hypnogram_marker=hypnogram_marker,
                                                                double_click_callback=self.on_hypnogram_double_click,
                                                                show_stage_colors = show_stage_colors)

        # Return pointer cursor
        QApplication.restoreOverrideCursor()

        # Write to log file
        logger.info(
            f"Jumped to new signal epoch ({new_epoch}, epoch offset {int(annotation_epoch_offset_start)})")

    # Epochs
    @staticmethod
    def show_ok_cancel_dialog(parent=None):
        msg_box = QMessageBox(parent)
        msg_box.setWindowTitle("Confirm Action")
        msg_box.setText(
            "Computing a multitaper spectrogram can be time consuming. Future versions will include a less computational alternative. \n\nDo you want to proceed?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Ok)

        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Ok:
            logger.info("OK clicked: Will continue ")
            return True
        else:
            logger.info(
                f"Message Dialog Box - Cancel clicked, Msg: {'Computing a multitaper spectrogram can be time consuming. Do you want to proceed?'} ")
            return False

    # Annotations
    @staticmethod
    def extract_event_indexes(entry_text):
        index_start = entry_text.find('Name')
        index_end   = entry_text.find('Input')
        return index_start, index_end

    # Epoch Buttons
    def set_epoch_to_first(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """

        # Turn off epoc buttons
        self.activate_epoch_buttons(activate_buttons=False)

        # Example: Set an internal index
        self.current_epoch = 1
        self.ui.textEdit_epoch.setText(f"{self.current_epoch}")
        self.ui.textEdit_epoch.setAlignment(Qt.AlignmentFlag.AlignRight)

        # update Signals
        self.draw_signal_in_graphic_views()


        # Plot Hypnogram
        hypnogram_marker = 0
        show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()
        self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                     hypnogram_marker=hypnogram_marker,
                                                     double_click_callback=self.on_hypnogram_double_click,
                                                     show_stage_colors=show_stage_colors)

        # Turn on epoc buttons
        self.activate_epoch_buttons(activate_buttons=True)

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to first ({self.current_epoch})")
    def set_epoch_to_next(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """

        # Turn off epoc buttons
        self.activate_epoch_buttons(activate_buttons=False)
        #print(f"Epoch set to next ({self.current_epoch})")
        # Example: Set an internal index
        if self.current_epoch + self.number_of_epochs_on_screen < self.max_epoch:
            self.current_epoch += self.number_of_epochs_on_screen
            self.ui.textEdit_epoch.setText(f"{self.current_epoch}")
            self.ui.textEdit_epoch.setAlignment(Qt.AlignmentFlag.AlignRight)

            # update Signals
            self.draw_signal_in_graphic_views(epochs_to_draw = self.number_of_epochs_on_screen)
            #print(f"Epoch set to next ({self.current_epoch})")

            # Plot Hypnogram
            cbox_val          = self.ui.comboBox_epoch.currentIndex()
            epoch_width_sec   = self.epoch_display_options_width_sec[cbox_val]
            hypnogram_marker  = epoch_width_sec * self.current_epoch
            show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()
            self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                         hypnogram_marker=hypnogram_marker,
                                                         show_stage_colors=show_stage_colors)
        # Turn of epoc buttons
        self.activate_epoch_buttons()

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to next ({self.current_epoch})")
    def set_epoch_from_text(self):
        # Turn of epoc buttons
        self.activate_epoch_buttons(activate_buttons=False)

        logger.info(f'User entered a new epoch')
        if self.edf_obj:
            new_epoch = int(self.ui.textEdit_epoch.toPlainText())
            if new_epoch < 1:
                new_epoch = 1
            elif new_epoch > self.max_epoch:
                new_epoch = self.max_epoch
            self.ui.textEdit_epoch.setText(f"{new_epoch}")
            self.ui.textEdit_epoch.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.current_epoch = new_epoch

            # update Signals
            self.draw_signal_in_graphic_views()

            # Plot Hypnogram
            cbox_val = self.ui.comboBox_epoch.currentIndex()
            epoch_width_sec = self.epoch_display_options_width_sec[cbox_val]
            hypnogram_marker = epoch_width_sec * self.current_epoch
            show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()
            self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                         hypnogram_marker=hypnogram_marker,
                                                         show_stage_colors=show_stage_colors)
        # Turn on epoc buttons
        self.activate_epoch_buttons(activate_buttons=True)
    def set_epoch_to_prev(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """

        # Turn of epoc buttons
        self.activate_epoch_buttons(activate_buttons=False)

        # Example: Set an internal index
        if self.current_epoch - self.number_of_epochs_on_screen  >= 1:
            self.current_epoch -= self.number_of_epochs_on_screen
            self.ui.textEdit_epoch.setText(f"{self.current_epoch}")
            self.ui.textEdit_epoch.setAlignment(Qt.AlignmentFlag.AlignRight)

            # update Signals
            self.draw_signal_in_graphic_views()

            # Plot Hypnogram
            cbox_val = self.ui.comboBox_epoch.currentIndex()
            epoch_width_sec = self.epoch_display_options_width_sec[cbox_val]
            hypnogram_marker = epoch_width_sec * self.current_epoch
            show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()
            self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                         hypnogram_marker=hypnogram_marker,
                                                         show_stage_colors=show_stage_colors)
        else:
            self.set_epoch_to_first()

        # Turn of epoc buttons
        self.activate_epoch_buttons()

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to prev ({self.current_epoch})")
    def set_epoch_to_last(self):
        """
        Set the current epoch to the first one (index 1).
        Update the UI and any associated data views accordingly.
        """

        # Turn of epoc buttons
        self.activate_epoch_buttons(activate_buttons=False)

        # Check for edge cases
        epochs_to_draw = self.max_epoch % self.number_of_epochs_on_screen

        # Example: Set an internal index
        max_num_pages = self.max_epoch//self.number_of_epochs_on_screen
        self.current_epoch = int(max_num_pages*self.number_of_epochs_on_screen)+1
        self.ui.textEdit_epoch.setText(f"{self.current_epoch }")
        self.ui.textEdit_epoch.setAlignment(Qt.AlignmentFlag.AlignRight)

        # update Signals
        self.draw_signal_in_graphic_views(epochs_to_draw = epochs_to_draw)

        # Plot Hypnogram
        cbox_val = self.ui.comboBox_epoch.currentIndex()
        epoch_width_sec = self.epoch_display_options_width_sec[cbox_val]
        hypnogram_marker = epoch_width_sec * self.current_epoch
        show_stage_colors = self.ui.pushButton_show_hypnogram_stages_in_color.isChecked()
        self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                     hypnogram_marker=hypnogram_marker,
                                                     show_stage_colors=show_stage_colors)

        # Turn of epoc buttons
        self.activate_epoch_buttons()

        # You can now update views, annotations, etc.
        logger.info(f"Epoch set to page ({self.current_epoch})")
    def enter_pressed_epoch_edit(self):
        # Get information to evaluate user entry
        text_field_epoch = int(self.ui.textEdit_epoch.toPlainText())
        epoch_width = self.epoch_display_options_width_sec[self.ui.comboBox_epoch.currentIndex()]
        max_time = self.xml_obj.sleep_stages_obj.max_time_sec

        # check for valid epoch
        epoch_min_test = text_field_epoch >= 1
        epoch_change_test = self.current_epoch != text_field_epoch
        epoch_max_test = text_field_epoch * epoch_width <= max_time

        # Respond to checks
        if not epoch_min_test:
            self.set_epoch_to_first()
        elif not epoch_max_test:
            self.set_epoch_to_last()
        elif epoch_change_test:
            self.set_epoch_from_text()
        else:
            logger.info('User epoch case not handled.')
        logger.info(f'Responding to user enter within epoch text field')
    def activate_epoch_buttons(self, activate_buttons = True):
        # Delay in milliseconds
        delay_in_mil_sec = 500

        # Define epoch buttons
        epoch_buttons = [self.ui.pushButton_first, self.ui.pushButton_next, self.ui.pushButton_update,
                        self.ui.pushButton_previous, self.ui.pushButton_last, self.ui.pushButton_epoch_show_stages]

        # Take action based on flag
        if not activate_buttons:
            for button in epoch_buttons:
                button.setEnabled(False)
        else:
            for button in epoch_buttons:
                QTimer.singleShot(delay_in_mil_sec, lambda b=button: b.setEnabled(True))
    def update_epoch_combobox (self, epoch_str):
        # turn off update signal combobox
        self.ui.comboBox_epoch.blockSignals(True)

        # Adjust epoch number to new width
        old_epoch_width_index = self.current_epoch_width_index
        old_epoch_width       = self.epoch_display_options_width_sec[old_epoch_width_index]
        new_epoch_width_index = int(self.ui.comboBox_epoch.currentIndex())
        new_epoch_width       = self.epoch_display_options_width_sec[new_epoch_width_index]

        print(f'old_epoch_width = {old_epoch_width}, new_epoch_width = {new_epoch_width}')

        # Get new maximum epochs
        signal_keys            = [label for label in self.edf_obj.edf_signals.signal_labels if label != '']
        new_maximum_epochs    = self.edf_obj.edf_signals.return_num_epochs(signal_keys[0], new_epoch_width)

        print(f'self.max_epoch = {self.max_epoch}, new_maximum_epochs = {new_maximum_epochs}')

        self.max_epoch        = new_maximum_epochs
        self.ui.label_page.setText(f' of {new_maximum_epochs} epochs')



        # Compute new epoch number
        current_epoch         = int(self.ui.textEdit_epoch.toPlainText())
        current_time_in_sec   = (current_epoch-1)*old_epoch_width
        new_epoch             = current_time_in_sec / new_epoch_width + 1
        if new_epoch <  1 :
            new_epoch = int(math.ceil(new_epoch))
        else:
            new_epoch = int(math.floor(new_epoch))

        print(f'current_epoch  = {current_epoch }, new_epoch = {new_epoch}')

        # Update epoch textEdit widget
        self.ui.textEdit_epoch.setText(str(new_epoch))

        # Update current width
        self.current_epoch_width_index = new_epoch_width_index
        self.current_epoch = new_epoch

        # Update signal graphic views
        self.draw_signal_in_graphic_views()

        # turn off update signal combobox
        self.ui.comboBox_epoch.blockSignals(False)

        # log action
        logger.info(f'Signal combobox changed to {epoch_str}')
    def show_signal_stages(self,checked):
        logger.info(f'Toggling show stages push button: {checked}')

        # turn off update signal combobox
        self.ui.pushButton_epoch_show_stages.blockSignals(True)

        # Update signal view
        self.draw_signal_in_graphic_views()

        # turn on update signal
        self.ui.pushButton_epoch_show_stages.blockSignals(False)

        logger.info(f'Set show staged button to: {checked}')

    # Utilities
    @staticmethod
    def return_time_string(epoch:int, epoch_width:int):
        val     = float((epoch-1)*epoch_width)
        seconds = val
        hours   = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds) % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"

