
import options

from map import *

from tkinter import *
from mapview import *
from menuview import *
from search import *
from glade import *
from progresspane import *

root = Tk()
root.title('Red Riding Hood Walk');
root.config(width=840);
root.resizable(width=FALSE, height=FALSE);

mp = MapView(root);

mmap= Map();
mmap.loadFile(options.mapfilepath)


mp.drawSquares(mmap)

search = Search(mmap)
search.setHeapCallback(mp.markSquare)
search.setVisitCallback(mp.drawStateArrow)
search.setFinishCallback(mp.drawSteps)

mn = MenuFrame(root);

def runEvent():
	mp.clearMarks()
	search.run()

mn.setRunCallback(runEvent)


root.mainloop();
