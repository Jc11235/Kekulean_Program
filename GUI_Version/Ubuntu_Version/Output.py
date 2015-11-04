from PIL import Image, ImageDraw
#from Checkers import *

import os
import math

#These methods act as a output for the program. They display the graph to the screen and create png's.
def faceGraphToIntss(faceGraph):
	rowCount = 0
	row = []
	intG = []

	for face in faceGraph:
		if face.getY() != rowCount:
			intG.append(row)
			rowCount = face.getY()
			row = list()
		row.append(face.getX())
	intG.append(row)
	return intG

def displayGraphs(graphs):
	if len(graphs) > 0:
		index = int(raw_input("what graph do you want to look at? (enter a negative number to quit) "))
		while index >= 0:
			index -= 1
			graph = graphs[index]

			print "Graph", index
			print graph.toString()
			
			graph.displayGraph()
			print "There are", len(graphs), "Kekule structures"
			index = int(raw_input("what graph do you want to look at? (enter a negative number to quit) "))

def savePNG(graphs, fileName):
	#set up PIL stuff 
	width = graphs[0].getWidth() * int(math.ceil(float(len(graphs))/20))
	#calculate PNG height
	if len(graphs) > 20:
		heightModifier = len(graphs)
	else:
		heightModifier = 20
	height = heightModifier * graphs[0].getNumberOfRows() * 40

	image = Image.new("RGB", (width, height), (255,255,255))
	draw = ImageDraw.Draw(image)

	#colors
	gray = (211, 211, 211)
	black = (0, 0, 0)
	red = (255, 0 ,0)
	green = (0, 255, 0)
	blue = (0, 0, 255)
	purple = (128, 0, 128);

	graphNumber = 0

	for g in graphs:
		for f in g.getFaceGraph():
			x = f.getX() 
			y = f.getY()
			faceColor = gray
			#assign colors for faces
			if f.isClars == True:
				faceColor = blue
			elif f.isFries == True:
				faceColor = green

			xoffset = g.getXOffset() + g.getWidth() * (int(math.floor(float(graphNumber) / 20)))
			yoffset = graphNumber % 20 * g.getNumberOfRows() * 40 + 15
			
			points = [0 + x*20 - y*10 + xoffset, 10 + y*30 +yoffset, 10 + x*20 - y*10 + xoffset, 0 + y*30 + yoffset, 20 + x*20 - y*10 + xoffset, 10 + y*30 + yoffset, 20 + x*20 - y*10 + xoffset, 30 + y*30 + yoffset, 10 + x*20 - y*10 + xoffset, 40 + y*30 + yoffset, 0 + x*20 - y*10 + xoffset, 30 + y*30 + yoffset]

			#draw hexagons
			draw.polygon(points, outline=black, fill=faceColor)

			pairs = g.getBondedVertices(f)

			for pair in pairs:
				#paint pair
				x1, y1, x2, y2, required = pair
				x1 += x*20 - y*10 + xoffset
				y1 += y*30 + yoffset
				x2 += x*20 - y*10 + xoffset
				y2 += y*30 + yoffset
				if required == True:
					lineColor = purple
				else:
					lineColor = red
				draw.line((x1, y1, x2, y2), fill=lineColor, width=2)

				if graphNumber % 20 == 0:
					draw.line((g.getWidth() * (int(math.floor(float(graphNumber) / 20))), 0, g.getWidth() * (int(math.floor(float(graphNumber) / 20))), height), fill=black, width=5)
		graphNumber += 1

	filename = fileName
	image.save(filename)

