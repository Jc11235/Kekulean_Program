from random import randint
import time
import copy
import math
import os

from PerfectMatchingData import *
from Face import *
from Vertex import *
from Graph import *
from VertexList import *
from DriverMethods import *
from Output import *
from KekuleanMethods import *
from Checkers import *

from PIL import Image, ImageDraw
from Tkinter import *

#The Main
settings = getSettings()

selection = 0

#print "Len of args:", len(sys.argv)
#print sys.argv
if len(sys.argv) == 2:
	print "in if"
	testConjecture(float(sys.argv[-1]))
	
else:
	while True:
		print "1) Read graph from graph.txt\n2) Get a random Kekulean graph\n3) Create and test random graphs\n4) Create several Kekuleans\n5) Refresh settings\n6) Test Nelson Thm\n7) Find Required Edges\n8) Combine Graphs\n9) View Details of Combined Graphs ***Not Complete***\n10) Test FCConjecture for Graphs with equal number of Faces\n11) Test KKFFConjecture for Graphs with equal number of Faces\n12) Test FFCCConjecture for Graphs with equal number of Faces\n13) Test Conjecture for Graphs with unequal number of Faces ***Not Complete*** \n14) Test Clar-Fries Subset Conjecture \n15) Quit"
		selection = int(raw_input("Selection: "))
		while selection < 0 and selection > 11:
			print "\nInvalid response, please enter a proper selection."
			print "1) Read graph from graph.txt\n2) Get a random Kekulean graph\n3) Create and test random graphs\n4) Create several Kekuleans\n5) Refresh settings\n6) Test Nelson Thm\n7) Find Required Edges\n8) Combine Graphs\n9) View Details of Combined Graphs ***Not Complete***\n10) Test FCConjecture for Graphs with equal number of Faces\n11) Test KKFFConjecture for Graphs with equal number of Faces\n12) Test FFCCConjecture for Graphs with equal number of Faces\n13) Test Conjecture for Graphs with unequal number of Faces ***Not Complete*** \n14) Test Clar-Fries Subset Conjecture \n15) Quit"
			selection = int(raw_input("Selection: "))

		if selection == 1:
			analyzeGraphFromFile()
		elif selection == 2:
			createRandomKekulean()
		elif selection == 3:
			randomIntoFiles()
		elif selection == 4:
			createManyKekuleans()
		elif selection == 5:
			getSettings()
			print 'Settings refreshed!'
		elif selection == 6:
			testKekuleanThms()
		elif selection == 7:
			findRequiredEdges()			
		elif selection == 8:
			combineGraphs()
			removeCombinedDuplicates()
		elif selection == 9:
			analyzeCombinedGraphs()
		elif selection == 10:
			testConjectureSameFaces()
		elif selection == 11:
			testConjectureSameFacesKKFF()
		elif selection == 12:
			testConjectureSameFacesFFCC()
		elif selection == 13:
			testConjectureDifferentFaces()
		elif selection == 14:
			clarSubsetDetermination()
		else:
			sys.exit()

