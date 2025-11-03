# Annotation XML Class - Python XML Annotation File Parser

A Python library for parsing, analyzing, and visualizing XML annotation files from the National Sleep Research Resource (NSRR), commonly used for sleep stage scoring and event annotation in polysomnography studies.

## Overview

The Annotation XML Class provides comprehensive access to sleep study annotation data stored in XML format, including sleep stages, scored events (apneas, arousals, etc.), epoch configuration, channel settings, and montage information. It offers powerful visualization capabilities and seamless integration with EDF signal data.

## Features

- **Complete XML Annotation Support**
  - Parse NSRR-format XML annotation files
  - Extract sleep stages, scored events, and metadata
  - Access epoch length, stepped channels, and montage configuration
  - Validate XML against schema definitions

- **Sleep Stage Analysis**
  - Multiple stage representations (numeric, text, NREM/REM, N3-collapsed)
  - Comprehensive stage statistics and summaries
  - Sleep timing metrics (sleep onset, offset, duration)
  - Export to CSV, Excel, and text formats

- **Scored Event Management**
  - Process polysomnography events (apneas, hypopneas, arousals, etc.)
  - Automatic color mapping for event types
  - Event filtering and summarization
  - DataFrame-based event analysis

- **Visualization**
  - Interactive hypnogram plotting with customizable stage colors
  - Annotation timeline visualization
  - Double-click navigation callbacks
  - PySide6/Qt integration for GUI applications
  - Color-coded background regions for sleep stages

- **Export Capabilities**
  - JSON/CSV summary exports
  - Excel/CSV event exports
  - Text-based sleep stage exports
  - Timestamped file generation

## Installation

### Requirements

```bash
pip install lxml pandas matplotlib PySide6 numpy openpyxl
```

### Optional Dependencies

For XML schema validation:
```bash
pip install lxml
```

## Quick Start

### Basic Usage

```python
from annotation_xml_class import AnnotationXml

# Load an annotation file
annotation = AnnotationXml('/path/to/annotation.xml', verbose=True)
annotation.load()

# Display comprehensive summary
annotation.summary()

# Access sleep stages
sleep_stages = annotation.sleep_stages_obj
print(f"Number of epochs: {sleep_stages.number_of_epochs}")
print(f"Recording duration: {sleep_stages.recording_duration_hr:.2f} hours")
```

### Working with Sleep Stages

```python
# Get sleep stage data in different formats
numeric_stages = sleep_stages.num_stages           # [0, 1, 2, 3, 5, ...]
text_stages = sleep_stages.sleep_stages_text       # ['W', 'N1', 'N2', 'N3', 'REM', ...]
nrem_rem = sleep_stages.sleep_stages_NremRem       # ['W', 'NREM', 'NREM', 'NREM', 'REM', ...]

# Get stage statistics
stage_summary = sleep_stages.stage_text_sum_dict
print(f"N2 sleep: {stage_summary['N2']} epochs")
print(f"REM sleep: {stage_summary['REM']} epochs")

# Get sleep timing
stage_times = sleep_stages.return_stage_time_dict()
print(f"Sleep onset: {stage_times['sleep_start_time']}s")
print(f"Sleep offset: {stage_times['sleep_end_time']}s")
```

### Export Sleep Stages

```python
# Set output directory
annotation.set_output_dir('./exports')

# Export sleep stages (tab-delimited text)
sleep_stages.export_sleep_stages(
    filename='sleep_stages.txt',
    output_dir='./exports',
    time_stamped=True
)

# Export summary to JSON
annotation.export_summary(
    filename='annotation_summary.json',
    fmt='json',
    output_dir='./exports'
)
```

### Working with Scored Events

```python
# Access scored events
events = annotation.scored_event_obj

# Get event statistics
events.summary_scored_events()

# Get unique event types
event_types = events.get_events_types()
print(f"Event types: {event_types}")

# Access events as DataFrame
events_df = events.sleep_events_df
print(events_df.head())

# Filter events by type
apnea_events = events_df[events_df['Name'] == 'Obstructive Apnea']
print(f"Total apneas: {len(apnea_events)}")
```

### Export Scored Events

