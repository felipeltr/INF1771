


import options

from utils import *

from itertools import combinations
from random import choice, random, randrange, shuffle

from progresspane import *

import sys

numGlades = None

class Individual:
	def __init__(self):
		self.sweetDrop = [None] * options.sweetTypes
	
	def setDrop(self,i,s):
		self.sweetDrop[i] = s

	def evaluate(self):
		# gladeSweet = tuple(g in self.sweetDrop[i] for i in range(options.sweetTypes))

		cost = 0
		for gi,dif in enumerate(options.gladeDif[:numGlades]):

			aprSum = sum( int(gi in self.sweetDrop[i]) * apr for i,apr in enumerate(options.sweetApr) )

			cost = (cost + dif/aprSum) if aprSum != 0 else float("inf")

		return cost


elitismRatio = 0.2
crossoverRatio = 0.8
mutationRatio = 0.25

class Population:	

	def __init__(self,size,glades):
		global numGlades
		numGlades = glades
		self.numGlades = glades

		self.popSize = size
		self.elitismInx = int(size*elitismRatio)
		self.crossoverInx = int(size*crossoverRatio)

		self.runInx = [True]*options.sweetTypes
		self.combLists = [None]*options.sweetTypes

		newBasket = getBasketForGA()
		self.sweetBasket = newBasket

		firstPop = list(Individual() for i in range(size))

		for i,sweetCount in enumerate(newBasket):

			if sweetCount >= numGlades: # If more sweets than glades for sweet type i, then type i has a trivial solution
				s = set(range(numGlades))
				self.runInx[i] = False
				for ind in firstPop:
					ind.setDrop(i,s)
				continue

			combList = list(combinations(range(numGlades),sweetCount))
			self.combLists[i] = combList

			for ind in firstPop:

				combInx = randrange(0,len(combList))
				ind.setDrop(i,combList[combInx])

		self.currPop = [(ind.evaluate(), ind) for ind in firstPop]
		self.sortPop()

		# self.printPop()

	def newIndividual(self,uselessParam):
		p1 = self.prevPop[randrange(0,self.crossoverInx)][1]
		p2 = self.prevPop[randrange(0,self.crossoverInx)][1]

		# print(p1.sweetDrop)
		# print(p2.sweetDrop)

		son = Individual()
		for i,sweetCount in enumerate(self.sweetBasket):
			if self.runInx[i]:
				r = random()
				# r = 1
				newSetList = None
				if r < 0.1:
					newSetList = p1.sweetDrop[i]
				elif r < 0.2:
					newSetList = p2.sweetDrop[i]
				else:
					s1 = set(p1.sweetDrop[i])
					s2 = set(p2.sweetDrop[i])
					commonSetList = list(s1 & s2)
					xorSetList = list(s1 ^ s2)

					# if(r < 0.5):
						# commonSetList, xorSetList = xorSetList, commonSetList

					if(len(commonSetList) > sweetCount):
						shuffle(commonSetList)
						newSetList = commonSetList[:sweetCount]
					elif(len(commonSetList) < sweetCount):
						shuffle(xorSetList)
						newSetList = commonSetList + xorSetList[:(sweetCount-len(commonSetList))]
					else:
						newSetList = commonSetList

				
				if(random() < mutationRatio):
					newSetList = choice(self.combLists[i])


				son.setDrop(i,set(newSetList))

			else:
				son.setDrop(i,p1.sweetDrop[i])

		# print(son.sweetDrop)


		# exit(-1)
		return (son.evaluate(),son)


	def runGA(self,iterations):
		if not any(self.runInx):
			self.bestSolution = self.currPop[0]
			return

		self.progress = ProgressPane(self.numGlades)

		pr = 0

		for it in range(iterations):
			
			self.prevPop = self.currPop

			
			self.currPop = self.prevPop[:self.elitismInx] + list(map(self.newIndividual,range(self.elitismInx,self.popSize)))
			self.sortPop()
			# self.printPop()
			# exit(-1)
			
			if (it*100)//iterations > pr:
				pr += 1
				self.progress.step(1)

			costs = [x[0] for x in self.currPop]

			print("GA Iteration: "+("{:5d}".format(it))+"/"+str(iterations)+" -> Best: "+("{:10.5f}".format(self.getBestCost())))
			# exit(-1)

		self.progress.destroy()






	def getBestCost(self):
		return self.bestSolution[0]

	def getBestSolution(self):
		return self.bestSolution[1]

	def printPop(self):
		for p in self.currPop:
			print(p[0])
			print(p[1].sweetDrop)

	def sortPop(self):
		self.currPop.sort(key=lambda x: x[0])
		self.bestSolution = self.currPop[0]


gladeCost = [None]*options.gladeCount
gladeSolution = [None]*options.gladeCount

# mpPool = mp.Pool(processes=8)

def getGladesCost(numGlades):
	if gladeCost[numGlades-1] == None:
		pop = Population(150,numGlades)
		iterations = 1000 + 600*(numGlades-min(options.sweetBasket))
		pop.runGA(iterations)
		print(pop.bestSolution[1].sweetDrop)
		gladeCost[numGlades-1] = pop.getBestCost()
		gladeSolution[numGlades-1] = pop.getBestSolution().sweetDrop
	return gladeCost[numGlades-1]

def getGladesSolution(numGlades):
	return gladeSolution[numGlades-1]

def printGladeSolution(numGlades):
	sol = getGladesSolution(numGlades)
	print("\033[1mGlade\tSweets to drop\033[0m")
	for gladeInx in range(options.gladeCount):
		sweets = []
		for sweetInx,sweetGlades in enumerate(sol):
			if(gladeInx in sweetGlades):
				sweets.append(sweetInx)

		print( "{:5d}".format(gladeInx+1) + "\t" + (", ".join(map(lambda x: options.sweetNames[x],sweets))) )


	
	



	


		

