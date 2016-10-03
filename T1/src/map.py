import options

class Map:


	def loadFile(self, path):
		# transposedData = [list(line)[:-1] for line in open(path, 'r')]
		# self.data = tuple(zip(*transposedData))
		self.data = [line.replace("\n","") for line in open(path, 'r')]

		self.size = ( len(self.data), len(self.data[0]) )

		for i,row in enumerate(self.data):
			for j,t in enumerate(row):
				if t == "I":
					self.start = (i,j)
				elif t == "F":
					self.finish = (i,j)

	def getPos(self,x,y):
		return self.data[x][y]

	def getPosCost(self,x,y):
		return options.posCosts[ self.data[x][y] ]