```python
# Export to Excel
events.export_event(
    filename='scored_events.xlsx',
    fmt='xlsx',
    output_dir='./exports'
)

# Export to CSV with timestamp
events.export_event(
    filename='scored_events.csv',
    fmt='csv',
    time_stamped=True
)
```

### Visualization

```python
from PySide6.QtWidgets import QWidget, QApplication
import sys

app = QApplication(sys.argv)

# Create a widget to hold the plot
plot_widget = QWidget()

# Plot hypnogram
sleep_stages.plot_hypnogram(
    parent_widget=plot_widget,
    stage_index=0,  # 0: standard, 1: NREM/REM, 2: N3-collapsed
    show_stage_colors=True  # Show colored background regions
)

plot_widget.show()
sys.exit(app.exec())
```

### Interactive Hypnogram with Callbacks

```python
def on_hypnogram_click(time_seconds, stage_value):
    """Handle hypnogram double-click events"""
    hours = int(time_seconds // 3600)
    minutes = int((time_seconds % 3600) // 60)
    print(f"Clicked at {hours:02d}:{minutes:02d}, Stage: {stage_value}")
    # Navigate to this time point in your application

# Plot with callback
sleep_stages.plot_hypnogram(
    parent_widget=plot_widget,
    double_click_callback=on_hypnogram_click,
    show_stage_colors=True
)
```

### Plot Scored Events Timeline

```python
# Get total recording time
total_time = sleep_stages.max_time_sec

# Plot all events
events.plot_annotation(
    total_time_in_seconds=total_time,
    parent_widget=annotation_widget
)

# Plot specific event type only
events.plot_annotation(
    total_time_in_seconds=total_time,
    parent_widget=annotation_widget,
    annotation_filter='Obstructive Apnea'
)
```

### Display Color Legends

```python
# Show sleep stage color legend
sleep_stages.show_sleep_stages_legend(qtparent=main_window)

# Show annotation color legend
events.show_annotation_legend(parent=main_window)
```

## Core Classes

### `AnnotationXml`
Main class for loading and managing XML annotation files.

**Key Methods:**
- `load()` - Parse and load annotation data
- `validate_xml()` - Validate against XML schema
- `summary()` - Display comprehensive summary
- `export_summary()` - Export summary to JSON/CSV
- `set_output_dir()` - Configure output directory

**Key Attributes:**
- `sleep_stages_obj` - SleepStages object with stage data
- `scored_event_obj` - SignalAnnotations object with events
- `epochLength` - Epoch duration in seconds
- `steppedChannels` - Stepped channel configuration
- `montage` - Signal montage configuration

### `SleepStages`
Manages sleep stage data with multiple representations and visualizations.

**Key Methods:**
- `plot_hypnogram()` - Generate interactive hypnogram
- `export_sleep_stages()` - Export stage data to file
- `return_stage_time_dict()` - Get sleep timing metrics
- `return_zeroed_sleep_stage_time_dictionary()` - Get time-based stage data
- `show_sleep_stages_legend()` - Display color legend

**Key Attributes:**
- `num_stages` - Numeric stage values [0-5]
- `sleep_stages_text` - Text labels ['W', 'N1', 'N2', 'N3', 'N4', 'REM']
- `sleep_stages_NremRem` - NREM/REM classification
- `stage_text_sum_dict` - Stage count summary
- `number_of_epochs` - Total epoch count
- `recording_duration_hr` - Recording duration in hours
- `default_stage_colors` - Color mapping for stages

### `SignalAnnotations`
Manages scored events (apneas, arousals, etc.) with visualization and analysis tools.

**Key Methods:**
- `plot_annotation()` - Visualize events on timeline
- `export_event()` - Export events to Excel/CSV
- `get_events_types()` - Get unique event type names
- `show_annotation_legend()` - Display event color legend
- `summarize_scoredEvents()` - Generate event summaries

**Key Attributes:**
- `sleep_events_df` - Pandas DataFrame with all events
- `scored_event_unique_names` - List of event types
- `scored_event_color_dict` - Event-to-color mapping
- `scoredEvents` - Raw event data (list of dicts)

## Sleep Stage Representations

The library provides multiple parallel representations:

