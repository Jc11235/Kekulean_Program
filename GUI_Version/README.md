Kekulean
========
###Overall Version 2.0.0
###GUI Version 1.0.0

Welcome to version 2.0.0! This version of the Kekulean program adds a windowed GUI system to make the process of doing this research simpler and easier to use for not only the experienced researcher but the citizen scientist as well. 

Please feel free to email me at the email listed at the end of this README if you encounter any issues with this version. Considering the extent of the upgrade there are bound to be some. However, it has been rigorously tested and is in working condition.

###Additions

-Version 2.0.0 is now released!

-All modules that create random graphs are now several times faster with the rewrite of how their settings are established.

-NOTICE: THIS EDITION IS NOT SUPPORTED FOR MAC OR WINDOWS YET, ONLY LINUX.

Introduction
------------
###What is this program?

The task of finding Kekulean structures (or perfect matchings from a graph theory perspective) in benzenoid graphs (also known as benzene patches, hexagonal systems, to name a few) is an easy-to-understand process but can be very time and labor consuming even with small graphs. On top of this problem, chemical graph theorists are often interested in finding the number of Clar and Fries face of the graph which are indictors of the stability of the patch that the graph represents. Finding all this information accurately can be time consuming and is hard or even impossible to generalize as details seem to be dependent on the structure of the graph.
This program is capable of generating graphs, determining if it is Kekulean, find all possible perfect matchings, determine the Clar and Fries number of each structure and output the results to a PNG file for later review (this makes up modules 1-4). It also has added modules that can be added on at a researchers discretion based on whatever topic they are working on (this makes up modules 5-quit).

###Technical Details of the program

The program is written in Python and is entirely open-source to better help others in field quickly test graphs and find properties of them without the time-consuming effort that is involved in manually replicating the process.  This program is run using Python 2. You must have at least version 2.6 as that verison introduced multiprocessing
To run the program, run ‘Kekulean.py’ by double-clicking it or via the terminal/command line
There is one outside dependency that is not included with the .zip of the program. The Pillow library provides the functionally to create PNG of the results of the programs. Pillow is needed in order for the program to run.
For most users, the Clar-Fries differential that is calculated may seem foreign as it is a property that I invented to relate the stability of a particular patch. This is a snapshot of a particular resonance structure of the graph, and the overall Clar-Fries differential has not been determined yet.

Installation
------------
###LINUX

**Python**

The program is designed to run using Python 2 and is not tested for Python 3. Python should be installed by default on Linux machines but you can update your version of Python by downloading from https://www.python.org/download/.  You can also use: ```sudo apt-get install python``` to update to the latest version, if you are on an Ubuntu/Ubuntu-based system.
You can check if you Python installed and what version by typing python into the terminal. This will bring you into python’s interactive mode. You exit interactive mode by pressing Ctrl+D.

**Pillow**

Fedora, Debian/Ubuntu, and ArchLinux all come with Pillow installed in place of the Python Imaging Library (PIL).  Debian/Ubuntu systems can install Pillow using the terminal command: ```sudo apt-get install python-dev python-setuptools``` 


How to use this program
-----------------------
The program allows the user to analyze benzenoid graphs and determine properties such as whether a graph is Kekulean, the number of Kekulean structures, and the Clars and Fries numbers of the graph.  Input and textual output are given using a coordinate based on the faces of the graph and will be explained later on in this section. 

###Analyze graph from text file
The first option in the program is to read a graph from ‘graph.txt’ and determine properties of said graph. It will tell you the graph is Kekulean, the number of Kekulean structures, and the Clars and Fries numbers. It will ask the user how they want the structures organized and display user-specified graphs. It also outputs all the structures to two PNG files, each one ranked according to Clars numbers or Fries numbers. Please note that the outputted PNGs will overwrite older ones so you should back up any files you want to save.  

###Analyze random Kekulean graph
The second option creates a randomly generated Kekulean graph. The program then analyzes it much like the above mentioned option. Please note that the outputted PNGs will overwrite older ones so you should back up any files you want to save.  

