## Vision

The Sleep Science Viewer aims to reduce the effort required to get started in sleep medicine. Its flexible architecture supports interface development, graph and summary generation, and command-line execution, including integration with computational notebooks. There is also the potential a tool to support different research models (animal and human) as wel as supporting interdisciplinary research (experimentation, data analysis, modeling, and machine learning/AI)

Advances in open-source software have enabled the rapid development of a multi-featured sleep stage viewer and data analysis engine. Central to this tool are visualizations that help users gain deeper insights into their data.

## Design Approach

### Feature Selection Principles

- What is the minimal set of visualizations required to effectively view the data?
- Does the tool provide end-to-end support from data selection through result generation and publication?
- Are there interactive elements that deepen users' understanding of the data?

### Release Strategy

Development follows a continuous release model, with each update introducing new or enhanced features. Each screen offers a new or refined view of the data, often centered around new analysis methods. Core visualization and processing functionality are incorporated into data loaders to support both command-line and headless execution.

### Key Feature Considerations

**Figure Generation**
- Plan for robust figure generation capabilities, as fine-tuning visualization parameters can be time-intensive
- Prioritize implementing Origin-like export options before developing full publication-ready visualization features, supporting customized, publication-quality templates

**Saving Spectral Results**
Work towards extensible and reproducible data formats for generated output.
- **HDF5 Format**: Store all inputs, data links, settings, parameters, and computed outputs, including pre-computed summaries to facilitate cross-participant aggregation
- **Annotated CSV Spectrogram Results**: Provide spectral annotations aligned with sleep stages by time, enabling result merging across participants
- **XML Format**: Consider including analysis parameters and results to improve interoperability with other tools and data management systems

### Research Support
Human and mouse model researchers have reached out with interest. 

Human researchers tend to ask for support for completing specific analysis especially in regards to EEG analysis easier to get started. There is also interest in computing many of the sleep disordered measures provided by the NSRR. 

Mouse model researchers ask about dealing with extremely large files and extending current methods. 

Both groups are enabled by existing MATLAB software. Python enabled software will need to provide capabilities that exceed what is currently possible. 

####Mouse Models####
Here are some links shared with me:
- https://github.com/zekebarger/AccuSleePy
- https://buzsakilab.com/wp/resources/buzcode/
- https://github.com/EtienneCmb/visbrain
- https://cognitive-neuroscience-open-tools.github.io/visbrain/auto_examples/gui_sleep/load_edf.html#sphx-glr-auto-examples-gui-sleep-load-edf-py