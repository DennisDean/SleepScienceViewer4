# Sleep Science Viewer - Release Notes
## Version [0.3.0] - [Octorber 29, 2025]
We're excited to announce the first major release of Sleep Science Viewer, featuring comprehensive signal spectral analysis capabilities and a flexible, user-customizable interface.

## 🎉 New Features
### Signal Spectral Analysis Module
The Sleep Science Viewer now supports **signal spectral analysis** as its first analysis module, enabling detailed frequency-domain examination of sleep study data.

### Customizable Interface

- **Show/Hide Controls**: Toggle visibility of interface components including:
  - Settings panel
  - Parameters panel
  - Hypnogram display
  - Spectrogram visualization
  - Marking sections
- Flexible workspace customization to suit individual workflow preferences

## Multiple Visualization Modes

- **Average Spectrum View**: Display average spectral power across selected data ranges
- **Band Boxplots**: Visualize spectral band distributions by sleep stage
- **Spectrogram View**: Full time-frequency representation of signal data
- **Stage-Based Summaries**: View data organized by:
    - All available stages
    - N1-N3 sleep stages
    - REM-NREM comparison

## Analysis Settings

- **Multi-Signal Selection**: Analyze up to 10 signals simultaneously
- **X-Axis Label Control**: Toggle axis labeling on/off
- **Signal Reference**: Interface ready (implementation pending)
- **Filtering Options**: Interface ready (implementation pending)

## Analysis Parameters
### Analysis Range Options
Automatically identify and analyze specific portions of your sleep data:

- *First Wake*: Initial wake period
- *First Wake and Sleep*: Combined wake and sleep onset
- *Sleep Only*: Isolated sleep periods (automatically detected)
- *Ending Wake*: Final wake period

The application intelligently identifies first and last sleep periods to define sleep boundaries.

### Multi-Taper Spectrogram

- Configurable multi-taper parameters for enhanced spectral estimation
- Adjustable balance between frequency and time resolution
- Greater flexibility compared to traditional Fourier transform methods
- Parameter selcection ptimized for the full range of signals available in sleep studies

### Noise Detection

- Automated detection algorithm identifies large perturbations in sleep EEG
- Generates noise detection masks including:

  - `delta_time_mask`
  - `beta_time_mask`
  - `union_time_mask`
  - `intersection_time_mask`


Masks saved as separate files for post-processing and further analysis

### Spectral Band Definition

Six customizable frequency bands with EEG-optimized defaults
Adjustable parameters for different signal types

### Filtering (Implemented)

- Band-pass filtering
- Notch filtering
- Filter effects reflected in spectrogram results
- Fully integrated with EDF and multi-taper modules

## Save and Export Functionality

- **Configuration Export**: Save analysis settings as XML files
- **Results Export: Computer**- and human-readable format
- **Per-Signal Output**: Individual result files and noise masks for each analyzed signal
- Preserve analysis configurations for reproducibility

## 🎯 Design Philosophy
This release emphasizes **interactive analysis** as the primary goal. The visual parameter interface enables users to manually review data in support of batch analyses, providing the flexibility needed for exploratory data analysis and quality control.

### 📋 Coming Soon

- Signal reference implementation
- Lights-on/lights-off timing for analysis range definition
- Additional analysis moduleslots

For questions, feedback, or support, please contact [dennis.a.dean@gmail.com]