### Numeric (0-5)
```python
0 = Wake
1 = N1
2 = N2
3 = N3
4 = N4
5 = REM
```

### Text Labels
```python
['W', 'N1', 'N2', 'N3', 'N4', 'REM']
```

### NREM/REM Reduced
```python
['W', 'NREM', 'NREM', 'NREM', 'NREM', 'REM']
```

### N3 Collapsed (N3 + N4 → N3)
```python
['W', 'N1', 'N2', 'N3', 'N3', 'REM']
```

## Stage Color Scheme

Default colors (customizable):

| Stage | Color | Hex Code |
|-------|-------|----------|
| Wake | Light orange | #FFE4B5 |
| N1 | Thistle | #D8BFD8 |
| N2 | Powder blue | #B0E0E6 |
| N3 | Pale green | #98FB98 |
| N4 | Medium sea green | #3CB371 |
| REM | Light pink | #FFB6C1 |
| NREM | Sky blue | #87CEEB |
| Artifact | Salmon | #FA8072 |

## XML File Structure

Expected XML schema elements:

```xml
<CMPStudyConfig>
  <EpochLength>30</EpochLength>
  <StepChannels>...</StepChannels>
  <ScoredEventSettings>...</ScoredEventSettings>
  <SleepStages>
    <SleepStage>0</SleepStage>
    <SleepStage>2</SleepStage>
    ...
  </SleepStages>
  <ScoredEvents>
    <ScoredEvent>
      <Name>Obstructive Apnea</Name>
      <Start>120.5</Start>
      <Duration>15.0</Duration>
      <Input>Airflow</Input>
    </ScoredEvent>
    ...
  </ScoredEvents>
  <Montage>...</Montage>
</CMPStudyConfig>
```

## Advanced Features

### Schema Validation

```python
# Validate XML against schema
is_valid = AnnotationXml.validate_xml(
    xml_path='annotation.xml',
    xsd_path='schema.xsd'
)

if is_valid:
    print("XML is valid")
else:
    print("XML validation failed")
```

### Custom Stage Color Mapping

```python
# Modify default colors
sleep_stages.default_stage_colors['N2'] = '#ADD8E6'  # Light blue
sleep_stages.default_stage_colors['REM'] = '#FF69B4'  # Hot pink

# Plot with custom colors
sleep_stages.plot_hypnogram(
    parent_widget=widget,
    show_stage_colors=True
)
```

### Event Filtering and Analysis

```python
# Get events DataFrame
df = events.sleep_events_df

# Filter by time range
morning_events = df[(df['Start'] >= 21600) & (df['Start'] < 28800)]

# Filter by signal input
eeg_events = df[df['Input'].str.contains('EEG')]

# Count events by type
event_counts = df['Name'].value_counts()
print(event_counts)
```

### Hypnogram Marker

```python
# Add vertical marker line at specific time
current_position = 3600  # 1 hour into recording

sleep_stages.plot_hypnogram(
    parent_widget=widget,
    hypnogram_marker=current_position  # Shows purple line at 1h
)
```

### Integration with EDF Signals

```python
from edf_file_class import EdfFile
from annotation_xml_class import AnnotationXml

# Load EDF and annotation files
edf = EdfFile('recording.edf')
edf.load()

annotation = AnnotationXml('recording.xml')
annotation.load()

# Get sleep stages for specific epoch
epoch_num = 100
epoch_width = annotation.epochLength
sleep_stage_info = annotation.sleep_stages_obj.return_zeroed_sleep_stage_time_dictionary(
    start_epoch=epoch_num,
    epoch_end=epoch_num + 1
)

# Plot EDF signal with sleep stage background
edf.edf_signals.plot_signal_segment(
    signal_key='EEG Fpz-Cz',
    signal_type='Continuous',
    epoch_num=epoch_num,
    epoch_width=epoch_width,
    sleep_stages=sleep_stage_info
)
```

## Utility Functions