###Create and test random graphs
The third option will create a user-specified number of randomly-generated graphs and then test to see if which ones are Kekulean or not.  Output is saved in the ‘Kekuleans.txt’ and ‘nonKekuleans.txt’ using the coordinate system that will be described later in this section.

###Create several Kekuleans
This fourth option creates a user-specified number of randomly-generated Kekulean graphs. It does not export the graphs to a PNG or text file.  This option is only recommend if you want to create a lot of graphs and find which one has the most Clars/Fries faces.

###Refresh Settings
Users can edit the properties that randomly generated graphs will have by editing ‘settings.txt’.  You should only change the numbers in the text file.  Normally this file is read only at the beginning of the program. If you change the numbers in ‘settings.txt’ and wish for your changes effect the program right away, selecting this option will update the random generation with the new settings mid-runtime.

###Find Required Edges
Users can search for required edges in a aprticular graph. Required edges are edages that are part of the edge set K (or double bonds if you are a chemist) that exist in all Kekule structures (resonance structures) of the graph. These can play a huge role when combining two graphs at required edges (you would be combining the graphs where each has a required edge).

###Combine Graphs
In theory, one can combine two graphs together at each other required edge to obtain a graph that will always be Kekulean. The program will create PNGs and put them in a directory called CombineGraphs. The resulting PNG should be that of the Kekule structure of the combined graph that contains the most Clar faces. THere have been instances where this was not the case however and we are working to fix this. This aspect of the program is still under heavy development and results may not be 100% accurate. We are also working to remove duplicated from the CombinedGraph directory. See Combined Graph details for more information.

###Combine Graphs Details
This portion of the program will ask the user which graph, out of all the combined graphs in CombinedGraphs, they would like to view. The program will then display details of the graphs and will also ask the user which kekule structure they would like t view. An image will be displayed that contains the Kekule structure, all bonds including required edges, and any Clar and Fries faces that structure contains.

###Test Conjecture
Users can test a conjecture that relates the number of Kekule structures, verticies, and faces of two graphs to their respective Clar and Fries numbers. In theory if we take two graphs with an equal number of verticies, the graph with the greater number of Kekule structures should also have a higher clar number. This program has shown that this is not true. The rest of this module test different dependencies to see when this conjecture would also fail. These different dependencies are still under development and results should not be trusted to be 100% accurate.

###Future Additions
Future additions to this program, that are not additional conjectures to test, but rather improvments to the overall program are being considered. One such addition would be the ability to remove duplicates from the random graph generator. Another addition being considered would be the ability to interact with the images such as a click-to-add-faces application. This functionality os a ways away but is strongly being considered as it would greatly improve our ability to interact with the graphs rather than hoping the ones we are looking for get randomly generated.

Contact
-------
For additional help, questions, or concerns or improvements you want made about this program, the original lead programmer can be reached at smorgasbordator@gmail.com. The new lead programmer can be reached at jameschapmanuconn@gmail.com. If you are interested in joining our project please feel free to contact me at jameschapmanuconn@gmail.com (any positions would not be paid, but your names would appear on any published papers). Please add Kekulean to the subject line for priority.

###Old versions log
###Version 1.0.2
###Bug Fixes
- Fixed an error where superGraph.txt would print
the graph starting on line 2 if the minimum y coordinate never equaled zero

###Additions
- Added PNGs for the graphs that are combined to make the super graph. These will be located in the CombinedGraphs directory.

###Issues
- If the two graphs being combined during COmbine Graphs touch at an non-required edge the program will crash. This is currently being worked on to find a way to determine face touchings, not just face overlaps. 

- Combine Graphs occasionally generates a super graph that did not combine at a required edge. We have no idea why this does this but we are looking into it. 

###Coming Soon
- Combine Graphs will have the ability to remove duplicated from the directory.

- The Windows edition should have it text document error fixed.

- Analyze Combined Graphs will have the ability to view the next graph after quitting the first graph.

- The FFCC method should be ready.

- More bug fixes!!!

