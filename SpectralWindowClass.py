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

        # Set up window control
        self.setup_control_bar()
        self.setup_menu()

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
