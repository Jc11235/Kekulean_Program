from PerfectMatchingData import *
from Face import *
from Vertex import *
from Graph import *
from VertexList import *
from Output import *
from KekuleanMethods import *
from Checkers import *
from RequiredEdgeMethods import *
from Tkinter import *
from AppInformation import *


from random import randint
import time
import os
import shutil
import multiprocessing as mp
import threading

Break = False
BreakLoop = False
#These methods the main drivers of the program. Some of their helper methods are also present here.
settings = {}

#function that reads in the graph returns a 2D string list of the graph

def getInput(fileName):
	faceGraph = []
	inputFile = open(fileName, 'r')
	
	row = inputFile.readline()
	y = 0
	while len(row) > 0:
		row = row.replace('\n', '')
		row = row.split(" ")		
		
		for i in range(len(row)):
			x = row[i]
			faceGraph.append((Face(int(x), y)))

		row = inputFile.readline()
		y += 1
		
	inputFile.close()
		
	return faceGraph

def getSettings():
	
	fileName = "settings.txt"

	inputFile = open(fileName, 'r')
		
	lineNumber = 0

	minW = 0
	maxW = 0
	minH = 0
	maxH = 0

	line = inputFile.readline()
	while len(line) > 0:
		line = line.replace('\n', '')

		settings[lineNumber] = float(line)

		line = inputFile.readline()
		lineNumber += 1
	inputFile.close()

def resetGraph(root,appInfo,submitGraph,graphNumberEntry,view):

	submitGraph.destroy()
	view.destroy()
	graphNumberEntry.destroy()


def analyzeGraph(root,appInfo):		

	root.geometry("600x400")

	selection = StringVar()

	choiceEntry = Entry(root, textvariable = selection)	

	choice = selection.get()	
		
	def callback(root,appInfo,choice,selection,choiceEntry,fileName = "graph.txt"):

		loading = Label(root, text="Analyzing graph data, this may take a few minutes.")
		loading.pack()				

		fileName = fileName
		faceGraph = getInput(fileName)

			#check for connectedness
		connected = isConnected(faceGraphToInts(faceGraph))			
			
		if connected == True:

			vertexGraph = makeVertexGraph(faceGraph)

			superGraph = Graph(faceGraph, vertexGraph)

			structures = assignMatching(superGraph)

			_findRequiredEdges(structures)

			loading.destroy()

			choiceEntry.pack()

			typeSelection = Label(root, text="Would you like to view the graphs ranked by Fries or Clars?")
			typeSelection.pack()

			submit = Button(root, text ="Submit", command = lambda: userInputStructures(root,appInfo,structures,choice,submit,typeSelection,choiceEntry))
			submit.pack(side = BOTTOM)	

			while True:
				choice = selection.get()

				flag = False
				exit = False

				if choice != 'fries' and choice != 'clars' and choice != "":
					againSelection = Label(root, text="That file does not exist, please try again.")
					againSelection.pack()
					print "again"
					flag = True
				
				while choice != 'fries' and choice != 'clars':
					submit.update_idletasks()
					choiceEntry.update_idletasks()
					typeSelection.update_idletasks()
					againSelection.update_idletasks()

					choice = selection.get()

				if exit == True:
					againSelection.destroy()
					break

				submit.update_idletasks()
				choiceEntry.update_idletasks()
				typeSelection.update_idletasks()								
				
	t = threading.Thread(target = lambda: callback(root,appInfo,choice,selection,choiceEntry))
	t.setDaemon(True)
	appInfo.setThreads(t)
	t.start()

def userInputStructures(root,appInfo,structures,choice,submit,typeSelection,choiceEntry):	

	structureNumber = IntVar()
	submit.destroy()
	typeSelection.destroy()
	choiceEntry.destroy()

	def displayClarFries(structureNumber,structures,choice):
		structures.sort()

		if choice == 'clars':
			Graph.comparison = 'clars'
				
		elif choice == 'fries':
			Graph.comparison = 'fries'

		structures.reverse()
			
		structures[structureNumber].displayGraph()

	view = Label(root, text="There are " + str(len(structures)) + " distince Kekule structures avaiable. Which would you like to view?")
	view.pack()

	graphNumberEntry = Entry(root, textvariable = structureNumber)
	graphNumberEntry.pack()

	number = structureNumber.get()

	submitGraph = Button(root, text ="Submit Structure", command = lambda: displayClarFries(number,structures,choice))
	submitGraph.pack(side = BOTTOM)

	def deleteB(button):
		button.destroy()

	reset = Button(root, text ="Quit", command = lambda: resetB(root,appInfo,submitGraph,graphNumberEntry,view))
	reset.pack(side = BOTTOM)

	def resetB(root,appInfo,submitGraph,graphNumberEntry,view):
		deleteB(reset)
		resetGraph(root,appInfo,submitGraph,graphNumberEntry,view)

#A user-entered number of graphs are generated and tested for Kekulean-ness and written to their proper text files
def randomIntoFiles():
	kekuleanFile = open("Kekuleans.txt", "w")
	notKekuleanFile = open("NotKekulean.txt", "w")
	
	numK = 0
	numNotK = 0
	
	trials = int(raw_input("How many graphs would you like to create? "))
	print "\n" #just to provide some visual space	
	
	t1 = time.time()

	for i in range(trials):
		faceGraph = createRandomConnectedGraph()
		vGraph = makeVertexGraph(faceGraph)
		randGraph = Graph(faceGraph, vGraph)

		if isKekulean(randGraph) == True:
			numK += 1
			
			kekuleanFile.write("Graph #" + str(numK) + "\n")
			kekuleanFile.write(randGraph.simpleToString() + '\n')
		else:
			numNotK += 1
			
			notKekuleanFile.write("Graph #" + str(numNotK) + "\n")
			notKekuleanFile.write(randGraph.simpleToString() + '\n')
		#print randGraph
		#print "\n"

	t2 = time.time()

	print "\n" + str(numK) + " Kekulean graph(s) were found.\n" + str(numNotK) + " non-Kekulean graph(s) were found."
	print "Time elapsed (in seconds): " + str(t2 - t1) + "\n"
	kekuleanFile.close()
	notKekuleanFile.close()

