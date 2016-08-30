import sys
import json
import os
import math
from datetime import datetime
import datetime as date

import numpy 
from sklearn.cluster import KMeans
import networkx as nx
import math 
import pygmaps

LATITUDE = 0
LONGITUDE = 1
TIMESTAMP = 2
SAME_LOCATION_RADIOUS = 0.007  
TIME_ELAPSE = 3600
SECONDS_IN_HOUR = 3600
MAX_LAT = 33.215401
MIN_LAT = 29.505809
MAX_LONG = 35.885547
MIN_LONG = 34.221494
CLUSTER_NUM = 30
FILE_LOCATIOM = 1
LAST = -1

def roundTime(dt=None, roundTo=60):
   """Round a datetime object to any time laps in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   """
   if dt == None : dt = date.datetime.now()
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + date.timedelta(0,rounding-seconds,-dt.microsecond)


def main():
	"""
	the program will analys the locations in the given json file and creat a personal map
	that represents the places that were repeatedly visited. There would be an edge between location a
	ans location b if there was a move from a to b in the location history.
	args: the first arg is the path to the json file with the user's locations data.
	"""

	# the program must get one file exactly - a path to the json file, in order to work.
	if not len(sys.argv) == 2:
		print "USAGE ERROR: You must enter only one path to your locations"
		sys.exit(1)

	# adding the maps into one graph
	path = os.path.expanduser(sys.argv[FILE_LOCATIOM])
	with open(path, 'r') as f:
		data = json.load(f)

	locations = data['locations']
	userLocations = []

	#the timestamp of the last location that was add to the userLocations list
	lastTimeStamp = 0

	# getting the different locations of the user
	for location in locations:
		# getting positions the are not on the way to a differnet location (without 'activitys')
		if 'activitys' not in location.keys():
			latitude = int(location["latitudeE7"]) / float(10000000)
			longitude = int(location["longitudeE7"]) / float(10000000)
			timeStamp = datetime.fromtimestamp(int(location["timestampMs"]) / 1000)

			newLocation  = [latitude, longitude, timeStamp]

			#if the new location is out of isreal  - the location is not added!
			if latitude > MAX_LAT or latitude < MIN_LAT or longitude > MAX_LONG or longitude < MIN_LONG:
                            continue;

            #if this is the first location - add it to the list
			if userLocations == []:
				lastTimeStamp = newLocation[TIMESTAMP]
				userLocations.append(newLocation)
			else:
				# check if the point is further enough from the last location in the userLocations to be 
				# considered a new location
				lastLocationIndex = len(userLocations) -1
				lastLocation = userLocations[lastLocationIndex]

	
				yDifference = lastLocation[LONGITUDE]-newLocation[LONGITUDE]
				xDifference = lastLocation[LATITUDE]-newLocation[LATITUDE]
				dist = math.sqrt(pow(yDifference,2)+ pow(xDifference,2))

				if dist > SAME_LOCATION_RADIOUS:

					# add the new location , and if the user was in the last location for less then a hour, remove the last location 
					diffTime = (lastTimeStamp - newLocation[TIMESTAMP]).total_seconds()
					if diffTime < TIME_ELAPSE:
						del userLocations[LAST]

					lastTimeStamp = newLocation[TIMESTAMP]
					userLocations.append(newLocation)

	#creating a list of the moves without the timestamp
	userLocationsNoTime = []
	for location in userLocations:
		userLocationsNoTime.append(location[:2])
	
	# finding the centers using Kmeans
	est = KMeans(n_clusters=CLUSTER_NUM)
	est.fit(userLocationsNoTime)
	centers = (est.cluster_centers_).tolist()
	lables = (est.labels_).tolist()

	# replacing the location with the centers
	for index in range(len(userLocations)):
		location = userLocations[index]
		locationCenterIndex = lables[index]
		locationCenter = centers[locationCenterIndex]
		location[LONGITUDE] = locationCenter[LONGITUDE]
		location[LATITUDE] = locationCenter[LATITUDE]

	#round all the times to the closest hour + making the string of the time be the hours only without date
	for location in userLocations:
		location[TIMESTAMP] = (roundTime(location[TIMESTAMP],roundTo=SECONDS_IN_HOUR)).strftime("%H:%M:%S")

	#change the locations to be tuples so they could be used as a node name
	userLocationsTuples = [tuple(location) for location in userLocations]
	nodes = set(userLocationsTuples)

	#create an html file with the centers drawn in google map 
	mymap = pygmaps.maps(31.7816,35.2192, 16) 
	for node in nodes:
		mymap.addpoint(node[LATITUDE], node[LONGITUDE], "#0000FF")
	mymap.draw('./mymap.html') 

	# creating a graph with the centers as is't nodes and there would be an edge according to the moves
	G = nx.DiGraph()
	#the centers would be nodes
	G.add_nodes_from(nodes)
	# initailizing all the edges to be zero
	for srceLocation in nodes:
		for destLocation in nodes:
			G.add_edge(srceLocation,destLocation,weight=0)

	#making the weights of the edges be the number of times this transition was made
	for index in range(len(userLocationsTuples)-1):
		src = userLocationsTuples[index]
		dest = userLocationsTuples[index + 1]
		G[src][dest]['weight'] += 1

	#making the weight of (src,dest) to be the probebility of dest given src
	for node in nodes:
		#calculate the sum of weights of all the edges contected to node
		sumW = 0.0
		for dest in nodes:
			w = G[node][dest]['weight'] 
			sumW = sumW + w

		# changing the weight of each edge to be -log(weight/sumW) or removing the edge of the probability is 0
		for dest in nodes:
			if G[node][dest]['weight'] == 0:
				G.remove_edge(node,dest)
			else:
				G[node][dest]['weight'] = -1*math.log((G[node][dest]['weight'])/sumW)


if __name__ == "__main__":
    main()
