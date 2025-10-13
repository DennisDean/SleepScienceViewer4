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
        self.setup_spectrogram()

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
        create_taper_menu_item_f = lambda x: f'{x:.2f} s'
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