#creates a random Kekulean graph ands does stuff with it and saves it to an png		
def createRandomKekulean():
	#creates a face graphs
	randomFaces = createRandomGraph()

	randomGraph = _createRandomKekulean()

	print "There are", len(randomGraph.getVertexGraph()), "vertices"

	graphs = assignMatching(randomGraph)
	graphs.sort()

	if len(graphs) > 0:
		#save graphs as PNG file
		savePNG(graphs, "graphs - Fries.png")

		Graph.comparison = 'clars'
		graphs.sort()

		savePNG(graphs, "graphs - Clars.png")

		while True:
			choice = raw_input("Would you like to view the graphs ranked by Fries or Clars? (or quit?) ")
			while choice.lower() != 'fries' and choice.lower() != 'clars' and choice.lower() != 'quit':
				choice = raw_input("Would you like to view the graphs ranked by Fries or Clars? (or quit?) ")
			if choice.lower() == 'clars':
				Graph.comparison = 'clars'

			elif choice.lower() == 'fries':
				Graph.comparison = 'fries'

			else:
				break
					
			graphs.sort()
			graphs.reverse()
			
			print "There are", len(graphs), "Kekulean structures"
			displayGraphs(graphs)
		
	else:
		print "error - Graph is Kekulean but has no perfect matching - see error.txt for graph"
		errorFile = open("error.txt", "w")
		errorFile.write(randomGraph.simpleToString() + '\n')

#Creates a random planar graph, which may not be connected			
def createRandomGraph():

	height = randint(settings[2], settings[3])
	
	randGraph = []
	for i in range(height):
		rowLength = randint(settings[0], settings[1])
		row = getRow(rowLength, i)
		while len(row) == 0:
			row = getRow(rowLength, i)
		randGraph.extend(row)
	
	if checkAlignment(randGraph) == False:
		randGraph = createRandomGraph()
	return randGraph

def checkAlignment(graph):
	for face in graph:
		if face.getX() == 0:
			break
	else:
		#there is no face on the y-axis
		return False
	for face in graph:
		if face.getY() == 0:
			break
	else:
		#there is no face on the x-axis
		return False
	#there is a face on the x-axis
	return True

def createRandomConnectedGraph():
	g = createRandomGraph()
	while isConnected(faceGraphToInts(g)) == False:
		g = createRandomGraph()

	return g

#generates a row for the the createRandomGraph method
def getRow(rl, rowNum):
	r = []
	for j in range(rl): 
			chance = randint(0, 100)
			if chance > settings[4] * 100:
				r.append(Face(j, rowNum))
	return r

def _createRandomKekulean():
	#creates a face graphs
	randomFaces = createRandomGraph()

	while isConnected(faceGraphToInts(randomFaces)) == False:
		randomFaces = createRandomGraph()

	vertexGraph = makeVertexGraph(randomFaces)
	randomGraph = Graph(randomFaces, vertexGraph)

	while isKekulean(randomGraph) == False:
		#print "making K"
		randomFaces = createRandomGraph()
		while isConnected(faceGraphToInts(randomFaces)) == False:
			randomFaces = createRandomGraph()

		vertexGraph = makeVertexGraph(randomFaces)
		randomGraph = Graph(randomFaces, vertexGraph)

	if isKekulean(randomGraph):
		return randomGraph
	else:
		return _createRandomKekulean()

def createManyKekuleans():
	graphs = [] #list of kekulean graphs 
	graphList = [] #list of the Kekulean graphs with their matchings, and Fries/Clars Faces 
	trials = int(raw_input("How many graphs would you like to create? "))

	pool = mp.Pool(mp.cpu_count())
	results = [pool.apply_async(_createRandomKekulean) for x in range(trials)]
	graphs = [r.get() for r in results]

	for g in graphs:
		graphList.extend(assignMatching(g))

	graphList.sort()

	if len(graphList) > 0:
		print "There are", len(graphList), "Kekulean structures"
		displayGraphs(graphList)

def testKekuleanThms():
	conflictFile = open("conflict.txt", "w")

	interval = float(raw_input("How many hours would you like to run the program?"))

	timeLimit = 3600 * interval
	print "limit:", timeLimit

	t1 = time.time()
	t2 = time.time()

	counter = 0
	while t2 - t1 < timeLimit:
		print "graph #" + str(counter)

		#creates a face graphs
		randomFaces = createRandomGraph()
		vertexGraph = []

		#Finds connected graph
		while len(vertexGraph) % 2 != 0 or len(vertexGraph) == 0 or countPeaksAndValleys(randomFaces) == False or isConnected(faceGraphToInts(randomFaces)) == False: 
			randomFaces = createRandomGraph()
			vertexGraph = makeVertexGraph(randomFaces)	

		randomGraph = Graph(randomFaces, vertexGraph)

		nelsonThm = isOldKekulean(randomGraph)
		perfectMatchingThm = isKekulean(randomGraph)

		if nelsonThm != perfectMatchingThm:
			
			conflictFile.write("Perfect matching: " + str(perfectMatchingThm) + " Nelson Thm: " + str(nelsonThm) + "\n")
			conflictFile.write(randomGraph.simpleToString())
			conflictFile.write("\n") 

		t2 = time.time()
		counter += 1
	conflictFile.close()