def saveSinglePNG(graph, fileName):
	#set up PIL stuff
	#Calculate PNG width 
	width = graph.getWidth() * 2
	#calculate PNG height
	height = graph.getNumberOfRows() * 75

	image = Image.new("RGB", (width, height), (255,255,255))
	draw = ImageDraw.Draw(image)

	#colors
	gray = (211, 211, 211)
	black = (0, 0, 0)
	red = (255, 0 ,0)
	green = (0, 255, 0)
	blue = (0, 0, 255)
	purple = (128, 0, 128);

	#print str(faceGraphToIntss(graph.getFaceGraph()))

	for f in graph.getFaceGraph():


		x = f.getX() 
		y = f.getY()
		faceColor = gray
		#assign colors for faces
		if f.isClars == True:
			faceColor = blue
		elif f.isFries == True:
			faceColor = green

		xoffset = graph.getXOffset()
		yoffset = graph.getNumberOfRows()
			
		points = [0 + x*20 - y*10 + xoffset, 10 + y*30 +yoffset, 10 + x*20 - y*10 + xoffset, 0 + y*30 + yoffset, 20 + x*20 - y*10 + xoffset, 10 + y*30 + yoffset, 20 + x*20 - y*10 + xoffset, 30 + y*30 + yoffset, 10 + x*20 - y*10 + xoffset, 40 + y*30 + yoffset, 0 + x*20 - y*10 + xoffset, 30 + y*30 + yoffset]

		#draw hexagons
		draw.polygon(points, outline=black, fill=faceColor)
		#print 'out'

		pairs = graph.getBondedVertices(f)

		#print str(pairs) 

		for pair in pairs:
			#print 'yes'
			x1, y1, x2, y2, required = pair
			x1 += x*20 - y*10 + xoffset
			y1 += y*30 + yoffset
			x2 += x*20 - y*10 + xoffset
			y2 += y*30 + yoffset
			if required == True:
				lineColor = purple
			else:
				lineColor = red
			draw.line((x1, y1, x2, y2), fill=lineColor, width=2)

	image.save(fileName)

def drawConflictsCC(g1, g2):
	if not os.path.exists("ConjectureConflicts"):
		os.mkdir("ConjectureConflicts")

	folderName = "ConjectureConflicts/" + str(g1.getNumVertices()) + "Verts_with_" + str(g1.getNumStructures()) + "_and_" + str(g2.getNumStructures())

	#setup folder
	if not os.path.exists(folderName):
		os.mkdir(folderName)
		#print "adding"
		fileName1 = folderName + "/graph1" + ".png"
		fileName2 = folderName + "/graph2" + ".png"
		#print fileName1
		saveSinglePNG(g1, fileName1)
		saveSinglePNG(g2, fileName2)

def drawConflictsKKFF(g1, g2):
	if not os.path.exists("KKFFConjectureConflicts"):
		os.mkdir("KKFFConjectureConflicts")

	folderName = "KKFFConjectureConflicts/" + str(g1.getNumVertices()) + "Verts_with_Structures " + str(g1.getNumStructures()) + "_and_" + str(g2.getNumStructures()) + "_and_Fries " + str(g1.getFriesNumber()) + "_and_" + str(g2.getFriesNumber())

	#setup folder
	if not os.path.exists(folderName):
		os.mkdir(folderName)
		#print "adding"
		fileName1 = folderName + "/graph1" + ".png"
		fileName2 = folderName + "/graph2" + ".png"
		#print fileName1
		saveSinglePNG(g1, fileName1)
		saveSinglePNG(g2, fileName2)

def drawConflictsFFCC(clarStructure1,clarStructure2,friesStructure1,friesStructure2):
	if not os.path.exists("FFCCConjectureConflicts"):
		os.mkdir("FFCCConjectureConflicts")
	folderName = "FFCCConjectureConflicts/" + str(clarStructure1.getNumVertices()) + "_and_Fries " + clarStructure1.getMaxFries() + "_and_" + clarStructure2.getMaxFries() + "_and_Clar " + clarStructure1.getMaxClar() + "_and_" + clarStructure2.getMaxClar() 

	#setup folder
	if not os.path.exists(folderName):
		os.mkdir(folderName)
		#print "adding"
		fileName1 = folderName + "/clar1" + ".png"
		fileName2 = folderName + "/clar2" + ".png"
		fileName3 = folderName + "/fries1" + ".png"
		fileName4 = folderName + "/fries2" + ".png"
		#print fileName1
		saveSinglePNG(clarStructure1, fileName1)
		saveSinglePNG(clarStructure2, fileName2)
		saveSinglePNG(friesStructure1, fileName3)
		saveSinglePNG(friesStructure2, fileName4)
