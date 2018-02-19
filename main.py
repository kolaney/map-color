import re

class Region: #Using a class to maintain heuristic information

	def __init__(self,name,neighbours):
		self.name = name #names are represented as integers, because thats easier right now
		self.neighbours = neighbours
		self.color = 0 #colors are represented as integers, because thats easier right now
		self.degree = 0
		self.legalVals = numColors
		self.tried = [] #heuristic information to identify what colors have already been attempted at a region

	def __str__(self):
		return str(self.name, self.neighbours, self.color)

	def getDegree(self): #Proper initialization of each region's adjacency.  Should only need to be run once per region
		self.degree = len(self.neighbours)

	def getLegalMoves(self): #Update the number of legal colorings for a region.  Will have to be run each time a color is assigned.
		self.legalVals = numColors
		for neighbor in range(self.degree):
			if world[self.neighbours[neighbor]].color != 0:
				self.legalVals = self.legalVals-1


def getAdjacency(): #Populates the neighbor list for each region based on user input
	print "Enter neighbor information as decribed in README.txt"
	while True:
		adjacency = raw_input("Enter neighbor information: ")
		if adjacency != "":
			adjacency = list(adjacency)
			if "(" in adjacency:
				adjacency.remove("(")
			if ")" in adjacency:
				adjacency.remove(")")
			adjacency = "".join(adjacency)
			adjacency = adjacency.split()
			currentRegion = world[int(adjacency[0])]
			for neighbor in range(1, len(adjacency)):
				currentRegion.neighbours.append(int(adjacency[neighbor]))
			currentRegion.getDegree()
			currentRegion.getLegalMoves()
		else:
			break

def getNextRegion(): #finds the next region to attempt to color based on the minimum remaining values and degree heuristics
	regionLegalVals = {}
	regionDegrees = {}
	for region in world: #leftover from a very early version of this search that I don't want to rebuild
		if world[region].color == 0:
			legals = {world[region].name: world[region].legalVals}
			regionLegalVals.update(legals)
			degrees = {world[region].name: world[region].degree}
			regionDegrees.update(degrees)
	legalValsList = list(regionLegalVals.values())
	try:
		minimumLegal = min(legalValsList)
	except:
		return 0
	degreeList = list(regionDegrees.values())
	maxDegree = max(degreeList)
	if legalValsList.count(minimumLegal) != 1: #looking if more than one region has the minimum legal value
		for region in world:
			if world[region].legalVals == minimumLegal and world[region].degree == maxDegree and world[region].color == 0: #if so we search based on degree as well
				return region
	else:
		for region in world:
			if world[region].legalVals == minimumLegal and world[region].color == 0: #otherwise we simply take the minimum legal value into account
				return region


def colorRegion(region):
	if region == 0:
		return
	legalColors = list(range(1, numColors+1)) #pass by reference again
	for neighbor in world[region].neighbours:
		if world[neighbor].color in legalColors:
			legalColors.remove(world[neighbor].color)
	for color in legalColors:
		if color in world[region].tried:
			legalColors.remove(color)
	if len(legalColors) != 0:
		world[region].color = min(legalColors)
		world[region].tried.append(min(legalColors))
		world[region].getLegalMoves
		for neighbor in world[region].neighbours:
			world[neighbor].getLegalMoves
		nextRegion = getNextRegion()
		colorRegion(nextRegion)
		return
	else:
		return

		


			
numRegions = raw_input("Enter number of regions: ")
numRegions = int(re.sub("\D", "", numRegions)) #Strips non-digits to make things easier to cast to int while maintaining whitespace.
numColors = raw_input("Enter number of colors: ")
numColors = int(re.sub("\D", "", numColors))

world = {}
for territory in range(1, numRegions+1):
	world.update({territory: Region(territory, [])})

colorList = list(range(1, numColors+1))

getAdjacency()
for region in world:
	world[region].getDegree()
	world[region].getLegalMoves()
nextRegion = getNextRegion()
colorRegion(nextRegion)

badworld = 0

for region in world:
	if world[region].color == 0:
		print "World cannot be colored"
		badworld = 1
		break

if badworld == 0:
	print "Region:Color"
	for region in world:
		print "     {reg}:{col}".format(reg=world[region].name, col=world[region].color)

raw_input("Done.  Press enter to quit.")