#takes a row and returns a the number of vertical edges in that row
def getRowEdgeCount(row):
	edgeCount = 0
	f = 0
	for i in range(len(row)):
		edgeCount += 1
		try:
			f = row[i+1]
		except:
			f = None
		if row[i] + 1 != f or f == None:
			edgeCount += 1
	return edgeCount

def getMinRows(g):
	minRows = {}
	index = 0
	minEdges = sys.maxint
	for r in g:
		edgeCount = getRowEdgeCount(r)
		if edgeCount < minEdges:
			minEdges = edgeCount
			minRows.clear()
			minRows[index] = r
		elif edgeCount == minEdges:
			minRows[index] = r
		index += 1
	return minRows
	
#counts up the number of peaks above each row and stores those values in a list at indexes that correspond to the the row of the graph
def getPeaksAboveRows(g):

	peaksAboveRow = [0]*(len(g))
	
	for r in range(len(g)):
		#print "r: " + str(r)
		row = g[r]
		if r > 0:
			peaksAboveRow[r] += peaksAboveRow[r-1]
		for col in range(len(row)):
			face = row[col]
			if searchRow(face, True, g, r) == True:
				peaksAboveRow[r] += 1
				#print "Peak at: " + str(r) + ", " + str(col)
			if searchRow(face, False, g, r) == True and r < len(g)-1:
				peaksAboveRow[r+1] -= 1
				#print "Valley at: " + str(r) + ", " + str(col)
			peaksAboveRow[r] = abs(peaksAboveRow[r])
				
	return peaksAboveRow
	
#Theorem I devoloped
def NelsonThm(peaks, g):
	kekulean = True
	minRows = getMinRows(g)
	for i, row in minRows.items():
		if peaks[i] > getRowEdgeCount(row):
			kekulean = False
			break
	return kekulean
	
#ckesks of a graph is Kekulean and returns a boolean
def isOldKekulean(graph):
	fg = faceGraphToInts(graph.getFaceGraph())	

	peaksAbove = getPeaksAboveRows(fg)
	#print peaksAbove
	
	kekulean = NelsonThm(peaksAbove, fg)
		
	return kekulean

def getUpperBounds(graph):
	#faceGraph = getInput(filename)
	#vertexGraph = makeVertexGraph(faceGraph)

	#graph = Graph(faceGraph, vertexGraph)

	kekulean = isKekulean(graph)
	if kekulean == True: 
		rowCount = [0] * graph.getNumberOfRows()
		whiteCount = [0] * graph.getNumberOfRows()
		blackCount = [0] * graph.getNumberOfRows()

		print "len:", len(whiteCount)

		for v in graph.getVertexGraph():
			#even y numbers mean the vertex is marked white on the graph
			if v.getY() % 2 == 0:
				index = v.getY() / 2
				if index < len(whiteCount):
					whiteCount[index] += 1
			#The else implies that the vertex's y is odd, and thus the verex is marked black 
			else:
				index = (v.getY() - 1) / 2
				if index < len(blackCount):
					blackCount[index] += 1

		print "Upper Bonds of the graph per row:"
		for index in range(len(rowCount)):
			count = abs(sum(whiteCount[0:index+1]) - sum(blackCount[0:index+1]))
			print count
			rowCount[index] = count

		totalUpperBonds = sum(rowCount)
		print "Upper bond of the graph:", totalUpperBonds


	else:
		print "The graph is not Kekulean"

def testConjectureSameFaces(root,interval):
	global Break
	Break = False

	quit = Button(root, text ="Quit", command = BreakModule)
	quit.pack(side = LEFT)

	scrollbar = Scrollbar(root)
	scrollbar.pack(side = RIGHT, fill = Y)

	text = Text(root,yscrollcommand = scrollbar.set)
	text.pack()

	scrollbar.config(command = text.yview)

	graphList = []
	graphNumber = 0
	counter = 0

	timeLimit = 3600 * interval

	t1 = time.time()
	t2 = time.time()

	while t2 - t1 < timeLimit:

		if Break == True:
			Break = False
			quit.destroy()
			break

		text.insert(CURRENT, "Graph " + str(graphNumber) + "\n")

		#creates a face graphs
		randomFaces = createRandomGraph()
		vertexGraph = []

		#Finds connected graph
		while len(vertexGraph) % 2 != 0 or len(vertexGraph) == 0 or countPeaksAndValleys(randomFaces) == False or isConnected(faceGraphToInts(randomFaces)) == False: 
			randomFaces = createRandomGraph()
			vertexGraph = makeVertexGraph(randomFaces)	

		randomGraph = Graph(randomFaces, vertexGraph)

		perfectMatchingThm = isKekulean(randomGraph)

		if perfectMatchingThm == True:
			structures = assignMatching(randomGraph)
			
			#must be 'fries' or 'clars'
			Graph.comparison = 'clars'
			structures.sort()

			h = structures[-1]
			h.setNumStructures(len(structures))
			h.setFaces(getNumFaces(faceGraphToInts(randomFaces)))
			#h.setString(structures[0].simpleToString())

			#is the data right?
			#print "Verts:", h.getNumVertices()
			#print "Structures:", h.getNumStructures()
			#print "Clar:", h.getFriesNumber()

			for g in graphList:
				if(h.getFaces() == g.getFaces()):
					if h.getNumVertices() == g.getNumVertices() :#and h.getNumVertices() <= 26:
						if h.getNumStructures() < g.getNumStructures():
#first part
							if h.getClarsNumber() > g.getClarsNumber():
								print 'Conjecture is false:'
						
								drawConflictsCC(g, h)
									#only adds graphs to list if it under some number of vertices
			graphList.append(h)

		t2 = time.time()

		counter += 1
		graphNumber += 1

		text.update_idletasks()
		quit.update_idletasks()
		scrollbar.update_idletasks()

	text.destroy()
	scrollbar.destroy()
	quit.destroy()
