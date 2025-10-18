# Vision
Reducing the effort to get started in sleep medicine is a major goal in developing 
this application. The architecture supports interface development, graph and summary 
generation, and command line execution including working with notebooks.

Advances in open source software make development of a multi-featured sleep stage 
viewer and data analysis engine feasible. Central to the development is including 
visualizations that create deeper understanding.

# Design Roadmap
## Feature Selection Questions
- What is the minimal set of visualizations required to 'see' the data?
- Does the tool assist from data selection to data/results publishing?
- Are there data interactions that assist in developing a deeper understanding of the data?

## Release Approach
- Continuous development and structuring releases around added features
- Screens provide new or developed views of the data, which will likely center around 
  new analysis methods
- Useful functionality and visualizations are pushed into data loaders to support 
  command line and headless execution

## Feature Consideration
- Generating Figures
  - Plan for adequate figure generation in the interface since fine control can be 
    time-consuming
  - Target supporting Origin-like exports prior to publication-ready visualization in 
    the interface. This approach will support individualized publication-ready templates.
- Saving Spectral Results
  - Hierarchical Data Format 5 (HDF5). Include all inputs, links to data, settings, 
    parameters, and computed parameters. Results including pre-computed summaries to 
    facilitate aggregation across individuals.
  - Annotation CSV Spectrogram Results. Spectral result annotation with sleep stages 
    by time allowing for merging results across individuals.
  - XML File. Consider writing analysis parameters and results to an XML file.