# Annotation XML Class
Python classes for accessing information from an annotation (XML) file.

## Overview
This module provides a comprehensive utility for accessing, analyzing, and exporting sleep annotation data stored in XML files, particularly those adhering to the NSRR (National Sleep Research Resource) schema. It supports parsing sleep stages, scored events, montage configurations, and other relevant metadata, facilitating integration with sleep research workflows and analysis tools.

The core of this module is the AnnotationXml class, which enables:

- Validation of XML annotation files against a schema.
- Loading and parsing annotation content such as sleep stages, events, and montage data.
- Summarizing and exporting annotation details.
- Visualizing hypnograms directly within Qt-based interfaces.
- Supporting robust access to annotation information for Python developers, complementing existing C utilities and NSRR data structures.
## Key Features
- **XML Validation**: Validate annotation files against an XSD schema.
- **Data Loading**: Parse sleep stages, scored events, montage configurations, and epoch length.
- **Summary Reports**: Generate human-readable summaries of annotation components.
- **Export Utilities**: Save sleep stages and events in CSV, JSON, or Excel formats.
- **Visualization**: Plot hypnograms within Qt widgets or standalone figures.
- **Modular Design**: Access sleep stages and scored events via dedicated classes (SleepStages, SignalAnnotations).

## Dependencies
This module requires the following Python packages:

- xml.etree.ElementTree (built-in)
- lxml (pip install lxml)
- pandas (pip install pandas)
- matplotlib (pip install matplotlib)
- PySide6 (pip install PySide6)
- numpy (pip install numpy)

## Intended Use
Jump start data analysis while providing an extensible framework to support future development. 


## Main Classes
- **AnnotationXml**: Handles loading, validating, summarizing, and exporting annotation data.
- **SleepStages**: Represents sleep stage annotations; supports summary and hypnogram plotting.
- **SignalAnnotations**: Manages scored events; supports exporting event data and generating summaries.

Example
```python
CopyRun
import os
from annotation_xml import AnnotationXml

# Initialize annotation object
annot = AnnotationXml('sample_annotation.xml', verbose=True)

# Load and validate
annot.load()
if annot.validate_xml('schema.xsd'):
    print("XML is valid.")

# Generate summaries
annot.summary()

# Export sleep stages
annot.sleep_stages_obj.export_sleep_stages('sleep_stages.txt')

# Export events
annot.scored_event_obj.export_event('sleep_events.xlsx')

# Save a JSON summary
annot.export_summary('annotation_summary.json', fmt='json')
```

## License
This project is licensed under the GNU Affero General Public License v3.0. See the LICENSE file for details.

## Acknowledgements
The code models previous MATLAB implementations from Case Western Reserve University and Brigham and Women's Hospital, adapted for Python to facilitate sleep data analysis and integration with NSRR datasets.

For further assistance or feature requests, please contact Dennis A. Dean, II, PhD.