#second part
def testConjectureSameFacesKKFF(root, interval):
	global Break
	Break = False

	quit = Button(root, text ="Quit", command = BreakModule)
	quit.pack(side = LEFT)

	scrollbar = Scrollbar(root)
	scrollbar.pack(side = RIGHT, fill = Y)

	text = Text(root,yscrollcommand = scrollbar.set)
	text.pack()

	scrollbar.config(command = text.yview)

	graphList = []
	graphNumber = 0
	counter = 0

	timeLimit = 3600 * interval

	t1 = time.time()
	t2 = time.time()

	while t2 - t1 < timeLimit:

		if Break == True:
			Break = False
			quit.destroy()
			break

		text.insert(CURRENT, "Graph " + str(graphNumber) + "\n")

		#creates a face graphs
		randomFaces = createRandomGraph()
		vertexGraph = []

		#Finds connected graph
		while len(vertexGraph) % 2 != 0 or len(vertexGraph) == 0 or countPeaksAndValleys(randomFaces) == False or isConnected(faceGraphToInts(randomFaces)) == False: 
			randomFaces = createRandomGraph()
			vertexGraph = makeVertexGraph(randomFaces)	

		randomGraph = Graph(randomFaces, vertexGraph)

		perfectMatchingThm = isKekulean(randomGraph)

		if perfectMatchingThm == True:
			structures = assignMatching(randomGraph)
			
			#must be 'fries' or 'clars'
			Graph.comparison = 'fries'
			structures.sort()

			h = structures[-1]
			h.setNumStructures(len(structures))
			h.setFaces(getNumFaces(faceGraphToInts(randomFaces)))

			clarNumberStructure = []
			friesNumberStructure = []
	
			for g in graphList:			

				if(h.getFaces() == g.getFaces()):
					if h.getNumVertices() == g.getNumVertices() :#and h.getNumVertices() <= 26:
						if h.getNumStructures() < g.getNumStructures():

							if h.getFriesNumber() > g.getFriesNumber():
								
								drawConflictsKKFF(g, h)			
			#only adds graphs to list if it under some number of vertices
			graphList.append(h)

		t2 = time.time()

		counter += 1
		graphNumber += 1

		text.update_idletasks()
		quit.update_idletasks()
		scrollbar.update_idletasks()

	text.destroy()
	scrollbar.destroy()
	quit.destroy()

def testConjectureSameFacesFFCC(root, interval):
	clarNumberStructures = []
	friesNumberStructures = []
	graphs = []
	graphList = []

	temp = 0
	graphNumber = 0
	counter = 0

	global Break
	Break = False

	quit = Button(root, text ="Quit", command = BreakModule)
	quit.pack(side = LEFT)

	scrollbar = Scrollbar(root)
	scrollbar.pack(side = RIGHT, fill = Y)

	text = Text(root,yscrollcommand = scrollbar.set)
	text.pack()

	scrollbar.config(command = text.yview)

	timeLimit = 3600 * interval

	t1 = time.time()
	t2 = time.time()

	while t2 - t1 < timeLimit:

		if Break == True:
			Break = False
			quit.destroy()
			break

		text.insert(CURRENT, "Graph " + str(graphNumber) + "\n")

		#creates a face graphs
		randomFaces = createRandomGraph()
		vertexGraph = []

		#Finds connected graph
		while len(vertexGraph) % 2 != 0 or len(vertexGraph) == 0 or countPeaksAndValleys(randomFaces) == False or isConnected(faceGraphToInts(randomFaces)) == False: 
			randomFaces = createRandomGraph()
			vertexGraph = makeVertexGraph(randomFaces)	

		randomGraph = Graph(randomFaces, vertexGraph)

		perfectMatchingThm = isKekulean(randomGraph)

		if perfectMatchingThm == True:
			structures = assignMatching(randomGraph)

			randomGraph.setMaxClarManual(setMaxClar(randomGraph))
			randomGraph.setMaxFriesManual(setMaxFries(randomGraph))

			h = structures[-1]

			graphs.append(randomGraph)

			h.setMaxClarManual(setMaxClar(randomGraph))
			h.setMaxFriesManual(setMaxFries(randomGraph))		

			h.setNumStructures(len(structures))
			h.setFaces(getNumFaces(faceGraphToInts(randomFaces)))

			graphCount = 0
			graphNumber += 1

			for g in graphList:

				if(g.getFaces() == h.getFaces()):

					if g.getNumVertices() == h.getNumVertices():

						if g.getNumStructures() < h.getNumStructures():	

							if g.getMaxClar() > h.getMaxClar():

								if g.getMaxFries() < h.getMaxFries():

									print 'Conjecture is false:\n'

									saveClarFaceFFCC(graphs[graphCount],randomGraph,temp)
									saveFriesFaceFFCC(graphs[graphCount],randomGraph,temp)

									folderName = "FFCCConjectureConflicts"

									fileName = folderName + "/" + str(randomGraph.getNumVertices()) + "_" + str(temp)+ "/info" + ".txt" 

									f = open(fileName,'w')							
									f.write("C1: " + str(g.getMaxClar()) + " C2: " + str(h.getMaxClar()) + " F1: " + str(g.getMaxFries()) + " F2: " + str(h.getMaxFries()) + "\n")
									f.write(str(faceGraphToInts(g.getFaceGraph())) + "\n")
									f.write(str(faceGraphToInts(h.getFaceGraph())) + "\n")
									f.close()

									temp += 1
				graphCount += 1
			#only adds graphs to list if it under some number of vertices
			graphList.append(h)
		t2 = time.time()
		counter += 1
		
