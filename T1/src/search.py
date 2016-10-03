
import queue

import options
import math

from time import sleep

from utils import *
from glade import *

mapInstance = None

class State:

	def __init__(self,prev,x,y,mov=None):
		self.prev = prev
		self.x = x
		self.y = y
		self.mov = mov
		# self.gladeCount = 
		# if mapInstance.data[x][y] == options.endPos:
			# return

		if type(prev) != type(None):
			self.gWithoutGlade = prev.gWithoutGlade
			self.gladeCount = prev.gladeCount
			self.gladeCost = prev.gladeCost
			
			if mapInstance.getPos(x,y) == options.gladePos:
				self.gladeCount += 1
				printlog(" >>> Obtaining cost for "+str(self.gladeCount)+" glades")
				self.gladeCost = getGladesCost(self.gladeCount)
				printGladeSolution(self.gladeCount)
				# if self.gladeCount == 6:
					# exit(-1)
			else:
				self.gWithoutGlade += mapInstance.getPosCost(x,y)

			self.g = self.gWithoutGlade + self.gladeCost
		else:
			self.gWithoutGlade = 0
			self.g = 0
			self.gladeCount = 0
			self.gladeCost = 0
		self.h = math.sqrt( (mapInstance.finish[0]-x)**2 + (mapInstance.finish[1]-y)**2 )
		self.f = self.g + self.h
		# self.gladesCount = gladesCount
		# printlog("Creating ("+str(self.x)+","+str(self.y)+") -> "+mapInstance.data[self.x][self.y]+" - g: "+str(self.g)+" / f: "+str(self.f))

	def logvisit(self):
		printlog( \
			"Visiting ("+("{:2d}".format(self.x))+","+("{:2d}".format(self.y))+") -> "+mapInstance.data[self.x][self.y]+\
			"  -  f: "+("{:10.5f}".format(self.f))+\
			"  /  g: "+("{:10.5f}".format(self.g))+\
			"  /  h: "+("{:10.5f}".format(self.h)) )

	# Comparison operators overloading to allow heapq module usage
	def __lt__(self, other):
		return self.f < other.f

	def __le__(self, other):
		return self.f <= other.f

	# def __eq__(self, other):
		# return self.f == other.f

	# def __ne__(self, other):
		# return self.f != other.f

	def __gt__(self, other):
		return self.f > other.f

	def __ge__(self, other):
		return self.f >= other.f


class Search:

	def __init__(self,mmap):
		self.map = mmap
		global mapInstance
		mapInstance = self.map

	def setVisitCallback(self,f):
		self.visitCallback = f

	def setFinishCallback(self,f):
		self.finishCallback = f

	def setHeapCallback(self,f):
		self.heapCallback = f

	def isToBeVisited(self,x,y):
		if x < 0 or x >= self.map.size[0] or y < 0 or y >= self.map.size[1]:
			return False
		# print(" validating -> "+str(x)+" "+str(y))
		return not self.visited[x][y]

	def run(self):
		self.states = []
		self.heap = queue.PriorityQueue()
		self.visited = [ [False]*self.map.size[1] for i in range(self.map.size[0])]

		# self.visited[self.map.start[0]][self.map.start[1]] = True
		newstate = State(None,self.map.start[0],self.map.start[1])
		self.heap.put( newstate )

		#while(True):
		while True:
			currentState = self.heap.get()
			if self.visited[currentState.x][currentState.y]:
				continue

			self.visited[currentState.x][currentState.y] = True
			currentState.logvisit()

			# print(self.visited)

			if hasattr(self,'visitCallback'):
				# self.visitCallback(currentState)
				self.visitCallback(currentState)

			if self.map.data[currentState.x][currentState.y] == options.endPos:
				self.finishCallback(currentState)
				printlog("Done!")
				print("\n\033[1m ---- Solution ----\033[0m")
				printGladeSolution(currentState.gladeCount)
				print("\n\033[1mWalk cost:\033[0m "+str(currentState.gWithoutGlade))
				print("\033[1mGlades cost:\033[0m "+str(currentState.gladeCost))
				print("\033[1mTotal cost:\033[0m "+str(currentState.g))
				print("")
				break

			for mov in ((0,-1),(-1,0),(0,1),(1,0)):
				newx = currentState.x + mov[0]
				newy = currentState.y + mov[1]

				if(self.isToBeVisited(newx,newy)):
					# print("-> "+str(newx)+" "+str(newy))
					if hasattr(self,'heapCallback'):
						self.heapCallback(newx,newy)
					
					newstate = State(currentState,newx,newy,mov)
					self.heap.put( newstate )

			# sleep(0.1)








