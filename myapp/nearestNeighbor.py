import math

def Prch_Vsn(distanceMatrix):
	VisitedNodes=[0]
	indexofMin=0
	for distance in distanceMatrix:
		idx=getMinIndex(distanceMatrix[indexofMin],VisitedNodes)
		VisitedNodes.append(idx)
		indexofMin=idx
	return(VisitedNodes)

def getMinIndex(Distances, Indexes):
	minDisIndex = 0

	minDistance = math.inf


	for disIndex in range(len(Distances)):
		if(Distances[disIndex] <= minDistance and disIndex not in Indexes):
			minDistance = Distances[disIndex]
			minDisIndex = disIndex
	
	return minDisIndex