def setMaxFries(graph):
	g = graph.getFaceGraph()

	v = makeVertexGraph(g)

	G = Graph(g,v)

	structures = assignMatching(G)

	Graph.comparison = 'fries'
	structures.sort()

	return structures[-1].getFriesNumber()

def setMaxClar(graph):
	g = graph.getFaceGraph()

	v = makeVertexGraph(g)

	G = Graph(g,v)

	structures = assignMatching(G)

	Graph.comparison = 'clars'
	structures.sort()

	return structures[-1].getClarsNumber()

def saveClarFaceFFCC(graph1,graph2,count):
	g1 = graph1.getFaceGraph()
	g2 = graph2.getFaceGraph()

	v1 = makeVertexGraph(g1)
	v2 = makeVertexGraph(g2)

	G1 = Graph(g1,v1)
	G2 = Graph(g2,v2)


	structures1 = assignMatching(G1)
	structures2 = assignMatching(G2)

	Graph.comparison = 'clars'
	structures1.sort()
	structures2.sort()

	h1 = structures1[-1]
	h2 = structures2[-1]

	if not os.path.exists("FFCCConjectureConflicts"):
		os.mkdir("FFCCConjectureConflicts")
	folderName = "FFCCConjectureConflicts/" + str(G1.getNumVertices()) + "_" + str(count)

	#setup folder
	if not os.path.exists(folderName):
		os.mkdir(folderName)
			#print "adding"
	fileName1 = folderName + "/clar1" + ".png"
	fileName2 = folderName + "/clar2" + ".png"
			#print fileName1
	saveSinglePNG(h1,fileName1)
	saveSinglePNG(h2,fileName2)

def saveFriesFaceFFCC(graph1,graph2,count):

	g1 = graph1.getFaceGraph()
	g2 = graph2.getFaceGraph()

	v1 = makeVertexGraph(g1)
	v2 = makeVertexGraph(g2)

	G1 = Graph(g1,v1)
	G2 = Graph(g2,v2)


	structures1 = assignMatching(G1)
	structures2 = assignMatching(G2)

	Graph.comparison = 'fries'
	structures1.sort()
	structures2.sort()

	h1 = structures1[-1]
	h2 = structures2[-1]

	if not os.path.exists("FFCCConjectureConflicts"):
		os.mkdir("FFCCConjectureConflicts")
	folderName = "FFCCConjectureConflicts/" + str(G1.getNumVertices()) + "_" + str(count)

	#setup folder
	if not os.path.exists(folderName):
		os.mkdir(folderName)
			#print "adding"
	fileName1 = folderName + "/fries1" + ".png"
	fileName2 = folderName + "/fries2" + ".png"
			#print fileName1
	saveSinglePNG(h1,fileName1)
	saveSinglePNG(h2,fileName2)

def testConjectureDifferentFaces(hours=0):
	graphList = []
	results = open("results.txt", "w")
	results.write("The program actually run!")

	if hours == 0:
		interval = float(raw_input("How many hours would you like to run the program? "))
	else:
		interval = hours

	timeLimit = 3600 * interval
	print "limit:", timeLimit

	t1 = time.time()
	t2 = time.time()

	counter = 0
	while t2 - t1 < timeLimit:
		print "graph #" + str(counter)

		#creates a face graphs
		randomFaces = createRandomGraph()
		vertexGraph = []

		#Finds connected graph
		while len(vertexGraph) % 2 != 0 or len(vertexGraph) == 0 or countPeaksAndValleys(randomFaces) == False or isConnected(faceGraphToInts(randomFaces)) == False: 
			randomFaces = createRandomGraph()
			vertexGraph = makeVertexGraph(randomFaces)	

		randomGraph = Graph(randomFaces, vertexGraph)

		perfectMatchingThm = isKekulean(randomGraph)

		if perfectMatchingThm == True:
			structures = assignMatching(randomGraph)

			for f in randomGraph.getFaceGraph():
				pairs = randomGraph.getBondedVertices(f)
				print str(pairs)
			
			#must be 'fries' or 'clars'
			Graph.comparison = 'clars'
			structures.sort()

			h = structures[-1]
			h.setNumStructures(len(structures))
			#h.setString(structures[0].simpleToString())

			#is the data right?
			#print "Verts:", h.getNumVertices()
			#print "Structures:", h.getNumStructures()
			#print "Clar:", h.getFriesNumber()

			for g in graphList:
				if h.getNumVertices() == g.getNumVertices() :#and h.getNumVertices() <= 26:
					if h.getNumStructures() < g.getNumStructures():

#first part
						if h.getClarsNumber() > g.getClarsNumber():
							print 'Conjecture is false:'
								
							results.write('\ngraph H: Clars: ' + str(h.getClarsNumber()) + " Number of Structures: " + str(h.getNumStructures()) + " Number of vertices: " + str(h.getNumVertices()) + "\n") 
							results.write(str(h))
							results.write('\ngraph G: Clars: ' + str(g.getClarsNumber()) + " Number of Structures: " + str(g.getNumStructures()) + " Number of vertices: " + str(g.getNumVertices()) + "\n") 
							results.write(str(g))
							results.write("\n\n")

							drawConflictsCC(g, h)
#second part

						if h.getFriesNumber() > g.getFriesNumber():
							print 'Conjecture is false:'
							results.write('\ngraph H: Fries: ' + str(h.getFriesNumber()) + " Number of Structures: " + str(h.getNumStructures()) + " Number of vertices: " + str(h.getNumVertices()) + "\n") 
							results.write(str(h))
							results.write('\ngraph G: Fries: ' + str(g.getFriesNumber()) + " Number of Structures: " + str(g.getNumStructures()) + " Number of vertices: " + str(g.getNumVertices()) + "\n") 
							results.write(str(g))
							results.write("\n\n")
	
							drawConflictsKKFF(g, h)
