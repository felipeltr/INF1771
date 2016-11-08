import options
import random
import math

from Queue import PriorityQueue

class Map:
	def __init__(self):
		self.deleteCallback = None

	def registerDeleteCallback(self,f):
		self.deleteCallback = f		

	def loadFile(self, path):

		self.data = [list(line.replace("\n","").replace("\r","")) for line in open(path, 'r')]

		self.size = ( len(self.data), len(self.data[0]) )

		self.enemies = dict()

		for i,row in enumerate(self.data):
			for j,t in enumerate(row):
				if t == options.smallEnemy or t == options.bigEnemy:
					# print("enemy: "+str(i)+ " "+str(j))
					self.enemies[(i,j)] = options.enemyEnergy


	def getPos(self,x,y):
		return self.data[x][y]

	def getAdjacents(self,pos,posList = None):
		x, y = pos
		l = []
		for mov in ((0,-1),(-1,0),(0,1),(1,0)):
			newx = x + mov[0]
			newy = y + mov[1]

			if newx < 0 or newx >= self.size[0] or newy < 0 or newy >= self.size[1]:
				continue
			p = (newx,newy)
			if posList == None or p in posList:
				l.append( p )

		return l

	def getSensors(self,pos):
		x, y = pos
		posValue = self.getPos(x,y)
		adjacents = self.getAdjacents(pos)

		a = {
			'gold': posValue == options.gold,
			'pit': any([self.getPos(*p) == options.pit for p in adjacents]),
			'tt': any([self.getPos(*p) == options.tt for p in adjacents]),
			'enemy': any([self.getPos(*p) == options.smallEnemy or self.getPos(*p) == options.bigEnemy for p in adjacents]),
		}

		return a

	def removeItem(self,x,y):
		if self.data[x][y] == options.regularTag:
			print("Trying to remove from empty square!")
			# exit(1)
		if self.deleteCallback:
			self.deleteCallback(x,y)

		self.data[x][y] = options.regularTag

	def scoredDistance(self, start, end):
		x = abs(start[0] - end[0])
		y = abs(start[1] - end[1])
		if x > 0 and y > 0:
			return x + y + 0.5
		return x + y 

	def findPath(self, start, end, posList):
		first = (self.scoredDistance(start, end), {'pos': start, 'prev': None})

		q = PriorityQueue()
		q.put_nowait(first)

		visited = set()

		while True:
			dist,state = q.get_nowait()

			if state['pos'] in visited:
				continue

			visited.add(state['pos'])

			if dist == 0:
				l = []
				s = state
				while s != None:
					l.append(s['pos'])
					s = s['prev']
				l.reverse()
				return l[1:]
			i = 0
			adj = self.getAdjacents(state['pos'],posList)			
			for adjacent in self.getAdjacents(state['pos'],posList):
				q.put_nowait( (self.scoredDistance(adjacent, end), {'pos': adjacent, 'prev': state}) )
					



