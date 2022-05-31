import csv
import geocoder

with open('cities2019_utf8.csv','r') as file1, open('citieslist19.csv','w') as file2:
	csvFile = csv.reader(file1)
	unique_cities = []
	city_counts = []
	lats = []
	lons = []
	for row in csvFile:
		for chunk in row:
			if chunk == '':
				break
			else:
				if '¬†' in chunk:
					splitup = chunk.split('¬†')
					chunk = splitup[0] + splitup[1]
				if not chunk in unique_cities:
					print(chunk)
					unique_cities.append(chunk)
					city_counts.append(1)
					g = geocoder.osm(chunk)
					latlng = g.latlng
					if latlng != None:	
						lats.append(latlng[0])
						lons.append(latlng[1])
					else:
						lats.append(0)
						lons.append(0)			
				else:
					index = unique_cities.index(chunk)
					city_counts[index] += 1
	csvwriter = csv.writer(file2)
	cols = ['city','frequency','latitude','longitude']
	csvwriter.writerow(cols)
	for i in range(len(unique_cities)):
		city_list = [unique_cities[i],city_counts[i],lats[i],lons[i]]
		csvwriter.writerow(city_list)