#third part
						if h.getClarsNumber() > g.getClarsNumber():  
							if h.getFriesNumber() < g.getFriesNumber():
								print 'Conjecture is false:'
								results.write('\ngraph H: Clars: ' + str(h.getClarsNumber()) + "graph H: Fries: " + str(h.getFriesNumber()) + " Number of Structures: " + str(h.getNumStructures()) + " Number of vertices: " + str(h.getNumVertices()) + "\n") 
								results.write(str(h))
								results.write('\ngraph G: Clars: ' + str(g.getClarsNumber()) + "graph G: Fries: " + str(g.getFriesNumber()) +" Number of Structures: " + str(g.getNumStructures()) + " Number of vertices: " + str(g.getNumVertices()) + "\n") 
								results.write(str(g))
								results.write("\n\n")

								drawConflictsFFCC(g, h)

			#only adds graphs to list if it under some number of vertices
			graphList.append(h)

		t2 = time.time()
		counter += 1

def findHighestClars(graphs):
	clars = 0
	for g in graphs:
		if g.getClarsNumber() > clars:
			clars = g.getClarsNumber()
	return clars

def _findRequiredEdges(graphs):
	masterSet = getRequiredSet(graphs)
	if len(masterSet) > 0:
		for edge in masterSet:
			v1, v2 = edge
			v1.required = True
			v2.required = True
		return True
	else:
		return False
	
def findRequiredEdges(hours=0):
	if not os.path.exists("requiredEdges"):
		os.mkdir("requiredEdges")

	edgeFile = open("requiredEdges/RequiredEdges.txt", "w")
	graphNumber = 0
	rqNum = 0

	flag = False
	if hours == 0:
		interval = float(raw_input("How many hours would you like to run the program? "))
	else:
		interval = hours

	timeLimit = 3600 * interval
	print "limit:", timeLimit

	t1 = time.time()
	t2 = time.time()

	while t2 - t1 < timeLimit:
		print "graph", graphNumber

		flag = False

		graph = _createRandomKekulean()
		graphs = assignMatching(graph)

		for f in graph.getFaceGraph():
			pairs = graph.getBondedVertices(f)
			print str(pairs)
		
		flag = _findRequiredEdges(graphs)
		if flag == True:
			print "Found graph with required edges"
			edgeFile.write("Graph: " + str(rqNum) + "\n")
			edgeFile.write(graph.simpleToString())
			edgeFile.write("\n\n")

			#save PNG's
			fileName = "requiredEdges/Graph" + str(rqNum) + ".png"
			saveSinglePNG(graphs[0], fileName)
			rqNum += 1

		graphNumber += 1
		t2 = time.time()

def BreakModule():
	global Break
	Break = True

def BreakLoop():
	global BreakLoop
	BreakLoop = True

def combineGraphs(root,interval):
	global Break
	Break = False

	quit = Button(root, text ="Quit", command = BreakModule)
	quit.pack(side = LEFT)

	graphNumber = 0
	superGraphNumber = 0
	deletedCount = 0

	scrollbar = Scrollbar(root)
	scrollbar.pack(side = RIGHT,fill = Y)	

	text = Text(root,yscrollcommand = scrollbar.set)
	text.pack()	

	scrollbar.config(command=text.yview)

	storedGraphs = {}

	timeLimit = 3600 * interval

	t1 = time.time()
	t2 = time.time()	

	while t2 - t1 < timeLimit:

		text.insert(CURRENT,"graph: " + str(graphNumber) + "\n")

		if Break == True:
			Break = False
			quit.destroy()
			break
		
		flag = False

#new stuff
		randomFaces = createRandomGraph()
		vertexGraph = []

		#Finds connected graph
		while len(vertexGraph) % 2 != 0 or len(vertexGraph) == 0 or countPeaksAndValleys(randomFaces) == False or isConnected(faceGraphToInts(randomFaces)) == False: 
			randomFaces = createRandomGraph()
			vertexGraph = makeVertexGraph(randomFaces)	

		randomGraph = Graph(randomFaces, vertexGraph)

		perfectMatchingThm = isKekulean(randomGraph)

		if perfectMatchingThm == True:
			structures = assignMatching(randomGraph)			
#end new stuff

		Graph.comparison = 'clars'
		structures.sort()
		randomGraph.maxClars = structures[-1].getClarsNumber()

		req_edges = getRequiredSet(structures)
		externalEdges = getExternalEdges(req_edges)

		if len(externalEdges) > 0:
			#add graph and edges to list
			storedGraphs[randomGraph] = externalEdges

			for g, edges in storedGraphs.items():
				complements = getComplements(externalEdges, edges)

				for edge, compEdge in complements:
					faceA = (edge[0].getFaces() & edge[1].getFaces()).pop()
					faceB = (compEdge[0].getFaces() & compEdge[1].getFaces()).pop()
					
					x = faceA.getX() - faceB.getX()
					y = faceA.getY() - faceB.getY()

					if edge[2] == "TOP_RIGHT" and compEdge[2] == "BOTTOM_LEFT":
						newGraph = offsetFaces(g, x, y + 1);
					elif edge[2] == "RIGHT" and compEdge[2] == "LEFT":
						newGraph = offsetFaces(g, x + 1, y);
					elif edge[2] == "TOP_LEFT" and compEdge[2] == "BOTTOM_RIGHT":
						newGraph = offsetFaces(g, x + 1, y + 1);

					elif edge[2] == "BOTTOM_LEFT" and compEdge[2] == "TOP_RIGHT":
						newGraph = offsetFaces(g, x, y - 1);
					elif edge[2] == "LEFT" and compEdge[2] == "RIGHT":
						newGraph = offsetFaces(g, x - 1, y);
					elif edge[2] == "BOTTOM_RIGHT" and compEdge[2] == "TOP_LEFT":
						newGraph = offsetFaces(g, x - 1, y - 1);

					overlap = checkFaceOverlap(randomGraph, newGraph)
					#print overlap
					if overlap is False:
						faceGraph = combineFaces(randomGraph, newGraph)
						faceGraph = adjustForNegatives(faceGraph)

						vertexGraph = makeVertexGraph(faceGraph)

						superGraph = Graph(faceGraph, vertexGraph)

						structures = assignMatching(superGraph)

						_findRequiredEdges(structures)
