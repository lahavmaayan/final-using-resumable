README file

DESCRIPTIONS:

	Welcom to the project By The Way! and thank you for reading this file :)
	By The Way is a project that allow you to create your own map (based on the locations gathered by Google) and even combain few maps
	into one map! using this you can find the shortest path between two locations in that combined map!

	the shortest path will be calculated based on the probability of the specific person to travel from one location to another. 
	A path will cross over between two personal maps if the two persons visited that same location.

	So, If you want to use this project all you need is to download your data (connected to your gmail account) from google dashboard and 
	use this programs.

	Pay attention, this code will only work using python 2.7 (and NOT! python 3.x) and using the following packages - pygmaps, numpy, networkx, sklearn.cluster.

HOW TO RUN OUR PROGRAMS:

	You can either use the data you downloaded from google (instructions below) or use the data attached to this file 
	(maayan.json and benny.json - both data of real people)

	In this project you can use one of two programs, for different uses:

	1. createPersonalMap.py - this program recieves a path to a json file containing your data, and will create an HTML file in the current
		directory (from which you ran the program) by the name of myMap.html . 
		The HTML file contains the main locations you visited (inside Israel only), displyed using google maps.
		There is a HTML attached to this file, by the name of - myMapExample.html
		
		Usage instructions in the cmd/shell/terminal write the following line:
		python createPersonalMap.py <PATH TO JSON FILE>

		(pay attention that if you want to insert pathes in the current directory, you should add  ./ in Linux or mac or .\ in Windows before the name of the json file)

		for example, using the data attached to this file, which is in the same directory of the python file, can write:
		In Windows: python createPersonalMap.py .\maayan.json
		In Linux or Mac: python createPersonalMap.py ./maayan.json

	2. getShortestPath.py - this program recieves at least one path to a json file containing your data and two decimal coordinates (must be inside Israel) 
		of the path - source and dest.
		The program will create a combined map of the given json data files, and calculate the shortest path between the two given coordinates (source and dest),
		using only locations (inside Israel) on the combined map. 
		The combined map and the path will be displayed on a HTML file that will be generated on the current directory (from which your ran the program) 
		by the name of shortestPath.html .
		There is an example of a HTML attached to this file, by the name of - shortestPathExample.html

		Usage instructions in the cmd/shell/terminal write the following line:
		python createPersonalMap.py <PATH TO JSON FILE>...<PATH TO JSON FILE> <SOURCE LATITUDE> <SOURCE LONGTITUDE> <DESTINATION LATITUDE> <DESTINATION LONGTITUDE>

		for example, using the data attached to this file, which is in the same directory of the python file, can write:
		In Linux or Mac: python createPersonalMap.py ./maayan.json ./benny.json 32.775595 35.020718 31.3455 34.4021
		In Windows: python createPersonalMap.py .\maayan.json .\benny.json 32.775595 35.020718 31.3455 34.4021


HOW TO DOWNLOAD YOUR OWN LOCATION'S DATA FROM GOOGLE:

	use this link to connect to your gmail account and download the data:
	https://www.google.com/settings/takeout/custom/location_history?hl=en&gl&expflags

	Pay attention that generating the data takes around 4-5 minutes, after which you can download it, The file size would be around several MBs.