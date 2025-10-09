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
            print(f"  - Widget: {widget.objectName()}")
            widget.setVisible(visible)

        # Check if the item is a nested layout
        nested_layout = item.layout()
        if nested_layout:
            # Recursively process the nested layout
            set_layout_visible(nested_layout, visible)


def traverse_layout_for_spacers(layout, spacer_sizes=None):
    """
    Recursively traverses a PySide6 QLayout to identify spacers and record their sizes.

    Args:
        layout: QLayout object to traverse (QVBoxLayout, QHBoxLayout, QGridLayout, etc.)
        spacer_sizes: dict - accumulator for spacer sizes (used in recursion)

    Returns:
        dict: Dictionary mapping spacer object names to their sizes
              Format: {spacer_name: {'width': int, 'height': int}}
    """
    if spacer_sizes is None:
        spacer_sizes = {}

    if layout is None:
        return spacer_sizes

    for i in range(layout.count()):
        item = layout.itemAt(i)

        if item is None:
            continue

        # Check if the item is a spacer
        spacer = item.spacerItem()
        if spacer:
            # Get spacer name from Qt Designer
            spacer_name = spacer.objectName()

            # Get spacer size hint
            size_hint = spacer.sizeHint()

            # Store spacer information
            spacer_sizes[spacer_name] = {
                'width': size_hint.width(),
                'height': size_hint.height(),
            }

            print(f"  - Spacer: {spacer_name} (size: {size_hint.width()}x{size_hint.height()})")

        # Check if the item is a widget (skip it, but check for nested layouts in the widget)
        widget = item.widget()
        if widget:
            # Some widgets contain their own layouts
            widget_layout = widget.layout()
            if widget_layout:
                traverse_layout_for_spacers(widget_layout, spacer_sizes)

        # Check if the item is a nested layout
        nested_layout = item.layout()
        if nested_layout:
            # Recursively process the nested layout
            traverse_layout_for_spacers(nested_layout, spacer_sizes)

    return spacer_sizes
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
        self.setWindowTitle("Signal Viewer")

        # Set up window control
        self.control_bar_setup()

    # Setup
    def control_bar_setup(self):
        # Identify spacers
        layout_spacers_parameters = traverse_layout_for_spacers(self.ui.horizontalLayout_parameters)
        print(layout_spacers_parameters)

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
