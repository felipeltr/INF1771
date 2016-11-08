from logic import *
from player import *
from map import *

from Tkinter import *
from mapview import *
from menuview import *



mmap= Map()
mmap.loadFile(options.mapfilepath)

player = Player(mmap)


root = Tk()
root.title('Wumpus World');
root.config(width=640);
root.resizable(width=FALSE, height=FALSE);

mp = MapView(root);

mp.drawSquares(mmap)

# search = Search(mmap)
# search.setHeapCallback(mp.markSquare)
# search.setVisitCallback(mp.drawStateArrow)
# search.setFinishCallback(mp.drawSteps)

mn = MenuFrame(root);

def updatePlayer(p):
	mp.redrawPlayer(p)
	mn.updateResultLabel(p)

updatePlayer(player)

player.registerPlayerRedrawCallbak(updatePlayer)

mmap.registerDeleteCallback(mp.deleteItem)

def runEvent():
	while True:

		action = player.logic.getAction()
		print "action: "+str(action)

		if action == None:
			break
		
		player.performAction(action)

		if action['A'] in ['escape','die']:
			break

		# if mmap.getPos(*player.position) in ['P','T','d','D']:
			# break


mn.setRunCallback(runEvent)

runEvent()

print(player.posList)



root.mainloop();