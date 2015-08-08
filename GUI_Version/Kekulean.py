from random import randint
import time
import copy
import math
import os
import tkMessageBox
import tkFileDialog
import threading
import sys
import re

from PerfectMatchingData import *
from Face import *
from Vertex import *
from Graph import *
from VertexList import *
from DriverMethods import *
from Output import *
from KekuleanMethods import *
from Checkers import *
from AppInformation import *
from threading import Thread

from PIL import Image, ImageDraw
from Tkinter import *
from ttk import *
from subprocess import Popen, PIPE

#The Main
settings = getSettings()

root = Tk()
appInfo = AppI()

root.title("New Window")
root.geometry("400x400")

#canvas = Canvas(bg = 'white', width = 400, height = 800)
#canvas.pack()

selection = 0
interval = -1
v = DoubleVar()
removeButtons = False
run = False

runningApps = []

def killsApps():
	for apps in runningApps:
		temp = apps
		runningApps.remove(apps)
		temp.destroy()

def runAnalyzeGraphFromFile():
	killsApps()

	fileName = "graph.txt"
	if not os.path.exists(fileName):
		label = Label(root, text="There are no files to analyze")
		label.pack()
		runningApps.append(label)

	if os.path.exists(fileName):
		def callback():
			analyzeGraph(root,appInfo)
		t = threading.Thread(target = callback)
		t.setDaemon(True)
		t.start()	

def runGetSettings(fileName = "settings.txt"):
	killsApps()		

	def callback():
		minW = IntVar()
		maxW = IntVar()
		minH = IntVar()
		maxH = IntVar()
		_porosity = DoubleVar()

		global min_width
		global max_width
		global min_height
		global max_height
		global porosity

		min_width = 0
		max_width= 0
		min_height= 0
		max_height= 0
		porosity= 0

		inputFile = open(fileName, 'r')
		
		lineNumber = 0

		line = inputFile.readline()
		while len(line) > 0:
			line = line.replace('\n', '')

			if lineNumber == 0:
				temp = line
				minW.set(int(temp))
			elif lineNumber == 1:
				temp = line
				maxW.set(int(temp))
			elif lineNumber == 2:
				temp = line
				minH.set(int(temp))
			elif lineNumber == 3:
				temp = line
				maxH.set(int(temp))
			elif lineNumber == 4:
				temp = line
				_porosity.set(float(temp))

			line = inputFile.readline()
			lineNumber += 1
		inputFile.close()

		minWentry = Entry(root, textvariable = minW)
		minWlabel = Label(root, text="The graph's minimum width")
		
		maxWentry = Entry(root, textvariable = maxW)
		maxWlabel = Label(root, text="The graph's maximum width")
		
		minHentry = Entry(root, textvariable = minH)
		minHlabel = Label(root, text="The graph's minimum height")
			
		maxHentry = Entry(root, textvariable = maxH)
		maxHlabel = Label(root, text="The graph's maximum height")

		porosityEntry = Entry(root, textvariable = _porosity)
		porosityLabel = Label(root, text="The graph's porosity")
		
		minWlabel.pack()
		minWentry.pack()

		maxWlabel.pack()
		maxWentry.pack()
		
		minHlabel.pack()
		minHentry.pack()
		
		maxHlabel.pack()
		maxHentry.pack()

		porosityLabel.pack()
		porosityEntry.pack()

		def deleteB(button):
			button.destroy()

		def saveSettings(fileName = "settings.txt"):
			min_width = minW.get()
			max_width =	maxW.get()
			min_height = minH.get()
			max_height = maxH.get()
			porosity = _porosity.get()

			f = open(fileName,'w')

			f.write(str(min_width) + "\n")
			f.write(str(max_width) + "\n")
			f.write(str(min_height) + "\n")
			f.write(str(max_height) + "\n")
			f.write(str(porosity))

			f.close()

			minWlabel.destroy()
			minWentry.destroy()

			maxWlabel.destroy()
			maxWentry.destroy()
		
			minHlabel.destroy()
			minHentry.destroy()
		
			maxHlabel.destroy()
			maxHentry.destroy()

			porosityLabel.destroy()
			porosityEntry.destroy()

		def resetSettings():
			saveSettings()
			deleteB(submit)

		submit = Button(root, text ="Submit", command = lambda: resetSettings())
		submit.pack(side = BOTTOM)
		runningApps.append(submit)

		minWentry.update_idletasks()
		maxWentry.update_idletasks()
		minHentry.update_idletasks()
		maxHentry.update_idletasks()
		porosityEntry.update_idletasks()
		submit.update_idletasks()			

	t = threading.Thread(target = callback)
	t.setDaemon(True)
	t.start()

def runFindRequiredEdges():
	killsApps()
	findRequiredEdges()

def _removeButtons():
	global removeButtons
	removeButtons = True

def _run():
	global run
	run = True

def runCombineGraphsMenu():
	killsApps()

	entry = Entry(root, textvariable = v)
	label = Label(root, text="How many hours would you like to run the program?")
	submit = Button(root, text ="Submit", command = lambda: runCombineGraphs(submit,entry,label))

	entry.pack()
	label.pack()
	submit.pack(side = RIGHT)

def runConjectureSameFacesMenu():
	killsApps()

	root.geometry("400x400")

	entry = Entry(root, textvariable = v)
	label = Label(root, text="How many hours would you like to run the program?")
	submit = Button(root, text ="Submit", command = lambda: runConjectureSameFaces(submit,entry,label))

	entry.pack()
	label.pack()
	submit.pack(side = RIGHT)

