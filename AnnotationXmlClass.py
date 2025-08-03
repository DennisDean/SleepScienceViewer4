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


© 2025 Dennis A. Dean II
This file is part of the SleepScienceViewer project.

This source code is licensed under the GNU Affero General Public License v3.0.
See the LICENSE file in the root directory of this source tree or visit
https://www.gnu.org/licenses/agpl-3.0.html for full terms.
"""
import xml.etree.ElementTree as ET
import os
import pandas as pd
import platform
import json
import csv
import logging
import traceback
from typing import List, Dict
from lxml import etree
from sympy.logic.boolalg import Boolean

# Plotting support
import numpy as np

# Required for plotting
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout

# TODO Show stages 1-3, collapse stage 4

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
    output_dir: str = Output directory if set)
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}{ext}"
    return os.path.join(output_dir, filename) if output_dir else filename
def generate_filename(prefix: str, ext: str = ".csv", output_dir: str = "") -> str:
    """Add a time stamp to a generated file

    prefix: str: File name
    ext: str = File type string
    output_dir: str = Output directory if set)
    """
    filename = f"{prefix}{ext}"
    return os.path.join(output_dir, filename) if output_dir else filename

# Sleep annotation classes
class SleepStages:
    def __init__(self, epoch:int, num_stages:list,
                 num_stage_to_num_dict: Dict[int,str]    = {0:0,   1:1,      2:2,      3:3,      4:4,     5:5},
                 num_stage_to_text_dict:Dict[int,str]    = {0:'W', 1:'N1',   2:'N2',   3:'N3',   4:'N4',  5:'REM'},
                 num_stage_to_nremrem_dict:Dict[int,str] = {0:'W', 1:'NREM', 2:'NREM', 3:'NREM', 4:'NREM', 5:'REM'},
                 num_stage_to_text_n3_dict: Dict[int, str] = {0: 'W', 1: 'N1', 2: 'N2', 3: 'N3', 4: 'N3', 5:'REM'},
                 nremrem_to_num_stage_dict:Dict[str,int] = {'W':0, 'NREM':1, 'REM':2},
                 num_stage_to_nremrem_reduced_dict:Dict[int,str] = {0:'W', 1:'NREM', 2:'REM'},
                 num_stage_to_text_n3_reduced_dict: Dict[int, str] = {0: 'W', 1: 'N1', 2: 'N2', 3: 'N3', 4:'REM'},
                 ):
        # Update log
        logging.info(f'Initializing SleepStagesClass: epoch{epoch}, num of stages {len(num_stages)}')

        # Set inputs and conversion
        self.sleep_epoch               = epoch
        self.num_stages                = num_stages
        self.num_stage_to_num_dict     = num_stage_to_num_dict
        self.num_stage_to_text_dict    = num_stage_to_text_dict
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
        print(set(num_stages))
        self.sleep_stages_text          = self.convert_num_stages_to_text(num_stages, num_stage_to_text_dict)
        print(set(self.sleep_stages_text ))
        self.sleep_stages_NremRem       = self.convert_num_stages_to_text(num_stages, num_stage_to_nremrem_dict)

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

        # Labels - will make self describing in another pass
        self.numeric_labels  = list(num_stage_to_text_dict.keys())
        self.numeric_labels.sort()
        self.text_labels     = get_unique_entries([num_stage_to_text_dict[i] for i in self.numeric_labels])
        self.nremrem_labels  = get_unique_entries([num_stage_to_nremrem_dict[i] for i in self.numeric_labels])
        self.text_n3_labels  = get_unique_entries([num_stage_to_text_n3_dict[i] for i in self.numeric_labels])
        self.numeric_labels  = get_unique_entries([str(num_stage_to_num_dict[i]) for i in self.numeric_labels])

        print(f'text_n3_labels {self.text_n3_labels}')

        # Create labels to assist with histogram plotting
        self.numeric_labels  = "_".join(self.numeric_labels)
        self.text_labels     = "_".join(self.text_labels)
        self.nremrem_labels  = "_".join(self.nremrem_labels)
        self.text_n3_labels  = "_".join(self.text_n3_labels)

        # Output Control
        self.output_dir = os.getcwd()
    # Utilities
    def set_output_dir(self, output_dir: str):
        """Set the directory to use for output files."""
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
    def convert_num_stages_to_text(self, stage_num_list: list[int], stage_dict: dict[int, str]) -> List[str]:
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
        sleep_stages_labels = [self.numeric_labels, self.text_labels, self.nremrem_labels, self.text_n3_labels ]
        return sleep_stages_labels
    def return_sleep_stage_mappings(self):
        sleep_stages_labels = [self.num_stage_to_text_dict, self.num_stage_to_nremrem_dict ]
        return sleep_stages_labels
    # Summarize and export
    def summarize_sleep_stages(self, stage_list: list, stage_dict: dict[int, str]) -> dict[int | str, int | str]:
        """
        Generate a dictionary that contains counts for each sleep stage in the included dictionary.

        :param stage_list:
        :param stage_dict:
        :return:
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
    # def return_sleep_stages(self) -> SleepStages:
        """
        Return sleep stages in numeric, N1-N4, and NREM-REM formats. Include dictionaries for
        translations

        :param filename
        :return: SleepStages Class
        """
        if self.epochLength == None:
            logger.error('AnnotationXMLClass: Load XML file prior to requesting sleep stage information.\
            Returning default (empty) SleepStages Class.')

        return SleepStages(self.number_of_epochs, self.sleepStages, self.sleep_state_to_text,
                           self.sleep_state_to_NremRemW)
    def summary_scored_sleep_stages(self) -> None:
        """
        Write sleep stage summary to the command line if verbose is set to True in constructor.

        :return: None
        """
        # Write if sleep stages are set
        if (self.num_stages != []) and (self.sleep_epoch != None):
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
        Export sleep stages in numeric, N1-N4, and NREM-REM formats.

        :param fn:
        :return:
        """
        # Log status
        logging.info(f'Preparing to export sleep stages to {filename}')

        # Set output directory if provided
        if output_dir != None:
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
                    file.write(f"{self.num_stages[i]}\t{self.sleep_stages_text[i]}\t{self.sleep_stages_NremRem[i]}\n")
        except Exception as e:
            logger.error(f'*** Could not export sleep stages: {filename}, error: {e}')
    # Plotting functions
    def plot_hypnogram(self, parent_widget=None, stage_index = 0):
        """
            Plots a hypnogram into a QGraphicsView if provided, or as a standalone matplotlib figure.
            The plot background is white, auto-scales, and fills available width.
            """
        # if not hasattr(self, 'sleep_stages') or not hasattr(self, 'epoch_times'):
        #    raise ValueError("Missing required data: 'sleep_stages' and 'epoch_times'")

        # Set Plot defaults
        grid_color      = '#cccccc'  # light gray
        signal_color    = 'blue'
        y_pad_c         = 0.25
        label_fontsize  = 7
        xlabel_offset   = 1 if stage_index == 0 else 0
        ylabel_offset   = 0.02*self.recording_duration_hr*3600
        grid_linewidth  = 0.8

        # Get hypnogram information
        stages    = self.num_stages
        times     = self.time_seconds
        time_axis = np.arange(len(stages)) * self.sleep_epoch

        # Time and stage data
        # times = sleep_stages.time_seconds
        # stages = sleep_stages.num_stages

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

        ax.step(time_axis, stages, color=signal_color, linewidth=1)

        ax.set_xlim(min(times), max(times))
        ax.set_ylim(min(y_ticks) - 0.5, max(y_ticks) + 0.5)
        ax.tick_params(axis='both', labelsize=9)


        # Reset x label offset as a proportion of ylim
        yl = ax.get_ylim()

        fig.tight_layout()

        # Clear tick marks
        ax.set_xticks([])
        ax.set_yticks([])

        # Horizontal grid lines (Y-axis)
        y_labels = stage_map
        for y, label in y_labels.items():
            ax.axhline(y=y, color=grid_color, linewidth=grid_linewidth, linestyle='-', zorder=0)



        # Draw custom y-axis labels
        # y_labels = stage_map
        # for y, label in y_labels.items():
        #    ax.text(ax.get_xlim()[0] + ylabel_offset, y, label,
        #            fontsize=label_fontsize, ha='right', va='center', color='black')

        #ax.set_xticks(x_ticks)
        #ax.set_xticklabels(x_labels, fontsize=label_fontsize)

        ax.set_yticks(list(stage_map.keys()))
        ax.set_yticklabels(list(stage_map.values()), fontsize=label_fontsize)

        # Draw custom x-axis labels
        x_ticks  = range(3600, int(max(times)), 3600)
        x_labels = map(lambda x: f'{str(int(x/3600))}h' , x_ticks)
        for x, label in zip(x_ticks, x_labels):
            ax.text(x, ax.get_ylim()[1] + xlabel_offset , label,
                  fontsize=label_fontsize, ha='center', va='bottom', color='black')

        # Compute vertical padding (5% headroom above and below)
        y_min = np.min(stages)
        y_max = np.max(stages)
        y_pad = y_pad_c * (y_max - y_min if y_max != y_min else 1)
        ax.set_ylim(y_min - y_pad, y_max + y_pad)
        ax.invert_yaxis()

        for spine in ax.spines.values():
            spine.set_visible(False)

        max_label_len = max([len(label) for label in stage_map.values()])
        left_margin = min(0.03, 0.02 * max_label_len)
        fig.subplots_adjust(left=left_margin, right=0.99, top=0.95, bottom=0.05)
        # fig.subplots_adjust(left=0.08, right=0.98, top=0.95, bottom=0.18)

        if parent_widget:
            # Create a new Figure Canvas
            canvas = FigureCanvas(fig)
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            canvas.updateGeometry()
            canvas.setStyleSheet("background-color: white;")  # Qt background

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
    def clear_hypnogram_plot(self, parent_widget = None):
        layout = parent_widget.layout()
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.setParent(None)
    # Class Functions
    def __str__(self)->str:
        # Override default class description
        return f'SleepStages(number of epochs = {len(self.num_stages)}, epoch duration = {self.sleep_epoch }")'
class SignalAnnotations:
    def __init__(self, scoredEvents, scoredEventSettings):

        # Define some variables set during initialization
        self.scored_events_sum_dict = {}
        self.scored_event_unique_names = []
        self.scored_event_unique_inputs = []
        self.scored_event_unique_keys = []
        self.scored_event_types = []

        # Process Scored Event Settings
        self.scoredEventSettings   = scoredEventSettings
        self.color_dict            = self.summarize_scored_settings()

        # Process Scored Events
        self.scoredEvents          = scoredEvents
        self.scoredEvents_sum_dict = self.summarize_scoredEvents(self.scoredEvents)
        self.sleep_events_df       = self.create_sleep_events_dataframe(self.scoredEvents)
        self.df_summary_cols       = ['Start', 'Name', 'Input']
        self.scored_event_name_source_time_list =  \
                                    self.df_columns_to_text(self.sleep_events_df, self.df_summary_cols)

        # Output Control
        self.output_dir = os.getcwd()
    def set_output_dir(self, output_dir: str):
        """Set the directory to use for output files."""
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
    # Return information
    def get_events_types(self)->List:
        """Get a list of scored event types"""
        if self.scoredEvents == [] and self.scored_event_types == []:
            logger.info(f'Scored events not loaded')
        elif self.scoredEvents != [] and self.scored_event_types == []:
            scored_event_types = []
            for event_dict in self.scoredEvents:
                scored_event_types.append(event_dict['Name'])
            scored_event_types = get_unique_entries(scored_event_types)
            self.scored_event_types = scored_event_types
            self.scored_event_types.sort()
        elif self.scored_event_types != []:
            logger.info(f'Scored events identified previously')
        return self.scored_event_types
    # Summarize
    def summary_scored_events(self)->None:
        """
        Write scored events summary to command line if DEBUG is set.

        :return:
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
    def summarize_scoredEvents(self, scoredEvents:List[Dict])->None:
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

        :return: Color dict with xml color as keys and entries in 32bit RGB colors
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
        Write scored event settings summary to the command line. Function not completely implemented.

        :return:
        """
        if self.scoredEventSettings != {}:

            # Write summary of the number of event settings.
            eventSettings = list(self.scoredEventSettings.keys())
            number_of_event_settings = len(eventSettings)
            eventSettings.sort()
            events_setting_str = ", ".join(eventSettings)
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
            color_dict = {}
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
        Export events to a file, where event dictionary is not uniform

        :param fn:
        :return:
        """
        if fmt != 'xlsx' and fmt != 'csv':
            fmt = 'csv'
        if output_dir != None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if filename != None:
            filename = os.path.join(self.output_dir, filename)
        if time_stamped:
            filename = filename or generate_timestamped_filename("sleep_events", '.'+fmt, self.output_dir)
        else:
            filename = filename or generate_filename("sleep_events", '.'+fmt, self.output_dir)
        # Write each scored event to a file. Scored event fields for each event are not uniform/
        event_df, existing_cols = self.sleep_events_to_dataframe(self.scoredEvents, filename)

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
        Convert a list of sleep event dictionaries to an Excel file.

        Args:
            events (list of dict): List of event dictionaries.
            filename (str): Output Excel filename.
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
    def sleep_events_to_dataframe(self, events: list[dict], filename: str = 'sleep_events.xlsx') -> pd:
        """
        Convert a list of sleep event dictionaries to an Excel file.

        Args:
            events (list of dict): List of event dictionaries.
            filename (str): Output Excel filename.
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
    def df_columns_to_text(self, df: pd.DataFrame, columns:List[str]=['Name'],hour_flag:Boolean=True) -> str:
        """
        Format specific DataFrame columns ('Name', 'Input', 'Start') into
        a left-justified string with aligned columns.

        Parameters:
            df (pd.DataFrame): Input DataFrame

        Returns:
            str: Formatted string
        """
        # Target columns
        # columns = ['Name', 'Input', 'Start']

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
        # # Calculate column widths based on longest content per column
        # col_widths = {
        #     col: max(df[col].astype(str).map(len).max(), len(col))
        #     for col in columns
        # }
        #
        # # Build format string
        # row_fmt = '  '.join(f"{{{col}:<{col_widths[col]}}}" for col in columns)
        #
        # # Header row
        # lines = [row_fmt.format(**{col: col for col in columns})]
        #
        # # Data rows
        # for _, row in df.iterrows():
        #     row_data = {col: str(row[col]) for col in columns}
        #     lines.append(row_fmt.format(**row_data))
        # split_lines = '\n'.join(lines)
        #
        # return split_lines.splitlines()
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
        Validate, Load, and access information stored in an XML annotation file.

        :param annotationFile: XML File as used by the National Sleep Research Resource
        :param verbose:
        """

        # File variables
        self.annotationFile = ''
        self.file_name      = None
        self.file_exists    = False

        # Class flags
        self.file_loaded = False

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
    def validate_xml(self, xml_path: str, xsd_path: str) -> bool:
        """
        Returns boolean results of the balidation of the XML file with the XML schema

        :param xml_path: Annotation file with path and file name
        :param xsd_path: XML schema file with path and file name
        :return:
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
        Load information stored in XML file

        :return:
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
                        stepChan = []
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
                                trace_dict = {}
                                for trace in traces:
                                    # print ('               {} '.format(trace.tag))
                                    trace_dict = {}
                                    for traceEntry in trace:
                                        trace_dict[traceEntry.tag] = traceEntry.text
                                    # print('                 ', trace_dict)
                                    input = trace_dict['Input']
                                    if input == None:
                                        input = self.montage_input_not_set
                                    del trace_dict['Input']
                                    self.montage[input] = trace_dict
            self.file_loaded = True
            if self.sleepStages != [] and self.epochLength:
                # Create Sleep Stages Object
                self.sleep_stages_obj = SleepStages(self.epochLength, self.sleepStages)

                # Moving Scored Events to Seperate Class
                self.scored_event_obj       = SignalAnnotations(self.scoredEvents, self.scoredEventSettings)
        else:
            logger.error(f"** File Not Found: {self.annotationFile} **")
            self.file_loaded = False
    # Summarize and export
    def summary_epoch_length(self)->None:
        """
        Echo epoch length summary to command line if verbose is set to truth in class constructor.

        :return:
        """
        # If epoch length set, echo epoch length to command line when verbose set to true.
        if self.epochLength != None:
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
        Export file summary in either CSV or JSON form.

        :param filename: Path+filename to write summary
        :param fmt: Either 'CSV' or 'JSON' format
        :return: None is returned
        """

        if output_dir != None:
            self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        if time_stamped:
            filename = os.path.join(self.output_dir, filename) or generate_timestamped_filename("edf_summary", ".", fmt, self.output_dir)
        else:
            filename = os.path.join(self.output_dir, filename) or generate_filename("edf_summary", ".", fmt, self.output_dir)

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
    os_name = platform.system()
    cur_working_dir = os.getcwd()
    if os_name == 'Windows':
        # Define files
        fn_1 = os.path.join(cur_working_dir, r"tutorial\tutorial\edfs\learn-nsrr01-profusion.xml")
        fn_2 = os.path.join(cur_working_dir, r"tutorial\tutorial\edfs\learn-nsrr02-profusion.xml")
        fn_3 = os.path.join(cur_working_dir, r"tutorial\tutorial\edfs\learn-nsrr03-profusion.xml")
        fn_4 = os.path.join(cur_working_dir, r"tutorial\tutorial\edfs\learn-nsrr03-profusion.xml")
        schema_fn = os.path.join(cur_working_dir, r"tutorial\tutorial\edfs\profusion_schema.xsd")
    else:
        fn_1 = os.path.join(cur_working_dir, r"/tutorial/tutorial/edfs/learn-nsrr01-profusion.xml")
        fn_2 = os.path.join(cur_working_dir, r"/tutorial/tutorial/edfs/learn-nsrr02-profusion.xml")
        fn_3 = os.path.join(cur_working_dir, r"/tutorial/tutorial/edfs/learn-nsrr03-profusion.xml")
        fn_4 = os.path.join(cur_working_dir, r"/tutorial/tutorial/edfs/learn-nsrr03-profusion.xml")
        schema_fn = os.path.join(cur_working_dir, r"./profusion_schema.xsd")

        fn_1 = r"/home/dennis/PycharmProjects/AnnotationXML/tutorial/tutorial/edfs/learn-nsrr01-profusion.xml"
        fn_2 = r"/home/dennis/PycharmProjects/AnnotationXML/tutorial/tutorial/edfs/learn-nsrr02-profusion.xml"
        fn_3 = r"/home/dennis/PycharmProjects/AnnotationXML/tutorial/tutorial/edfs/learn-nsrr03-profusion.xml"
        fn_4 = r"/home/dennis/PycharmProjects/AnnotationXML/tutorial/tutorial/edfs/learn-nsrr03-profusion.xml"
        schema_fn = r"/home/dennis/PycharmProjects/AnnotationXML/tutorial/tutorial/edfs/profusion_schema.xsd"

    AnnotateObject1 = AnnotationXml(fn_1)
    AnnotateObject1.load()
    valid_xml_file = AnnotateObject1.validate_xml(fn_1, schema_fn)
    AnnotateObject1.summary()
    AnnotateObject1.set_output_dir("./export/json")
    AnnotateObject1.export_summary('learn-nsrr01-profusion_summary.json', fmt='json')
    AnnotateObject1.set_output_dir("./export/csv")
    AnnotateObject1.export_summary('learn-nsrr01-profusion_summary.csv', fmt='csv')

    AnnotateObject2 = AnnotationXml(fn_2, verbose = False)
    AnnotateObject2.load()
    AnnotateObject2.summary()

    AnnotateObject3 = AnnotationXml(fn_3, verbose = False)
    AnnotateObject3.load()
    AnnotateObject3.summary()

    AnnotateObject4 = AnnotationXml(fn_4, verbose = True)
    AnnotateObject4.load()
    AnnotateObject4.summary()
    AnnotateObject4.set_output_dir("./export/summary")
    AnnotateObject4.export_summary('learn-nsrr03-profusion_summary.json', fmt='json')
    AnnotateObject4.export_summary('learn-nsrr03-profusion_summary.csv', fmt='csv')

    AnnotateObject5 = AnnotationXml(fn_4, verbose = False)
    logger.info(f'Annotation Object 5 validate? {AnnotateObject5.validate_xml(fn_4, schema_fn)}')
    AnnotateObject5.load()
    AnnotateObject5.summary()
    AnnotateObject5.set_output_dir("./export/sleep_stages")
    AnnotateObject5.sleep_stages_obj.export_sleep_stages('sleep_stages.txt')
    AnnotateObject5.set_output_dir("./export/sleep_events")
    AnnotateObject5.scored_event_obj.export_event('sleep_events.xlsx')
    AnnotateObject5.scored_event_obj.export_event(fmt = 'csv')
    AnnotateObject5.set_output_dir("./export/summary")
    sleep_events = AnnotateObject5.scored_event_obj.get_events_types()
    logger.info(f'Sleep Events: {sleep_events}')
    AnnotateObject5.export_summary('learn-nsrr03-profusion_summary.json', fmt='json')
    AnnotateObject5.export_summary('learn-nsrr03-profusion_summary.csv', fmt='csv')

    AnnotateObject6 = AnnotationXml('fn_4', verbose = False)
    AnnotateObject6.load()
if __name__ == "__main__":
    main()