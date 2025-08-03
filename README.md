# Sleep Science Viewer

A python native EDF and XML annotation viewer. 

## Description

A python native sleep science viewer that allows users to review EDF and corresponding 
annotations files (XML).The interface displays the file hypnogram and up to ten signals, and 
can show up to ten signals. Listed annotations can be filtered by type and double clicking an
annotation will advance the signal to the epoch containing the annotation. Optionally, the user 
can change the display epoch duration, generate a multi-taper spectrogram, and can adjust how 
stages are displays in the hypnogram. 

The generate options supports user report generations. EDF generated outputs include an [EDF summary](Media/edf_summary.webm)
and the ability to [export signals](Media/signal_export.png) to a folders. Annotation exports include a [summary report](), 
[annotation listing](Media/sleep_event_export.png), and sleep stages. 


## Getting Started

The Sleep Science viewer requires an EDF and Annotation file. We used files downloaded in a tutorial for the 
[National Sleep Rsearch Resource](https://sleepdata.org/) to develop the interface. 

We reccomend using a virtual environment when running the Sleep Science Viewer.

In the install folder type. python SleepScienceViewer.py

### Dependencies
Program developed with python 3.12 with PySide6 used for developing the interface. See [Requirements.txt ](requirements.txt)for additional dependencies.

### Installing

Clone to local environment. See below for run command.

### Executing program

* How to run the program

```
cd .../Install_Folder/
python SleepScienceViewerApp
```

## Help

Will add as questions are received. 

## Authors

Contributors names and contact info

Dennis A. Dean, II, Phd
dennis.a.dean@gmail.com

## Version History

* 0.1
    * First functioning release


## License

This project is licensed under the GNU Affero General Public License v3.0 License - see the LICENSE.md file for details

## Acknowledgments

The python code extends into a class structure code I wrote when I was at Brigham and Women's Hospital. The
authored Matlab code benefited from feedback received following public release on MATLAB central. The original Matlab
code benefitted from Matlab code developed at Case Western University. 

A refactored version of the [multitaper_spectorgram_python.py](https://github.com/preraulab/multitaper_toolbox/blob/master/python/multitaper_spectrogram_python.py) file was used to provide a multi-taper spectrogram option. 
Information about the method can be found [here](https://prerau.bwh.harvard.edu/multitaper/). 