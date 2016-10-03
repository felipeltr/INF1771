from tkinter import *

colorMap = {"D":"dark gray", ".":"white", "G":"light gray", "C":"yellow", "I":"orange", "F":"green"}

SQUARE_SIZE=15
MAP_OFFSET=5

class Square:
	def __init__(self,x,y,size,typ):
		self.x = x
		self.y = y
		self.size = size
		self.type = typ

	def draw(self, canvas):
		canvas.create_rectangle(self.x,self.y,self.x+self.size,self.y+self.size,fill=colorMap[self.type])


class MapView:
	def __init__(self,master):
		self.canvas = Canvas(master, width=640, height=640);
		self.canvas.grid(row=0,column=0,padx=10,pady=10);

		self.dotIds = None


	def drawSquares(self,mapInstance):
		for i,row in enumerate(mapInstance.data):
			for j,t in enumerate(row):
				sq = Square(SQUARE_SIZE*j+MAP_OFFSET, SQUARE_SIZE*i+MAP_OFFSET, SQUARE_SIZE, t)
				sq.draw(self.canvas)

		if self.dotIds == None:
			self.dotIds = [[None]*mapInstance.size[1] for i in range(mapInstance.size[0])]


	def markSquare(self,i,j):
		if self.dotIds[i][j] != None:
			return

		cj = SQUARE_SIZE*j+MAP_OFFSET+SQUARE_SIZE//2
		ci = SQUARE_SIZE*i+MAP_OFFSET+SQUARE_SIZE//2
		color = "#707070"
		# self.dotIds[i][j] = self.canvas.create_oval(cj-1,ci-1,cj+3,ci+3,fill=color,outline=color)
		self.dotIds[i][j] = self.canvas.create_text(SQUARE_SIZE*j+MAP_OFFSET+SQUARE_SIZE//2+1,SQUARE_SIZE*i+MAP_OFFSET+SQUARE_SIZE//2+1,text="H",fill=color,tags="mark")
		# self.canvas.update()

	def drawStateArrow(self,state):
		# self.canvas.create_text(SQUARE_SIZE*state.y+MAP_OFFSET+SQUARE_SIZE//2,SQUARE_SIZE*state.x+MAP_OFFSET+SQUARE_SIZE//2+1,text="X",fill="#505050",tags="mark")
		self.canvas.delete(self.dotIds[state.x][state.y])
		# self.canvas.update()
		

		if type(state.prev) != type(None):
			self.canvas.create_line(SQUARE_SIZE*state.prev.y+MAP_OFFSET+SQUARE_SIZE//2+1+3*state.mov[1],SQUARE_SIZE*state.prev.x+MAP_OFFSET+SQUARE_SIZE//2+1+3*state.mov[0],
				SQUARE_SIZE*state.y+MAP_OFFSET+SQUARE_SIZE//2+1+state.mov[1],SQUARE_SIZE*state.x+MAP_OFFSET+SQUARE_SIZE//2+1+state.mov[0],arrow=LAST,width=1,tags="mark",fill="#505050",arrowshape=(6,6,2))

		self.canvas.update()
		

	def drawStep(self,state):
		if type(state.prev) != type(None):
			offset = state.mov if (state.f-state.g) == 0 else (0,0)
			self.canvas.create_line(SQUARE_SIZE*state.prev.y+MAP_OFFSET+SQUARE_SIZE//2+1,SQUARE_SIZE*state.prev.x+MAP_OFFSET+SQUARE_SIZE//2+1,
				SQUARE_SIZE*state.y+MAP_OFFSET+SQUARE_SIZE//2+1+offset[0],SQUARE_SIZE*state.x+MAP_OFFSET+SQUARE_SIZE//2+1+offset[1],arrow=LAST if (state.f-state.g) == 0 else NONE,width=2,tags="mark")
		

	def drawSteps(self,state):
		while(state.prev != None):
			self.drawStep(state)
			# self.canvas.update_idletasks()
			state = state.prev



	def clearMarks(self):
		self.canvas.delete("mark")


	def clear(self):
		self.canvas.delete(ALL)