#start new stuff
						if len(structures) > 0:
							#setup folder 
							folderName = "CombinedTemps"
							if not os.path.exists(folderName):
								os.mkdir(folderName)

							fileName = folderName + "/superGraph.txt" 
							f = open(folderName + "/superGraph" + str(superGraphNumber) + ".txt" ,'w')							
							f.write(str(superGraph) + '\n')
							f.close()	

							Graph.comparison = 'clars'
							structures.sort()

							if not os.path.exists("CombinedGraphs"):
								os.mkdir("CombinedGraphs")

							folderNameCG = "CombinedGraphs/superGraph" + str(superGraphNumber)
							#setup folder
							if not os.path.exists(folderNameCG):
								os.mkdir(folderNameCG)

							superName = folderNameCG + "/superGraph" + str(superGraphNumber) + ".png"
							
							saveSinglePNG(structures[0], superName)
							addCombinationsPNG(randomGraph, newGraph,superGraph, superGraphNumber, deletedCount)
							
							superGraphNumber += 1
		graphNumber += 1

		t2 = time.time()

		quit.update_idletasks()
		
	quit.destroy()

def resetCombinedGraphs(root,appInfo,submitGraph,graphNumberEntry,view):

	submitGraph.destroy()
	view.destroy()
	graphNumberEntry.destroy()

def analyzeCombinedGraphsSetup(root,appInfo,path = "CombinedTemps",extension = ".txt"):
	
	runningApps = []
	root.geometry("600x400")

	graphNumber = IntVar()	

	entry = Entry(root, textvariable = graphNumber)
	entry.pack()
	runningApps.append(entry)

	if not os.path.exists(path):
		os.mkdir(path)

	num_files = len([f for f in os.listdir(path)
                	if os.path.isfile(os.path.join(path, f))])
	num_files -= 1

		#for i in range(0,num_files):
			#oldFilename = path + "/superGraph" + str(k+1) + extension
			#os.rename(oldFilename, path + "/superGraph" + str(i) + extension)

	label = Label(root, text="There are " + str(num_files) + " files in the directory. Which wuold you like to look at?")
	label.pack()
	runningApps.append(label)

	i = 0

	submit = Button(root, text ="Submit", command = lambda: checkAnalyze(root,appInfo,num_files,quit,entry,label,i,graphNumber,submit,runningApps))
	submit.pack(side = BOTTOM)

	while i == 0:
		i = graphNumber.get()

		submit.update_idletasks()
		entry.update_idletasks()
		label.update_idletasks()

def checkAnalyze(root,appInfo,num_files,quit,entry,label,i,graphNumber,submit,runningApps):
	submit.destroy()	

	again = Label(root, text="That file does not exist, please try again.")
	
	submit = Button(root, text ="Submit", command = lambda: analyzeCombinedGraphs(root,appInfo,i,runningApps,submit,again,label,entry))
	submit.pack(side = BOTTOM)	

	if i < -1 or i > num_files:		
		again.pack()

	else:
		analyzeCombinedGraphs(root,appInfo,i,runningApps,submit,again,label,entry)
		
	while (i < -1 or i > num_files):
		submit.update_idletasks()
		entry.update_idletasks()
		label.update_idletasks()
		again.update_idletasks()

		i = graphNumber.get()

def analyzeCombinedGraphs(root,appInfo,i,runningApps,submit,again,label,entry):		
	submit.destroy()
	again.destroy()
	label.destroy()
	entry.destroy()

	selection = StringVar()

	choiceEntry = Entry(root, textvariable = selection)	

	choice = selection.get()	
		
	def callback(root,appInfo,i,choice,selection,choiceEntry,extension = ".txt",path = "CombinedTemps"):

		loading = Label(root, text="Analyzing graph data, this may take a few minutes.")
		loading.pack()				

		fileName = "/superGraph" + str(i) + extension
		faceGraph = getInput(path + "/superGraph" + str(i) + extension)

			#check for connectedness
		connected = isConnected(faceGraphToInts(faceGraph))			
			
		if connected == True:

			vertexGraph = makeVertexGraph(faceGraph)

			superGraph = Graph(faceGraph, vertexGraph)

			structures = assignMatching(superGraph)

			_findRequiredEdges(structures)

			loading.destroy()

			choiceEntry.pack()

			typeSelection = Label(root, text="Would you like to view the graphs ranked by Fries or Clars?")
			typeSelection.pack()

			submit = Button(root, text ="Submit", command = lambda: userInputStructures(root,appInfo,structures,choice,submit,typeSelection,choiceEntry))
			submit.pack(side = BOTTOM)	

			while True:
				choice = selection.get()

				flag = False
				exit = False

				if choice != 'fries' and choice != 'clars' and choice != "":
					againSelection = Label(root, text="That file does not exist, please try again.")
					againSelection.pack()
					print "again"
					flag = True
				
				while choice != 'fries' and choice != 'clars':
					submit.update_idletasks()
					choiceEntry.update_idletasks()
					typeSelection.update_idletasks()
					againSelection.update_idletasks()

					choice = selection.get()

				if exit == True:
					againSelection.destroy()
					break

				submit.update_idletasks()
				choiceEntry.update_idletasks()
				typeSelection.update_idletasks()								
				
	t = threading.Thread(target = lambda: callback(root,appInfo,i,choice,selection,choiceEntry))
	t.setDaemon(True)
	appInfo.setThreads(t)
	t.start()

