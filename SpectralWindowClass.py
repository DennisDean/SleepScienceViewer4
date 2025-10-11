# Spectral Window Class
#
# Generate and independent window for performing signal spectral analysis. The interface allows the user to set
# select signals, set analysis bands, and set multi-taper parameters. Interface provides a summary and visualization
# options to support interpretation of results. Bands, Paramerters, epoch level noise detection, and results can be
# exported for further analysis.
#

# To Do:

# Modules
import logging
import psutil
from functools import partial
import math
import numpy as np
import copy

# Interface packages and modules
from PySide6.QtWidgets import QMainWindow, QSizePolicy, QListWidgetItem, QApplication, QMessageBox
from PySide6.QtCore import QEvent, Qt, QObject,Signal, QTimer
from PySide6.QtGui import QColor, QBrush, QFont, QFontDatabase
from PySide6.QtGui import QKeyEvent

# Sleep Science Classes
from EdfFileClass import EdfFile, EdfSignalAnalysis
from AnnotationXmlClass import AnnotationXml

# GUI Interface
from SpectralViewer import Ui_MainWindow  # the generated file from your .ui

# Set up a module-level logger
logger = logging.getLogger(__name__)

# To Do List


# Utilities
def clear_graphic_view_plot(parent_widget = None):
    layout = parent_widget.layout()
    if layout:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
def create_layout_toggle(layout):
    """Create a toggle function for a specific layout."""
    def toggle(visible: bool):
        set_layout_visible(layout, visible)
    return toggle
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
            #print(f"  - Widget: {widget.objectName()}")
            widget.setVisible(visible)

        # Check if the item is a nested layout
        nested_layout = item.layout()
        if nested_layout:
            # Recursively process the nested layout
            set_layout_visible(nested_layout, visible)
def is_first_nonlayout_widget_visible(layout):
    """
    Recursively check whether the first non-layout widget
    inside this layout (or any sub-layout) is visible.
    Returns True if found and visible, otherwise False.
    """
    if layout is None or layout.count() == 0:
        return False

    for i in range(layout.count()):
        item = layout.itemAt(i)

        # Case 1: the item is a widget
        widget = item.widget()
        if widget is not None:
            return widget.isVisible()

        # Case 2: the item is another layout — search recursively
        sublayout = item.layout()
        if sublayout is not None:
            result = is_first_nonlayout_widget_visible(sublayout)
            if result is not None:
                return result

    # No widget found in this layout or sub-layouts
    return False
def toggle_layout_and_button(layout,button):
    visible = not is_first_nonlayout_widget_visible(layout)
    set_layout_visible(layout, visible)
    button.setChecked(visible)
    logger.info(f'Setting {layout} viability setting to {visible}')
def toggle_layout(layout):
    visible = not is_first_nonlayout_widget_visible(layout)
    set_layout_visible(layout, visible)
    logger.info(f'Setting {layout} viability setting to {visible}')

