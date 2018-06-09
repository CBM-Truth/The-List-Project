import googlemaps
import bs4 as bs
import requests
import operator 

key = '<API KEY>'
maps = googlemaps.Client(key=key)

page = requests.get('http://www.foopee.com/punk/the-list/')

soup = bs.BeautifulSoup(page.content, 'html.parser')

dd_elements = soup.find_all('dd')

table = dd_elements[len(dd_elements) - 1]

anchors = table.find_all('a')

locations = [a.contents[0] for a in anchors]

distances = {}

for location in locations:
	route = maps.distance_matrix('UC Berkeley', location)
	print('pass')
	rows = route.get('rows')
	rowDict = rows[0]
	elements = rowDict.get('elements')
	subDict = elements[0]
	dct = subDict.get('distance')
	if type(dct) is dict:
		distance = dct.get('value')
		distances[location] = distance / 1000
	else:
		print('Address invalid.')

distances = sorted(distances.items(), key=operator.itemgetter(1))

for pair in distances:
	print(pair[0] + ' - ' + str(pair[1]) + 'KM')

with open('output.txt', 'w+') as f:
	for pair in distances:
		if pair[0] is not None and pair[1] is not None:
			f.write(pair[0] + ' - ' + str(pair[1]) + 'KM' + '\n')
	f.close()












