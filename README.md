terminal rendering engine (tre)
================================

overview
--------
terminal rendering engine (tre) is a python-based 3d rendering engine designed to run entirely within a terminal. it processes .obj models and displays them as ascii art using the curses library. the engine provides interactive controls for model rotation, zooming, vertex modification, and texturing. modified models can be saved or exported in .obj format.

features
--------
- accepts .obj file format 
- parses and loads model data into memory using a custom parser
- renders 3d models as ascii art within a terminal using curses
- implements projection algorithms to convert 3d coordinates to 2d ascii positions
- implements interactable 2d ui ascii elements with a 2d renderer 
- supports user-controlled rotation about the x, y, and z axes
- provides zoom in/out functionality via 2d rendered ui
- allows users to modify vertex positions and apply basic texturing
- exports updated models in .obj format with custom python exporter

technical specifications
------------------------
input models:
  - .obj format support 
  - custom python parser converts file data into internal data structures

rendering:
  - uses the curses library to draw ascii art representations of models
  - implements a perspective projection to map 3d vertices to 2d terminal coordinates
  - calculates shading and depth cues based on vertex positions

user interaction:
  - keyboard controls / clickable terminal ui elements allow rotation, zooming, and navigation around the model
  - allows dragging and dropping of vertices in screen space, updating the model
  - realtime update of the ascii textures with clickable terminal ui elements 

model modification and export:
  - vertex positions and ascii texture can be edited
  - modifications are maintained in an internal structure
  - users can save changes or save as a new .obj file with updated vertex data

dependencies
------------
- python (version 3.x)
- curses (built-in on unix-like systems)
- standard python modules for math, file i/o, and data processing (numpy, etc)
- cupy for gpu matrix multiplication (faster) // work in progress


usage
-----
- launch the engine from a terminal window by running cli.py
- load an .obj model via shapesstorage folder (auto gen)
- use mouse interaction to move / scale /rotate model
- apply texture changes through changing color / ascii letter 
- select the save or save-as option to export the modified model to .obj

notes
-----
- terminal rendering engine is intended for unix-like terminal environments (does work in windows powershell)
- performance may vary based on terminal resolution and supported features ( performance i s very bad as it is a 3d engine running in the python terminal, so small models are needed )
- this engine is a proof-of-concept and may require further enhancements for complex models as visual clarity of ascii 3d models is low without scaling 
