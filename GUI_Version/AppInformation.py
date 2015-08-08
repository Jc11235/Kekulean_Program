from Tkinter import *
import threading

class AppI(object):

	__slots__ = ['runningApps','runningAppsNames','runningThreads']

	def __init__(self):

		self.runningApps = []
		self.runningAppsNames = []
		self.runningThreads = []

	def setApps(self,app,appName):
		print appName
		self.runningApps.append(app)
		self.runningAppsNames.append(appName)

	def setThreads(self,thread):
		self.runningThreads.append(thread)

	def killApps(self):
		i = 0
		print str(len(self.runningApps))

		for apps in self.runningApps:
			print str(self.runningAppsNames[i]) + "\n"
			apps.destroy()
			self.runningApps.remove(apps)
			i += 1

	def killThreads(self):
		for threads in self.runningThreads:
			threads.kill_received = True