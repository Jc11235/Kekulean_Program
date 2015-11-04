from Tkinter import *
import threading

class AppI(object):

	__slots__ = ['runningApps','runningAppsNames','runningThreads','timeUp']

	def __init__(self):

		self.runningApps = []
		self.runningAppsNames = []
		self.runningThreads = []

		self.timeUp = False

	def getTimeUp(self):
		return self.timeUp

	def setTimeUp(self,flag):
		self.timeUp = flag

	def setApps(self,app,appName):
		print appName
		self.runningApps.append(app)
		self.runningAppsNames.append(appName)

	def setThreads(self,thread):
		self.runningThreads.append(thread)

	def killApps(self):
		for apps in self.runningApps:
			apps.destroy()
			self.runningApps.remove(apps)

	def killThreads(self):
		for threads in self.runningThreads:
			threads.exit()