from tkinter import *

def textField(parent,label,entryWidth):
	f = Frame(parent);
	f.pack(anchor=N,side=TOP,fill=X);
	Label(f, text=label).pack(anchor=W,side=TOP);
	v=StringVar();
	entry = Entry(f,width=entryWidth,textvariable=v);
	entry.pack(anchor=W,side=TOP);
	return v;

class MenuFrame:
	def __init__(self,master):
		self.frame = Frame(master, width=300, height=480);
		self.frame.grid(row=0,column=1,sticky=S,padx=20,pady=10);


		self.runButton = Button(self.frame, text="Run!",width=10);
		self.runButton.pack(anchor=N,side=TOP,fill=X,pady=10);
		exitButton = Button(self.frame, text="Exit",width=10);
		exitButton.pack(anchor=N,side=TOP,fill=X,pady=10);
		exitButton.config(command=lambda: exit(-1));
		self.result1 = Label(self.frame, text='');
		self.result1.pack(anchor=W,side=TOP);
		self.result2 = Label(self.frame, text='');
		self.result2.pack(anchor=W,side=TOP);

	def setRunCallback(self,callback):
		self.runButton.config(command=callback);

	def setAddCallback(self,callback):
		self.addButton.config(command=callback);

	def setRmCallback(self,callback):
		self.rmButton.config(command=callback);

	def setLoadExCallback(self,callback):
		self.exButton.config(command=callback);

	def setChangeStartCallback(self,callback):
		self.changeStartButton.config(command=callback);

	def updateResultLabel(self,text):
		self.result1.config(text='Distance:');
		self.result2.config(text=text);

	def updateStartLabel(self,text):
		self.startLabel.config(text='Start: '+text);

