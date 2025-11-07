# Spectral Window Class
#
# Generate and independent window for performing signal spectral analysis. The interface allows the user to set
# select signals, set analysis bands, and set multi-taper parameters. Interface provides a summary and visualization
# options to support interpretation of results. Bands, Paramerters, epoch level noise detection, and results can be
# exported for further analysis.
#

# To Do:
# Essential
# TODO: Check band plot figure, pretty, not clear it is accurate
# TODO: Add epoch level noise exclusion
#
# Facilitate large scale analysis
# TODO: save range values, stage masks, nrem-rem masks
# TODO: Include mask description in configureation file

# Modules
import csv
import logging
import math
import numpy as np
import os
import pandas as pd
import psutil
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Callable

# Interface packages and modules
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget
from PySide6.QtWidgets import (QPushButton, QLabel, QLineEdit, QFileDialog, QMainWindow, QTextEdit, QGraphicsView,
                               QGraphicsScene, QMenu, QFormLayout, QDialogButtonBox, QDoubleSpinBox, QSizePolicy)
from PySide6.QtCore import QEvent, Qt, QObject,Signal
from PySide6.QtGui import QKeyEvent

# Class Extension
class FigureGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.figure = None
        self.canvas_item = None

    # --- Optional if you embed figures dynamically ---
    def set_figure(self, figure):
        if self.canvas_item:
            self.scene.removeItem(self.canvas_item)
        self.figure = figure
        canvas = FigureCanvas(figure)
        self.scene.addWidget(canvas)
        self.canvas_item = canvas

    # --- Right-click context menu ---
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        save_action = menu.addAction("Save Figure...")
        menu.addSeparator()
        menu.addAction("Cancel")

        action = menu.exec(event.globalPos())

        if action == save_action:
            self.open_save_dialog()

    # --- Save dialog ---
    def open_save_dialog(self):
        if self.figure is None:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Save Figure")
        layout = QFormLayout(dialog)

        width_spin = QDoubleSpinBox()
        width_spin.setRange(1.0, 50.0)
        width_spin.setValue(self.figure.get_size_inches()[0])
        layout.addRow("Width (inches):", width_spin)

        height_spin = QDoubleSpinBox()
        height_spin.setRange(1.0, 50.0)
        height_spin.setValue(self.figure.get_size_inches()[1])
        layout.addRow("Height (inches):", height_spin)

        dpi_spin = QDoubleSpinBox()
        dpi_spin.setRange(50, 1200)
        dpi_spin.setValue(self.figure.dpi)
        layout.addRow("DPI:", dpi_spin)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addRow(buttons)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.Accepted:
            width = width_spin.value()
            height = height_spin.value()
            dpi = dpi_spin.value()
            self.save_figure_to_file(width, height, dpi)
    def show_context_menu(self, pos):
        menu = QMenu(self)
        save_action = menu.addAction("Save Figure…")
        menu.addSeparator()
        menu.addAction("Cancel")
        action = menu.exec(self.mapToGlobal(pos))
        if action == save_action:
            self.open_save_dialog()

    # --- Save file method ---
    def save_figure_to_file(self, width, height, dpi):
        if self.figure is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Figure", "", "PNG Files (*.png);;PDF Files (*.pdf);;SVG Files (*.svg)"
        )
        if not file_path:
            return

        # Save original size
        original_size = self.figure.get_size_inches().copy()
        original_dpi = self.figure.dpi

        try:
            # Set new size for saving
            self.figure.set_size_inches(width, height)
            self.figure.savefig(file_path, dpi=dpi, bbox_inches='tight')
        finally:
            # Restore original size
            self.figure.set_size_inches(original_size)
            self.figure.dpi = original_dpi

            # Redraw the canvas to reflect restored size
            if self.canvas_item:
                self.canvas_item.draw()

# Sleep Science Classes
from EdfFileClass import EdfFile, EdfSignalAnalysis
from AnnotationXmlClass import AnnotationXml

# Analsysis Classes
from multitaper_spectrogram_python_class import MultitaperSpectrogram

# GUI Interface
from SpectralViewer import Ui_MainWindow

# Dialog Boxes
class SpectralFolderDialog(QDialog):
    def __init__(self, parent=None, default_folder=""):
        super().__init__(parent)
        self.setWindowTitle("Save Spectral Results")
        self.setMinimumSize(500, 200)
        self.selected_folder = None
        self.default_folder = default_folder

        # Description label
        description = QLabel("Select a folder where spectral analysis results will be saved.")
        description.setWordWrap(True)

        # Folder selection row
        folder_label = QLabel("Folder:")
        self.folder_path = QLineEdit()
        self.folder_path.setPlaceholderText("No folder selected")
        self.folder_path.setReadOnly(True)

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_folder)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_path)
        folder_layout.addWidget(browse_button)

        # Buttons
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)

        self.ok_button = QPushButton("OK")
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self.accept_selection)
        self.ok_button.setDefault(True)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.ok_button)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(description)
        layout.addSpacing(10)
        layout.addLayout(folder_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        self.setLayout(layout)
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder for Spectral Results",
            self.default_folder,  # Start in this directory
            QFileDialog.Option.ShowDirsOnly
        )

        if folder:
            self.folder_path.setText(folder)
            self.selected_folder = folder
            self.ok_button.setEnabled(True)
    def accept_selection(self):
        if not self.selected_folder:
            QMessageBox.warning(self, "No Folder Selected",
                                "Please select a folder before continuing.")
            return

        folder_path = Path(self.selected_folder)
        if not folder_path.exists() or not folder_path.is_dir():
            QMessageBox.warning(self, "Invalid Folder",
                                "The selected folder is not valid.")
            return

        self.accept()
    def get_selected_folder(self):
        return self.selected_folder

