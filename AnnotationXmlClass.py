"""
Annotation XML Class provides access to information stored in an XML annotation file

Annotation XML Class

Overview:
Annotation class is a utility for accessing information stored within an XML file which is the
standard for the National Sleeep Research Resource (NSRR). The file is commonly used to access sleep
stages. In addition, the file contains the epoch length, stepped channels, scored event settings,
scored events, and montage. The class provides comprehensive access to the information stored in the
file.

In order to support multiple applications, the class supports setting the XML file, checking the
file schema, loading the file, summarizing the file, exporting the sleep stages, exporting scored
events, and exporting a summary. Executing the class in verbose modes echos summaries to the command
line.

The expectation is that this python of an annotation loader will provide strong access
for python developers and will complement the NSRR code base, Luna and available utilities, primarily
written in C.

Constructor:
AnnotationXml(self, annotationFile:str, verbose: bool=True)
     annotationFile: A text string that includes the path and file name to an XML annotation file
     verbose:        Facilitates writing summary functions to the command line

Author:
Dennis A. Dean, II, PhD
Sleep Science

Completion Date: June 20, 2025

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
import xml.etree.ElementTree as ET
import os
import pandas as pd
import json
import csv
import logging
import traceback
import datetime
from typing import List, Dict, Any, Optional
from lxml import etree

# Plotting support
import numpy as np

# Required for plotting
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
plt.ioff()

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# User Interface
from PySide6.QtWidgets import QSizePolicy, QApplication
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                                QPushButton, QScrollArea, QWidget, QFrame)
from PySide6.QtCore import Qt

# To Do List
# TODO: Add N3 collapse summary to json export

# Set up a module-level logger
logger = logging.getLogger(__name__)

#Utilities
def column_print(string_list:list, number_of_columns: int = 2, space: int = 5):
    """
    Utility printing XML component summaries to the command line

    :param string_list: A list of strings that describe information stored in the annotation file
    :param number_of_columns: The number of columns to use when printing the list
    :param space: The space between columns
    :return: None is returned
    """
    # Pad strings to the same length and calculate the number of rows to print
    width = max([len(string) for string in string_list])+space
    string_list = [string.ljust(width) for string in string_list]
    string_list.sort()
    num_complete_rows = len(string_list)//number_of_columns
    remaining_entries = len(string_list)%number_of_columns

    # Use logger utility to write rows to the command line
    for r in range(num_complete_rows):
        start = r * number_of_columns
        end   = start + number_of_columns
        logger.info(" ".join(string_list[start:end]))
    if remaining_entries > 0:
        logger.info(" ".join(string_list[num_complete_rows * number_of_columns:]))
def convert_dict_to_summary_string(key_value_dict: dict)->str:
    """
    Convert key-value pairs into a single line string

    :param key_value_dict:
    :return: key_value_str:
    """
    dict_list = []
    dict_keys = list(key_value_dict.keys())
    dict_keys.sort()
    for key in dict_keys:
        dict_list.append(f"{key}: {key_value_dict[key]}")
    dict_str = ',  '.join(dict_list)
    return dict_str
def get_unique_entries(input_list:list)->list:
    """
    Return unique entries in a list

    :param input_list:
    :return:
    """
    # Returns unique values in a list as a list. Wrote to reduce the number of external dependencies
    output = []
    for x in input_list:
        if x not in output:
            output.append(x)
    output.sort()
    return output
def generate_timestamped_filename(prefix: str, ext: str = ".csv", output_dir: str = "") -> str:
    """Add a time stamp to a generated file

    prefix: str: File name
    ext: str = File type string
    output_dir: str = Output directory if set
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}{ext}"
    return os.path.join(output_dir, filename) if output_dir else filename
def generate_filename(prefix: str, ext: str = ".csv", output_dir: str = "") -> str:
    """Add a time stamp to a generated file

    prefix: str: File name
    ext: str = File type string
    output_dir: str = Output directory if set
    """
    filename = f"{prefix}{ext}"
    return os.path.join(output_dir, filename) if output_dir else filename