def runConjectureSameFacesKKFFMenu():
	killsApps()

	root.geometry("400x400")

	entry = Entry(root, textvariable = v)
	label = Label(root, text="How many hours would you like to run the program?")
	submit = Button(root, text ="Submit", command = lambda: runConjectureSameFacesKKFF(submit,entry,label))

	entry.pack()
	label.pack()
	submit.pack(side = RIGHT)

def runConjectureSameFacesFFCCMenu():
	killsApps()

	root.geometry("400x400")

	entry = Entry(root, textvariable = v)
	label = Label(root, text="How many hours would you like to run the program?")
	submit = Button(root, text ="Submit", command = lambda: runConjectureSameFacesFFCC(submit,entry,label))

	entry.pack()
	label.pack()
	submit.pack(side = RIGHT)

def runCombineGraphs(submit,label,entry):
	killsApps()

	entry.update_idletasks()

	interval = v.get()

	if interval > 0:

		entry.destroy()
		label.destroy()
		submit.destroy()				

		def callback():

			combineGraphs(root,interval)

			global removeButtons
			global run

			removeButtons = False
			run = False

			start = True

			label = Label(root, text="Would you like to analyze the graphs?")
			yes = Button(root, text ="Yes", command = _run)
			no = Button(root, text ="No", command = _removeButtons)

			label.pack()
			yes.pack(side = TOP)
			no.pack(side = TOP)

			while start == True:
				yes.update_idletasks()
				no.update_idletasks()

				runningApps.append(yes)
				runningApps.append(no)
				runningApps.append(label)

				if removeButtons == True:
					killsApps()
					removeButtons = False
					break
				if run == True:
					killsApps()
					run = False
					runAnalyzeCombinedGraphsSetup(root)
					break					

		t = threading.Thread(target = callback)
		t.setDaemon(True)
		t.start()

def runAnalyzeCombinedGraphsSetup(root):
	killsApps()

	folderName = "CombinedTemps"
	if not os.path.exists(folderName):
		label = Label(root, text="There are no files to analyze")
		label.pack()
		runningApps.append(label)

	if os.path.exists(folderName):
		def callback():
			analyzeCombinedGraphsSetup(root,appInfo)
		t = threading.Thread(target = callback)
		t.setDaemon(True)
		appInfo.setThreads(t)
		t.start()
			
def runAnalyzeCombinedGraphs():
	killsApps()	

	def callback():
		analyzeCombinedGraphsSetup(root,appInfo)
	t = threading.Thread(target = lambda: callback())
	t.setDaemon(True)
	t.start()

def runConjectureSameFaces(submit,label,entry):
	killsApps()
	entry.update_idletasks()

	interval = v.get()

	if interval > 0:

		entry.destroy()
		label.destroy()
		submit.destroy()				

		def callback():

			testConjectureSameFaces(root,interval)

			global removeButtons
			global run

			removeButtons = False
			run = False					

		t = threading.Thread(target = callback)
		t.setDaemon(True)
		t.start()

def runConjectureSameFacesKKFF(submit,label,entry):
	killsApps()
	entry.update_idletasks()

	interval = v.get()

	if interval > 0:

		entry.destroy()
		label.destroy()
		submit.destroy()				

		def callback():

			testConjectureSameFacesKKFF(root,interval)

			global removeButtons
			global run

			removeButtons = False
			run = False					

		t = threading.Thread(target = callback)
		t.setDaemon(True)
		t.start()

def runConjectureSameFacesFFCC(submit,label,entry):
	killsApps()
	entry.update_idletasks()

	interval = v.get()

	if interval > 0:

		entry.destroy()
		label.destroy()
		submit.destroy()				

		def callback():

			testConjectureSameFacesFFCC(root,interval)

			global removeButtons
			global run

			removeButtons = False
			run = False					

		t = threading.Thread(target = callback)
		t.setDaemon(True)
		t.start()

def runConjectureDifferentFaces():
	killsApps()
	testConjectureDifferentFaces()

def runCreateGraphsManually():
	x = 0

def Quit():
	os._exit(0)
	root.destroy()

#ADDS MENUS
menu = Menu(root)
root.config(menu = menu)
			
moduleMenu = Menu(menu)
fileMenu = Menu(menu)

menu.add_cascade(label = "File", menu = fileMenu)
menu.add_cascade(label = "Modules", menu = moduleMenu)


moduleMenu.add_command(label = "Analyze Graph From File", command = runAnalyzeGraphFromFile)
moduleMenu.add_command(label = "Get Settings", command = runGetSettings)
moduleMenu.add_command(label = "Combine Graphs", command = runCombineGraphsMenu)
moduleMenu.add_command(label = "Analyze Combined Graphs", command = runAnalyzeCombinedGraphs)
moduleMenu.add_command(label = "Test Conjecture With Same Number of Faces", command = runConjectureSameFacesMenu)
moduleMenu.add_command(label = "Test Conjecture With Same Number of FacesKKFF", command = runConjectureSameFacesKKFFMenu)
moduleMenu.add_command(label = "Test Conjecture With Same Number of FacesFFCC", command = runConjectureSameFacesFFCCMenu)

fileMenu.add_command(label = "Quit", command = Quit)

root.mainloop()