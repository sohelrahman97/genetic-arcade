# genetic-arcade

Genetic-Arcade is a python based project that showcases the power of genetic algorithms in a variety of visual environments. 

## Required python modules

The following python modules are needed to run the project:

* pygame
* neat-python
* matplotlib

## Installing modules

  ```sh
pip install pygame
pip install neat-python
pip install matplotlib
  ```
## Running the project
Use python to execute the main python file:

    python3 main.py

The individual modules can also be executed if desired. 

## Neural Network settings
Most of the important settings related to the neural networks can be viewed and changed in the file config-feedforward.txt. 
The codebase is extensively commented and I tried my best to keep the descriptions as simple as possible, so the remaining settings can all the other settings can be changed inside the main codebase.

## Project modules
The entry point of the project is intended to be at main.py, even though I designed the modules to be individually executable too. Doing it through the main.py keeps the flow of execution as intended. I will include a brief description of the modules:
* main.py -> This module has the main-menu. It serves as the base from which the rest of the project runs
* button.py -> A simple module that enables me to tailor-fit buttons for the menu screen as needed.
* flappy_bird.py -> This module does most of the heavy lifting. Everything from rendering the birds to configuring the neural networks and more.
* graph_results.py -> This works with some of the statistical files spewed out from the program and condenses it into output.csv, which is then plotted on the screen with matplotlib.

## Documentation
The neat-python module has a well-written documentation that can be found at:
https://neat-python.readthedocs.io/en/latest/neat_overview.html

Please look at the "NEAT Overview," "Configuration file description," and "Module summaries/statistics" for a quick read of the most important parts.  

## Future improvements
I’m currently working on two new modules for this project. 
* Module 1 will be a predator-prey environment simulation where I will model both groups with movable on screen dots, attached NEAT networks to all of them and have them fight for survival! 
* Module 2 will be a clone of the classic snake game where it will teach itself to play the game like in my flappy bird clone.
* In addition to that, I want to add a visualizer for the neural network itself. Python’s graphviz module will probably be used.