def userInputStructures(root,appInfo,structures,choice,submit,typeSelection,choiceEntry):	

	structureNumber = IntVar()
	submit.destroy()
	typeSelection.destroy()
	choiceEntry.destroy()

	def displayCombinedClarFries(structureNumber,structures,choice):
		structures.sort()

		if choice == 'clars':
			Graph.comparison = 'clars'
				
		elif choice == 'fries':
			Graph.comparison = 'fries'

		structures.reverse()
			
		structures[structureNumber].displayGraph()

	view = Label(root, text="There are " + str(len(structures)) + " distince Kekule structures avaiable. Which would you like to view?")
	view.pack()

	graphNumberEntry = Entry(root, textvariable = structureNumber)
	graphNumberEntry.pack()

	number = structureNumber.get()

	submitGraph = Button(root, text ="Submit Structure", command = lambda: displayCombinedClarFries(number,structures,choice))
	submitGraph.pack(side = BOTTOM)

	def deleteB(button):
		button.destroy()

	reset = Button(root, text ="Quit", command = lambda: resetB(root,appInfo,submitGraph,graphNumberEntry,view))
	reset.pack(side = BOTTOM)

	def resetB(root,appInfo,submitGraph,graphNumberEntry,view):
		deleteB(reset)
		resetCombinedGraphs(root,appInfo,submitGraph,graphNumberEntry,view)

def addCombinationsPNG(graph,newGraph,superGraph,superGraphNumber,deletedCount):
	new1 = graph.getFaceGraph()
	new2 = newGraph.getFaceGraph()

	vertexG1 = makeVertexGraph(new1)
	vertexG2 = makeVertexGraph(new2)

	g1 = Graph(new1,vertexG1)
	g2 = Graph(new2,vertexG2)

	firstStructures = assignMatching(g1)
	secondStructures = assignMatching(g2)

	_findRequiredEdges(firstStructures)
	_findRequiredEdges(secondStructures)

	Graph.comparison = 'clars'
	firstStructures.sort()
	secondStructures.sort()

	if(isKekulean(g2) == True and isKekulean(g1) == True):		

		folderNameCG = "CombinedGraphs/superGraph" + str(superGraphNumber)

		firstName = folderNameCG + "/Graph" + str(1) + ".png"
		secondName = folderNameCG + "/Graph" + str(2) + ".png"

		saveSinglePNG(firstStructures[0], firstName)
		saveSinglePNG(secondStructures[0], secondName)	
	else:

		directoryName = "CombinedDeleted"

		if not os.path.exists(directoryName):
			os.mkdir(directoryName)

		folderName = "CombinedDeleted/superGraph" + str(superGraphNumber) + "_" + str(deletedCount)

		if not os.path.exists(folderName):
			os.mkdir(folderName)

		f = superGraph.getFaceGraph()

		v3 = makeVertexGraph(f)

		g3 = Graph(f,v3)

		superGraphStructure = assignMatching(g3)

		fileName = folderName + "/superDeleted" + str(superGraphNumber) + ".png"
		firstName = folderName + "/Graph" + str(1) + ".png"
		secondName = folderName + "/Graph" + str(2) + ".png"

		saveSinglePNG(superGraphStructure[0], fileName)
		saveSinglePNG(firstStructures[0], firstName)
		saveSinglePNG(secondStructures[0], secondName)

		shutil.rmtree("CombinedGraphs/superGraph" + str(superGraphNumber))

		superGraphNumber -= 1
		deletedCount += 1

def removeCombinedDuplicates(path = "CombinedTemps",extension = ".txt"):
	num_files = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])
	print num_files
	num_files -= 7
	print num_files

	masterFaceGraph = []

	for i in range(0,num_files):
		filename = "/superGraph" + str(i) + extension
		faceGraph = getInput(path + "/superGraph" + str(i) + extension)
		masterFaceGraph.append(faceGraphToInts(faceGraph))

	for f in range(0, len(masterFaceGraph)):

		for k in range(f+1, len(masterFaceGraph)):

			flag = True
			
			for h in range(0,len(masterFaceGraph[f])):

				a = masterFaceGraph[f][h]
				b = masterFaceGraph[k][h]

				if len(a) != len(b):
						flag = False	
						break

				for t in range(0,len(masterFaceGraph[f][h])):

					c = a[t]
					d = b[t]

					if c != d:
						flag = False
						break

				if flag == False:
					break

			if (flag == True):

				masterFaceGraph.remove(masterFaceGraph[k])
				shutil.rmtree("CombinedGraphs/superGraph" + str(k))
				os.remove("CombinedTemps/superGraph" + str(k) + extension)

				for i in range(k+1,num_files):
					path1 = "CombinedGraphs"
					path2 = "CombinedTemps"

					oldFilename1 = path1 + "/superGraph" + str(i)
					oldFilename2 = path2 + "/superGraph" + str(i) + extension
				
					os.rename(oldFilename1 + "/superGraph" + str(i) + ".png", oldFilename1 + "/superGraph" + str(i-1) + ".png")	
					os.rename(oldFilename1, path1 + "/superGraph" + str(i-1))		

					os.rename(oldFilename2, path2 + "/superGraph" + str(i-1) + extension)	

				num_files -= 1