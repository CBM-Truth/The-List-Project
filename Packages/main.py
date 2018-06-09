import googlemaps
import bs4 as bs
import requests
import operator 

#Initialize API Client Connection with provided API Key.
key = '<API KEY>'
maps = googlemaps.Client(key=key)

#Grab contents of webpage.
page = requests.get('http://www.foopee.com/punk/the-list/')

#Creat BeauitfulSoup object as an HTML parser for acquired webpage.
soup = bs.BeautifulSoup(page.content, 'html.parser')

#Find all elements with a 'dd' tag within the HTML page.
dd_elements = soup.find_all('dd')

#Pick out desired table from the 'dd' tag elements.
table = dd_elements[len(dd_elements) - 1]

#Find all anchor elements within the table.
anchors = table.find_all('a')

#Populate list with locations as strings acquired from the table.
locations = [a.contents[0] for a in anchors]

#Initialize auxiliary dictionary
distances = {}

#Looping through each location string.
for location in locations:
	#Call googlemaps API to initialize distance matrix
	route = maps.distance_matrix('UC Berkeley', location)
	#Parsing object returned from the API call
	rows = route.get('rows')
	rowDict = rows[0]
	elements = rowDict.get('elements')
	subDict = elements[0]
	dct = subDict.get('distance')
	#If the object returned from the API is initialized,
	#pull raw distance from API object.
	#Print "Address invalid." otherwise.
	if type(dct) is dict:
		distance = dct.get('value')
		distances[location] = distance / 1000
	else:
		print('Address invalid.')

#Convert dictionary into a list of tuples in the form of (location, distance)
# sorted by raw distance.
distances = sorted(distances.items(), key=operator.itemgetter(1))

#Print out contents of the list in ascending order.
for pair in distances:
	print(pair[0] + ' - ' + str(pair[1]) + 'KM')

#Write contents of the list in ascending order to an output file.
with open('output.txt', 'w+') as f:
	for pair in distances:
		if pair[0] is not None and pair[1] is not None:
			f.write(pair[0] + ' - ' + str(pair[1]) + 'KM' + '\n')
	f.close()