# Example MainWindow class that uses the dialog
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spectral Analysis Application")
        self.setGeometry(100, 100, 800, 600)
        self.save_folder = None

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Title
        title = QLabel("Spectral Analysis Tool")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Info display
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setPlaceholderText("Select a save folder to begin...")

        # Current folder display
        self.current_folder_label = QLabel("Current Save Folder: <i>Not set</i>")
        self.current_folder_label.setTextFormat(Qt.TextFormat.RichText)

        # Buttons
        select_folder_button = QPushButton("Select Save Folder")
        select_folder_button.clicked.connect(self.open_folder_dialog)

        self.run_analysis_button = QPushButton("Run Analysis")
        self.run_analysis_button.setEnabled(False)
        self.run_analysis_button.clicked.connect(self.run_analysis)

        button_layout = QHBoxLayout()
        button_layout.addWidget(select_folder_button)
        button_layout.addWidget(self.run_analysis_button)
        button_layout.addStretch()

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.info_text)
        layout.addWidget(self.current_folder_label)
        layout.addLayout(button_layout)
        central_widget.setLayout(layout)

    def open_folder_dialog(self):
        dialog = SpectralFolderDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.save_folder = dialog.get_selected_folder()
            self.current_folder_label.setText(f"Current Save Folder: <b>{self.save_folder}</b>")
            self.run_analysis_button.setEnabled(True)
            self.info_text.append(f"✓ Save folder set to: {self.save_folder}\n")
        else:
            self.info_text.append("Folder selection cancelled.\n")

    def run_analysis(self):
        if self.save_folder:
            self.info_text.append(f"Running spectral analysis...\n")
            self.info_text.append(f"Results will be saved to: {self.save_folder}\n")
            self.info_text.append("Analysis complete!\n\n")

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
def make_xml_safe_tag(key: str) -> str:
    """
    Convert a given key into a valid XML tag name.

    Rules:
    - Must start with a letter or underscore
    - Contains only letters, digits, hyphens, underscores, and periods
    - Replace invalid characters with underscores
    - If starts with 'xml' (case-insensitive), prefix with '_'
    """

    # Replace invalid characters with underscores
    safe_key = re.sub(r'[^a-zA-Z0-9_.-]', '_', key)

    # Ensure the first character is a letter or underscore
    if not re.match(r'[A-Za-z_]', safe_key[0]):
        safe_key = '_' + safe_key

    # Avoid reserved XML prefixes like "xml"
    if safe_key.lower().startswith('xml'):
        safe_key = '_' + safe_key

    return safe_key
def make_dict_from_list(list_labels, list_entries, exisiting_dict:dict|None=None):
    """ Return dictionary from list and labels"""

    # Create return dictionary
    if exisiting_dict is None:
        return_dict = {}
    else:
        return_dict = exisiting_dict

    # Create or add to, redundant stages are overwritten
    for lkey, lentry in zip(list_labels, list_entries):
        return_dict[lkey] = lentry

    return return_dict


