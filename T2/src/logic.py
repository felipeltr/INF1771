from pyswip import *
import options


class Logic:
	def __init__(self):
		self.prolog = Prolog()
		self.prolog.consult(options.rulefilepath)

	def getAction(self):
		q = 'best_action(A,X,Y)'
		result = list(self.prolog.query(q, maxresult=1))
		self.logQuery(q)
		
		if len(result) == 0:
			return None
		return result[0]

	def query(self, q, ):
		self.logQuery(q)
		return list(self.prolog.query(q))

	def logQuery(self, q):
		print("\tPROLOG: "+q)

	def getSafeList(self):
		return [ (s['X'], s['Y']) for s in list(self.query("safe(X, Y)")) ]

	def getVisitedList(self):
		return [ (s['X'], s['Y']) for s in list(self.query("visited(X, Y)")) ]

	def logThreat(self,x,y):
		self.query('assertz(dont_go(%d, %d))' % (x, y))

	def updateSensorFacts(self, data, x, y):
		for p in data.keys():
			if p=='gold' :
				format = "sensor_%s(%d, %d)"
			else:
				format = "sensor(%s,%d, %d)"

			self.query( 'retract('+(format % (p, x, y)) +')' )
			if data[p]:
				self.query( 'assertz('+(format % (p, x, y)) +')' )


	def updateCurrentFacts(self, player):
		x, y = player.position
		self.query('retractall(on(_, _))')
		self.query('retract(visited(%d, %d))' % (x, y))
		self.query('assertz(current(%d, %d))' % (x, y))
		self.query('assertz(visited(%d, %d))' % (x, y))
		self.query('retractall(energy(_))')
		self.query('assertz(energy(%d))' % player.energy)
		self.query('retractall(ammo(_))')
		self.query('assertz(ammo(%d))' % player.ammo)

		