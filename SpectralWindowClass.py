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
import math
from functools import partial
from typing import Callable

# Interface packages and modules
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide6.QtCore import QEvent, Qt, QObject,Signal
from PySide6.QtGui import QKeyEvent

# Sleep Science Classes
from EdfFileClass import EdfFile, EdfSignalAnalysis
from AnnotationXmlClass import AnnotationXml

# GUI Interface
from SpectralViewer import Ui_MainWindow

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

# Classes
from multitaper_spectrogram_python_class import MultitaperSpectrogram

# Set up a module-level logger
logger = logging.getLogger(__name__)

# To Do List


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
        self.noise_delta_n_factor:list[float]
        self.noise_beta_n_factor:list[float]
        self.noise_selta_n_menu_items:list[str]
        self.noise_beta_n_menu_items:list[str]

        # Parameter Dictionaries - Inprocess of replacing single varaibles
        self.param_noise_names = ['delta', 'beta']
        self.param_noise_dict:dict|None = None
        self.param_taper_names = ['window', 'step', 'num_cpus']
        self.param_taper_dict:dict|None = None
        self.param_band_names = ['alpha', 'theta', 'alpha', 'sigma', 'beta', 'gamma']
        self.param_band_dict:dict|None = None
        self.param_analysis_names = ['range']
        self.param_analysis_dict:dict|None = None

        # Setting Dictionaries
        self.setting_description_dict:dict|None = None
        self.setting_description_names = ['description', 'output_suffix']
        self.setting_signal_dict:dict|None = None
        self.setting_signal_names = ['reference_method', 'analysis_signals', 'reference_signal']
        self.setting_plotting_dict:dict|None = None
        self.setting_plotting_names = ['show_x_labels']
        self.setting_analysis_dict:dict|None = None
        self.setting_analaysis_names = ['apply_band', 'band_low', 'band_high', 'apply_notch', 'notch']

        # Set up window control
        self.setup_control_bar()
        self.setup_menu()
        self.setup_settings()
        self.setup_parmeters()

        # Set up histogram
        self.hypnogram_combobox_selection:int|None = None
        self.automatic_histogram_redraw:bool|None = None
        self.hypnogram_combobox_selection:int|None = None
        self.sleep_stage_mappings:dict|None = None
        self.setup_hypnogram()

        # Set up spectrogram
        self.signal_labels:list[str]|None = None
        self.signal_label:str|None = None
        self.multitaper_spectrogram_obj:MultitaperSpectrogram|None = None
        self.setup_spectrogram()

        # Setup parameters
        self.spectral_bands_low_cb:list|None = None
        self.spectral_bands_high_cb:list|None = None

        # Settings and Parameter dictionaries
        self.setting_description_dict:dict|None = None
        self.setting_signal_dict:dict|None = None
        self.setting_plotting_dict:dict|None = None
        self.setting_filter_dict:dict|None = None
        self.noise_param_dict:dict|None = None
        self.taper_param_dict:dict|None = None
        self.band_params_dict:dict|None = None

        # Set up analysis
        self.analyis_signal_labels:list|None = None
        self.analyis_signal_combo_boxes:list|None = None
        self.results_graphic_views:list|None = None
        self.result_layouts:list|None = None
        self.setup_analysis()

        # Set up spectral analysis list
        self.result_spectrograph_obj_list:list|None=None

        # Set up summary
        self.setup_summarize()

        # Result Varaibiles
        self.result_spectrogram_obj_list:list|None = None
        self.result_average_spectrogram_list:list|None = None

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

        # get visability defaults from UI
        layout_toggle_functions = [show_layout_spectrogram, show_layout_settings, show_layout_parameters,
                                   show_layout_hypnogram, show_layout_markings]
        layout_control_buttons = [self.ui.pushButton_control_spectrogram, self.ui.pushButton_control_settings,
                                  self.ui.pushButton_control_parameters, self.ui.pushButton_control_hypnogram,
                                  self.ui.pushButton_control_markings]
        for layout_tupple in zip(layout_toggle_functions, layout_control_buttons):
            toggle_function, layout_control_button = layout_tupple
            is_checked = layout_control_button.isChecked()
            toggle_function(is_checked)
            layout_control_button.toggled.connect(toggle_function)

        # Set up analysis buttons
        self.enable_spectrogram_options(False)
    def setup_settings(self):
        # Log status
        logger.info(f'Preparing setting options')

        #  Set filter combo box values
        band_low_values         = [0.1, 0.5, 1.0, 10.0 ]
        band_high_values        = [50.0, 60.0, 70.0]
        notch_values            = [50.0, 60.0]
        create_freq_menu_item_f = lambda x:f'{x:.1f}'
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
        self.ui.comboBox_settings_reference_method.clear()
        self.ui.comboBox_settings_reference_method.addItems(reference_methods)

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
        noise_delta_n_factor = [1.50, 2.00, 2.25, 2.50, 2.75, 3.00]
        noise_beta_n_factor = [1.50, 2.00, 2.25, 2.50, 2.75, 3.00]
        noise_delta_default_value = 2.0
        noise_beta_default_value  = 2.5
        noise_delta_index =  noise_delta_n_factor.index(noise_delta_default_value)
        noise_beta_index  =  noise_beta_n_factor.index(noise_beta_default_value)
        create_noise_menu_item_f = lambda x: f'{x:.2f}'
        noise_delta_n_menu_items = list(map(create_noise_menu_item_f, noise_delta_n_factor))
        noise_beta_n_menu_items = list(map(create_noise_menu_item_f, noise_beta_n_factor))

        # setup noise detection menu
        self.ui.comboBox_parameters_noise_delta.addItems(noise_delta_n_menu_items)
        self.ui.comboBox_parameters_noise_beta.addItems(noise_beta_n_menu_items)
        self.ui.comboBox_parameters_noise_delta.setCurrentIndex(noise_delta_index)
        self.ui.comboBox_parameters_noise_beta.setCurrentIndex(noise_beta_index)


        # setup taper windows
        taper_window_values = [1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0]
        taper_step_values = [0.25, 0.50, 1.0, 2.0, 3.0, 4.0, 5.0]
        default_taper_window = 5.0
        default_taper_step   = 1.0
        create_taper_menu_item_f = lambda x: f'{x:.2f}'
        taper_window_menu_items = list(map(create_taper_menu_item_f, taper_window_values))
        taper_step_menu_items   = list(map(create_taper_menu_item_f, taper_step_values))

        # setup taper combo box
        self.ui.comboBox_parameters_taper_window.addItems(taper_window_menu_items)
        self.ui.comboBox_parameters_taper_step.addItems(taper_step_menu_items)
        self.ui.comboBox_parameters_taper_window.setCurrentIndex(taper_window_values.index(default_taper_window))
        self.ui.comboBox_parameters_taper_step.setCurrentIndex(taper_step_values.index(default_taper_step))

        # setup cpu selection
        num_physical_cpu = psutil.cpu_count(logical=True)
        cpu_list_menu_items = [str(c) for c in range(1,num_physical_cpu+1,1)]
        default_index = math.ceil(float(num_physical_cpu)/2)
        self.ui.comboBox_parameters_taper_num_cpus.addItems(cpu_list_menu_items)
        self.ui.comboBox_parameters_taper_num_cpus.setCurrentIndex(default_index)

        # Set up band values
        band_default_low  = [[0.5, 4.0],  [4.0,8.0],  [8.0,12.0], [12.0,15.0], [15.0,30.0], [30.0,50.0]]
        band_combos_low  = [[self.ui.comboBox_parameters_band_delta_low, self.ui.comboBox_parameters_band_delta_high],
                            [self.ui.comboBox_parameters_band_theta_low, self.ui.comboBox_parameters_band_theta_high],
                            [self.ui.comboBox_parameters_band_alpha_low, self.ui.comboBox_parameters_band_alpha_high],
                            [self.ui.comboBox_parameters_band_sigma_low, self.ui.comboBox_parameters_band_sigma_high]]
        band_default_high = [[15.0, 30.0], [30.0, 50.0]]
        band_combos_high = [[self.ui.comboBox_parameters_band_beta_low,  self.ui.comboBox_parameters_band_beta_high],
                            [self.ui.comboBox_parameters_band_gamma_low, self.ui.comboBox_parameters_band_gamma_high]]
        band_menu_items_low  = [0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0,
                                12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]
        band_menu_items_high = list(range(10, 101, 1))
        for combo_pair, default_pair in zip(band_combos_low, band_default_low):
            bcl_low, bcl_high = combo_pair
            def_low, def_hgh = default_pair
            bcl_low.clear()
            bcl_high.clear()
            bcl_low.addItems([f'{x:.1f}' for x in band_menu_items_low])
            bcl_high.addItems([f'{x:.1f}' for x in band_menu_items_low])
            bcl_low.setCurrentIndex(band_menu_items_low.index(def_low))
            bcl_high.setCurrentIndex(band_menu_items_low.index(def_hgh))
        for combo_pair, default_pair in zip(band_combos_high, band_default_high):
            bcl_low, bcl_high = combo_pair
            def_low, def_hgh = default_pair
            bcl_low.clear()
            bcl_high.clear()
            bcl_low.addItems([f'{x:.1f}' for x in band_menu_items_high])
            bcl_high.addItems([f'{x:.1f}' for x in band_menu_items_high])
            bcl_low.setCurrentIndex(band_menu_items_high.index(def_low))
            bcl_high.setCurrentIndex(band_menu_items_high.index(def_hgh))

        # Set up analysis
        analysis_range_values = ['All', 'Wake', 'Wake through Sleep', 'Sleep Only', 'Ending Wake']
        self.ui.comboBox_parameters_analysis_range.clear()
        self.ui.comboBox_parameters_analysis_range.addItems(analysis_range_values)

        # Save parameters
        self.noise_delta_n_factor = noise_delta_n_factor
        self.noise_beta_n_factor = noise_beta_n_factor
        self.create_noise_menu_item_f = create_noise_menu_item_f
        self.noise_delta_n_menu_items = noise_delta_n_menu_items
        self.noise_beta_n_menu_items = noise_beta_n_menu_items

        # Save interface

    # Hypnogram
    def setup_hypnogram(self):
        # Set Sleep Stage Labels
        sleep_stage_labels = self.xml_obj.sleep_stages_obj.return_sleep_stage_labels()
        sleep_stage_labels.remove(sleep_stage_labels[0])
        self.ui.comboBox_hynogram.blockSignals(True)
        self.ui.comboBox_hynogram.clear()
        self.ui.comboBox_hynogram.addItems(sleep_stage_labels)

        # Get Sleep Stage Mappings
        self.sleep_stage_mappings = self.xml_obj.sleep_stages_obj.return_sleep_stage_mappings()

        # Connect Responses
        self.ui.comboBox_hynogram.currentIndexChanged.connect(self.on_hypnogram_changed)
        self.hypnogram_combobox_selection = None
        self.ui.pushButton_hypnogram_show_stages.toggled.connect(self.show_stages_on_hypnogram)
        self.ui.pushButton_hypnogram_legend.clicked.connect(self.show_hypnogram_legend)

        # Plot Hypnogram
        show_stage_colors = self.ui.pushButton_hypnogram_show_stages.isChecked()
        self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                     show_stage_colors = show_stage_colors)

        # Turn on hypnogram signal
        self.ui.comboBox_hynogram.blockSignals(False)
        self.automatic_histogram_redraw = True
    def on_hypnogram_changed(self, index):
        # Update Variables
        if self.automatic_histogram_redraw:
            selected_text = self.ui.comboBox_hynogram.itemText(index)
            self.hypnogram_combobox_selection = index
            logger.info(f"Combo box changed to index {index}: {selected_text}")

            # Update Hypnogram
            if self.sleep_stage_mappings is not None:
                # Get stage flag
                show_stage_colors = self.ui.pushButton_hypnogram_show_stages.isChecked()

                stage_map = index
                self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.ui.graphicsView_hypnogram,
                                                            stage_index=stage_map,
                                                            show_stage_colors=show_stage_colors)
    def show_stages_on_hypnogram(self):
        # Pretend hypnogram combobox change to update
        if self.automatic_histogram_redraw:
            index = self.ui.comboBox_hynogram.currentIndex()
            self.on_hypnogram_changed(index)
    def show_hypnogram_legend(self):
        self.xml_obj.sleep_stages_obj.show_sleep_stages_legend()

    # Spectrogram
    def setup_spectrogram(self):
        # Add signal list
        # Set signal labels
        self.signal_labels = self.edf_obj.edf_signals.signal_labels
        self.ui.comboBox_spectrogram_signals.addItems(self.signal_labels )
        signal_combobox_index = 0
        self.signal_label = self.signal_labels[signal_combobox_index]
        self.ui.comboBox_spectrogram_signals.setCurrentIndex(signal_combobox_index)

        # Spectrogram Buttons
        self.ui.pushButton_spectrogram_show.clicked.connect(self.compute_and_display_spectrogram)
        self.ui.pushButton_spectrogram_legend.clicked.connect(self.show_spectrogram_legend)
        self.ui.pushButton_spectrogram_heatmap_show.clicked.connect(self.show_heatmap)
        self.ui.pushButton_sectrogram_heatmap_legend.clicked.connect(self.show_heapmap_legend)
    def compute_and_display_spectrogram(self):
        # Check before starting long computation

        process_eeg = False
        if self.edf_obj is not None:
            process_eeg = self.show_ok_cancel_dialog()
        else:
            logger.info(f'EDF file not loaded. Can not compute spectrogram.')

        if process_eeg:
            self.result_spectrograph_obj_list = [] if self.result_spectrograph_obj_list == None else self.result_spectrograph_obj_list
            # Turn on busy cursor
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

            # Make sure figures are not inadvertenly generated
            self.automatic_signal_redraw = False

            # Get Continuous Signals
            signal_label = self.ui.comboBox_spectrogram_signals.currentText()
            signal_obj = self.edf_obj.edf_signals.return_edf_signal(signal_label)
            signal_analysis_obj = EdfSignalAnalysis(signal_obj)

            # Compute Spectrogram
            logger.info(f'Computing spectrogram ({signal_label}): computation may be time consuming')
            multitaper_spectrogram_obj = signal_analysis_obj.multitapper_spectrogram()

            if multitaper_spectrogram_obj.spectrogram_computed:
                # Plot spectrogram if computer
                multitaper_spectrogram_obj.plot(self.ui.graphicsView_spectrogram)
                self.multitaper_spectrogram_obj = multitaper_spectrogram_obj

                # Update log
                logger.info(f'Spectrogram plotted')
            else:
                # Plot signal heatmap
                multitaper_spectrogram_obj.plot_data(self.ui.graphicsView_spectrogram)
                logger.info(f'Plotted heatmap instead')

            self.multitaper_spectrogram_obj = multitaper_spectrogram_obj

            # Turn off busy cursor
            QApplication.restoreOverrideCursor()

            # Turn on signal update
            self.automatic_signal_redraw = True

            # Turn on Legend Pushbutton
            self.ui.pushButton_spectrogram_legend.setEnabled(True)
    def on_spectrogram_double_click(self, x_value, _y_value):
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
        signal_label = self.ui.comboBox_spectrogram_signals.currentText()
        signal_obj = self.edf_obj.edf_signals.return_edf_signal(signal_label)
        signal_analysis_obj = EdfSignalAnalysis(signal_obj)

        # Compute Spectrogram
        logger.info(f'Plotting heatmap: ({signal_label})')
        multitaper_spectrogram_obj = signal_analysis_obj.multitapper_spectrogram()

        # Plot signal heatmap
        multitaper_spectrogram_obj.plot_data(self.ui.graphicsView_spectrogram,
                                        double_click_callback=self.on_spectrogram_double_click)
        self.multitaper_spectrogram_obj = multitaper_spectrogram_obj

        # Record Spectrogram Completions
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

    # Compute
    def setup_analysis(self):
        # Define analysis variables
        self.analyis_signal_labels = [self.ui.label_results_1, self.ui.label_results_2,
                                      self.ui.label_results_3, self.ui.label_results_4,
                                      self.ui.label_results_5, self.ui.label_results_6,
                                      self.ui.label_results_7, self.ui.label_results_8,
                                      self.ui.label_results_9, self.ui.label_results_10]
        self.analyis_signal_combo_boxes = [self.ui.comboBox_settings_analysis_sig1, self.ui.comboBox_settings_analysis_sig2,
                                      self.ui.comboBox_settings_analysis_sig3, self.ui.comboBox_settings_analysis_sig4,
                                      self.ui.comboBox_settings_analysis_sig5, self.ui.comboBox_settings_analysis_sig6,
                                      self.ui.comboBox_settings_analysis_sig7, self.ui.comboBox_settings_analysis_sig8,
                                      self.ui.comboBox_settings_analysis_sig9, self.ui.comboBox_settings_analysis_sig10]
        self.reference_signal_combo_boxes = [self.ui.comboBox_settings_ref_sig1, self.ui.comboBox_settings_ref_sig2,
                                      self.ui.comboBox_settings_ref_sig3, self.ui.comboBox_settings_ref_sig4,
                                      self.ui.comboBox_settings_ref_sig5, self.ui.comboBox_settings_ref_sig6,
                                      self.ui.comboBox_settings_ref_sig7, self.ui.comboBox_settings_ref_sig8,
                                      self.ui.comboBox_settings_ref_sig9, self.ui.comboBox_settings_ref_sig10]
        self.results_graphic_views = [self.ui.graphicsView_results_1, self.ui.graphicsView_results_2,
                                      self.ui.graphicsView_results_3, self.ui.graphicsView_results_4,
                                      self.ui.graphicsView_results_5, self.ui.graphicsView_results_6,
                                      self.ui.graphicsView_results_7, self.ui.graphicsView_results_9,
                                      self.ui.graphicsView_results_9, self.ui.graphicsView_results_10]
        self.result_layouts = [self.ui.horizontalLayout_results_1, self.ui.horizontalLayout_results_2,
                               self.ui.horizontalLayout_results_3, self.ui.horizontalLayout_results_4,
                               self.ui.horizontalLayout_results_5, self.ui.horizontalLayout_results_6,
                               self.ui.horizontalLayout_results_7, self.ui.horizontalLayout_results_8,
                               self.ui.horizontalLayout_results_9, self.ui.horizontalLayout_results_10]

        # Setup bands
        self.spectral_bands_low_cb = [self.ui.comboBox_parameters_band_alpha_low,
                                      self.ui.comboBox_parameters_band_theta_low,
                                      self.ui.comboBox_parameters_band_alpha_low,
                                      self.ui.comboBox_parameters_band_sigma_low,
                                      self.ui.comboBox_parameters_band_beta_low,
                                      self.ui.comboBox_parameters_band_gamma_low]
        self.spectral_bands_high_cb = [self.ui.comboBox_parameters_band_alpha_high,
                                      self.ui.comboBox_parameters_band_theta_high,
                                      self.ui.comboBox_parameters_band_alpha_high,
                                      self.ui.comboBox_parameters_band_sigma_high,
                                      self.ui.comboBox_parameters_band_beta_high,
                                      self.ui.comboBox_parameters_band_gamma_high]

        # Setup pushButtons
        self.ui.pushButton_control_compute.clicked.connect(self.analyze_signal_list)
        self.ui.pushButton_control_display_spectrogram.clicked.connect(self.display_spectrogram)
        self.ui.pushButton_control_band.clicked.connect(self.display_bands)
    def get_settings(self)->tuple[dict,dict,dict,dict]:
        # Create setting description dictionary
        setting_description_dict = {}
        setting_description_names = self.setting_description_names
        setting_description_cb = [self.ui.plainTextEdit_settings_description,
                                  self.ui.plainTextEdit_settings_output_suffix]
        for setting_param in zip(setting_description_names, setting_description_cb):
            name, cb = setting_param
            setting_description_dict[name] = cb.toPlainText()

        # Signals
        reference_method = self.ui.comboBox_settings_reference_method.currentText()

        # Analysis Signal Label
        analysis_signal_labels = []
        for cb in self.analyis_signal_combo_boxes:
            analysis_signal_labels.append(cb.currentText())
        analysis_signal_labels = [s for s in analysis_signal_labels if s.strip()]
        self.analysis_signal_labels = analysis_signal_labels

        # Reference Signal Label
        reference_signal_labels = []
        for cb in self.reference_signal_combo_boxes:
            reference_signal_labels.append(cb.currentText())
        reference_signal_labels = [s for s in reference_signal_labels if s.strip()]
        self.reference_signal_labels = reference_signal_labels

        setting_signal_dict = {}
        setting_signal_dict['reference_method'] = reference_method
        setting_signal_dict['analysis_signals'] = analysis_signal_labels
        setting_signal_dict['reference_signal'] = reference_signal_labels

        # Plotting
        setting_plotting_dict = {}
        setting_plotting_dict['show_x_labels'] = self.ui.checkBox_plotting_xlabels.isChecked()

        # Filter
        setting_filter_dict = {}
        setting_filter_dict['apply_band'] = self.ui.checkBox_settings_band.isChecked()
        safe_float_f = lambda x: float(x) if x.strip() else None
        setting_filter_dict['band_low'] = safe_float_f(self.ui.comboBox_settings_band_low.currentText())
        setting_filter_dict['band_high'] = safe_float_f(self.ui.comboBox_settings_band_high.currentText())
        setting_filter_dict['apply_notch'] = self.ui.checkBox_settings_notch.isChecked()
        setting_filter_dict['notch'] = safe_float_f(self.ui.comboBox_settings_notch.currentText())

        return setting_description_dict, setting_signal_dict, setting_plotting_dict, setting_filter_dict
    def get_parameters(self):
        # Noise Detection
        names = self.param_noise_names
        cbs = [self.ui.comboBox_parameters_noise_delta, self.ui.comboBox_parameters_noise_beta]
        noise_param_dict = self.create_param_dict(names, cbs, float)

        # Multi-taper
        param_taper_names = self.param_taper_names
        taper_cbs = [self.ui.comboBox_parameters_taper_window, self.ui.comboBox_parameters_taper_step,
                     self.ui.comboBox_parameters_taper_num_cpus]
        taper_param_dict = self.create_param_dict(param_taper_names, taper_cbs, float)

        # Spectral bands - Create a dictionary to create bands
        band_params_dict = {}
        param_band_names = self.param_band_names
        for band_limits in zip(param_band_names, self.spectral_bands_low_cb, self.spectral_bands_high_cb):
            # Get band limits and add to parmeter dictionary
            band_name, band_low_cb, band_high_cb = band_limits
            band_params_dict[band_name] = [float(band_low_cb.currentText()), float(band_high_cb.currentText())]

        # Analysis
        analysis_param_dict = {}
        param_analysis_names = self.param_analysis_names
        analysis_cb = [self.ui.comboBox_parameters_analysis_range]
        for analysis_tuple in zip(param_analysis_names, analysis_cb):
            analysis_name, analysis_cb = analysis_tuple
            analysis_param_dict[analysis_name] = analysis_cb.currentText()

        return noise_param_dict, taper_param_dict, band_params_dict, analysis_param_dict
    def create_param_dict(self, names:list[str], cbs:list, convert_f:Callable=lambda x:x)->dict:
        param_dict = {}
        for taper_bands in zip(names, cbs):
            name, cb = taper_bands
            param_dict[name] = convert_f(cb.currentText())
        return param_dict
    def analyze_signal_list(self):
        # Check user if we should move forward
        process_signals = False
        if self.edf_obj is not None:
            process_eeg = self.show_ok_cancel_dialog()
        else:
            logger.info(f'EDF file not loaded. Can not analyze signal list.')

        # Write to log file
        logger.info(f'Preparing to compute spectrograms.')

        # Get settings
        setting_description_dict, setting_signal_dict, setting_plotting_dict, setting_filter_dict = self.get_settings()
        analysis_signal_labels = setting_signal_dict['analysis_signals']
        self.analysis_signal_labels = analysis_signal_labels
        if not analysis_signal_labels:
            logger.info('Aborting spectral analysis: No analysis signals selected.')
            return

        # Get parameters
        noise_param_dict, taper_param_dict, band_params_dict, analysis_param_dict = self.get_parameters()
        noise_delta = noise_param_dict['delta']
        noise_beta = noise_param_dict['beta']
        n_jobs = taper_param_dict['num_cpus']
        window_params = [taper_param_dict['window'], taper_param_dict['step']]
        multiprocess = False if n_jobs >= 1 else True

        filter_param = [-1, -1, -1]
        if setting_filter_dict['apply_band']:
            filter_param[0] = setting_filter_dict['band_low']
            filter_param[1] = setting_filter_dict['band_high']
        if setting_filter_dict['apply_notch']:
            filter_param[2] = setting_filter_dict['notch']

        # Turn on busy cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        # Check if x-labels
        turn_axis_units_off = not self.ui.checkBox_plotting_xlabels.isChecked()
        set_layout_visible(self.ui.horizontalLayout_time_axis, turn_axis_units_off)

        self.result_spectrogram_obj_list = []
        for i, signal_label in enumerate(analysis_signal_labels):
            # Setup labels
            gui_signal_lbl = self.analyis_signal_labels[i]
            gui_signal_lbl.setText(signal_label)

            # Setup and compute spectrogram
            signal_obj = self.edf_obj.edf_signals.return_edf_signal(signal_label)
            signal_analysis_obj = EdfSignalAnalysis(signal_obj, multiprocess=multiprocess, n_jobs=n_jobs,
                                                    window_params=window_params, filter_param=filter_param)
            multitaper_spectrogram_obj = signal_analysis_obj.multitapper_spectrogram()
            self.result_spectrogram_obj_list.append(multitaper_spectrogram_obj)

            # Plot spectrogram
            layout = self.result_layouts[i]
            set_layout_visible(layout, True)

            # Plot spectrogram or heatmap if not computed
            if multitaper_spectrogram_obj.spectrogram_computed:
                # Plot spectrogram if computer
                show_legend = True
                multitaper_spectrogram_obj.plot(self.results_graphic_views[i], turn_axis_units_off=turn_axis_units_off,
                                                show_legend=show_legend)

                # Update log
                logger.info(f'Spectrogram plotted')
            else:
                # Plot signal heatmap
                multitaper_spectrogram_obj.plot_data(self.results_graphic_views[i])
                logger.info(f'Plotted heatmap instead')

        # Hide graphic views not used
        for i in range(len(analysis_signal_labels), len(self.results_graphic_views)):
            layout = self.result_layouts[i]
            set_layout_visible(layout, False)

        # Set time axis
        self.ui.label_results_time.setText('Time')

        # Create x-axis for reference
        turn_axis_units_off = False
        axis_only = True
        graphics_view = self.ui.graphicsView_time_axis
        signal_label = analysis_signal_labels[0]
        signal_obj = self.edf_obj.edf_signals.return_edf_signal(signal_label)
        signal_analysis_obj = EdfSignalAnalysis(signal_obj)
        multitaper_spectrogram_obj = signal_analysis_obj.multitapper_spectrogram()
        multitaper_spectrogram_obj.plot(graphics_view, turn_axis_units_off=turn_axis_units_off, axis_only=axis_only)

        # Set up analysis buttons
        self.enable_spectrogram_options(True)

        # Save settings and parameters dictionaries
        self.setting_description_dict = setting_description_dict
        self.setting_signal_dict = setting_signal_dict
        self.setting_plotting_dict = setting_plotting_dict
        self.setting_filter_dict = setting_filter_dict
        self.noise_param_dict = noise_param_dict
        self.taper_param_dict = taper_param_dict
        self.band_params_dict = band_params_dict
        self.analysis_param_dict = analysis_param_dict

        # Turn on summarize button
        self.enable_spectrogram_options(True)

        # Turn off busy cursor
        QApplication.restoreOverrideCursor()
    def enable_spectrogram_options(self, enable:bool=True):
        spectral_analysis_options = [self.ui.pushButton_control_display_spectrogram,
                                     self.ui.pushButton_control_spectrum_average,
                                     self.ui.pushButton_control_band]

        for each_button in spectral_analysis_options:
            each_button.setEnabled(enable)
    def display_spectrogram(self):
        # Check if spectrogram results are available
        if self.result_spectrogram_obj_list is None:
            logger.info('Spectrogram results are not available.')
            return

        # Update log file
        logger.info('Summarize spectrogram by stage.')

        # Turn off button
        self.ui.pushButton_control_display_spectrogram.setEnabled(False)

        # Check if spectrogram is avaialble
        show_legend = True
        for i, spec_obj in enumerate(self.result_spectrogram_obj_list):
            multi_taper_spec_reult_dict = spec_obj.get_multi_taper_results()
            turn_axis_units_off = True
            spec_obj.plot(self.results_graphic_views[i], turn_axis_units_off=turn_axis_units_off,
                          show_legend=show_legend)

        # Turn Off X axis
        set_layout_visible(self.ui.horizontalLayout_time_axis, False)

        # Turn off button
        self.ui.pushButton_control_display_spectrogram.setEnabled(True)

    # Summarize
    def setup_summarize(self):
        # Turn off spectrum button
        self.enable_spectrogram_options(False)
        self.ui.pushButton_control_spectrum_average.clicked.connect(self.summarize_by_stage)
    def summarize_by_stage(self, analysis_range_str:str=''):
        # Check if spectrogram results are available
        if self.result_spectrogram_obj_list is None:
            logger.info('Spectrogram results are not available.')
            return

        # Update log file
        logger.info('Summarize spectrogram by stage.')

        # Turn off button
        self.ui.pushButton_control_spectrum_average.setEnabled(False)

        # Get analysis range
        analysis_range_setting = self.ui.comboBox_parameters_analysis_range.currentText()

        # Enable Data Segment Selection
        stage_time_dict = self.xml_obj.sleep_stages_obj.return_stage_time_dict()
        sleep_start_time = stage_time_dict['sleep_start_time']
        sleep_end_time = stage_time_dict['sleep_end_time']
        max_recording_time = self.xml_obj.sleep_stages_obj.max_time_sec
        analysis_range = [0.0, max_recording_time]
        if  analysis_range_setting == 'All':
            analysis_range = [0.0, max_recording_time]
        elif analysis_range_setting == 'Wake':
            analysis_range = [0.0, sleep_start_time]
        elif analysis_range_setting == 'Wake through Sleep':
            analysis_range = [0.0, sleep_end_time]
        elif analysis_range_setting == 'Sleep Only':
            analysis_range = [sleep_start_time, sleep_end_time]
        elif analysis_range_setting == 'Ending Wake':
            analysis_range = [sleep_end_time, max_recording_time]

        # Enable Sorting by stage
        epoch = self.xml_obj.sleep_stages_obj.sleep_epoch
        hypnogram_style = self.ui.comboBox_hynogram.currentText()
        stages = self.xml_obj.sleep_stages_obj.sleep_stages_text
        if hypnogram_style == 'NREM_REM_W':
            stages = self.xml_obj.sleep_stages_obj.sleep_stages_NremRem
        elif hypnogram_style == 'N1_N2_N3_REM_W':
            stages = self.xml_obj.sleep_stages_obj.sleep_stages_N3
        stage_information = [epoch, stages]

        # Get Default Colors
        stage_colors = self.xml_obj.sleep_stages_obj.default_stage_colors

        # Check if spectrogram is avaialble
        for i, spec_obj in enumerate(self.result_spectrogram_obj_list):
            turn_axis_units_off = False
            p_widget = self.results_graphic_views[i]
            spec_obj.plot_spectral_summary(parent_widget=p_widget, turn_axis_units_off=turn_axis_units_off,
                                           analysis_range=analysis_range, stage_information = stage_information,
                                           stage_colors=stage_colors)

        # Turn Off X axis
        set_layout_visible(self.ui.horizontalLayout_time_axis, False)

        # Turn off button
        self.ui.pushButton_control_spectrum_average.setEnabled(True)
    def display_bands(self):
        # Check if spectrogram results are available
        if self.result_spectrogram_obj_list is None:
            logger.info('Spectrogram results are not available.')
            return

        # Update log file
        logger.info('Summarize spectrogram by stage.')

        # Turn off button
        self.ui.pushButton_control_spectrum_average.setEnabled(False)

        # Get analysis range
        analysis_range_setting = self.ui.comboBox_parameters_analysis_range.currentText()

        # Enable Data Segment Selection
        stage_time_dict = self.xml_obj.sleep_stages_obj.return_stage_time_dict()
        sleep_start_time = stage_time_dict['sleep_start_time']
        sleep_end_time = stage_time_dict['sleep_end_time']
        max_recording_time = self.xml_obj.sleep_stages_obj.max_time_sec
        analysis_range = [0.0, max_recording_time]
        if analysis_range_setting == 'All':
            analysis_range = [0.0, max_recording_time]
        elif analysis_range_setting == 'Wake':
            analysis_range = [0.0, sleep_start_time]
        elif analysis_range_setting == 'Wake through Sleep':
            analysis_range = [0.0, sleep_end_time]
        elif analysis_range_setting == 'Sleep Only':
            analysis_range = [sleep_start_time, sleep_end_time]
        elif analysis_range_setting == 'Ending Wake':
            analysis_range = [sleep_end_time, max_recording_time]

        # Check if spectrogram is avaialble
        for i, spec_obj in enumerate(self.result_spectrogram_obj_list):
            turn_axis_units_off = False
            p_widget = self.results_graphic_views[i]
            spec_obj.plot_band_summary(parent_widget=p_widget, turn_axis_units_off=turn_axis_units_off,
                                           analysis_range=analysis_range)

        # Turn Off X axis
        set_layout_visible(self.ui.horizontalLayout_time_axis, False)

        # Turn off button
        self.ui.pushButton_control_spectrum_average.setEnabled(True)