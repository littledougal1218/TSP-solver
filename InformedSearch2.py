import sys, string, math, datetime, heapq, queue
from TSPObjects import *

def CalculatePathCost(path):
	pathcost = 0
	for i in range(1, len(path)):
		pathcost = pathcost + 0

	return pathcost

def MinimumCostRoad(visitedCities, roads, mst):
	for road in roads:
		if road not in mst:
			if (road.dest not in visitedCities):
				if (road.source in visitedCities):
					mst.append(road)
					visitedCities.append(road.dest)
					return road.cost
			elif (road.source not in visitedCities):
				if (road.dest in visitedCities):
					mst.append(road)
					visitedCities.append(road.source)
					return road.cost
	return 0

def PrimMST(cities):
	if len(cities) <= 1:
		return 0

	roads = ConstructRoads(cities)
	firstRoad = roads.pop(0)
	mst = [firstRoad]

	mstCost = firstRoad.cost
	visitedCities = [firstRoad.source, firstRoad.dest]

	while len(visitedCities) < len(cities):
		mstCost = mstCost + MinimumCostRoad(visitedCities, roads, mst)

	return mstCost

def FindUnvisitedCities(path, cities):
	unvisitedCities = []

	if len(path) > 1:
		if (path[0] != path[-1]):
			unvisitedCities.append(path[0])

	for city in cities:
		if not city in path:
			unvisitedCities.append(city)

	return unvisitedCities

def FindSuccessors(node, cities):
	successors = []

	if len(node.path) > 1:
		if (node.path[0] == node.path[-1]):
			return successors

	pathcost = CalculatePathCost(node.path)

	unvisitedCities = FindUnvisitedCities(node.path, cities)
	mstcost = PrimMST(unvisitedCities)

	for city in cities:
		if city not in node.path:
			nPath = list(node.path)
			nPath.append(city)
			f = pathcost + mstcost + 0
			successors.append(CostTuple(f, nPath))

	if not successors:
		nPath = list(node.path)
		nPath.append(node.path[0])
		f = pathcost + mstcost + 0
		successors.append(CostTuple(f, nPath))

	return sorted(successors)

def Search(cities):
	totalCities = len(cities)
	nodesGenerated = 0

	if len(cities) == 1:
		return (nodesGenerated, [cities[0]])

	startingNode = CostTuple(0, [cities[0]])
	fringe = queue.PriorityQueue()
	fringe.put(startingNode)

	while fringe:
		node = fringe.get()
		
		if (len(node.path) == (totalCities+1)):
			if (node.path[0] == node.path[-1]):
				return (nodesGenerated, node.path)

		
		successors = FindSuccessors(node, cities)
		nodesGenerated = nodesGenerated + len(successors)

		for successor in successors:
			fringe.put(successor)

	return (nodesGenerated, node.path)

def main():
	if len(sys.argv) != 2:							
		print("Wrong number of inputs.")
		quit()
	else:
		filename = sys.argv[1]

		cities = readcity(filename)

		starttime = datetime.datetime.now()
		results = Search(cities)
		endtime = datetime.datetime.now()

		pathcost = CalculatePathCost(results[1])
		
		pathstring = ""
		p = results[1]
		for i in range(0, len(p)):
			if i != 0:
				pathstring = pathstring + "," + p[i].id
			else:
				pathstring = pathstring + p[i].id

		path = "Path: {}".format(pathstring)

		print("Total nodes: " + str(results[0]))

main()
