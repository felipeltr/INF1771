from tkinter import *
from ttk import *

class ProgressPane:
	def __init__(self,numGlades):
		
		self.top = Toplevel();
		self.top.title('Running Genetic Algorithm');
		f = Frame(self.top)
		f.grid(ipadx=30)
		f = Frame(f, width=200, height=480);
		f.grid(padx=30,pady=0)
		f.pack();
		l = Label(f, text="Calculating optimal cost for "+str(numGlades)+" glades")
		l.pack(anchor=W)
		l.grid(padx=30,pady=10, row=0, column=0)
		
		bf = Frame(f)
		bf.grid(row=1, column=0,pady=20)
		bar = Progressbar(bf,length=250)
		# bar.pack(anchor=S)
		bar.grid(row=0,column=0)
		
		# bar.start()
		l = Label(bf, text="  0 %")
		l.pack(anchor=N)
		l.grid(row=0,column=1,padx=10)

		self.top.update()

		self.bar = bar
		self.i = 0
		self.frame = f
		self.label = l

	def step(self,s=1):
		self.i += 1
		self.bar.step(s)
		self.label.config(text=("{:3d}".format(self.i))+" %")
		self.top.update()

	def destroy(self):
		self.top.destroy()
		# self.top.update()

