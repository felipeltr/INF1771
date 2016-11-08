from Tkinter import *
# from Tkinter.font import *
# from tkFont import font

from time import sleep

import options


SQUARE_SIZE=30
MAP_OFFSET=5

class Square:
	def __init__(self,x,y,size,typ):
		self.x = x
		self.y = y
		self.size = size
		self.type = typ

	def draw(self, canvas):
		canvas.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,fill="white")
		if self.type != options.regularTag:
			if self.type in [options.powerUp,options.gold]:
				color = "#707070"
			else:
				color = "red"
			return canvas.create_text(self.x+15,self.y+15,text=self.type,fill=color,tags="mark",font=("Helvetica",22,"bold"))


class MapView:
	def __init__(self,master):
		self.canvas = Canvas(master, width=420, height=420);
		self.canvas.grid(row=0,column=0,padx=10,pady=10);

		self.dotIds = None

		self.playerId = None
		self.itemIds = dict()

	def redrawPlayer(self,p):
		if self.playerId != None:
			self.canvas.delete(self.playerId)		

		# xoffsets=None
		# yoffsets=None
		if p.direction % 2 == 1: #horizontal
			xoffsets=(5,SQUARE_SIZE-5)
			yoffsets=(SQUARE_SIZE//2,SQUARE_SIZE//2)
		else: #vertical
			xoffsets=(SQUARE_SIZE//2,SQUARE_SIZE//2)
			yoffsets=(SQUARE_SIZE-5,5)

		if p.direction in [2,3]:
			arrow=LAST
		else:
			arrow=FIRST

		j,i = p.position

		self.playerId = self.canvas.create_line(SQUARE_SIZE*i+MAP_OFFSET+xoffsets[0],SQUARE_SIZE*j+MAP_OFFSET+yoffsets[0], \
				SQUARE_SIZE*i+MAP_OFFSET+xoffsets[1],SQUARE_SIZE*j+MAP_OFFSET+yoffsets[1],arrow=arrow,width=3,tags="mark",fill="black",arrowshape=(12,12,4))

		self.canvas.update()

		if options.stepTime > 0:
			sleep(options.stepTime)



	def drawSquares(self,mapInstance):
		for i,row in enumerate(mapInstance.data):
			for j,t in enumerate(row):
				# if t != '.':
					# print((i,j,t))
				sq = Square(SQUARE_SIZE*j+MAP_OFFSET, SQUARE_SIZE*i+MAP_OFFSET, SQUARE_SIZE, t)
				item = sq.draw(self.canvas)
				if item != None:
					self.itemIds[(i,j)] = item
			# break

		if self.dotIds == None:
			self.dotIds = [[None]*mapInstance.size[1] for i in range(mapInstance.size[0])]

	def deleteItem(self,x,y):
		if (x,y) in self.itemIds:
			self.canvas.delete(self.itemIds[(x,y)])
			self.canvas.update()


	def clear(self):
		self.canvas.delete(ALL)