# Sleep annotation Dialog Boxes
class AnnotationLegendDialog(QDialog):
    """
    Pop-up dialog that displays annotation names with their corresponding colors.
    """
    def __init__(self, color_map, parent=None):
        """
        Initialize the dialog.

        Args:
            color_map (dict): Dictionary mapping annotation names to color strings
            parent: Parent widget
        """
        super().__init__(parent)
        self.color_map = color_map
        self.setup_ui()
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Annotation Legend")
        self.setModal(True)  # Make it modal
        self.resize(300, 400)  # Default size

        # Main layout
        main_layout = QVBoxLayout(self)

        # Scroll area for legend items
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Widget to hold legend items
        legend_widget = QWidget()
        legend_layout = QVBoxLayout(legend_widget)
        legend_layout.setSpacing(5)
        legend_layout.setContentsMargins(10, 10, 10, 10)

        # Create legend items
        for annotation_name, color in sorted(self.color_map.items()):
            legend_item = self.create_legend_item(annotation_name, color)
            legend_layout.addWidget(legend_item)

        # Add stretch to push items to top
        legend_layout.addStretch()

        scroll_area.setWidget(legend_widget)
        main_layout.addWidget(scroll_area)

        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        close_button = QPushButton("Close")
        close_button.setMinimumWidth(80)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        main_layout.addLayout(button_layout)
    @staticmethod
    def create_legend_item(annotation_name, color):
        """
        Create a legend item with color box and label.

        Args:
            annotation_name (str): Name of the annotation
            color (str): Color hex string

        Returns:
            QWidget: Widget containing the legend item
        """
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(5, 2, 5, 2)
        item_layout.setSpacing(10)

        # Color box
        color_box = QFrame()
        color_box.setFixedSize(20, 15)
        color_box.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border: 1px solid #666666;
                border-radius: 2px;
            }}
        """)

        # Annotation name label
        name_label = QLabel(annotation_name)
        name_label.setStyleSheet("QLabel { color: black; }")

        # Add to layout
        item_layout.addWidget(color_box)
        item_layout.addWidget(name_label)
        item_layout.addStretch()  # Push everything to the left

        # Add hover effect
        item_widget.setStyleSheet("""
            QWidget:hover {
                background-color: #f0f0f0;
                border-radius: 3px;
            }
        """)

        return item_widget
class StageColorDialog(QDialog):
    """
        A dialog window for displaying sleep stage colors.

        This dialog presents a list of sleep stages with their associated colors
        as small swatches. It is primarily intended for visual reference and
        does not allow editing. Colors are pulled from the `default_stage_colors`
        attribute of the `owner` object provided at initialization.

        If no stage colors are defined, a message is displayed instead of the list.

        Parameters
        ----------
        owner : object
            An object that defines a `default_stage_colors` attribute, which is
            expected to be a dictionary mapping stage names (str) to color values
            in hex format (e.g., "#FF0000").
        parent : QWidget, optional
            The parent widget. Defaults to None.

        UI Elements
        -----------
        - Stage label: Displays the name of each sleep stage.
        - Color swatch: A small rectangular preview of the associated color.
        - Close button: Closes the dialog when clicked.

        Notes
        -----
        - The dialog is modal and blocks interaction with the parent window
          until closed.
        - This class is read-only; it does not allow editing or reassigning colors.

        """
    def __init__(self, owner: Any, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)  # parent must be QWidget or None

        self.setWindowTitle("Sleep Stage Colors")
        self.setModal(True)
        self.resize(320, 300)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Pull colors directly from owner
        stage_colors = getattr(owner, "default_stage_colors", {})

        if not stage_colors:
            msg = QLabel("No stage colors defined.")
            layout.addWidget(msg, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            for stage, hex_color in stage_colors.items():
                row = QHBoxLayout()

                label = QLabel(stage)
                label.setMinimumWidth(80)

                swatch = QLabel()
                swatch.setFixedSize(40, 20)
                swatch.setStyleSheet(
                    f"background-color: {hex_color}; "
                    "border: 1px solid #444; border-radius: 3px;"
                )

                row.addWidget(label)
                row.addWidget(swatch)
                row.addStretch()
                layout.addLayout(row)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

# Sleep annotation classes
class SleepStages:
    """
        Container class for handling sleep stage representations, summaries, and metadata.

        This class provides multiple mappings and derived representations of sleep stages
        from numeric values to text labels, NREM/REM categories, and collapsed N3/N4
        groupings. It also computes useful recording-level metadata such as duration,
        number of epochs, time indices, and label sets for plotting or summarization.

        The class is designed to be flexible with stage definitions by allowing
        dictionaries for different mappings to be passed in or overridden.

        Parameters
        ----------
        epoch : int
            Epoch length in seconds (e.g., 30s, 20s).
        num_stages : list[int]
            A list of numeric stage values representing the hypnogram sequence.
        num_stage_to_num_dict : Dict[int, int], optional
            Mapping of stage index to itself (default: identity mapping 0–5).
        num_stage_to_text_dict : Dict[int, str], optional
            Mapping of numeric stage index to standard text labels (e.g., 0 → "W").
        num_stage_to_nremrem_dict : Dict[int, str], optional
            Mapping of numeric stage index to reduced NREM/REM categories.
        num_stage_to_text_n3_dict : Dict[int, str], optional
            Mapping of numeric stage index where N3 and N4 are collapsed.
        nremrem_to_num_stage_dict : Dict[str, int], optional
            Mapping from NREM/REM text labels back to numeric indices.
        num_stage_to_nremrem_reduced_dict : Dict[int, str], optional
            Reduced mapping of numeric stages to NREM/REM categories.
        num_stage_to_text_n3_reduced_dict : Dict[int, str], optional
            Reduced mapping of numeric stages to text labels with N3 collapsed.

        Attributes
        ----------
        sleep_epoch : int
            Epoch duration in seconds.
        num_stages : list[int]
            Original list of numeric stages.
        num_stage_n3 : list[int]
            Stage sequence with N3/N4 collapsed.
        recording_duration : float
            Total recording duration in hours.
        sleep_stages_text : list[str]
            Stage sequence converted to text labels (W, N1, N2, N3, N4, REM).
        sleep_stages_NremRem : list[str]
            Stage sequence converted to NREM/REM/W categories.
        sleep_stages_N3 : list[str]
            Stage sequence with N3 and N4 collapsed to a single stage.
        sleep_stages_NremRem_num : list[int]
            Stage sequence converted into numeric representation of NREM/REM.
        stage_num_sum_dict : dict
            Summary counts of stages by numeric representation.
        stage_text_sum_dict : dict
            Summary counts of stages by text labels.
        stage_remnrem_sum_dict : dict
            Summary counts of stages by NREM/REM categories.
        number_of_epochs : int
            Number of epochs in the recording.
        recording_duration_hr : float
            Recording duration in hours.
        time_seconds : list[float]
            List of time indices in seconds for each epoch.
        max_time_sec : int
            Total recording length in seconds.
        numeric_labels : str
            Underscore-joined string of numeric labels present.
        text_labels : str
            Underscore-joined string of text labels present.
        nremrem_labels : str
            Underscore-joined string of NREM/REM labels present.
        text_n3_labels : str
            Underscore-joined string of text labels with N3 collapsed.
        output_dir : str
            Directory path for saving outputs (defaults to current working directory).
        current_hypnogram_ax : Any
            Placeholder for matplotlib Axes object for hypnogram plotting.
        current_hypnogram_fig : Any
            Placeholder for matplotlib Figure object for hypnogram plotting.
        current_hypnogram_canvas : Any
            Placeholder for GUI canvas (if used in PySide6/Qt).
        hypnogram_double_click_callback : Optional[Callable]
            Callback for double-click events on the hypnogram.
        default_stage_colors : dict
            Dictionary mapping stage names to default hex color codes for plotting.
        hypnogram_connection : list
            List of event connection IDs for hypnogram plotting.

        Notes
        -----
        - Provides multiple parallel representations of the hypnogram for analysis.
        - Designed to support plotting, statistical summaries, and interactive GUIs.
        - Default mappings follow AASM guidelines but can be overridden.

        Example
        -------
        >>> stages = SleepStages(epoch=30, num_stages=[0,1,2,2,3,5,0])
        >>> stages.recording_duration_hr
        0.058333...
        >>> stages.sleep_stages_text
        ['W', 'N1', 'N2', 'N2', 'N3', 'REM', 'W']
        """
    def __init__(self,epoch: int, num_stages: List[int],
                 num_stage_to_num_dict: Dict[int, int] | None = None,
                 num_stage_to_text_dict: Dict[int, str] | None = None,
                 num_stage_to_nremrem_dict: Dict[int, str] | None = None,
                 num_stage_to_text_n3_dict: Dict[int, str] | None = None,
                 nremrem_to_num_stage_dict: Dict[str, int] | None = None,
                 num_stage_to_nremrem_reduced_dict: Dict[int, str] | None = None,
                 num_stage_to_text_n3_reduced_dict: Dict[int, str] | None = None) -> None:

        # Set defaults if None
        if num_stage_to_num_dict is None:
            num_stage_to_num_dict = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
        if num_stage_to_text_dict is None:
            num_stage_to_text_dict = {0: "W", 1: "N1", 2: "N2", 3: "N3", 4: "N4", 5: "REM"}
        if num_stage_to_nremrem_dict is None:
            num_stage_to_nremrem_dict = {0: "W", 1: "NREM", 2: "NREM", 3: "NREM", 4: "NREM", 5: "REM"}
        if num_stage_to_text_n3_dict is None:
            num_stage_to_text_n3_dict = {0: "W", 1: "N1", 2: "N2", 3: "N3", 4: "N3", 5: "REM"}
        if nremrem_to_num_stage_dict is None:
            nremrem_to_num_stage_dict = {"W": 0, "NREM": 1, "REM": 2}
        if num_stage_to_nremrem_reduced_dict is None:
            num_stage_to_nremrem_reduced_dict = {0: "W", 1: "NREM", 2: "REM"}
        if num_stage_to_text_n3_reduced_dict is None:
            num_stage_to_text_n3_reduced_dict = {0: "W", 1: "N1", 2: "N2", 3: "N3", 4: "REM"}

        # Update log
        logging.info(f'Initializing SleepStagesClass: epoch{epoch}, num of stages {len(num_stages)}')

        # Set inputs and conversion
        self.sleep_epoch                       = epoch
        self.num_stages                        = num_stages

        self.num_stage_to_num_dict             = num_stage_to_num_dict
        self.num_stage_to_text_dict            = num_stage_to_text_dict
        self.num_stage_to_nremrem_dict         = num_stage_to_nremrem_dict
        self.nremrem_to_num_stage_dict         = nremrem_to_num_stage_dict
        self.num_stage_to_nremrem_reduced_dict = num_stage_to_nremrem_reduced_dict
        self.num_stage_to_text_n3_dict         = num_stage_to_text_n3_dict
        self.num_stage_to_text_n3_reduced_dict = num_stage_to_text_n3_reduced_dict

        # Convert num stages to
        self.collapse_n3_n4_dict   = {0:0, 1:1,   2:2,   3:3,   4:3,  5:4}
        self.num_stage_n3          = [self.collapse_n3_n4_dict[i] for i in num_stages]


        # Compute recording duration
        self.recording_duration        = (self.sleep_epoch * len(self.num_stages))/3600

        # Convert numeric sleep stages to text
        self.sleep_stages_text          = self.convert_num_stages_to_text(num_stages, num_stage_to_text_dict)
        self.sleep_stages_NremRem       = self.convert_num_stages_to_text(num_stages, num_stage_to_nremrem_dict)
        self.sleep_stages_N3            = self.convert_num_stages_to_text(num_stages, num_stage_to_text_n3_dict)

        # Create a new numeric representation for nremrem
        self.sleep_stages_NremRem_num   = self.convert_num_stages_to_text(self.sleep_stages_NremRem , nremrem_to_num_stage_dict)

        # Create sleep stage summaries by representation
        self.stage_num_sum_dict      = self.summarize_sleep_stages(self.num_stages, num_stage_to_num_dict)
        self.stage_text_sum_dict     = self.summarize_sleep_stages(self.sleep_stages_text, self.num_stage_to_text_dict)
        self.stage_remnrem_sum_dict  = self.summarize_sleep_stages(self.sleep_stages_NremRem,
                                                                   self.num_stage_to_nremrem_dict)
        # Time and duration related variabls
        self.number_of_epochs        = len(num_stages)
        self.recording_duration_hr   = self.number_of_epochs * self.sleep_epoch / 60 / 60
        self.time_seconds            = [float(i * epoch) for i in range(len(num_stages))]
        self.max_time_sec            = self.number_of_epochs * self.sleep_epoch

        # Labels - will make self describing in another pass
        self.numeric_labels  = list(num_stage_to_text_dict.keys())
        self.numeric_labels.sort()
        self.text_labels     = get_unique_entries([num_stage_to_text_dict[i] for i in self.numeric_labels])
        self.nremrem_labels  = get_unique_entries([num_stage_to_nremrem_dict[i] for i in self.numeric_labels])
        self.text_n3_labels  = get_unique_entries([num_stage_to_text_n3_dict[i] for i in self.numeric_labels])
        self.numeric_labels  = get_unique_entries([str(num_stage_to_num_dict[i]) for i in self.numeric_labels])

        # Create labels to assist with histogram plotting
        self.numeric_labels  = "_".join(self.numeric_labels)
        self.text_labels     = "_".join(self.text_labels)
        self.nremrem_labels  = "_".join(self.nremrem_labels)
        self.text_n3_labels  = "_".join(self.text_n3_labels)

        # Output Control
        self.output_dir = os.getcwd()

        # Store hypnogram plotting information
        self.current_hypnogram_ax = None
        self.current_hypnogram_fig = None
        self.current_hypnogram_canvas = None
        self.hypnogram_double_click_callback = None

        # Default colors for stages
        self.default_stage_colors = {
            'W': '#FFE4B5',       # Light orange
            'Wake': '#FFE4B5',    # Light orange
            'REM': '#FFB6C1',     # Light pink
            'N1': '#D8BFD8',      # Thistle
            'N2': '#B0E0E6',      # Powder blue
            'N3': '#98FB98',      # Pale green
            'N4': '#3CB371',      # Medium sea green (darker than N3)
            'NREM': '#87CEEB',    # Sky blue
            'Artifact': '#FA8072' # Salmon
        }

        # Collect Connection IDS
        self.hypnogram_connection = []

    # Event Management
    def cleanup_events(self):
        """
            Disconnects all Matplotlib event handlers associated with the hypnogram figure.

            Iterates over all connection IDs stored in `self.hypnogram_connection` and attempts
            to disconnect them from the current hypnogram figure's canvas. Handles cases where
            the connection may already have been removed. After cleanup, the list of connections
            is cleared.

            Side effects:
                - Disconnects all existing hypnogram event handlers.
                - Clears `self.hypnogram_connection`.
                - Logs cleanup action.
            """
        for cid in self.hypnogram_connection:
            try:
                self.current_hypnogram_fig.canvas.mpl_disconnect(cid)
            except (ValueError, KeyError, AttributeError):
                pass  # In case connection is already gone
        self.hypnogram_connection.clear()

        logger.info(f'Sleep stages - clean up events')
    def setup_events(self):
        """
            Sets up Matplotlib event handlers for the hypnogram figure if not already connected.

            Prevents duplicate connections by checking whether `self.hypnogram_connection`
            already contains active connection IDs. If empty, attaches a handler for the
            'button_press_event' event, which is used to respond to double-clicks on the hypnogram.

            Side effects:
                - Adds a new Matplotlib connection ID to `self.hypnogram_connection`.
                - Logs setup action.
            """
        if self.hypnogram_connection:
            return  # Already setup

        # Reconnect spectrogram event handlers
        cid = self.current_hypnogram_fig.canvas.mpl_connect('button_press_event', self._on_hypnogram_double_click)
        self.hypnogram_connection.append(cid)

        logger.info(f'Sleep stages - setup up events')

    # Utilities
    def set_output_dir(self, output_dir: str):
        """Set the directory to use for output files."""
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
    @staticmethod
    def convert_num_stages_to_text(stage_num_list: list[int], stage_dict: dict[int, str]) -> List[str]:
        """
        Generic function for converting numeric sleep stages to text with a dictionary. Dictionaries
        corresponding to NSRR values are preset (stage_text_sum_dict, stage_remnrem_sum_dict)

        :param stage_num_list:
        :param stage_dict:
        :return:
        """
        # Use dictionary to map numerical stages to text.
        stage_str_list = [stage_dict[x] for x in stage_num_list]
        return stage_str_list

    # Return values
    def return_sleep_stage_labels(self):
        """
                Return the available sleep stage label sets.

                Returns:
                    list:
                        A list containing multiple representations of sleep stage labels:
                        - self.numeric_labels: Numeric identifiers for sleep stages.
                        - self.text_labels: Text descriptions of sleep stages (e.g., "N1", "N2").
                        - self.nremrem_labels: Grouped NREM/REM stage labels.
                        - self.text_n3_labels: Text labels with explicit N3 stage handling.

                Notes:
                    These different label sets are used to provide flexibility when displaying
                    or exporting hypnogram data.
                """
        sleep_stages_labels = [self.numeric_labels, self.text_labels, self.nremrem_labels, self.text_n3_labels ]
        return sleep_stages_labels
    def return_sleep_stage_mappings(self):
        """
                Return the available sleep stage mapping dictionaries.

                Returns:
                    list:
                        A list containing mappings between numeric and textual stage representations:
                        - self.num_stage_to_text_dict: Maps numeric stage codes to text labels.
                        - self.num_stage_to_nremrem_dict: Maps numeric stage codes to NREM/REM groupings.

                Notes:
                    These mappings are typically used for translating sleep stages
                    between numeric and text-based representations in plots and summaries.
                """
        sleep_stages_labels = [self.num_stage_to_text_dict, self.num_stage_to_nremrem_dict ]
        return sleep_stages_labels
    def return_zeroed_sleep_stage_time_dictionary(self, start_epoch:int, epoch_end:int|None):
        """
        Convert sleep stages to time-based dictionary format with epochs zeroed to start_epoch.

        Creates a list of sleep stage dictionaries with time boundaries relative to the starting
        epoch. Each entry contains start_time, end_time, and stage text for a single epoch.

        :param start_epoch: Starting epoch number (inclusive)
        :param epoch_end: Ending epoch number (exclusive). If None, processes only start_epoch
        :return: List of dictionaries with 'start_time', 'end_time', and 'stage' keys
        """
        epoch_width     = self.sleep_epoch
        sleep_stages_N3 = self.sleep_stages_N3

        # print(f'start_epoch = {start_epoch}, epoch end = {epoch_end}, epoch_width = {epoch_width}, sleep_stages_N3 = {sleep_stages_N3}')

        # Determine the range of epochs to process
        if epoch_end is None:
            start_epoch = int(start_epoch)
            end_epoch   = int(start_epoch)
        else:
            start_epoch = int(start_epoch)
            end_epoch   = int(epoch_end)

        sleep_stages = []

        # Convert each epoch's text stage to time-based dictionary
        for current_epoch in range(start_epoch, end_epoch):
            # Check if we have data for this epoch
            #print(current_epoch)
            if current_epoch < len(sleep_stages_N3):
                stage_text = sleep_stages_N3[current_epoch]

                # Calculate time boundaries for this epoch
                start_time = (current_epoch - start_epoch) * epoch_width
                end_time = start_time + epoch_width

                # Create dictionary entry
                stage_dict = {
                    'start_time': start_time,
                    'end_time': end_time,
                    'stage': stage_text
                }

                sleep_stages.append(stage_dict)

        return sleep_stages

        # Summarize and export
    @staticmethod
    def summarize_sleep_stages(stage_list: list, stage_dict: dict[int, str]) -> dict[int | str, int | str]:
        """
        Generate a summary of sleep stage occurrences from a list of stages.

        Creates a dictionary containing the count of occurrences for each sleep stage
        defined in the stage dictionary. All stages from stage_dict are included in
        the output, even if they have zero occurrences in stage_list.

        Args:
            stage_list: List of sleep stage names (strings) to be counted.
            stage_dict: Dictionary mapping integer stage codes to their string names.
                   Example: {0: 'Wake', 1: 'REM', 2: 'Light', 3: 'Deep'}

        Returns:
            Dictionary with sleep stage names as keys and their occurrence counts as values.
            Example: {'Deep': 45, 'Light': 120, 'REM': 30, 'Wake': 15}
        """
        # Define Variables
        stage_summary = {}
        stage_keys = [stage_dict[x] for x in stage_dict.keys()]
        stage_keys.sort()

        # Create empty return dictionary to ensure all stages are included in retur
        for stage in stage_keys:
            stage_summary[stage] = 0

        # Count number of entries for each stage
        for stage in stage_keys:
            stage_summary[stage] = sum([x == stage for x in stage_list])
        return stage_summary
    def summary_scored_sleep_stages(self) -> None:
        """
        Log a comprehensive summary of scored sleep stages to the console.

        Outputs a formatted summary including the total number of stage entries,
        recording duration, and occurrence counts for each sleep stage across
        three different classification systems (numeric, text, and REM/NREM).
        Only logs output if sleep stages have been loaded and epoch length is defined.

        The summary includes:
        - Total number of sleep stage entries
        - Total recording duration in hours
        - Stage counts using numeric codes (e.g., 0, 1, 2, 3)
        - Stage counts using text labels (e.g., 'Wake', 'REM', 'Light', 'Deep')
        - Stage counts using REM/NREM classification

        Requires:
            self.num_stages: List of numeric sleep stage codes (must be non-empty)
            self.sleep_epoch: Duration of each sleep epoch in seconds (must not be None)
            self.stage_num_sum_dict: Dictionary with numeric stage summaries
            self.stage_text_sum_dict: Dictionary with text label stage summaries
            self.stage_remnrem_sum_dict: Dictionary with REM/NREM stage summaries

        Returns:
            None. Output is logged via the logger at INFO or ERROR level.

        Example output:
            Scored Sleep Stages:
            -------------------
            Number of Entries = 960, Recording Duration = 8.0 hr
            Sleep Stages: 0 = 45, 1 = 120, 2 = 585, 3 = 210
            Sleep Stages: Deep = 210, Light = 585, REM = 120, Wake = 45
            Sleep Stages: NREM = 795, REM = 120, Wake = 45
        """
        # Write if sleep stages are set
        if (self.num_stages != []) and (self.sleep_epoch is not None):
            # Write header
            logger.info('')
            logger.info('Scored Sleep Stages:')
            logger.info('-------------------')
            output_str = f'Number of Entries = {len(self.num_stages)}, '
            output_str += f'Recording Duration = {len(self.num_stages) * self.sleep_epoch / 60 / 60:.1f} hr'
            logger.info(output_str)

            # Write summaries for each dictionary stored in list
            summaries = [self.stage_num_sum_dict, self.stage_text_sum_dict, self.stage_remnrem_sum_dict]
            for summary in summaries:
                keys = list(summary.keys())
                keys.sort()
                output_str = f'Sleep Stages: '
                for i in range(len(keys) - 1):
                    output_str += f'{keys[i]} = {summary[keys[i]]}, '
                output_str += f'{keys[-1]} = {summary[keys[-1]]} '
                logger.info(output_str)
        else:
            logger.error('** Sleep Stages or Epoch Length Not Loaded **')
    def export_sleep_stages(self, filename: str, output_dir: str = None, time_stamped: bool = False) -> None:
        """
        Export sleep stage data to a tab-delimited text file in multiple classification formats.

        Creates a text file containing sleep stages in four different formats per line:
        numeric codes, text labels (N1-N4/Wake/REM), REM/NREM classification, and N3
        classification. Each epoch is written on a separate line with tab-separated values.

        The output file format is:
        <numeric>\t<text>\t<NREM/REM>\t<N3>

        Args:
            filename: Name of the output file (e.g., 'sleep_data.txt').
                    Will be placed in output_dir if specified.
            output_dir: Optional directory path for the output file. If provided,
                    updates self.output_dir and creates the directory if it doesn't exist.
                    Defaults to None (uses existing self.output_dir).
            time_stamped: If True, appends a timestamp to the filename to ensure uniqueness.
                     If False, uses the filename as-is (may overwrite existing files).
                     Defaults to False.

        Returns:
            None. Creates a text file at the specified location.

        Raises:
            Logs an error message if file writing fails due to permissions, disk space,
            or other I/O errors.

        Requires:
            self.num_stages: List of numeric sleep stage codes
            self.sleep_stages_text: List of text sleep stage labels
            self.sleep_stages_NremRem: List of NREM/REM classifications
            self.sleep_stages_N3: List of N3 classifications

        Example output file content:
            0\tWake\tWake\tWake
            2\tN2\tNREM\tNREM-Light
            3\tN3\tNREM\tNREM-Deep
            5\tREM\tREM\tREM

        """
        # Log status
        logging.info(f'Preparing to export sleep stages to {filename}')

        # Set output directory if provided
        if output_dir is not None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        ##### Changing behavior to work wit
        if time_stamped:
            filename = (os.path.join(self.output_dir, filename) or
                        generate_timestamped_filename("sleep_stages", ".txt", self.output_dir))
        else:
            filename = (os.path.join(self.output_dir, filename) or
                        generate_filename("sleep_stages", ".txt", self.output_dir))

        logging.info(f'Preparing to export sleep stages ({len(self.num_stages)})')

        # Export numeric ad text sleep stages
        try:
            logging.info(f'Opening file to write {len(self.num_stages)} sleep stages')
            with open(filename, 'w') as file:
                for i in range(len(self.num_stages)):
                    file.write(f"{self.num_stages[i]}\t{self.sleep_stages_text[i]}\t{self.sleep_stages_NremRem[i]}\t{self.sleep_stages_N3[i]}\n")
        except Exception as e:
            logger.error(f'*** Could not export sleep stages: {filename}, error: {e}')

    # Plotting functions
    def plot_hypnogram(self, parent_widget=None, stage_index = 0, hypnogram_marker:float|None=None,
                       double_click_callback=None, show_stage_colors = False):
        """
        Generate and display a hypnogram (sleep stage visualization) as a step plot.

        Creates a hypnogram showing sleep stages over time, either embedded in a Qt widget
        or as a standalone matplotlib figure. The plot features a white background,
        auto-scaling, horizontal grid lines at each stage level, and hourly time markers.
        Optionally displays colored background regions corresponding to each sleep stage.

        Args:
            parent_widget: Optional Qt widget to embed the plot. If provided, the hypnogram
                        is rendered as a FigureCanvas within this widget. If None, creates
                        a standalone matplotlib figure. Defaults to None.
            stage_index: Integer selecting which sleep stage classification to display:
                        - 0: Standard text labels (Wake, N1, N2, N3, REM)
                        - 1: NREM/REM reduced classification
                        - 2: N3-based reduced classification
                        Defaults to 0.
            hypnogram_marker: Optional x-axis position (in seconds) to display a vertical
                            purple marker line. Useful for indicating a specific time point
                            or playback position. Defaults to None (no marker).
            double_click_callback: Optional callback function to invoke when the hypnogram
                                is double-clicked. Receives matplotlib button_press_event
                                as argument. Defaults to None.
            show_stage_colors: If True, draws colored rectangles behind the hypnogram line
                            corresponding to each sleep stage's standard color. If False,
                            displays only the blue step plot line. Defaults to False.

        Returns:
            None. Updates instance attributes and displays the plot.

        Side Effects:
            - Sets self.current_hypnogram_ax to the matplotlib axes object
            - Sets self.current_hypnogram_fig to the matplotlib figure object
            - Sets self.current_hypnogram_canvas to the FigureCanvas (if parent_widget provided)
            - Sets self.hypnogram_double_click_callback to the provided callback
            - Appends connection ID to self.hypnogram_connection list
            - If parent_widget provided, replaces its layout contents with the new canvas

        Requires:
            self.num_stages: List of numeric sleep stage codes
            self.time_seconds: Array of time values in seconds
            self.sleep_epoch: Duration of each epoch in seconds
            self.recording_duration_hr: Total recording duration in hours
            self.default_stage_colors: Dictionary mapping stage labels to color codes
            self.num_stage_to_text_dict: Mapping from numeric to text stage labels
            self.num_stage_to_nremrem_reduced_dict: NREM/REM classification mapping
            self.num_stage_to_text_n3_reduced_dict: N3-based classification mapping
            self.sleep_stages_NremRem_num: Numeric NREM/REM stage array
            self.num_stage_n3: Numeric N3-based stage array

        Notes:
            - Y-axis is inverted (deeper sleep stages appear lower)
            - X-axis shows hourly markers (1h, 2h, 3h, etc.)
            - Blue step plot shows stage transitions
            - Purple vertical line marks hypnogram_marker position if provided
            - Grid lines appear at each sleep stage level
        """
        # if not hasattr(self, 'sleep_stages') or not hasattr(self, 'epoch_times'):
        #    raise ValueError("Missing required data: 'sleep_stages' and 'epoch_times'")

        # Set Plot defaults
        grid_color             = '#cccccc'  # light gray
        signal_color           = 'blue'
        y_pad_c                = 0.25
        label_fontsize         = 8
        xlabel_offset_dict     = {0:1, 1:0, 2:0.5}
        xlabel_offset          = xlabel_offset_dict[stage_index]
        # ylabel_offset          = 0.02*self.recording_duration_hr*3600
        grid_linewidth         = 0.8
        marker_line_width      = 0.8
        hypnogram_marker_color = 'purple'

        # Get stage color information
        # stage_color = self.default_stage_colors

        # Get hypnogram information
        stages    = self.num_stages
        times     = self.time_seconds
        time_axis = np.arange(len(stages)) * self.sleep_epoch

        # Check interface for histogram
        stage_mapping = [self.num_stage_to_text_dict, self.num_stage_to_nremrem_reduced_dict,
                         self.num_stage_to_text_n3_reduced_dict]
        stage_arrays  = [self.num_stages, self.sleep_stages_NremRem_num,
                         self.num_stage_n3 ]
        stage_map = stage_mapping[stage_index]
        stages    = stage_arrays[stage_index]

        # Stage to Y-axis mapping (traditional inverted)
        y_ticks   = list(stage_map.keys())
        y_ticks.sort()

        # Create figure and axis
        fig = Figure(figsize=(12, 2))
        ax = fig.add_subplot(111)
        ax.invert_yaxis()

        # Plot colored rectangles for each stage if enabled
        if show_stage_colors:
            stage_colors = self.default_stage_colors
            for i, stage_num in enumerate(stages):
                if i < len(stages) - 1:
                    # Get stage text label
                    stage_label = stage_map.get(stage_num, 'Unknown')
                    stage_color = stage_colors.get(stage_label, '#F0F0F0')  # Default light gray

                    # Calculate rectangle boundaries
                    x_start = time_axis[i]
                    x_end = time_axis[i + 1] if i + 1 < len(time_axis) else time_axis[i] + self.sleep_epoch
                    y_bottom = min(y_ticks) - 0.5
                    y_top = max(y_ticks) + 0.5

                    # Draw rectangle
                    ax.add_patch(plt.Rectangle((x_start, y_bottom),
                                               x_end - x_start,
                                               y_top - y_bottom,
                                               facecolor=stage_color,
                                               alpha=0.8,
                                               edgecolor='none',
                                               zorder=0))

        # Plot hypnogram
        plot_y_labels, plot_stages = self.reorder_labels_stages(stage_map, stages)
        ax.step(time_axis, plot_stages, color=signal_color, linewidth=1, zorder=2)

        ax.set_xlim(min(times), max(times)+self.sleep_epoch*2)
        ax.set_ylim(min(y_ticks) - 0.5, max(y_ticks) + 0.5)
        ax.tick_params(axis='both', labelsize=label_fontsize)

        fig.tight_layout()

        # Clear tick marks
        ax.set_xticks([])
        ax.set_yticks([])

        # Horizontal grid lines (Y-axis)
        # y_labels = plot_y_labels

        for y, label in plot_y_labels.items():
            ax.axhline(y=y, color=grid_color, linewidth=grid_linewidth, linestyle='-', zorder=1)

        # Draw custom y-axis labels
        ax.set_yticks(list(plot_y_labels.keys()))
        ax.set_yticklabels(list(plot_y_labels.values()), fontsize=label_fontsize)

        # Draw custom x-axis labels
        x_ticks  = range(3600, int(max(times)), 3600)
        x_labels = map(lambda seconds: f'{str(int(seconds/3600))}h' , x_ticks)
        for x, label in zip(x_ticks, x_labels):
            ax.text(x, ax.get_ylim()[1] + xlabel_offset , label,
                  fontsize=label_fontsize, ha='center', va='bottom', color='black')

        # Compute vertical padding (5% headroom above and below)
        y_min = float(np.min(stages))
        y_max = float(np.max(stages))
        y_pad = y_pad_c * (y_max - y_min if y_max != y_min else 1)
        ax.set_ylim(y_min - y_pad, y_max + y_pad)
        ax.invert_yaxis()

        for spine in ax.spines.values():
            spine.set_visible(False)

        max_label_len = max([len(label) for label in stage_map.values()])
        left_margin = min(0.03, 0.02 * max_label_len)
        fig.subplots_adjust(left=left_margin, right=0.99, top=0.95, bottom=0.05)

        if hypnogram_marker is not None:
            ax.axvline(x=hypnogram_marker, color=hypnogram_marker_color, linestyle='-', label=f'Set Point: {hypnogram_marker}',
                       linewidth=marker_line_width, zorder=3)

        # Store reference to axes and figure
        self.current_hypnogram_ax = ax
        self.current_hypnogram_fig = fig
        self.hypnogram_double_click_callback = double_click_callback

        if parent_widget:
            # Create a new Figure Canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()
            canvas.setStyleSheet("background-color: white;")  # Qt background

            # Double click handler
            cid = canvas.mpl_connect('button_press_event', self._on_hypnogram_double_click)
            self.hypnogram_connection.append(cid)

            # Store canvas
            self.current_hypnogram_canvas = canvas

            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)
        else:
            pass
    @staticmethod
    def reorder_labels_stages(y_labels:dict[int,str], stages:list[int]):
        """
            Reorders sleep stage labels and stages for hypnogram plotting.
            Desired order: Wake, REM, then NREM stages (N1, N2, N3, N4, or NREM)

            Works with various labeling schemes:
            - Individual NREM stages: N1, N2, N3, N4
            - Reduced NREM stages: N1, N2, N3 (no N4)
            - Consolidated NREM: just "NREM"
            - 3-stage system: W, NREM, REM
            - Alternative formats: Stage 1, S1, etc.

            Args:
                y_labels: Dictionary mapping original stage numbers to stage labels
                stages: List of stage numbers from sleep data

            Returns:
                plot_labels_plot: Dictionary mapping new stage numbers to stage labels
                plot_stages: List of remapped stage numbers for plotting
            """
        plot_labels_plot = {}
        #plot_stages = []

        # Create mapping from original stage number to new plot position
        original_to_plot = {}
        plot_position = 0

        # Step 1: Find and map Wake stages first
        wake_patterns = ['W', 'WAKE', 'AWAKE']
        for original_stage_num, label in y_labels.items():
            if any(pattern in label.upper() for pattern in wake_patterns):
                original_to_plot[original_stage_num] = plot_position
                plot_labels_plot[plot_position] = label
                plot_position += 1

        # Step 2: Find and map REM stages second
        # rem_patterns = ['REM', 'R']
        for original_stage_num, label in y_labels.items():
            if (label.upper().strip() == "REM" and
                    original_stage_num not in original_to_plot):
                original_to_plot[original_stage_num] = plot_position
                plot_labels_plot[plot_position] = label
                plot_position += 1

        # Step 3: Find and map NREM stages in order (N1, N2, N3, N4, or NREM)
        # First try specific NREM stages in numerical order
        nrem_patterns = ['N1', 'N2', 'N3', 'N4', 'STAGE 1', 'STAGE 2', 'STAGE 3', 'STAGE 4', 'S1', 'S2', 'S3', 'S4']
        for nrem_pattern in nrem_patterns:
            for original_stage_num, label in y_labels.items():
                if (label.upper().strip() == nrem_pattern and
                        original_stage_num not in original_to_plot):
                    original_to_plot[original_stage_num] = plot_position
                    plot_labels_plot[plot_position] = label
                    plot_position += 1
                    break  # Only add the first match for each pattern

        # Step 4: Handle general NREM label (if present and no specific N1-N4 found)
        # Check if we have any specific NREM stages in the original labels
        has_specific_nrem = any('N' in label.upper() and any(char.isdigit() for char in label)
                                for label in y_labels.values())

        if not has_specific_nrem:  # Only add general NREM if no specific stages exist
            for original_stage_num, label in y_labels.items():
                if ('NREM' in label.upper() and
                        original_stage_num not in original_to_plot):
                    original_to_plot[original_stage_num] = plot_position
                    plot_labels_plot[plot_position] = label
                    plot_position += 1

        # Step 5: Add any remaining stages that weren't categorized
        for original_stage_num, label in y_labels.items():
            if original_stage_num not in original_to_plot:
                original_to_plot[original_stage_num] = plot_position
                plot_labels_plot[plot_position] = label
                plot_position += 1

        # Remap the stages array using the new mapping
        plot_stages = [original_to_plot[stage] for stage in stages]

        return plot_labels_plot, plot_stages
    @staticmethod
    def clear_hypnogram_plot(parent_widget = None):
        layout = parent_widget.layout()
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.setParent(None)
    def _on_hypnogram_double_click(self, event):
        """
        Handle double-click events on the hypnogram plot and trigger callbacks.

        Internal event handler that processes matplotlib button press events on the
        hypnogram canvas. Extracts the time (x-axis) and sleep stage (y-axis) values at the click
        position and invokes the registered callback function if available.

        The cursor changes to a wait cursor during processing and is automatically
        restored afterward.

        Args:
            event: matplotlib MouseEvent object containing click information.
                Expected attributes:
                - dblclick (bool): True if this was a double click
                - inaxes: The axes object if click was inside axes, None otherwise
                - xdata (float): X-axis data coordinate (time in seconds)
                - ydata (float): Y-axis data coordinate (sleep stage numeric value)

        Returns:
            None. Invokes callback if conditions are met.

        Behavior:
            - Only processes events that are double-clicks AND within plot axes
            - Extracts x_value (time in seconds) and y_value (sleep stage)
            - Converts time to HH:MM:SS format for potential display
            - Calls self.hypnogram_double_click_callback(x_value, y_value) if set
            - Changes cursor to wait cursor during processing
            - Automatically restores normal cursor when complete

        Requires:
            self.current_hypnogram_ax: Reference to the current hypnogram axes object
            self.hypnogram_double_click_callback: Optional callback function that
                                                accepts (x_value, y_value) arguments

        Callback Signature:
            callback(x_value: float, y_value: float) -> None
            Where:
            - x_value: Time position in seconds from start of recording
            - y_value: Numeric sleep stage value at clicked position

        Example:
            # >>> # This method is typically connected via matplotlib event system
            # >>> canvas.mpl_connect('button_press_event', self._on_hypnogram_double_click)
            #
            # >>> # Define a callback to handle double-clicks
            # >>> def on_hypnogram_click(time_sec, stage_value):
            # ...     print("User clicked at {{time_sec}}s, stage {{stage_value}}")
            # ...     # Navigate to this time point in the recording
            #
            # >>> sleep_analyzer.hypnogram_double_click_callback = on_hypnogram_click

        Notes:
            - This is an internal method (indicated by leading underscore)
            - Silently ignores clicks outside axes or single clicks
            - Time conversion to HH:MM:SS is computed but currently unused
            - Cursor changes provide visual feedback during callback execution
        """
        # Set busy cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        # Check for a double click and within the axes
        if event.dblclick and event.inaxes and hasattr(self, 'current_hypnogram_ax'):
            x_value = event.xdata  # Time in seconds
            y_value = event.ydata  # Sleep stage value

            if x_value is not None and y_value is not None:
                # Convert time to hours:minutes format for display
                # hours = int(x_value // 3600)
                # minutes = int((x_value % 3600) // 60)
                # seconds = int(x_value % 60)
                #time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                # print(f"Hypnogram double-clicked at time: {x_value:.2f}s ({time_str})")

                # Call callback method if it exists
                if hasattr(self, 'hypnogram_double_click_callback') and self.hypnogram_double_click_callback is not None:
                    self.hypnogram_double_click_callback(x_value, y_value)

        # Revert to point cursor
        QApplication.restoreOverrideCursor()
    def show_sleep_stages_legend(self, qtparent = None):
        """
        Display a modal dialog showing the legend for sleep stage colors.

        Creates and shows a StageColorDialog that displays the color scheme used
        for visualizing different sleep stages in hypnograms and other plots.
        The dialog is modal, blocking interaction with other windows until closed.

        Args:
            qtparent: Optional parent Qt widget for the dialog. If provided, the
                     dialog will be centered relative to this parent widget and
                     follow standard parent-child Qt widget behavior. If None,
                     the dialog appears as a standalone window. Defaults to None.

        Returns:
            None. The dialog's exec() result (accept/reject status) is not captured.

        Side Effects:
            - Creates a new StageColorDialog instance
            - Blocks execution until the dialog is closed by the user
            - Dialog displays color mappings from self.default_stage_colors

        Requires:
            self.default_stage_colors: Dictionary mapping sleep stage names to
                                      color codes (e.g., {'Wake': '#FF0000', ...})

        Notes:
            - Dialog is modal (exec() is used instead of show())
            - User must close the dialog before continuing interaction
            - The 'owner' parameter passes self to allow dialog access to instance data
            - Common use case: Allow users to reference colors when interpreting plots
        """
        dialog = StageColorDialog(owner=self, parent=qtparent)
        dialog.exec()

    # Class Functions
    def __str__(self)->str:
        """
            Return string representation showing epoch count and duration.

            Returns:
                str: Format 'SleepStages(number of epochs = <count>, epoch duration = <seconds>")'

        """
        return f'SleepStages(number of epochs = {len(self.num_stages)}, epoch duration = {self.sleep_epoch }")'

class SignalAnnotations:
    """
        Manage and visualize signal annotations (scored events) from sleep studies.

        This class processes scored events from polysomnography recordings, organizing
        annotations by type, signal input, and timing. It provides color mapping,
        summarization, and DataFrame conversion for analysis and visualization.

        Attributes:
            scoredEvents (List[Dict[str, any]]): List of scored event dictionaries containing
                                                 annotation data (name, start, duration, signal).
            scoredEventSettings (Dict[str, Dict[str, str]]): Configuration for each event type,
                                                            including color codes and properties.
            scored_events_sum_dict (dict): Summary dictionary with counts per annotation type.
            scored_event_unique_names (list[str]): List of unique annotation type names.
            scored_event_unique_inputs (list[str]): List of unique signal channels used.
            scored_event_unique_keys (list[str]): List of unique annotation-signal pairs.
            scored_event_color_dict (dict[str, str]): Maps event types to hex color codes.
            annotation_colors (list[str]): Fallback color palette for annotations.
            color_map (dict[str, str] | None): Dynamic color mapping generated during plotting.
            sleep_events_df (DataFrame): Pandas DataFrame containing all scored events.
            scored_event_name_source_time_list (list[str]): Text summary of events with
                                                            start time, name, and input.
            output_dir (str): Directory path for exported files. Defaults to current directory.
            current_annotation_ax: Matplotlib axes object for current annotation plot.
            current_annotation_fig: Matplotlib figure object for current annotation plot.
            current_annotation_canvas: Qt FigureCanvas for embedded annotation plots.
            annotation_double_click_callback: Callback function for plot double-click events.
            annotation_connection (list): List of matplotlib event connection IDs.

        Args:
            scoredEvents: List of dictionaries, each representing a scored event with keys
                         like 'Name', 'Start', 'Duration', 'Input', etc.
            scoredEventSettings: Dictionary mapping event type names to their settings,
                               including 'Colour' (24-bit integer) and other properties.

        Example:
            >>> scored_events = [
            ...     {'Name': 'Apnea', 'Start': 120.5, 'Duration': 15.0, 'Input': 'Airflow'},
            ...     {'Name': 'Arousal', 'Start': 300.0, 'Duration': 3.0, 'Input': 'EEG'}
            ... ]
            >>> settings = {
            ...     'Apnea': {'Colour': '16711680'},  # Red in 24-bit
            ...     'Arousal': {'Colour': '65280'}    # Green in 24-bit
            ... }
            >>> annotations = SignalAnnotations(scored_events, settings)
            >>> print(len(annotations.sleep_events_df))
            2

        Notes:
            - Color codes in scoredEventSettings are 24-bit integers, converted to hex
            - The color_map attribute is generated dynamically during plotting
            - Annotation plot references are initialized to None and set during plotting
            - Event connection IDs are stored to allow disconnection when needed
        """
    def __init__(self, scoredEvents:List[Dict[str,any]], scoredEventSettings: Dict[str,Dict[str,str]]):

        # Define some variables set during initialization
        self.scored_events_sum_dict                   = {} # Annotation summary dictionary
        self.scored_event_unique_names:list[str]      = [] # types of annotations
        self.scored_event_unique_inputs:list[str]     = [] # Signals used during scoring
        self.scored_event_unique_keys:list[str]       = [] # Unique annotation-signal pairs
        self.scored_event_types                       = []

        # Process Scored Event Settings
        self.scoredEventSettings:Dict[str, Dict[str, str]] = scoredEventSettings
        self.color_dict                 = self.summarize_scored_settings()

        # Create an annotation dictionary
        self.scored_event_color_f       = lambda annot_key : int(scoredEventSettings[annot_key]['Colour'])
        self.color_24_to_hex_f          = lambda color_int : "#{:06X}".format(color_int)
        self.scored_event_color_dict    = {}
        for key in self.scoredEventSettings.keys():
           self.scored_event_color_dict[key] = self.color_24_to_hex_f(self.scored_event_color_f(key))

        # Colors from file didn't always work. Generated a list to try
        self.annotation_colors = [
            "#E41A1C",  # red
            "#FF7F00",  # orange
            "#FFD700",  # gold
            "#4DAF4A",  # green
            "#00BFC4",  # teal
            "#984EA3",  # purple
            "#F781BF",  # magenta
            "#A65628",  # brown
            "#999933",  # olive
            "#666666"  # dark gray
        ]
        self.color_map:dict[str,str]|None = None # Color map generated on the fly from plot annotations.
                                                 # TODO: Move color map generation code to init

        # Process Scored Events
        self.scoredEvents          = scoredEvents
        self.scoredEvents_sum_dict = self.summarize_scoredEvents(self.scoredEvents)
        self.sleep_events_df       = self.create_sleep_events_dataframe(self.scoredEvents)
        self.df_summary_cols       = ['Start', 'Name', 'Input']
        self.scored_event_name_source_time_list \
                                   = self.df_columns_to_text(self.sleep_events_df, self.df_summary_cols)

        # Output Control
        self.output_dir            = os.getcwd()

        # Safe External Values
        #total_time_in_seconds:float = None

        # Initialize annotation plot references (add these lines)
        self.current_annotation_ax            = None
        self.current_annotation_fig           = None
        self.current_annotation_canvas        = None
        self.annotation_double_click_callback = None
        self.color_map                        = None

        # Store event connections
        self.annotation_connection            = []

    # Manage Plot and App Events
    def cleanup_events(self):
        """
            Disconnect all matplotlib event handlers and clear connection list.

            Side Effects:
                - Disconnects handlers in self.annotation_connection
                - Clears the connection list
                - Silently ignores already-removed connections
            """
        for cid in self.annotation_connection:
            try:
                self.current_annotation_fig.canvas.mpl_disconnect(cid)
            except (ValueError, KeyError):
                pass  # In case connection is already gone
        self.annotation_connection.clear()
    def setup_events(self):
        """
            Connect double-click event handler for annotation plot.

            Idempotent: does nothing if handlers already connected.
            Stores connection ID in self.annotation_connection for later cleanup.
            """
        # Only setup if not already connected (avoid duplicate connections)
        if self.annotation_connection:
            return  # Already setup

        # Reconnect spectrogram event handlers
        cid = self.current_annotation_fig.canvas.mpl_connect('button_press_event', self._on_annotation_double_click)
        self.annotation_connection.append(cid)
    def set_output_dir(self, output_dir: str):
        """
            Set directory for exported files. Creates directory if it doesn't exist.

            Args:
                output_dir: Path to output directory (absolute or relative).
            """

        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    # Return information
    def get_events_types(self)->List:
        """
        Get list of unique scored event type names, sorted alphabetically.

        Extracts unique event types from self.scoredEvents on first call and caches
        the result in self.scored_event_types. Subsequent calls return the cached list.

        Returns:
            List[str]: Sorted list of unique event type names (e.g., ['Apnea', 'Arousal', 'Hypopnea']).
                    Empty list if no events are loaded.

        Side Effects:
            - Populates and sorts self.scored_event_types on first call
            - Logs info message if events not loaded or already processed
         """
        if self.scoredEvents == [] and self.scored_event_types == []:
            logger.info(f'Scored events not loaded')
        elif self.scoredEvents != [] and self.scored_event_types == []:
            scored_event_types = []
            for event_dict in self.scoredEvents:
                scored_event_types.append(event_dict['Name'])
            scored_event_types = get_unique_entries(scored_event_types)
            self.scored_event_types = scored_event_types
            self.scored_event_types.sort()
        elif self.scored_event_types:
            logger.info(f'Scored events identified previously')
        return self.scored_event_types
    # Plot Annotation
    def plot_annotation(self, total_time_in_seconds: float,
                        parent_widget=None,
                        annotation_filter:str|None = None,
                        double_click_callback = None):

        """
        Plot scored events as vertical lines with color-coded annotation types.

        Creates a timeline visualization showing when scored events (apneas, arousals,
        desaturations, etc.) occur during the recording. Each event type is displayed
        as a vertical line with a unique color. Can be embedded in a Qt widget or
        displayed as a standalone matplotlib figure.

        Args:
            total_time_in_seconds: Maximum recording duration in seconds for x-axis scaling.
            parent_widget: Optional Qt widget to embed the plot. If provided, renders as
                      a FigureCanvas within this widget. If None, creates standalone
                      matplotlib figure. Defaults to None.
            annotation_filter: Optional event type name to display. If specified, only events
                          matching this name are shown. If None or "All", displays all
                          event types. Defaults to None.
            double_click_callback: Optional callback function invoked on double-clicks.
                              Receives (x_value, y_value) as arguments where x_value
                              is time in seconds. Defaults to None.

        Returns:
            tuple: (fig, ax) - matplotlib Figure and Axes objects for the plot.
                Returns None if no scored events exist.

        Side Effects:
            - Sets self.current_annotation_ax to the matplotlib axes
            - Sets self.current_annotation_fig to the matplotlib figure
            - Sets self.current_annotation_canvas to FigureCanvas (if parent_widget provided)
            - Sets self.annotation_double_click_callback to the provided callback
            - Populates self.color_map with annotation-to-color mappings on first call
            - Appends connection ID to self.annotation_connection list
            - Replaces parent_widget's layout contents if provided

        Requires:
            self.scoredEvents: List of scored event dictionaries
            self.sleep_events_df: DataFrame with 'Start' and 'Name' columns
            self.scored_event_unique_names: List of unique event type names
            self.annotation_colors: List of color codes for event types



        Notes:
            - Each event type gets a unique color from self.annotation_colors
            - X-axis shows hourly markers (1h, 2h, 3h, etc.)
            - Vertical grid lines mark each hour
            - Legend is disabled by default (turn_off_legend=True)
            - Returns early if no scored events are loaded
        """
        # Controls
        turn_off_legend = True

        # Set Plot defaults
        annotation_colors = self.annotation_colors

        # Set Plot defaults
        grid_color = '#cccccc'  # light gray
        # y_pad_c = 0.05
        label_fontsize = 8
        grid_linewidth = 0.8
        line_width = 1.5
        alpha = 0.8

        # Check if we have scored events
        if not hasattr(self, 'scoredEvents') or not self.scoredEvents:
            print("No scored events to plot")
            return

        # Create figure and axis
        fig = Figure(figsize=(12, 2))
        ax = fig.add_subplot(111)

        # Store references for event handling
        self.current_annotation_ax            = ax
        self.current_annotation_fig           = fig
        self.annotation_double_click_callback = double_click_callback

        # Get unique annotation names and assign colors
        start_times = [float(entry) for entry in list(self.sleep_events_df['Start'])]
        names = list(self.sleep_events_df['Name'])

        if annotation_filter and annotation_filter != "All":
            # Keep only events matching the filter
            filtered_indices = [
                i for i, name in enumerate(names) if name == annotation_filter
            ]
            start_times = [start_times[i] for i in filtered_indices]
            names = [names[i] for i in filtered_indices]
            unique_annotations = [annotation_filter]
        else:
            unique_annotations = sorted(list(self.scored_event_unique_names[1:]))


        if self.color_map is None:
            # Setup color map
            color_map = {}
            for i, annotation in enumerate(unique_annotations):
                color_map[annotation] = annotation_colors[i % len(annotation_colors)]
            self.color_map = color_map  # save color map for automated legend generation
        else:
            # Assume color map is set up upon init to 'All'
            # Avoids having two parameters
            color_map = self.color_map


        # Use the provided total time parameter
        max_time = max(total_time_in_seconds)
        min_time = 0

        # print(f"Debug: Using time range: {min_time} to {max_time}")
        # print(f"Debug: Found {len(start_times)} events with {len(unique_annotations)} unique annotations")

        # Set up the plot area
        ax.set_xlim(min_time, max_time)
        ax.set_ylim(-0.5, 0.5)  # Narrow vertical range for line display

        # Plot vertical lines for each event
        plotted_annotations = set()
        for start_time, annotation_name in zip(start_times, names):
            color = color_map.get(annotation_name, 'black')  # fallback color
            ax.axvline(x=start_time, color=color, linewidth=line_width,
                       alpha=alpha, label=annotation_name if annotation_name not in plotted_annotations else "")
            plotted_annotations.add(annotation_name)

        # Configure axis
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.tick_params(axis='both', labelsize=label_fontsize)

        # Set y tick label to white to align with hypnogram
        # ax.set_yticks([0])  # Single tick at center
        # ax.set_yticklabels(['REM'], fontsize=label_fontsize, color='white')
        ax.set_yticks([])

        # Draw custom x-axis labels (hours)
        x_ticks = range(3600, int(max_time), 3600)
        x_labels = [f'{int(x / 3600)}h' for x in x_ticks]
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_labels, fontsize=label_fontsize)

        # Add light vertical grid lines for hours
        for x_tick in x_ticks:
            ax.axvline(x=x_tick, color=grid_color, linewidth=grid_linewidth,
                       linestyle='--', alpha=0.5, zorder=0)

        # Remove spines
        for i, spine in enumerate(ax.spines.values()):
            if i > 1:
                spine.set_visible(True)
                spine.set_color('gray')
                spine.set_linewidth(0.5)
            else:
                spine.set_visible(False)

        # Add legend if there are annotations
        if plotted_annotations and not turn_off_legend:
            legend = ax.legend(loc='upper right', fontsize=label_fontsize - 1,
                               framealpha=0.8, fancybox=True, shadow=True)
            legend.get_frame().set_facecolor('white')

        # Adjust layout
        fig.subplots_adjust(left=0.03, right=0.99, top=0.95, bottom=0.05)

        # Handle widget integration
        if parent_widget:
            # Create a new Figure Canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.updateGeometry()
            canvas.setStyleSheet("background-color: white;")  # Qt background

            # Connect double-click event handler
            cid = canvas.mpl_connect('button_press_event', self._on_annotation_double_click)
            self.annotation_connection.append(cid)

            # Store canvas reference
            self.current_annotation_canvas = canvas

            # Clear existing layout
            existing_layout = parent_widget.layout()
            if existing_layout:
                while existing_layout.count():
                    item = existing_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            else:
                existing_layout = QVBoxLayout(parent_widget)
                parent_widget.setLayout(existing_layout)

            existing_layout.setContentsMargins(0, 0, 0, 0)
            existing_layout.addWidget(canvas)

        return #fig, ax
    def show_annotation_legend(self, parent=None):
        """
        Convenience function to show the annotation legend dialog.

        Args:
            parent: Parent widget

        Returns:
            int: Dialog result (QDialog.Accepted or QDialog.Rejected)
        """
        color_map = self.color_map
        dialog = AnnotationLegendDialog(color_map, parent)
        return dialog.exec()
    def _on_annotation_double_click(self, event):
        """Handle double-click events on the annotation plot."""
        """Handle double - click events on annotation plot and invoke callback with time coordinates."""
        if event.dblclick and event.inaxes:
            x_value = event.xdata  # Time in seconds
            y_value = event.ydata  # Y position (not meaningful for annotation plot)

            if x_value is not None:
                # Convert time to hours:minutes format for display
                # hours = int(x_value // 3600)
                # minutes = int((x_value % 3600) // 60)
                # seconds = int(x_value % 60)
                # time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                # print(f"Annotation plot double-clicked at time: {x_value:.2f}s ({time_str})")

                # Call the callback function if provided
                if (hasattr(self, 'annotation_double_click_callback') and
                        self.annotation_double_click_callback is not None):
                    self.annotation_double_click_callback(x_value, y_value)
    # Summarize
    def summary_scored_events(self)->None:
        """
        Log a summary of scored events including unique event types, signal inputs, and event-signal pair counts.

        Outputs the summary to the logger if scored events are loaded. Logs an error if no scored events exist.
        """
        # Check if scored events is set
        if self.scoredEvents_sum_dict != {}:
            # Write scored events summary
            logger.info('')
            logger.info('Scored Event:')
            logger.info('-------------------')

            # Write unique events types to the command line
            output_str = 'Unique Events:             '
            for index in range(len(self.scored_event_unique_names)-1):
                output_str += f'{self.scored_event_unique_names[index]}, '
            output_str += f'{self.scored_event_unique_names[-1]}'
            logger.info(output_str)

            # Write unique signals used in scoring to the command line
            output_str = 'Unique Signal Inputs:      '
            for index in range(len(self.scored_event_unique_inputs)-1):
                output_str += f'{self.scored_event_unique_inputs[index]}, '
            output_str += f'{self.scored_event_unique_inputs[-1]}'
            logger.info(output_str)

            # Write unique keys (event+signal) with counts to the command line
            output_str = 'Unique Event-Signal Pairs: '
            for index in range(len(self.scored_event_unique_keys)-1):
                key = self.scored_event_unique_keys[index]
                output_str += f'\'{key}\' = {self.scoredEvents_sum_dict[key]}, '
            key = self.scored_event_unique_keys[-1]
            output_str += f'\'{key}\' = {self.scoredEvents_sum_dict[key]}'
            logger.info(output_str)
        else:
            logger.error('** Scored Event Not Loaded **')
    def summarize_scoredEvents(self, scoredEvents:List[Dict])->Dict:
        """
        Identify events types scored, signals used for scoring, and summary of sleep events for each signal.

        :param scoredEvents: List of event dictionaries, where each dictionary includes a name and imput field
        :return: A dictionary with keys defined as 'Event'+'-'+'Signal' and the counts for each key
        """
        # Retrieve 'Name' and 'Input' fields to create a composite summary key
        scored_event_names  = [x['Name']  for x in scoredEvents]
        scored_event_inputs = [x['Input'] for x in scoredEvents]
        scored_event_keys   = [x['Name']+'-'+x['Input'] for x in scoredEvents]

        # Get unique names, inputs, and scored event keys
        self.scored_event_unique_names  = get_unique_entries(scored_event_names)
        self.scored_event_unique_inputs = get_unique_entries(scored_event_inputs)
        self.scored_event_unique_keys   = get_unique_entries(scored_event_keys)

        # Create dictionary with counts for each scored event key
        scoredEvent_sum_dict = {}
        for key in self.scored_event_unique_keys:
            scoredEvent_sum_dict[key] = 0
        for key in self.scored_event_unique_keys:
            scoredEvent_sum_dict[key] = sum([x['Name']+'-'+x['Input'] == key for x in scoredEvents])

        return scoredEvent_sum_dict
    def summarize_scored_settings(self)->Dict[int,tuple[int,int,int]]:
        """
        Extract and convert unique color values from scored event settings to RGB format.

        :return: Dictionary mapping 32-bit color integers to RGB tuples (r, g, b)
        """
        # Write dictionary to command line
        color_values = []
        eventSettings = self.scoredEventSettings.keys()
        for key in eventSettings:
            setting_dict = self.scoredEventSettings[key]
            color_values.append(int(setting_dict['Colour']))
            color_values.append(int(setting_dict['TextColour']))
        # Write RGB color values
        colors = get_unique_entries(color_values)
        colors.sort()

        # Create color dictionary
        self.color_dict = {}
        for color in colors:
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            self.color_dict[color] = (r, g, b)

        return self.color_dict
    def summary_scored_event_setting(self)->None:
        """
        Log a summary of scored event settings including count, names, details, and color mappings.

        Outputs event setting names in columns, detailed settings for each event, and converts
        24-bit color values to RGB format. Logs an error if no scored event settings are loaded.
        """
        if self.scoredEventSettings != {}:

            # Write summary of the number of event settings.
            eventSettings = list(self.scoredEventSettings.keys())
            number_of_event_settings = len(eventSettings)
            eventSettings.sort()
            # events_setting_str = ", ".join(eventSettings)
            logger.info('')
            logger.info('Scored Event Setting:')
            logger.info('--------------------')
            logger.info('Number of Settings = {}'.format(number_of_event_settings))
            column_print(eventSettings, number_of_columns=4, space=5)

            # Write dictionary to command line
            logger.info('')
            color_values = []
            for key in eventSettings:
                dict_str = convert_dict_to_summary_string(self.scoredEventSettings[key])
                logger.info(f'{key}: {dict_str}')
                setting_dict = self.scoredEventSettings[key]
                color_values.append(int(setting_dict['Colour']))
                color_values.append(int(setting_dict['TextColour']))
            # Write RGB color values
            colors = get_unique_entries(color_values)
            colors.sort()
            logger.info('')
            logger.info('24bit to RGB')

            # Create color dictionary - convert 24 bit color to 32bit rgb
            # color_dict = {}
            for color in colors:
                r = (color >> 16) & 0xFF
                g = (color >> 8) & 0xFF
                b = color & 0xFF
                logger.info(f'color {color}: ({r:3} {g:3} {b:3}) ')
                self.color_dict[color] = (r,g,b)
        else:
            logger.error('** Scored Events Not Loaded **')
    # Export utilities
    def export_event(self, filename:str = None, fmt: str = 'xlsx', time_stamped: bool = False, output_dir: str = None)->None:
        """
        Export scored events to an Excel or CSV file.

        :param filename: Output filename (generated if None)
        :param fmt: Export format, either 'xlsx' or 'csv' (defaults to 'csv' if invalid)
        :param time_stamped: Append timestamp to filename if True
        :param output_dir: Output directory (uses self.output_dir if None)
        """
        if fmt != 'xlsx' and fmt != 'csv':
            fmt = 'csv'
        if output_dir is not None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if filename is not None:
            filename = os.path.join(self.output_dir, filename)
        if time_stamped:
            filename = filename or generate_timestamped_filename("sleep_events", '.'+fmt, self.output_dir)
        else:
            filename = filename or generate_filename("sleep_events", '.'+fmt, self.output_dir)
        # Write each scored event to a file. Scored event fields for each event are not uniform/
        event_df, existing_cols = self.sleep_events_to_dataframe(self.scoredEvents)

        # Save to Excel
        logger.info(f'AnnotationXmlClass: Preparing to export events')
        try:
            if fmt == 'xlsx':
                event_df.to_excel(filename, index=False)
                logger.info(f"Saved {filename} with columns: {existing_cols}")
            elif fmt == 'csv':
                event_df.to_csv(filename, index=False)
                logger.info(f"Saved {filename} with columns: {existing_cols}")
            else:
                logger.error(f"Could not saved {filename} with columns: {existing_cols}, file type not supported")
        except Exception as e:
            logger.error(f"Could not save {filename} with columns: {existing_cols}. Error: {e}")
            logger.error(traceback.format_exc())
    def create_sleep_events_dataframe(self, events: list[dict]) -> pd.DataFrame:
        """
        Convert a list of sleep event dictionaries to a DataFrame with standardized column ordering.

        Orders columns with 'Name', 'Input', 'Start', 'Duration' first, followed by remaining
        columns in alphabetical order. Stores result in self.sleep_events_df.

        :param events: List of event dictionaries
        :return: DataFrame containing all events with ordered columns
        :raises ValueError: If events list is empty
        """
        if not events:
            raise ValueError("The events list is empty.")

        # Collect all keys from all events
        all_keys = set()
        for event in events:
            all_keys.update(event.keys())

        # Required columns
        first_cols = ['Name', 'Input', 'Start', 'Duration']
        # Remaining columns in alphabetical order
        extra_cols = sorted(all_keys - set(first_cols))

        # Final column order
        column_order = first_cols + extra_cols

        # Create DataFrame
        df = pd.DataFrame(events)

        # Reorder columns, include only columns that exist in DataFrame
        existing_cols = [col for col in column_order if col in df.columns]
        self.sleep_events_df = df.reindex(columns=existing_cols)

        return self.sleep_events_df
    @staticmethod
    def sleep_events_to_dataframe(events: list[dict]) -> tuple[pd.DataFrame, list[str]]:
        """
        Convert a list of sleep event dictionaries to a DataFrame with standardized column ordering.

        Orders columns with 'Name', 'Input', 'Start', 'Duration' first, followed by remaining
        columns in alphabetical order.

        :param events: List of event dictionaries
        :return: Tuple of (DataFrame with ordered columns, list of column names)
        :raises ValueError: If events list is empty
        """
        if not events:
            raise ValueError("The events list is empty.")

        # Collect all keys from all events
        all_keys = set()
        for event in events:
            all_keys.update(event.keys())

        # Required columns
        first_cols = ['Name', 'Input', 'Start', 'Duration']
        # Remaining columns in alphabetical order
        extra_cols = sorted(all_keys - set(first_cols))

        # Final column order
        column_order = first_cols + extra_cols

        # Create DataFrame
        df = pd.DataFrame(events)

        # Reorder columns, include only columns that exist in DataFrame
        existing_cols = [col for col in column_order if col in df.columns]
        df = df.reindex(columns=existing_cols)

        return df, existing_cols
    @staticmethod
    def df_columns_to_text(df: pd.DataFrame, columns: List[str] | None = None,hour_flag:bool=True) -> str:
        """
        Format specified DataFrame columns into left-justified strings with aligned columns.

        Converts 'Start' columns from seconds to HH:MM:SS format if hour_flag is True.
        Returns a list of formatted strings with header and data rows.

        :param df: Input DataFrame
        :param columns: List of column names to format (default: ['Name'])
        :param hour_flag: If True, convert 'Start' columns from seconds to HH:MM:SS format
        :return: List of formatted strings, one per row (including header)
        :raises ValueError: If any specified column is missing from DataFrame
        """
        # Target columns
        # columns = ['Name', 'Input', 'Start']
        if columns is None:
            columns = ['Name']

        # Ensure columns exist
        for col in columns:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        # If hour_flag is True, convert 'Start' columns from hours to seconds
        df_copy = df.copy()
        if hour_flag:
            for col in columns:
                if 'Start' in col:
                    def format_hours_colon_minutes(val):
                        try:
                            seconds = float(val)
                            hours   = int(seconds // 3600)
                            minutes = int((seconds % 3600) // 60)
                            seconds = int(seconds) % 60
                            return f"{hours}:{minutes:02d}:{seconds:02d}"
                        except (ValueError, TypeError):
                            return str(val)  # Leave non-numeric values as-is

                    df_copy[col] = df_copy[col].map(format_hours_colon_minutes)


        # Determine max width of each column for alignment
        col_widths = {
            col: max(df_copy[col].astype(str).map(len).max(), len(col))
            for col in columns
        }

        # Build row format
        row_fmt = '  '.join(f"{{{col}:<{col_widths[col]}}}" for col in columns)

        # Header
        lines = [row_fmt.format(**{col: col for col in columns})]

        # Rows
        for _, row in df_copy.iterrows():
            row_data = {col: str(row[col]) for col in columns}
            lines.append(row_fmt.format(**row_data))

        return lines  # Already split into lines
    def __str__(self)->str:
        # Override default class description
        return f'SignalAnnotations(unique events = "{self.scored_event_unique_names}")'
class AnnotationXml:
    """
    Utility for accessing information stored in annotation file stored in an XML file. Since a formal
    specification was not available, the schema is inferred from sample files available from the
    National Sleep Resource Repository.

    Class Constructor
        AnnotationXml(self, annotationFile:str, verbose: bool=True)
    Class Definitions
        Validate and Load
          validate_xml(self, xml_path: str, xsd_path: str) -> bool
          load(self)->None
        Sleep Stage Functions
          convert_num_stages_to_text(self, stage_num_list:list[int], stage_dict:dict[int,str])->List[str]
          summarize_sleep_stages(self, stage_list:list, stage_dict:dict[int,str])->dict[int|str, int|str]
        Scored Events Functions
          summarize_scoredEvents(self, scoredEvents:List[Dict])->None
        Export Functions
          export_sleep_stages(self, fn:str)->None
          export_event(self, fn:str)->None
          export_summary(self, filename: str, fmt: str = 'json') -> None
        Summary Functions (Command Line)
          summary_epoch_length(self)->None
          summary_stepped_channels(self)->None
          summary_scored_event_setting(self)->None
          summary_scored_sleep_stages(self)->None
          summary_scored_events(self)->None
          summary_montage(self)->None
          summary(self)->None
    Support Functions
        column_print(string_list:list, number_of_columns: int = 2, space: int = 5)
        get_unique_entries(input_list:list)->list
    """
    def __init__(self, annotationFile:str, verbose: bool=False, output_dir: str = os.getcwd()):
        """
        Utility for parsing and accessing information from XML annotation files used by the National Sleep Research Resource.

        The schema is inferred from sample files as no formal specification is available. Provides methods to load,
        validate, summarize, and export sleep stages, scored events, and other annotation data.

        Key Methods:
            - validate_xml(): Validate XML against schema
            - load(): Parse and load annotation data
            - export_sleep_stages(), export_event(), export_summary(): Export data to files
            - summary(): Display comprehensive summary to command line
            - Various summary_*() methods: Display specific annotation components
        """

        # File variables
        self.annotationFile  = ''
        self.file_name       = None
        self.file_exists     = False

        # Class flags
        self.file_loaded     = False

        # XML Variables
        self.xml_tree        = None
        self.xml_root        = None
        self.xml_annotations = []

        # Schema Variables Read From XML file
        # Use appropriate object to access
        self.epochLength         = None
        self.steppedChannels     = {}
        self.scoredEventSettings = {}
        self.sleepStages         = []
        self.scoredEvents        = []
        self.montage             = {}

        # Computed Variable
        self.recording_duration_hr = None
        self.number_of_epochs      = None

        # Sleep Stage Variables
        self.sleep_stages_obj: SleepStages | None = None

        # Scored Event Variables
        self.scored_event_obj: SignalAnnotations|None = None

        # Montage Variables
        self.montage_input_not_set   = '** Input Not Set **'

        # Store File Name
        self.annotationFile = annotationFile
        self.output_dir = None
        self.set_output_dir(output_dir)


        # Need to get rid one of these.... using output directory now
        self.file_name       = os.path.basename(annotationFile)
        self.file_path       = os.path.dirname(annotationFile)

        #Set Logger Level
        if not verbose:
            logger.setLevel(logging.CRITICAL + 1)
        else:
            logger.setLevel(logging.INFO)
    # Initialize and validate
    @staticmethod
    def validate_xml(xml_path: str, xsd_path: str) -> bool:
        """
        Validate an XML annotation file against an XML schema (XSD).

        :param xml_path: Path to the XML annotation file
        :param xsd_path: Path to the XML schema definition file
        :return: True if validation succeeds, False otherwise
        """
        # open and load schema file
        with open(xsd_path, 'rb') as schema_file:  # FIXED: use 'rb'
            schema_doc = etree.XML(schema_file.read())
            schema = etree.XMLSchema(schema_doc)

        parser = etree.XMLParser(schema=schema)

        # Open annotation XML File and validate with loaded schema
        try:
            with open(xml_path, 'rb') as xml_file:
                etree.fromstring(xml_file.read(), parser)
            logger.info("XML is valid.")
            return True
        except etree.XMLSyntaxError as e:
            logger.error(f"XML validation error: {e}")
            return False
    def set_output_dir(self, output_dir: str):
        """Set the directory to use for output files."""
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
    # Load
    def load(self)->None:
        """
        Parse and load all annotation data from the XML file.

        Extracts epoch length, stepped channels, scored event settings, scored events, sleep stages,
        and montage configuration. Creates SleepStages and SignalAnnotations objects if sufficient
        data is available. Sets self.file_loaded to True on success.

        :raises: Logs error if file not found or XML parsing fails
        """
        # Check if file exists
        if os.path.exists(self.annotationFile):
            try:
                xml_tree = ET.parse(self.annotationFile)
                xml_root = xml_tree.getroot()
            except (ET.ParseError, OSError) as e:
                logger.error(f"Error parsing XML: {e}")
                return
            # print(xml_root.find('CMPStudyConfig'))
            for e in xml_root:
                # print(e.tag)
                if e.tag == 'EpochLength':
                    self.epochLength = float(e.text)
                elif e.tag == 'StepChannels':
                    for steps in e:
                        # print('     {}'.format(e.tag))
                        # stepChan = []
                        label_tags = ''
                        new_step_channel = ''
                        for step in steps:
                            # print ('          {}'.format(step.tag))
                            if step.tag == 'Input':
                                new_step_channel = step.text
                            if step.tag == 'Labels':
                                label_tags = []
                                for labels in step:
                                    label_tags.append(labels.text)
                        self.steppedChannels[new_step_channel] = label_tags
                        # print(self.steppedChannels)
                elif e.tag == 'ScoredEventSettings':
                    for eventSets in e:
                        # print('     {}: {}'.format(eventSets.tag, eventSets.text))
                        eventSetEntry = {}
                        for eventSet in eventSets:
                            eventSetEntry[eventSet.tag] = eventSet.text
                        name = eventSetEntry['Name']
                        del eventSetEntry['Name']
                        self.scoredEventSettings[name] = eventSetEntry
                elif e.tag == 'ScoredEvents':
                    for scoreEvent in e:
                        entry = {}
                        for score in scoreEvent:
                            entry[score.tag] = score.text
                        self.scoredEvents.append(entry)
                elif e.tag == 'SleepStages':
                    for sleepStage in e:
                        # print('     {}: {}'.format(sleepStage.tag, sleepStage.text))
                        self.sleepStages.append(int(sleepStage.text))
                elif e.tag == 'Montage':
                    # print('                   montage')
                    for montage in e:
                        # print('     {}'.format(montage.tag))
                        for tracePane in montage:
                            # print('     {}'.format(tracePane.tag))
                            for traces in tracePane:
                                # print('        {}'.format(traces.tag))
                                # trace_dict = {}
                                for trace in traces:
                                    # print ('               {} '.format(trace.tag))
                                    trace_dict = {}
                                    for traceEntry in trace:
                                        trace_dict[traceEntry.tag] = traceEntry.text
                                    # print('                 ', trace_dict)
                                    input_name = trace_dict['Input']
                                    if input_name is None:
                                        input_name = self.montage_input_not_set
                                    del trace_dict['Input']
                                    self.montage[input_name] = trace_dict
            self.file_loaded = True
            if self.sleepStages != [] and self.epochLength:
                # Create Sleep Stages Object
                self.sleep_stages_obj = SleepStages(self.epochLength, self.sleepStages)

                # Moving Scored Events to Separate Class
                self.scored_event_obj       = SignalAnnotations(self.scoredEvents, self.scoredEventSettings)
        else:
            logger.error(f"** File Not Found: {self.annotationFile} **")
            self.file_loaded = False
    # Summarize and export
    def summary_epoch_length(self)->None:
        """
        Log the epoch length in seconds to the command line.

        Logs an error if epoch length has not been loaded.
        """
        # If epoch length set, echo epoch length to command line when verbose set to true.
        if self.epochLength is not None:
            logger.info("")
            logger.info('Epoch Length: {} s'.format(self.epochLength))
        else:
            logger.error('** Epoch Length Not Loaded **')
    def summary_stepped_channels(self)->None:
        """
        # Write stepped channel summary to command line when verbose set to true.

        :return: None
        """
        # Write summary for each channel if stepped channels is set
        if self.steppedChannels != {}:
            logger.info("")
            logger.info('Stepped Channels:')
            logger.info('----------------')
            stepped_channels = list(self.steppedChannels.keys())
            stepped_channels.sort()
            for channel in stepped_channels:
                setting_string = list(self.steppedChannels[channel])
                setting_string = ', '.join(setting_string)
                logger.info('{}: {}'.format(channel, setting_string))
        else:
            logger.info('** Stepped Channels Not Loaded **')
    def summary_montage(self)->None:
        """
            Log the montage input channels in a multi-column format.

            Displays channel names in 5 columns. Logs an error if montage data has not been loaded.
            """
        if len(self.montage) > 0:
            logger.info('')
            inputs = list(self.montage.keys())
            logger.info('Montage:')
            logger.info('-------')
            column_print(inputs, number_of_columns=5, space=10)
        else:
            logger.error('** Montage Not Loaded **')
    def summary(self)->None:
        """
        Logging module used to write and XML file summary to the command line when DEBUG is set to verbose.
        The function calls summary functions written for epoch_length, stepped_channels, scored events settings,
        scored sleep stages, scored events, and montage.

        :return: None
        """
        # Logger moduled used to create a
        logger.info('')
        logger.info('')
        logger.info('')
        logger.info('Annotation XML Summary:')
        logger.info('----------------------')
        logger.info('----------------------')
        logger.info('File Name: {}'.format(self.file_name))
        logger.info('File Path: {}'.format(self.file_path))

        # Call XML file component summaries
        self.summary_epoch_length()
        self.summary_stepped_channels()
        self.scored_event_obj.summary_scored_event_setting()
        self.sleep_stages_obj.summary_scored_sleep_stages()
        self.scored_event_obj.summary_scored_events()
        self.summary_montage()
    def export_summary(self, filename: str = None, fmt: str = 'json', output_dir: str = None, time_stamped: bool = False) -> None:
        """
        Export annotation summary data to a JSON or CSV file.

        Exports comprehensive summary including epoch length, recording duration, sleep stage counts,
        scored events, channel configuration, montage inputs, event settings, and color mappings.

        :param filename: Output filename (generated if None)
        :param fmt: Export format, either 'json' or 'csv' (default: 'json')
        :param output_dir: Output directory (uses self.output_dir if None)
        :param time_stamped: Append timestamp to filename if True
        """

        if output_dir is not None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if time_stamped:
            filename = os.path.join(self.output_dir, filename) or generate_timestamped_filename("edf_summary", "."+fmt, self.output_dir)
        else:
            filename = os.path.join(self.output_dir, filename) or generate_filename("edf_summary", "."+fmt, self.output_dir)

        # Dictionary of structures to write into file
        summary_data = {
            "file_name": self.file_name,
            "epoch_length": self.epochLength,
            "recording_duration_hr": self.recording_duration_hr,
            "sleep_stage_counts": self.sleep_stages_obj.stage_text_sum_dict,
            "sleep_stage_categories": self.sleep_stages_obj.stage_remnrem_sum_dict,
            "scored_events": self.scored_event_obj.scoredEvents_sum_dict,
            "stepped_channels": self.steppedChannels,
            "montage_inputs": list(self.montage.keys()),
            "scored_event_settings": self.scored_event_obj.scoredEventSettings,
            "color_dict": self.scored_event_obj.color_dict
        }

        # Write summary information to a file is designated type
        try:
            if fmt.lower() == 'json':
                with open(filename, 'w') as f:
                    json.dump(summary_data, f, indent=4)
            elif fmt.lower() == 'csv':
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    for key, value in summary_data.items():
                        writer.writerow([key, value])
            else:
                logger.error(f"Unsupported format: {fmt}")
        except Exception as e:
            logger.error(f"Failed to export summary: {e}")
    def __str__(self)->str:
        # Override default class description
        return f'AnnotationXml(file_name="{self.file_name}", file_loaded={self.file_loaded})'

# Main
def main():
    """
    Main function used to test and enhance functionality.

    :return:
    """
    pass

if __name__ == "__main__":
    main()