import options

def printlog(x):
	print(x)


def getBasketForGA():
	# Put aside one sweet of the lowest apreciation kind
	## (and higher count, in case of tie)
	minApr = min(options.sweetApr)

	a = filter( (lambda x: x[0]), [(v==minApr,i) for i,v in enumerate(options.sweetApr)] )
	minAprSweetInxs = [s[1] for s in a]

	minAprSweetCounts = [(i,options.sweetBasket[i]) for i in minAprSweetInxs]
	minAprSweetCounts.sort(key=lambda x: x[1])

	# Index of the one to be put aside
	minAprSweetInx = minAprSweetCounts[-1][0]

	newBasket = tuple(v if i != minAprSweetInx else v-1 for i,v in enumerate(options.sweetBasket))

	return newBasket



