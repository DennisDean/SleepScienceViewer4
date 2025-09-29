# Sleep Science Viewer

A Python-native EDF file and XML annotation viewer.

## Description

SleepScienceViewer is a Python-native application for visualizing and analyzing sleep data stored in EDF (European Data Format) and corresponding annotation files (XML). Designed with sleep science workflows in mind, the tool enables efficient review of signals and sleep stages through a responsive and customizable GUI.

SleepScienceViewer uses a class-based architecture to [represent EDF](Media/Docs/EDF_File_Class.md) and [annotation files](Media/Docs/Annotation_XML_Class.md). These classes can also be used independently to access specific information from the files, supporting flexible review and analysis within notebooks or other Python programs.

![SleepScienceViewer](Media/SleepScienceViewer.png)
*Figure 1. Sleep Science Viewer interface with signals, hypnogram, spectrogram, and annotations.*

## Key Features

* **EDF & Annotation Support**

  * Load EDF files with associated XML annotation files
  * Visualize up to 10 simultaneous signals
  * View and interact with a full hypnogram display (see Figure 1)

* **Annotation Interaction**

  * Filter listed annotations by type
  * Hypnogram-aligned annotation plot with [automatically assigned colors](Media/annotation_legend.png)
  * Annotation combo box directly linked to annotation plot and list for synchronized selection (see Figure 1)

* **Custom Display Options**

  * Change epoch duration for signal navigation
  * Toggle visibility of hypnogram, spectrogram, and annotation plots (see Figure 3 for signal-only mode)
  * Switch hypnogram rendering between line trace and background-colored stage rectangles
  * Generate multi-taper spectrograms for selected signals; if not feasible (e.g., low sampling frequency), display a compact heatmap instead
  * Customize signal colors via color picker; choices persist across pan/zoom events
  * Legends automatically update with user-defined signal colors

* **Report Generation & Export Tools**

  * Generate [EDF summary reports](Media/edf_summary.png)
  * Export individual [signals to folder](Media/signal_export.png)(s) for downstream use
  * Export annotation data including:

    * A [full annotation listing](Media/sleep_event_export.png)
    * [Sleep stage timeline](Media/sleep_stages.png)
    * [Summary reports](Media/sleep_event_summary.png) for review and documentation

* **Interface**

  * Show/hide hypnogram, spectrogram, and annotation panels from the main menu (see Figures 1 and 3)

* **Navigation**

  * Double-click on hypnogram, spectrogram, or annotation plots to move to the selected epoch
  * Double-click on annotation list entries to jump to annotation start times

![Signal Viewer Interface](Media/signal_viewer_beta.png)
*Figure 2. Signal Viewer interface displaying a single channel with epochs and overlays.*

* **Signal Viewer**

  * Signals

    * View a single signal as a raster plot with 15 epochs displayed vertically (see Figure 2)
    * Sleep stages shown as background rectangles behind the signal trace
    * X-axis moved to the bottom of the plot for improved readability
  * Interface/Plotting

    * Toggle hypnogram, spectrogram, and annotation overlays similar to the main viewer
    * Signal-only mode available (see Figure 4)
  * Processing & Analysis

    * Compute spectrograms (or default to heatmap if sampling frequency is insufficient)
    * Apply common Band Pass and Notch filters on demand
  * Considering (future work)

    * Displaying annotations directly on signal plots
    * Support for marking epochs in-progress

<p align="center">    
<img src="Media/SleepScienceViewer_signals_only.png" width="600" /><br>
*Figure 3. Sleep Science Viewer with hypnogram, spectrogram, and annotations hidden (signal-only mode).*
</p>

<p align="center">    
<img src="Media/signal_viewer_beta_signals_only.png" width="600" /><br>
*Figure 4. Signal Viewer in signal-only mode with hypnogram, spectrogram, and annotations hidden.*
</p>

## Workarounds

Double-click navigation is implemented but may be unstable due to limitations in how matplotlib interacts with PySide6. Framework code is in place, but full functionality is not guaranteed. Known workarounds:

* Avoid frequent switching between the Sleep Science Viewer and Signal Viewer windows.
* Redrawing figures within a window or reloading data often restores expected behavior.

## Getting Started

The Sleep Science Viewer requires an EDF and Annotation file. We used files downloaded from the [National Sleep Research Resource](https://sleepdata.org/) tutorial to develop the interface.

We recommend using a virtual environment when running the Sleep Science Viewer.

## Intended Use

Ideal for researchers, clinicians, and developers working in sleep research, human performance, or bio-signal analysis. The interface and tools are designed to streamline review and reporting workflows for sleep study data.

## Dependencies

This application was developed in Python 3.12, with the GUI built using PySide6. Please refer to [requirements.txt](requirements.txt) for a complete list of required dependencies.

## Download Test Data

We tested the SleepScienceViewer with data from [here](https://zzz.bwh.harvard.edu/luna/tut/tut1/).

## Installing

**1. Install pipx**

```
python -m pip install --user pipx
python -m pipx ensurepath
```

**2. Download install package**

```
git clone https://github.com/DennisDean/SleepScienceViewer4.git
cd SleepScienceViewer4/dist
```

**3. Install SleepScience Viewer**

```
pipx install sleepscienceviewer-0.1.0-py3-none-any.whl
```

## Running the Application

To launch the application:

```
SleepScienceViewer
```

## Help

Help documentation will be added as questions are received and common usage scenarios emerge.
For questions or feedback, feel free to reach out to the author listed below.

## Authors

**Dennis A. Dean, II, PhD**
[dennis.a.dean@gmail.com](mailto:dennis.a.dean@gmail.com)

## Version History

* v0.1.1

  * Added display toggles for hypnogram, spectrogram, and annotation panels
  * Hypnogram background color rendering for sleep stages
  * Annotation synchronization between combo box, plot, and list
  * Spectrogram-to-heatmap fallback for low sampling rates
  * Signal color customization with legends
  * Added Signal Viewer with raster view of single-channel data

* v0.1

  * First functioning release

## License

This project is licensed under the **GNU Affero General Public License v3.0 License**.
See the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

This project builds on work originally developed during my time at **Brigham and Women's Hospital**, where a similar class structure was used in earlier internal tools.

The original **MATLAB version** of this tool was shaped by valuable community feedback received following its public release on **MATLAB Central**.

It also benefited from code developed at **Case Western Reserve University**.

Special thanks to the authors of the [multitaper_spectrogram_python.py](https://github.com/preraulab/multitaper_toolbox/blob/master/python/multitaper_spectrogram_python.py) module, which was refactored for this application to support multi-taper spectrogram visualization. More information on the multi-taper method can be found on the [Prerau Lab website](https://prerau.bwh.harvard.edu/multitaper/).