```python
# Generate unique entries from list
from annotation_xml_class import get_unique_entries
unique_values = get_unique_entries([1, 2, 2, 3, 1, 4])
# Returns: [1, 2, 3, 4]

# Column printing for summaries
from annotation_xml_class import column_print
channel_list = ['C3', 'C4', 'F3', 'F4', 'O1', 'O2', 'Cz', 'Fz']
column_print(channel_list, number_of_columns=4, space=5)

# Generate timestamped filenames
from annotation_xml_class import generate_timestamped_filename
filename = generate_timestamped_filename("export", ".csv", "./output")
# Returns: ./output/export_20250620_143052.csv
```

## File Export Formats

### Sleep Stages Export (Text)
Tab-delimited format with multiple representations:
```
0	W	W	W
1	N1	NREM	N1
2	N2	NREM	N2
3	N3	NREM	N3
5	REM	REM	REM
```

### Scored Events Export (Excel/CSV)
| Name | Input | Start | Duration | Notes |
|------|-------|-------|----------|-------|
| Obstructive Apnea | Airflow | 120.5 | 15.0 | ... |
| Central Apnea | Airflow | 450.2 | 12.5 | ... |

### Summary Export (JSON)
```json
{
  "file_name": "recording.xml",
  "epoch_length": 30,
  "recording_duration_hr": 8.5,
  "sleep_stage_counts": {
    "W": 120,
    "N1": 45,
    "N2": 580,
    "N3": 210,
    "REM": 65
  },
  "scored_events": {
    "Obstructive Apnea-Airflow": 145,
    "Central Apnea-Airflow": 23,
    "Arousal-EEG": 87
  }
}
```

## Event Handling

### Double-Click Events

Both hypnogram and annotation plots support double-click callbacks:

```python
def handle_plot_click(x_value, y_value):
    """Generic handler for plot interactions"""
    epoch_num = int(x_value / annotation.epochLength)
    print(f"Navigating to epoch {epoch_num}")
    # Update your GUI or perform actions

# Connect to hypnogram
sleep_stages.plot_hypnogram(
    parent_widget=widget,
    double_click_callback=handle_plot_click
)

# Connect to annotation timeline
events.plot_annotation(
    total_time_in_seconds=total_time,
    parent_widget=widget,
    double_click_callback=handle_plot_click
)
```

### Event Cleanup

```python
# Clean up matplotlib event connections
sleep_stages.cleanup_events()
events.cleanup_events()

# Re-establish connections
sleep_stages.setup_events()
events.setup_events()
```

## Examples

### Complete Analysis Workflow

```python
from annotation_xml_class import AnnotationXml

# Load annotation
annotation = AnnotationXml('study.xml', verbose=True)
annotation.load()
annotation.set_output_dir('./analysis_output')

# Display summary
annotation.summary()

# Analyze sleep stages
stages = annotation.sleep_stages_obj
print(f"Total sleep time: {sum(stages.stage_text_sum_dict.values()) * stages.sleep_epoch / 3600:.1f} hours")
print(f"Sleep efficiency: {(1 - stages.stage_text_sum_dict['W'] / stages.number_of_epochs) * 100:.1f}%")

# Export data
stages.export_sleep_stages('sleep_stages.txt', output_dir='./analysis_output')
annotation.scored_event_obj.export_event('events.xlsx', fmt='xlsx', output_dir='./analysis_output')
annotation.export_summary('summary.json', fmt='json', output_dir='./analysis_output')
```

## Acknowledgments

This Python implementation is based on previous MATLAB versions developed at:
- Case Western Reserve University
- Brigham and Women's Hospital

The code has benefited from community feedback and is designed to complement the NSRR ecosystem and Luna software.

## License

This source code is licensed under the **GNU Affero General Public License v3.0**.

See the LICENSE file in the root directory or visit https://www.gnu.org/licenses/agpl-3.0.html for full terms.

Copyright 2025 Dennis A. Dean II, PhD - Sleep Science

## Author

**Dennis A. Dean, II, PhD**  
Sleep Science  
Completion Date: June 20, 2025

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style conventions
- Functions include comprehensive docstrings
- New features include usage examples
- Changes are tested with NSRR-format XML files

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

---

**Note:** This library is specifically designed for the National Sleep Research Resource (NSRR) XML annotation format and is intended for research and clinical applications in sleep medicine and polysomnography analysis.