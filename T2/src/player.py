import options
from logic import *
from random import randint

class Player:
	def __init__(self, mmap):
		self.logic = Logic()
		self.map = mmap
		self.posList = []

		self.energy = options.initialEnergy
		self.cost = 0
		self.position = options.startPos
		self.ammo = options.initialAmmo

		self.redrawPlayer = None
		self.direction = 3

		self.checkPosition()
		self.updateProlog()


	def updateProlog(self):
		self.logic.updateSensorFacts(self.map.getSensors(self.position), *self.position)
		self.logic.updateCurrentFacts(self)

	def getCurrentPos(self):
		return self.map.getPos(*self.position)

	def registerPlayerRedrawCallbak(self,f):
		self.redrawPlayer = f

	def performAction(self, action):
		name = action['A']
		pos = (action['X'],action['Y'])

		action = getattr(self, name)
		action(*pos)

		self.updateProlog()

	def die (self, arg1, arg2):
		self.cost -= 1000
		self.posList.append(self.position)

	def escape (self,a1,a2):
		self.walk(*options.endPos)
		if(self.position == options.endPos):
			self.cost -= 1

	

	def pickGold(self, x, y):
		self.walk(x, y)

		self.posList.append(self.position)
		self.map.removeItem(x,y)
		
		self.cost -= 1
		self.cost += 1000

	def moveForward(self,x,y):
		self.cost -= 1
		self.position = (x,y)
		
		self.posList.append(self.position)
		self.redrawPlayer(self)

	def turn(self):
		self.cost -= 1
		
		self.posList.append(self.position)
		self.direction += 1
		self.direction %= 4
		self.redrawPlayer(self)

	def turnTo(self, x, y):
		xcurr, ycurr = self.position

		if xcurr == x and ycurr == y:
			return

		if x - xcurr > 0:
			d = 0
		elif ycurr - y > 0:
			d = 1
		elif xcurr - x > 0:
			d = 2
		else:
			d = 3

		turns = (d - self.direction) % 4
		for i in range(turns):
			self.turn()

	def walk(self, x, y, posListExtra = None):
		if self.position == (x, y):
			return

		safe = self.logic.getSafeList()

		if posListExtra:
			safe.extend(posListExtra)

		try:
			path = self.map.findPath(self.position, (x, y), safe)
		except:
			visited = self.logic.getVisitedList()
			if posListExtra:
				visited.extend(posListExtra)
			path = self.map.findPath(self.position, (x, y), visited)

		for pos in path:
			self.turnTo(*pos)
			self.moveForward(*pos)
			self.position = pos
			self.checkPosition()
			if pos != path[-1]:
				self.updateProlog()

	def shoot(self, x, y):
		# print("shoot: "+str(x)+" "+str(y))
		# return

		safe = self.logic.getSafeList()
		adjacents = self.map.getAdjacents((x, y), safe)
		adjacent = adjacents[0]
		self.walk(*adjacent)

		
		self.turnTo(x, y)
		
		
		self.posList.append(self.position)
		self.cost -= 10
		self.ammo -= 1
		if (x,y) in self.map.enemies:
			self.map.enemies[(x,y)] -= randint(20,50)
			if self.map.enemies[(x,y)] <= 0:
				self.map.removeItem(x,y)


		self.updateProlog()

	def checkPosition(self):
		currPos = self.getCurrentPos()
		if currPos == options.powerUp:
			self.energy += 20
			self.map.removeItem(*self.position)
		elif currPos == options.tt:
			self.logic.logThreat(*self.position)
			self.teleport()
			self.cost -= 1000
		elif currPos == options.smallEnemy:
			self.cost -= 20
			self.energy -= 20
			self.logic.logThreat(*self.position)
		elif currPos == options.bigEnemy:
			self.cost -= 50
			self.energy -= 50
			self.logic.logThreat(*self.position)
		elif currPos == options.pit:
			self.cost -= 1000
			self.logic.logThreat(*self.position)



	def recklessWalk(self,x,y):
		self.walk(x, y, [(x, y)])
		self.updateProlog()
		self.checkPosition()


	def teleport(self):

		print("teleport")
		self.position = (randint(0, 11), randint(0, 11))
		self.posList.append(self.position)
		


