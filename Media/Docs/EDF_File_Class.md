# EDF File Class
The EDF File Class provides native Python access to an EDF (European Data Format) file. 

## Description
This module is designed to facilitate working with EDF files by providing classes that model their structure and content. It supports reading EDF files, extracting signal data, calculating statistics, and exporting information for further analysis.

## Key Features
- Load and parse EDF headers and signal headers
- Access and manipulate EDF signals
- Compute statistical summaries of signals
- Export signal data and statistics to CSV, Excel, and JSON formats
- Visualize signal segments within GUI applications


## Intended Use
The main class is EdfFile, which handles loading and processing EDF files. Additional classes model headers, signals, and statistical summaries, providing comprehensive access to EDF data.

## Example
```python
from edf_file import EdfFile

# Load an EDF file
edf = EdfFile("path/to/file.edf")
edf.load()

# View summary
edf.summary()

# Calculate statistics
edf.calculate_signal_stats()

# Export signal statistics
edf.edf_signals.export_sig_stats_to_csv()
```

## Modules and Classes
- **EdfHeader**: Stores EDF header info
- **EdfSignalHeader**: Stores signal header info
- **EdfSignals**: Manages signal data and analysis
- **EdfSignal**: Represents individual signals
- **EdfSignalsStats**: Holds computed signal statistics
- **EdfFile**: Main class for loading and processing EDF files

## Utilities
Includes functions for generating timestamped filenames, converting objects for JSON serialization, and plotting signal segments within GUIs.

For detailed class descriptions and methods, please refer to the inline documentation within the source code.

## Author
**Dennis A. Dean, II, PhD**

dennis.a.dean@gmail.com

## Version History

- v0.1
  - First functioning release

## License
This project is licensed under the **GNU Affero General Public License v3.0**.
See [LICENSE](LICENSE) for details.

## Acknowledgements
This Python implementation models previous MATLAB versions and benefits from feedback on MATLAB Central, building on MATLAB code from Case Western Reserve University and Brigham and Women's Hospital.