# To Do
#TODO: Add check box support for dictionaries to hold parameters
#TODO: Add checks for empty data slices
#TODO: Add support for saving spectrogram support

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

        # Overide Graphic Views
        self.graphicsView_hypnogram: QGraphicsView | None = None
        self.graphicsView_hypnogram = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_hypnogram)

        self.graphicsView_spectrogram: QGraphicsView | None = None
        self.graphicsView_spectrogram = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_spectrogram)

        self.graphicsView_results_1: QGraphicsView | None = None
        self.graphicsView_results_1 = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_results_1)

        self.graphicsView_results_2: QGraphicsView | None = None
        self.graphicsView_results_2 = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_results_2)

        self.graphicsView_results_3: QGraphicsView | None = None
        self.graphicsView_results_3 = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_results_3)

        self.graphicsView_results_4: QGraphicsView | None = None
        self.graphicsView_results_4 = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_results_4)

        self.graphicsView_results_5: QGraphicsView | None = None
        self.graphicsView_results_5 = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_results_5)

        self.graphicsView_results_6: QGraphicsView | None = None
        self.graphicsView_results_6 = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_results_6)

        self.graphicsView_results_7: QGraphicsView | None = None
        self.graphicsView_results_7 = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_results_7)

        self.graphicsView_results_8: QGraphicsView | None = None
        self.graphicsView_results_8 = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_results_8)

        self.graphicsView_results_9: QGraphicsView | None = None
        self.graphicsView_results_9 = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_results_9)

        self.graphicsView_results_10: QGraphicsView | None = None
        self.graphicsView_results_10 = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_results_10)

        self.graphicsView_time_axis: QGraphicsView | None = None
        self.graphicsView_time_axis = self.replace_designer_graphic_view_with_custom(self.ui.graphicsView_time_axis)

        # Save signals and annotations
        self.edf_obj = edf_obj
        self.xml_obj = xml_obj

        # Control
        self.automatic_signal_redraw:bool|None=None
        self.current_epoch:int|None=None
        self.reference_signal_labels:list|None=None

        # Define settings variables
        self.settings_brief_description_default:str = 'Multi-taper Spectrogram computed with Sleep Science Viewer'
        self.settings_output_suffic:str ='multi_taper'
        self.spectral_bands_default:list[list]
        self.spectral_bands_titles_default:list
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
        # currently includes only combo boxes, need to add check boxes
        self.param_noise_names = ['delta_factor','delta_low','delta_high','beta_factor','beta_low','beta_high']
        self.param_noise_dict:dict|None = None
        self.param_taper_names = ['window', 'step', 'num_cpus']
        self.param_taper_dict:dict|None = None
        self.param_band_names = ['delta', 'theta', 'alpha', 'sigma', 'beta', 'gamma']
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

        # Noise Parameters
        self.noise_delta_n_factor:float|None = None
        self.noise_beta_n_factor:float|None = None
        self.create_noise_menu_item_f:float|None = None
        self.noise_delta_n_menu_items:float|None = None
        self.noise_beta_n_menu_items:float|None = None

        # Setup parameters
        self.band_low_values:list|None = None
        self.band_high_values:list|None = None
        self.notch_values:list|None = None
        self.band_low_menu_items:list|None = None
        self.band_high_menu_items:list|None = None
        self.notch_menu_items:list|None = None
        self.spectral_bands_low_cb:list|None = None
        self.spectral_bands_high_cb:list|None = None
        self.spectral_bands_default = [[0.5, 4.0], [4.0, 8.0], [8.0, 12.0], [12.0, 15.0], [15.0, 30.0], [30.0, 50.0]]
        self.spectral_bands_titles_default = ['delta', 'beta', 'alpha', 'sigma', 'beta', 'gamma']

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
        self.reference_signal_combo_boxes:list|None = None
        self.results_graphic_views:list|None = None
        self.result_layouts:list|None = None
        self.setup_analysis()

        # Set up spectral analysis list
        self.result_spectrograph_obj_list:list|None=None
        self.signal_input_obj_list:list|None=None

        # Set up summary
        self.setup_summarize()

        # Result Varaibiles
        self.result_spectrogram_obj_list:list|None = None
        self.result_average_spectrogram_list:list|None = None
        self.input_signal_obj_list:list|None = None
        self.noise_mask_list:list|None=None
        self.stage_mask_list:list|None=None
        self.analysis_param_dict:dict|None=None
        self.analysis_signal_labels:dict|None=None

    # Init Utilities
    def replace_designer_graphic_view_with_custom(self, old_graphic_view: QGraphicsView):
        # Capture the original geometry and size policy
        old_height = old_graphic_view.height()
        old_policy = old_graphic_view.sizePolicy()

        # Create the new graphics view
        new_graphic_view = FigureGraphicsView(self)

        # Apply the same size policy and fixed height
        new_graphic_view.setSizePolicy(old_policy)
        if old_policy.verticalPolicy() == QSizePolicy.Policy.Fixed:
            new_graphic_view.setFixedHeight(old_height)
        else:
            # Maintain the same min/max height if not fixed
            new_graphic_view.setMinimumHeight(old_graphic_view.minimumHeight())
            new_graphic_view.setMaximumHeight(old_graphic_view.maximumHeight())

        # Replace in the parent layout
        layout = old_graphic_view.parent().layout()
        layout.replaceWidget(old_graphic_view, new_graphic_view)
        old_graphic_view.deleteLater()

        # Match geometry explicitly to prevent layout recalculation from resizing it
        new_graphic_view.setGeometry(old_graphic_view.geometry())

        return new_graphic_view

    # Manage connections
    def focusOutEvent(self, event):
        """Called when window loses focus"""
        # Clean up events when switching away from this window

        # Clear hypnogram plot connections
        if hasattr(self.xml_obj, 'annotation_xml_obj'):  # Replace with your actual object name
            if hasattr(self.xml_obj, 'sleep_stages_obj'):  # Replace with your actual object name
                self.xml_obj.sleep_stages_obj.cleanup_events()

        # Clear annotation plot connections
        if hasattr(self, 'xml_obj'):  # Replace with your actual object name
            if hasattr(self.xml_obj, 'scored_event_obj'):  # Replace with your actual object name
                self.xml_obj.scored_event_obj.cleanup_events()

        # Clear spectrogram and heatmap connections
        if hasattr(self, 'multitaper_spectrogram_obj'):
            self.multitaper_spectrogram_obj.cleanup_events()

        # Write to log file
        logger.info(f'Spectral Window - focusOutEvent')

        super().focusOutEvent(event)
    def focusInEvent(self, event):
        """Called when window gains focus"""

        # Clear hypnogram plot connections
        if hasattr(self, 'xml_obj'):  # Replace with your actual object name
            if hasattr(self.xml_obj, 'sleep_stages_obj'):  # Replace with your actual object name
                self.xml_obj.sleep_stages_obj.setup_events()

        # Clear annotation plot connections
        if hasattr(self, 'xml_obj'):  # Replace with your actual object name
            if hasattr(self.xml_obj, 'scored_event_obj'):  # Replace with your actual object name
                self.xml_obj.scored_event_obj.setup_events()

        # Clear spectrogram and heatmap connections
        if hasattr(self, 'multitaper_spectrogram_obj'):
            self.multitaper_spectrogram_obj.setup_events()

        # Write to log file
        logger.info(f'Spectral Window - focusInEvent')

        super().focusInEvent(event)
    def closeEvent(self, event):
        """Called when window is closing"""
        # Clean up events when closing the window

        # Clear hypnogram plot connections
        if hasattr(self, 'xml_obj') and self.xml_obj is not None:  # Replace with your actual object name
            if hasattr(self.xml_obj,
                       'sleep_stages_obj') and self.xml_obj.sleep_stages_obj is not None:  # Replace with your actual object name
                self.xml_obj.sleep_stages_obj.cleanup_events()

        # Clear annotation plot connections
        if hasattr(self, 'xml_obj') and self.xml_obj is not None:  # Replace with your actual object name
            if hasattr(self.xml_obj,
                       'scored_event_obj') and self.xml_obj.scored_event_obj is not None:  # Replace with your actual object name
                self.xml_obj.scored_event_obj.cleanup_events()

        # Clear spectrogram and heatmap connections
        if hasattr(self, 'multitaper_spectrogram_obj') and self.multitaper_spectrogram_obj is not None:
            self.multitaper_spectrogram_obj.cleanup_events()

        # Write to log file
        logger.info(f'Spectral Viewer - closeEvent')

        event.accept()
        super().closeEvent(event)

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

        # Setup description
        self.ui.plainTextEdit_settings_description.setPlainText(self.settings_brief_description_default)
        self.ui.plainTextEdit_setting_output_suffix.setPlainText(self.settings_output_suffic)

        # Set filter combo box values
        band_low_values         = [0.1, 0.5, 1.0, 10.0 ]
        band_high_values        = [50.0, 60.0, 70.0]
        notch_values            = [50.0, 60.0]
        create_freq_menu_item_f = lambda x:f'{x:.1f}'
        band_low_menu_items     = list(map(create_freq_menu_item_f, band_low_values))
        band_high_menu_items    = list(map(create_freq_menu_item_f, band_high_values))
        notch_menu_items        = list(map(create_freq_menu_item_f, notch_values))
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
        # setup noise factor
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
        self.ui.comboBox_parameters_noise_delta_factor.addItems(noise_delta_n_menu_items)
        self.ui.comboBox_parameters_noise_beta_factor.addItems(noise_beta_n_menu_items)
        self.ui.comboBox_parameters_noise_delta_factor.setCurrentIndex(noise_delta_index)
        self.ui.comboBox_parameters_noise_beta_factor.setCurrentIndex(noise_beta_index)

        # setup delta frequency menu
        noise_hertz_low = np.arange(0.1,10.1,.1)
        noise_hertz_high = np.arange(30.0,70.0,1.0)
        create_noise_menu_item_f = lambda x: f'{x:.1f}'
        noise_hertz_low_items = list(map(create_noise_menu_item_f, noise_hertz_low))
        noise_hertz_high_items = list(map(create_noise_menu_item_f, noise_hertz_high))
        noise_delta_hertz_low_default = 0.6
        noise_delta_hertz_high_degault = 4.6
        noise_beta_hertz_low_default = 40.0
        moise_beta_hertz_high_default = 60.0
        noise_delta_hertz_low_default_index = int(np.where(noise_hertz_low == noise_delta_hertz_low_default)[0][0])
        noise_delta_hertz_high_default_index  = int(np.where(noise_hertz_low == noise_delta_hertz_high_degault)[0][0])
        noise_beta_hertz_low_default_index  = int(np.where(noise_hertz_high == noise_beta_hertz_low_default)[0][0])
        moise_beta_hertz_high_default_index  = int(np.where(noise_hertz_high == moise_beta_hertz_high_default)[0][0])

        # setup noise detection menu
        self.ui.comboBox_parameters_noise_delta_low.addItems(noise_hertz_low_items)
        self.ui.comboBox_parameters_noise_delta_high.addItems(noise_hertz_low_items)
        self.ui.comboBox_parameters_noise_beta_low.addItems(noise_hertz_high_items)
        self.ui.comboBox_parameters_noise_beta_high.addItems(noise_hertz_high_items)
        self.ui.comboBox_parameters_noise_delta_low.setCurrentIndex(noise_delta_hertz_low_default_index)
        self.ui.comboBox_parameters_noise_delta_high.setCurrentIndex(noise_delta_hertz_high_default_index)
        self.ui.comboBox_parameters_noise_beta_low.setCurrentIndex(noise_beta_hertz_low_default_index)
        self.ui.comboBox_parameters_noise_beta_high.setCurrentIndex(moise_beta_hertz_high_default_index)

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
        # Plot parameters
        self.spectral_bands_default = [[0.5, 4.0], [4.0, 8.0], [8.0, 12.0], [12.0, 15.0], [15.0, 30.0], [30.0, 50.0]]
        self.spectral_bands_titles_default = ['delta', 'beta', 'alpha', 'sigma', 'beta', 'gamma']
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
        self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.graphicsView_hypnogram,
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
                self.xml_obj.sleep_stages_obj.plot_hypnogram(parent_widget=self.graphicsView_hypnogram,
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
            self.result_spectrograph_obj_list = [] if self.result_spectrograph_obj_list is None else self.result_spectrograph_obj_list
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
                show_legend = self.ui.checkBox_description_plotting_legend.isChecked()
                multitaper_spectrogram_obj.plot(self.graphicsView_spectrogram, show_legend=show_legend)
                self.multitaper_spectrogram_obj = multitaper_spectrogram_obj

                # Update log
                logger.info(f'Spectrogram plotted')
            else:
                # Plot signal heatmap
                multitaper_spectrogram_obj.plot_data(self.graphicsView_spectrogram)
                logger.info(f'Plotted heatmap instead')

            self.multitaper_spectrogram_obj = multitaper_spectrogram_obj

            # Turn off busy cursor
            QApplication.restoreOverrideCursor()

            # Turn on signal update
            self.automatic_signal_redraw = True

            # Turn on Legend Pushbutton
            self.ui.pushButton_spectrogram_legend.setEnabled(True)
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
        multitaper_spectrogram_obj.plot_data(self.graphicsView_spectrogram)
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
        self.results_graphic_views = [self.graphicsView_results_1, self.graphicsView_results_2,
                                      self.graphicsView_results_3, self.graphicsView_results_4,
                                      self.graphicsView_results_5, self.graphicsView_results_6,
                                      self.graphicsView_results_7, self.graphicsView_results_8,
                                      self.graphicsView_results_9, self.graphicsView_results_10]
        self.result_layouts = [self.ui.horizontalLayout_results_1, self.ui.horizontalLayout_results_2,
                               self.ui.horizontalLayout_results_3, self.ui.horizontalLayout_results_4,
                               self.ui.horizontalLayout_results_5, self.ui.horizontalLayout_results_6,
                               self.ui.horizontalLayout_results_7, self.ui.horizontalLayout_results_8,
                               self.ui.horizontalLayout_results_9, self.ui.horizontalLayout_results_10]

        # Setup bands
        self.spectral_bands_low_cb = [self.ui.comboBox_parameters_band_delta_low,
                                      self.ui.comboBox_parameters_band_theta_low,
                                      self.ui.comboBox_parameters_band_alpha_low,
                                      self.ui.comboBox_parameters_band_sigma_low,
                                      self.ui.comboBox_parameters_band_beta_low,
                                      self.ui.comboBox_parameters_band_gamma_low]
        self.spectral_bands_high_cb = [self.ui.comboBox_parameters_band_delta_high,
                                      self.ui.comboBox_parameters_band_theta_high,
                                      self.ui.comboBox_parameters_band_alpha_high,
                                      self.ui.comboBox_parameters_band_sigma_high,
                                      self.ui.comboBox_parameters_band_beta_high,
                                      self.ui.comboBox_parameters_band_gamma_high]

        # Setup pushButtons
        self.ui.pushButton_control_compute.clicked.connect(self.analyze_signal_list)
        self.ui.pushButton_control_display_spectrogram.clicked.connect(self.display_spectrogram)
        self.ui.pushButton_control_band.clicked.connect(self.display_bands)
        self.ui.pushButton_control_save.clicked.connect(self.save_spectral_results)
    def get_settings(self)->tuple[dict,dict,dict,dict]:
        # Create setting description dictionary
        setting_description_dict = {}
        setting_description_names = self.setting_description_names
        setting_description_cb = [self.ui.plainTextEdit_settings_description,
                                  self.ui.plainTextEdit_setting_output_suffix]
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

        setting_signal_dict = {'reference_method':reference_method, 'analysis_signals':analysis_signal_labels,
                               'reference_signal':reference_signal_labels}

        # Plotting
        setting_plotting_dict = {'show_x_labels':self.ui.checkBox_plotting_xlabels.isChecked(),
                                 'show_legend':self.ui.checkBox_description_plotting_legend.isChecked()}

        # Filter
        safe_float_f = lambda x: float(x) if x.strip() else None
        setting_filter_dict = { 'apply_band':self.ui.checkBox_settings_band.isChecked(),
                                'band_low':safe_float_f(self.ui.comboBox_settings_band_low.currentText()),
                                'band_high':safe_float_f(self.ui.comboBox_settings_band_high.currentText()),
                                'apply_notch':self.ui.checkBox_settings_notch.isChecked(),
                                'notch':safe_float_f(self.ui.comboBox_settings_notch.currentText())}

        return setting_description_dict, setting_signal_dict, setting_plotting_dict, setting_filter_dict
    def get_parameters(self):
        # Noise Detection
        names = self.param_noise_names
        cbs = [self.ui.comboBox_parameters_noise_delta_factor, self.ui.comboBox_parameters_noise_delta_low,
               self.ui.comboBox_parameters_noise_delta_high,
               self.ui.comboBox_parameters_noise_beta_factor, self.ui.comboBox_parameters_noise_beta_low,
               self.ui.comboBox_parameters_noise_beta_high]
        noise_param_dict = self.create_param_dict(names, cbs, float)
        noise_param_dict['apply_noise_detection'] = self.ui.checkBox_parameters_noise_detection.isChecked()

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
    @staticmethod
    def create_param_dict(names:list[str], cbs:list, convert_f:Callable=lambda x:x)->dict:
        param_dict = {}
        for taper_bands in zip(names, cbs):
            name, cb = taper_bands
            param_dict[name] = convert_f(cb.currentText())
        return param_dict
    def analyze_signal_list(self):
        # Check user if we should move forward
        process_eeg = False
        if self.edf_obj is not None:
            process_eeg = self.show_ok_cancel_dialog()
            logger.info(f'EDF file not loaded. Can not analyze signal list.')
        if not process_eeg:
            logger.info(f'User cancelled analysis.')
            return

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
        noise_detect_param_dict = noise_param_dict
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

        # Show legend
        show_legend = self.ui.checkBox_description_plotting_legend.isChecked()

        # Process each signal
        epoch_width = self.xml_obj.sleep_stages_obj.sleep_epoch
        self.result_spectrogram_obj_list = []
        self.input_signal_obj_list = []
        self.noise_mask_list = []
        self.stage_mask_list = []
        for i, signal_label in enumerate(analysis_signal_labels):
            # Setup labels
            gui_signal_lbl = self.analyis_signal_labels[i]
            gui_signal_lbl.setText(signal_label)

            # Setup and compute spectrogram
            signal_obj = self.edf_obj.edf_signals.return_edf_signal(signal_label, epoch_width = epoch_width)
            signal_analysis_obj = EdfSignalAnalysis(signal_obj, multiprocess=multiprocess, n_jobs=n_jobs,
                                                    window_params=window_params, filter_param=filter_param,
                                                    noise_detect_param_dict=noise_detect_param_dict)
            multitaper_spectrogram_obj = signal_analysis_obj.multitapper_spectrogram()

            # Store Results
            self.input_signal_obj_list.append(signal_obj)
            self.result_spectrogram_obj_list.append(multitaper_spectrogram_obj)
            noise_mask_dict = signal_analysis_obj.noise_mask_dict
            self.noise_mask_list.append(noise_mask_dict)

            # Plot spectrogram
            layout = self.result_layouts[i]
            set_layout_visible(layout, True)

            # Plot spectrogram or heatmap if not computed
            if multitaper_spectrogram_obj.spectrogram_computed:
                # Plot spectrogram if computer
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
        graphics_view = self.graphicsView_time_axis
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
                                     self.ui.pushButton_control_band,
                                     self.ui.pushButton_control_save]

        for each_button in spectral_analysis_options:
            each_button.setEnabled(enable)
    def display_spectrogram(self):
        # Check if spectrogram results are available
        if self.result_spectrogram_obj_list is None:
            logger.info('Spectrogram results are not available.')
            return

        # Update log file
        logger.info('Summarize spectrogram by stage.')

        # Set wait cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        # Turn off button
        self.ui.pushButton_control_display_spectrogram.setEnabled(False)

        # Check if spectrogram is avaialble
        turn_axis_units_off = not self.ui.checkBox_plotting_xlabels.isChecked()
        show_legend = self.ui.checkBox_description_plotting_legend.isChecked()
        for i, spec_obj in enumerate(self.result_spectrogram_obj_list):
            spec_obj.plot(self.results_graphic_views[i], turn_axis_units_off=turn_axis_units_off,
                          show_legend=show_legend)

        # Turn Off X axis
        show_x_axis_layout = turn_axis_units_off
        set_layout_visible(self.ui.horizontalLayout_time_axis, show_x_axis_layout)

        # Create x-axis for reference
        if show_x_axis_layout:
            turn_axis_units_off = False
            axis_only = True
            graphics_view = self.graphicsView_time_axis
            signal_label = self.analysis_signal_labels[0]
            signal_obj = self.edf_obj.edf_signals.return_edf_signal(signal_label)
            signal_analysis_obj = EdfSignalAnalysis(signal_obj)
            multitaper_spectrogram_obj = signal_analysis_obj.multitapper_spectrogram()
            multitaper_spectrogram_obj.plot(graphics_view, turn_axis_units_off=turn_axis_units_off, axis_only=axis_only)

        # Turn on button
        self.ui.pushButton_control_display_spectrogram.setEnabled(True)

        # Turn off busy cursor
        QApplication.restoreOverrideCursor()

    # Summarize
    def setup_summarize(self):
        # Turn off spectrum button
        self.enable_spectrogram_options(False)
        self.ui.pushButton_control_spectrum_average.clicked.connect(self.summarize_by_stage)
    def summarize_by_stage(self):
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

        # Set spectral bands
        spectral_bands = self.spectral_bands_default
        spectral_titles = self.spectral_bands_titles_default

        # Enable Sorting by stage
        epoch = self.xml_obj.sleep_stages_obj.sleep_epoch
        hypnogram_style = self.ui.comboBox_hynogram.currentText()
        stages = self.xml_obj.sleep_stages_obj.sleep_stages_text
        if hypnogram_style == 'NREM_REM_W':
            stages = self.xml_obj.sleep_stages_obj.sleep_stages_NremRem
        elif hypnogram_style == 'N1_N2_N3_REM_W':
            stages = self.xml_obj.sleep_stages_obj.sleep_stages_N3
        stage_information = [epoch, stages]

        # Define Stage Colors
        stage_colors = self.xml_obj.sleep_stages_obj.default_stage_colors

        # Check if spectrogram is avaialble
        for i, spec_obj in enumerate(self.result_spectrogram_obj_list):
            p_widget = self.results_graphic_views[i]
            spec_obj.plot_band_summary(parent_widget=p_widget,
                                       analysis_range=analysis_range, spectral_bands=spectral_bands,
                                       stage_information=stage_information, stage_colors=stage_colors,
                                       spectral_titles=spectral_titles)

        # Turn Off X axis
        set_layout_visible(self.ui.horizontalLayout_time_axis, False)

        # Turn off button
        self.ui.pushButton_control_spectrum_average.setEnabled(True)

    # Save
    def save_spectral_results(self):
        """
            Save spectral results and parameters to files.
            Creates an XML file with settings/parameters and CSV files for each signal.
            """

        # Get EDF file name base
        edf_base_name = os.path.basename(self.edf_obj.file_name)
        edf_base_name, _ = os.path.splitext(edf_base_name)
        default_folder = os.path.abspath(self.edf_obj.file_name)

        # Launch dialog box
        dialog = SpectralFolderDialog(self, default_folder=default_folder)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_folder = dialog.get_selected_folder()
            logger.info(f"Selected folder: {selected_folder}")
        else:
            logger.info("Spectral results dialog cancelled")
            return

        # Turn on busy cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        # Create output directory if it doesn't exist
        output_dir = selected_folder
        os.makedirs(output_dir, exist_ok=True)

        # Get settings and parameters
        setting_description_dict, setting_signal_dict, setting_plotting_dict, setting_filter_dict = self.get_settings()
        noise_param_dict, taper_param_dict, band_params_dict, analysis_param_dict = self.get_parameters()

        # Generate default filename with timestamp (not using timestamp during development)
        output_suffix = self.ui.plainTextEdit_setting_output_suffix.toPlainText()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{edf_base_name}_{output_suffix}"

        # Collect signal information for XML
        signal_info_list = []

        # Get stage information
        epoch_width = self.xml_obj.epochLength
        n_stages = self.xml_obj.sleep_stages_obj.sleep_stages_N3
        nrem_stage = self.xml_obj.sleep_stages_obj.sleep_stages_NremRem

        # Get sleep start and end
        sleep_stage_time_dict = self.xml_obj.sleep_stages_obj.return_stage_time_dict()
        first_sleep_time = sleep_stage_time_dict['sleep_start_time']
        last_sleep_time = sleep_stage_time_dict['sleep_end_time']

        noise_fn_dict = {}
        stage_mask_fn_dict = {}
        analysis_range_fn_dict = {}
        band_freq_fn_dict = {}
        for idx, input_output_noise_obj in enumerate(zip(self.input_signal_obj_list,
                                                   self.result_spectrogram_obj_list,
                                                   self.noise_mask_list)):
            in_signal_obj, multi_taper_obj, noise_mask_dict = input_output_noise_obj

            # Signal Information
            signal_label = in_signal_obj.signal_label
            signal_units = in_signal_obj.signal_units
            signal_sampling_time = in_signal_obj.signal_sampling_time

            # Spectrogram Information
            mt_spectrogram = multi_taper_obj.mt_spectrogram
            stimes = multi_taper_obj.stimes
            sfreqs = multi_taper_obj.sfreqs

            # Create CSV filename for this signal
            safe_label = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in signal_label)
            csv_filename = f"{base_filename}_{str(idx+1).zfill(3)}_{safe_label}.csv"
            csv_filepath = os.path.join(output_dir, csv_filename)

            # Save spectrogram data to CSV (transpose: times as rows, frequencies as columns)
            with open(csv_filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Write header: 'Time' followed by frequency values
                header = ['Time'] + [f'{freq:.4f}' for freq in sfreqs]
                writer.writerow(header)

                # Write data rows: each row is [time, power_at_freq1, power_at_freq2, ...]
                # mt_spectrogram shape is typically (frequencies, times), so we transpose
                spectrogram_transposed = mt_spectrogram.T  # Now shape is (times, frequencies)

                for time_idx, time_val in enumerate(stimes):
                    row = [f'{time_val:.6f}'] + [f'{val:.6e}' for val in spectrogram_transposed[time_idx]]
                    writer.writerow(row)

            # Store signal info for XML
            signal_info_list.append({
                'index': idx,
                'label': signal_label,
                'units': signal_units,
                'sampling_time': signal_sampling_time,
                'csv_file': csv_filename,
                'num_times': len(stimes),
                'num_freqs': len(sfreqs),
                'time_range': (float(stimes[0]), float(stimes[-1])),
                'freq_range': (float(sfreqs[0]), float(sfreqs[-1]))
            })

            # Write stage masks
            stage_fn = f'{edf_base_name}_{output_suffix}_{str(idx+1).zfill(3)}_{safe_label}_stage_masks'
            stage_n_mask_list, stage_n_mask_label_list = multi_taper_obj.generate_stage_masks(epoch_width, n_stages, stimes)
            stage_mask_dict = make_dict_from_list(stage_n_mask_label_list, stage_n_mask_list)
            stage_nrem__mask_list, stage_nrem_mask_label_list = multi_taper_obj.generate_stage_masks(epoch_width, nrem_stage, stimes)
            stage_mask_dict = make_dict_from_list(stage_nrem_mask_label_list, stage_nrem__mask_list, exisiting_dict=stage_mask_dict)
            stage_fn = self.save_stage_masks(stage_mask_dict, stimes, output_dir, base_filename=stage_fn)
            stage_mask_fn_dict[safe_label] = stage_fn

            # Write analysis range masks
            analysis_fn = f'{edf_base_name}_{output_suffix}_{str(idx + 1).zfill(3)}_{safe_label}_analysis_range_masks'
            analysis_range_mask_dict = multi_taper_obj.generate_analysis_range_masks(first_sleep_time, last_sleep_time, stimes)
            analysis_fn = self.save_analysis_range_masks(analysis_range_mask_dict, stimes, output_dir, base_filename=analysis_fn)
            analysis_range_fn_dict[safe_label] = analysis_fn

            # Write noise masks
            noise_fn = f'{edf_base_name}_{output_suffix}_{str(idx + 1).zfill(3)}_{safe_label}_noise_masks'
            noise_fn = self.save_noise_masks(noise_mask_dict, stimes, output_dir, base_filename=noise_fn)
            noise_fn_dict[signal_label] = noise_fn

            # Write band frequency masks
            band_freq_fn = f'{edf_base_name}_{output_suffix}_{str(idx + 1).zfill(3)}_{safe_label}_band_freq_masks'
            band_freq_mask_dict = multi_taper_obj.generate_band_freq_masks(band_params_dict, sfreqs)
            band_freq_fn = self.save_freq_band_masks(band_freq_mask_dict, sfreqs, output_dir, base_filename=band_freq_fn)
            band_freq_fn_dict[signal_label] = band_freq_fn

        # Create XML file with settings and parameters
        xml_filename = f"{base_filename}_{str(0).zfill(3)}_config.xml"
        xml_filepath = os.path.join(output_dir, xml_filename)

        root = ET.Element('SpectralAnalysis')
        root.set('timestamp', timestamp)

        # Add Settings section
        settings_elem = ET.SubElement(root, 'Settings')

        # Description settings
        desc_elem = ET.SubElement(settings_elem, 'Description')
        for key, value in setting_description_dict.items():
            item = ET.SubElement(desc_elem, key)
            item.text = str(value)

        # Signal settings
        signal_elem = ET.SubElement(settings_elem, 'Signal')
        for key, value in setting_signal_dict.items():
            item = ET.SubElement(signal_elem, key)
            item.text = str(value)

        # Plotting settings
        plot_elem = ET.SubElement(settings_elem, 'Plotting')
        for key, value in setting_plotting_dict.items():
            item = ET.SubElement(plot_elem, key)
            item.text = str(value)

        # Filter settings
        filter_elem = ET.SubElement(settings_elem, 'Filter')
        for key, value in setting_filter_dict.items():
            item = ET.SubElement(filter_elem, key)
            item.text = str(value)

        # Add Parameters section
        params_elem = ET.SubElement(root, 'Parameters')

        # Noise parameters
        noise_elem = ET.SubElement(params_elem, 'Noise')
        for key, value in noise_param_dict.items():
            item = ET.SubElement(noise_elem, key)
            item.text = str(value)

        # Taper parameters
        taper_elem = ET.SubElement(params_elem, 'Taper')
        for key, value in taper_param_dict.items():
            item = ET.SubElement(taper_elem, key)
            item.text = str(value)

        # Band parameters
        band_elem = ET.SubElement(params_elem, 'Band')
        for key, value in band_params_dict.items():
            item = ET.SubElement(band_elem, key)
            item.text = str(value)

        # Analysis parameters
        analysis_elem = ET.SubElement(params_elem, 'Analysis')
        for key, value in analysis_param_dict.items():
            item = ET.SubElement(analysis_elem, key)
            item.text = str(value)

        # Add Signals section
        signals_elem = ET.SubElement(root, 'Signals')
        for sig_info in signal_info_list:
            sig_elem = ET.SubElement(signals_elem, 'Signal')
            sig_elem.set('index', str(sig_info['index']))

            ET.SubElement(sig_elem, 'Label').text = sig_info['label']
            ET.SubElement(sig_elem, 'Units').text = sig_info['units']
            ET.SubElement(sig_elem, 'SamplingTime').text = str(sig_info['sampling_time'])
            ET.SubElement(sig_elem, 'CSVFile').text = sig_info['csv_file']
            ET.SubElement(sig_elem, 'NumTimePoints').text = str(sig_info['num_times'])
            ET.SubElement(sig_elem, 'NumFrequencies').text = str(sig_info['num_freqs'])

            time_range_elem = ET.SubElement(sig_elem, 'TimeRange')
            time_range_elem.set('start', str(sig_info['time_range'][0]))
            time_range_elem.set('end', str(sig_info['time_range'][1]))

            freq_range_elem = ET.SubElement(sig_elem, 'FrequencyRange')
            freq_range_elem.set('start', str(sig_info['freq_range'][0]))
            freq_range_elem.set('end', str(sig_info['freq_range'][1]))

        # Stage Mask Filename
        mask_elem = ET.SubElement(root, 'Masks')
        stage_elem = ET.SubElement(mask_elem, 'Stage_Mask_Files')
        for key, value in stage_mask_fn_dict.items():
            item = ET.SubElement(stage_elem, make_xml_safe_tag(key))
            item.text = str(value)

        # Noise Mask Filename
        noise_elem = ET.SubElement(mask_elem, 'Noise_Mask_Files')
        for key, value in noise_fn_dict.items():
            item = ET.SubElement(noise_elem, make_xml_safe_tag(key))
            item.text = str(value)


        # Analysis Range Mask Filename
        analysis_range_elem = ET.SubElement(mask_elem, 'Analysis_Range_Mask_Files')
        for key, value in analysis_range_fn_dict.items():
            item = ET.SubElement(analysis_range_elem, make_xml_safe_tag(key))
            item.text = str(value)



        # Write XML file with pretty formatting
        tree = ET.ElementTree(root)
        ET.indent(tree, space='  ')
        tree.write(xml_filepath, encoding='utf-8', xml_declaration=True)

        logger.info(f"Spectral results saved to: {output_dir}")
        logger.info(f"Configuration file: {xml_filename}")
        logger.info(f"CSV files: {len(signal_info_list)} signal(s) saved")

        # Turn off busy cursor
        QApplication.restoreOverrideCursor()

        return
    @staticmethod
    def save_analysis_range_masks(analysis_range_masks, stimes, save_dir, base_filename='range_masks'):
        """
        Save noise detection results (time-resolution masks) to a CSV file.

        Args:
            noise_mask (dict): Output from simple_noise_detection().
            stimes (np.ndarray): Time vector (same length as time masks).
            save_dir (str): Directory where CSV will be saved.
            base_filename (str): Base name for the output CSV file (default 'noise_masks').

        Returns:
            str: Full path to the saved CSV file.
        """
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{base_filename}.csv")

        # Validate lengths
        for key in analysis_range_masks.keys():
            if len(analysis_range_masks[key]) != len(stimes):
                raise ValueError(f"Mask '{key}' length ({len(noise_mask[key])}) "
                                 f"does not match time vector ({len(stimes)}).")

        # Construct DataFrame
        df = pd.DataFrame({'time_sec': stimes})
        for key in analysis_range_masks.keys():
            df[key] = analysis_range_masks[key].astype(int)  # Save as 1 (True) / 0 (False)

        # Save CSV
        df.to_csv(save_path, index=False)
        logger.info(f"Saved noise mask CSV to {save_path}")

        return save_path
    @staticmethod
    def save_stage_masks(stage_mask_dict, stimes, save_dir, base_filename='stage_masks'):
        tuple[list[np.ndarray], list[str]]
        """
                Save sstge masks (time-resolution masks) to a CSV file.

                Args:
                    noise_mask (tuple[list[np.ndarray]): Stage binary mask for each stage label.
                    stage_label_list (list[str]): Stage labels
                    stimes (np.ndarray): Time vector (same length as time masks).
                    save_dir (str): Directory where CSV will be saved.
                    base_filename (str): Base name for the output CSV file (default 'noise_masks').

                Returns:
                    str: Full path to the saved CSV file.
                """

        # Create file
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{base_filename}.csv")

        # Validate lengths
        for key in stage_mask_dict.keys():
            if len(stage_mask_dict[key]) != len(stimes):
                raise ValueError(f"Mask '{key}' length ({len(stage_mask_dict[key])}) "
                                 f"does not match time vector ({len(stimes)}).")

        # Construct DataFrame
        df = pd.DataFrame({'time_sec': stimes})
        for key in stage_mask_dict.keys():
            df[key] = stage_mask_dict[key].astype(int)  # Save as 1 (True) / 0 (False)

        # Save CSV
        df.to_csv(save_path, index=False)
        logger.info(f"Saved stage mask CSV to {save_path}")

        return save_path
    @staticmethod
    def save_noise_masks(noise_mask, stimes, save_dir, base_filename='noise_masks'):
        """
        Save noise detection results (time-resolution masks) to a CSV file.

        Args:
            noise_mask (dict): Output from simple_noise_detection().
            stimes (np.ndarray): Time vector (same length as time masks).
            save_dir (str): Directory where CSV will be saved.
            base_filename (str): Base name for the output CSV file (default 'noise_masks').

        Returns:
            str: Full path to the saved CSV file.
        """
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{base_filename}.csv")

        # Select only time-resolution keys (same length as stimes)
        time_mask_keys = [k for k in noise_mask.keys() if k.endswith('_time_mask')]

        # Validate lengths
        for key in time_mask_keys:
            if len(noise_mask[key]) != len(stimes):
                raise ValueError(f"Mask '{key}' length ({len(noise_mask[key])}) "
                                 f"does not match time vector ({len(stimes)}).")

        # Construct DataFrame
        df = pd.DataFrame({'time_sec': stimes})
        for key in time_mask_keys:
            df[key] = noise_mask[key].astype(int)  # Save as 1 (True) / 0 (False)

        # Save CSV
        df.to_csv(save_path, index=False)
        logger.info(f"Saved noise mask CSV to {save_path}")

        return save_path
    @staticmethod
    def save_freq_band_masks(band_mask, sfreq, save_dir, base_filename='freq_masks'):
        """
        Save noise detection results (time-resolution masks) to a CSV file.

        Args:
            noise_mask (dict): Output from simple_noise_detection().
            sfreq (np.ndarray): Frequency vector in Hz (same length as time masks).
            save_dir (str): Directory where CSV will be saved.
            base_filename (str): Base name for the output CSV file (default 'noise_masks').

        Returns:
            str: Full path to the saved CSV file.
        """
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{base_filename}.csv")

        # Validate lengths
        for key in band_mask.keys():
            if len(band_mask[key]) != len(sfreq):
                raise ValueError(f"Mask '{key}' length ({len(band_mask[key])}) "
                                 f"does not match time vector ({len(sfreq)}).")

        # Construct DataFrame
        df = pd.DataFrame({'Frequency(s)': sfreq})
        for key in band_mask:
            df[key] = band_mask[key].astype(int)  # Save as 1 (True) / 0 (False)

        # Save CSV
        df.to_csv(save_path, index=False)
        logger.info(f"Saved noise mask CSV to {save_path}")

        return save_path
