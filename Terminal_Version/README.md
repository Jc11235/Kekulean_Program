Kekulean
========
###Overall Version 2.0.0
###Terminal Version 1.1.3

###Fixes
-Fixed several spelling errors in the README.

###Additions
-The user can now test a subset conjecture that looks to see if the faces belong to the Clar set are always a subset of the faces belonging to the Fries set.

-The required edge find method in "analyze a graph from file (1)" has been removed for now.

###Issues
- If the two graphs being combined during Combine Graphs touch at an non-required edge the program will crash. This is currently being worked on to find a way to determine face touchings, not just face overlaps.

###Coming Soon
- Remove duplicates should be universal, not just for combine graphs.

- More bug fixes!!!

Introduction
------------
###What is this program?

The task of finding Kekulean structures (or perfect matchings from a graph theory perspective) in benzenoid graphs (also known as benzene patches, hexagonal systems, to name a few) is an easy-to-understand process but can be very time and labor consuming even with small graphs. On top of this problem, chemical graph theorists are often interested in finding the number of Clar and Fries face of the graph which are indictors of the stability of the patch that the graph represents. Finding all this information accurately can be time consuming and is hard or even impossible to generalize as details seem to be dependent on the structure of the graph.
This program is capable of generating graphs, determining if it is Kekulean, find all possible perfect matchings, determine the Clar and Fries number of each structure and output the results to a PNG file for later review (this makes up modules 1-4). It also has added modules that can be added on at a researcher's discretion based on whatever topic they are working on (this makes up modules 5-quit).

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

###MAC OSX

**Python**

The program is designed to run using Python 2 and is not tested for Python 3. Python should be installed by default on Mac OSX machines but you can update your version of Python by downloading from https://www.python.org/download/.  

You can check if you Python installed and what version by typing python into the terminal. This will bring you into python’s interactive mode. You exit interactive mode by pressing Ctrl+D.


**Pillow**

You can download the source from https://pypi.python.org/pypi/Pillow, extract it, and run python setup.py install from the terminal while in the same directory as the extracted files. If you have pip installed you can run: ```pip install Pillow``` in the terminal. If you do not have pip you can use: ```easy_install Pillow``` in the terminal to install Pillow

###Windows

**Python**

You can download a Windows installer from the https://www.python.org/download/ website. There are installers for both 32-bit and 64-bit processors. If you do not know what version you have (most likely you have 32-bit, especially on older machines), you should download the regular installer (the one that is not labeled as the X86-64 installer (This is the 64-bit processor one)).  If you encounter errors now or later, you may have installed the wrong version and should retry with to the other installer.  You can check to see if python installed, or is installed, by searching your computer for a program called IDLE. This a Python IDE that is packaged with Python and can be used to write and run Python programs.

**Pillow**

You can download a Pillow installer from https://pypi.python.org/pypi/Pillow/2.2.1#downloads and select an installer based on what version of Windows you are running (32-bit processor vs 64-bit processor) and what version of Python you are using (2.7 or 2.6; program is not tested for Python3).
Run the .exe file and follow the on screen instructions.

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
Users can test a conjecture that relates the number of Kekule structures, verticies, and faces of two graphs to their respective Clar and Fries numbers. In theory if we take two graphs with an equal number of verticies, the graph with the greater number of Kekule structures should also have a higher clar number. This program has shown that this is not true. The rest of this module test different dependencies to see when this conjecture would also fail. THere are now several additions to this module, including the ability to test the conjecture with the restriction that not only the number of verticies must be equal, but the number of faces as well.

###Subset Conjecture
Users can test a conjecture stating that the faces belong to the Clar set must be a subset of the faces belonging to the Fries set. This module can be very time intesive and should only be run on machines with at least 8GB of memory dedicated to the program. THis module can handle graphs up to 8X8 in size, but will take several hours to test.

###Future Additions
Future additions to this program, that are not additional conjectures to test, but rather improvments to the overall program are being considered. One such addition would be the ability to remove duplicates from the random graph generator. Another addition being considered would be the ability to interact with the images such as a click-to-add-faces application. This functionality is a ways away but is strongly being considered as it would greatly improve our ability to interact with the graphs rather than hoping the ones we are looking for get randomly generated.

Contact
-------
For additional help, questions, or concerns or improvements you want made about this program, the original lead programmer can be reached at smorgasbordator@gmail.com. The new lead programmer can be reached at jameschapmanuconn@gmail.com. If you are interested in joining our project please feel free to contact me at jameschapmanuconn@gmail.com (any positions would not be paid, but your names would appear on any published papers). Please add Kekulean to the subject line for priority.

###Old versions log
###Overall Version 2.0.0
###Terminal Version 1.1.2
###Bug Fixes
-Fixed an issue with Combine Graphs where the method would immediately break when trying to see if there were graphs already in the combined folders.

###Additions
-Upgraded the settings reader to the new GUI version; this speeds up the program significantly.

###Issues
- If the two graphs being combined during Combine Graphs touch at an non-required edge the program will crash. This is currently being worked on to find a way to determine face touchings, not just face overlaps.

###Coming Soon
- Remove duplicates should be universal, not just for combine graphs.

- More bug fixes!!!
###Version 1.1.0
###Bug Fixes
-Combined Graphs no longer produces graphs that are not Kekulean. You can however view the graphs that were produced in a directory that gets created when the module runs.

###Additions
-You can now view the entire list of combined graphs in Analyze Combined Graphs without exiting the module.

-Combine Graphs will now remove duplicates of each graph combination. Orientation has not been implemented though, so a max of 3 duplicates can still exist (one for each different possible rotation). 

- The FFCC Conjecture module is now finished. The file will give you a result name of vertices_number. The second number is merely for coding purposes and should be ignored.

###Issues
- If the two graphs being combined during Combine Graphs touch at an non-required edge the program will crash. This is currently being worked on to find a way to determine face touchings, not just face overlaps. 

- Because of the remove duplicated feature in combined graphs, when using analyze graphs the file names are no longer in sync with the file reader function and the program will crash. Until the issue is fixed it is advised to not use the Analyze Graphs module. 

###Coming Soon
- The Windows edition should have it text document error fixed.

- More bug fixes!!!

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