# Utility Classes
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
class SpectralWindow(QMainWindow):
    # Initialize
    def __init__(self, edf_obj:EdfFile=None, xml_obj:AnnotationXml=None, parent=None):
        super().__init__(parent)


        # Setup and Draw Window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Spectral Viewer")

        # Save signals and annotations
        self.edf_obj = edf_obj
        self.xml_obj = xml_obj

        # Define settings variables
        self.band_low_values:list[float]
        self.band_high_values:list[float]
        self.notch_values:list[float]
        self.band_low_menu_items:list[str]
        self.band_high_menu_items:list[str]
        self.notch_menu_items:list[str]

        # Define parameter variables
        self.noise_alpha_n_factor:list[float]
        self.noise_beta_n_factor:list[float]
        self.noise_alpha_n_menu_items:list[str]
        self.noise_beta_n_menu_items:list[str]

        # Set up window control
        self.setup_control_bar()
        self.setup_menu()
        self.setup_settings()
        self.setup_parmeters()

    # Setup
    def setup_menu(self):
        # Create function make menu selection a toggle switch
        show_layout_control_bar = partial(toggle_layout, self.ui.verticalLayout_top_controls)
        self.ui.actionControl_Bar.triggered.connect(show_layout_control_bar)

        # Set up
        show_layout_spectrogram = partial(toggle_layout_and_button,
                            self.ui.horizontalLayout_spectrogram,self.ui.pushButton_control_spectrogram)
        show_layout_settings = partial(toggle_layout_and_button,
                            self.ui.horizontalLayout_settings, self.ui.pushButton_control_settings)
        show_layout_parameters = partial(toggle_layout_and_button,
                            self.ui.horizontalLayout_parameters,self.ui.pushButton_control_parameters)
        show_layout_hypnogram = partial(toggle_layout_and_button,
                            self.ui.horizontalLayout_hypnogram, self.ui.pushButton_control_hypnogram)
        show_layout_markings = partial(toggle_layout_and_button,
                            self.ui.verticalLayout_mark, self.ui.pushButton_control_markings)

        # Turn on menu options
        self.ui.actionSettings.triggered.connect(show_layout_settings)
        self.ui.actionParameters.triggered.connect(show_layout_parameters)
        self.ui.actionHypnogram.triggered.connect(show_layout_hypnogram)
        self.ui.actionSpectrogram.triggered.connect(show_layout_spectrogram)
        self.ui.actionMarkings.triggered.connect(show_layout_markings)
    def setup_control_bar(self):
        # Create functions to respond to pushbutton
        show_layout_spectrogram = partial(set_layout_visible, self.ui.horizontalLayout_spectrogram)
        show_layout_settings = partial(set_layout_visible, self.ui.horizontalLayout_settings)
        show_layout_parameters = partial(set_layout_visible, self.ui.horizontalLayout_parameters)
        show_layout_hypnogram = partial(set_layout_visible, self.ui.horizontalLayout_hypnogram)
        show_layout_markings= partial(set_layout_visible, self.ui.verticalLayout_mark)

        # connect push buttons to actions
        self.ui.pushButton_control_spectrogram.toggled.connect(show_layout_spectrogram)
        self.ui.pushButton_control_settings.toggled.connect(show_layout_settings)
        self.ui.pushButton_control_parameters.toggled.connect(show_layout_parameters)
        self.ui.pushButton_control_hypnogram.toggled.connect(show_layout_hypnogram)
        self.ui.pushButton_control_markings.toggled.connect(show_layout_markings)

        # Add signals to combobox
    def setup_settings(self):
        # Log status
        logger.info(f'Preparing setting options')

        #  Set filter combo box values
        band_low_values         = [0.1, 0.5, 1.0, 10.0 ]
        band_high_values        = [50.0, 60.0, 70.0]
        notch_values            = [50.0, 60.0]
        create_freq_menu_item_f = lambda x:f'{x:.1f} Hz'
        band_low_menu_items     = list(map(create_freq_menu_item_f, band_low_values))
        band_high_menu_items    = list(map(create_freq_menu_item_f, band_high_values))
        notch_menu_items        = list(map(create_freq_menu_item_f, notch_values))
        add_blank_menu_item_f   = lambda x:x.insert(0, '')
        for l in [band_low_menu_items, band_high_menu_items, notch_menu_items]:
            l.insert(0,'')

        # Combo box settings
        settings_combo_boxes = [self.ui.comboBox_settings_band_low, self.ui.comboBox_settings_band_low,
                                self.ui.comboBox_settings_band_high,self.ui.comboBox_settings_notch,
                                self.ui.comboBox_settings_reference_method]
        for cb in settings_combo_boxes:
            cb.clear()

        # Set filter combobox values
        self.ui.comboBox_settings_band_low.addItems(band_low_menu_items)
        self.ui.comboBox_settings_band_high.addItems(band_high_menu_items)
        self.ui.comboBox_settings_notch.addItems(notch_menu_items)

        # Set reference methods
        reference_methods = ['No Reference', 'Single Reference', 'Reference Each Signal', 'Average Reference']
        self.ui.comboBox_settings_reference_method.addItems(reference_methods)
        print(reference_methods)

        # Setup signal comboboxes
        signal_labels = self.edf_obj.edf_signals.signal_labels
        signal_labels.insert(0, '')

        # Clear combo boxes
        signal_combo_boxes = [self.ui.comboBox_settings_analysis_sig1, self.ui.comboBox_settings_analysis_sig2,
                              self.ui.comboBox_settings_analysis_sig3, self.ui.comboBox_settings_analysis_sig4,
                              self.ui.comboBox_settings_analysis_sig5, self.ui.comboBox_settings_analysis_sig6,
                              self.ui.comboBox_settings_analysis_sig7, self.ui.comboBox_settings_analysis_sig8,
                              self.ui.comboBox_settings_analysis_sig9, self.ui.comboBox_settings_analysis_sig10,
                              self.ui.comboBox_settings_ref_sig1,      self.ui.comboBox_settings_ref_sig2,
                              self.ui.comboBox_settings_ref_sig3,      self.ui.comboBox_settings_ref_sig4,
                              self.ui.comboBox_settings_ref_sig5,      self.ui.comboBox_settings_ref_sig6,
                              self.ui.comboBox_settings_ref_sig7,      self.ui.comboBox_settings_ref_sig8,
                              self.ui.comboBox_settings_ref_sig9,      self.ui.comboBox_settings_ref_sig10]
        for cb in signal_combo_boxes:
            cb.clear()
            cb.addItems(signal_labels)

        # Record settings
        self.band_low_values       = band_low_values
        self.band_high_values      = band_high_values
        self.notch_values          = notch_values
        self.band_low_menu_items   = band_low_menu_items
        self.band_high_menu_items  = band_high_menu_items
        self.notch_menu_items      = notch_menu_items
    def setup_parmeters(self):
        # setup noise detection
        noise_alpha_n_factor = [1.50, 2.00, 2.25, 2.50, 2.75, 3.00]
        noise_beta_n_factor = [1.50, 2.00, 2.25, 2.50, 2.75, 3.00]
        create_noise_menu_item_f = lambda x: f'{x:.2f}'
        noise_alpha_n_menu_items = list(map(create_noise_menu_item_f, noise_alpha_n_factor))
        noise_beta_n_menu_items = list(map(create_noise_menu_item_f, noise_beta_n_factor))

        # setup noise detection menu
        self.ui.comboBox_parameters_noise_delta.addItems(noise_alpha_n_menu_items)
        self.ui.comboBox_parameters_noise_beta.addItems(noise_beta_n_menu_items)


        # setup taper windows
        taper_window_values = [1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0]
        taper_step_values = [0.25, 0.50, 1.0, 2.0, 3.0, 4.0, 5.0]
        create_taper_menu_item_f = lambda x: f'{x:.2f} s'
        taper_window_menu_items = list(map(create_taper_menu_item_f, taper_window_values))
        taper_step_menu_items   = list(map(create_taper_menu_item_f, taper_step_values))

        # setup taper combo box
        self.ui.comboBox_parameters_taper_window.addItems(taper_window_menu_items)
        self.ui.comboBox_parameters_taper_step.addItems(taper_step_menu_items)


        # setup cpu selection
        num_physical_cpu = psutil.cpu_count(logical=True)
        cpu_list_menu_items = [str(c) for c in range(1,num_physical_cpu+1,1)]
        self.ui.comboBox_parameters_taper_num_cpus.addItems(cpu_list_menu_items)

        # Save parameters
        self.noise_alpha_n_factor = noise_alpha_n_factor
        self.noise_beta_n_factor = noise_beta_n_factor
        self.create_noise_menu_item_f = create_noise_menu_item_f
        self.noise_alpha_n_menu_items = noise_alpha_n_menu_items
        self.noise_beta_n_menu_items = noise_beta_n_menu_items
