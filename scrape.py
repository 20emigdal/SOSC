import requests
from bs4 import BeautifulSoup
import csv

start = 'https://patft.uspto.gov'

headers = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15" }

file = open('cities2020.csv','w')
writer = csv.writer(file)

def find_city(link):
	response = requests.get(link, headers = headers)
	soup = BeautifulSoup(response.text, 'html.parser')
	tables = soup.find_all('table')
	row = tables[3].find('tr')
	inventors = row.find('td').contents
	cities = []
	for i in range(len(inventors)):
		if '(' in inventors[i] and ')' in inventors[i]:
			chunk = inventors[i]
			city = chunk[2:(len(chunk)-1)].strip(')')
			cities.append(city)
	print(cities)

	table = soup.find('center').find('table')
	row = table.find_all('tr')[1]
	links = row.find_all('a')
	if len(links) == 5 and links[3].img.get('alt') == '[NEXT_DOC]':
		next = links[3].get('href')
	else:
		if links[1].img.get('alt') == '[NEXT_LIST]':
			response_page = requests.get((start + links[1].get('href')), headers = headers)
			soup_page = BeautifulSoup(response_page.text,'html.parser')
			rows = soup.find_all('tr')
			chunk = rows[1].find('td').find_all('a')
			next = chunk[3].get('href')
		elif links[2].img.get('alt') == '[NEXT_LIST]':
			response_page = requests.get(start + links[2].get('href'), headers = headers)
			soup_page = BeautifulSoup(response_page.text, 'html.parser')
			rows = soup_page.find('table').find_all('tr')
			chunk = rows[1].find_all('td')[3]
			next = chunk.find('a').get('href')
		elif links[2].img.get('alt') == '[NEXT_DOC]':
			next = links[2].get('href')
		else:
			next = None

	writer.writerow(cities)

	return next
		
url = 'https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=1&f=G&l=50&d=PTXT&s1=((((%22San+Francisco%22.ASCI.)+AND+%40AD%3E%3D20200101%3C%3D20201231)+AND+US.INCO.)+AND+(G06$.CPCL.+OR+H04L.CPCL.))&p=1&OS=AC/%22San+Francisco%22+and+APD/1/1/2020-%3E12/31/2020+and+ICN/US+and+(CPCL/G06$+or+CPCL/H04L)&RS=(((AC/%22San+Francisco%22+AND+APD/20200101-%3E20201231)+AND+ICN/US)+AND+(CPCL/G06$+OR+CPCL/H04L))'

url1 = 'https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=2&f=G&l=50&d=PTXT&s1=((((%22San+Francisco%22.ASCI.)+AND+%40AD%3E%3D20200101%3C%3D20201231)+AND+US.INCO.)+AND+(G06$.CPCL.+OR+H04L.CPCL.))&p=1&OS=AC/%22San+Francisco%22+and+APD/1/1/2020-%3E12/31/2020+and+ICN/US+and+(CPCL/G06$+or+CPCL/H04L)'

url50 = 'https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=50&f=G&l=50&d=PTXT&p=1&S1=((((%22San+Francisco%22.ASCI.)+AND+%40AD%3E%3D20190101%3C%3D20191231)+AND+US.INCO.)+AND+(G06$.CPCL.+OR+H04L.CPCL.))&OS=AC/%22San+Francisco%22+and+APD/1/1/2019-%3E12/31/2019+and+ICN/US+and+(CPCL/G06$+or+CPCL/H04L)&RS=(((AC/%22San+Francisco%22+AND+APD/20190101-%3E20191231)+AND+ICN/US)+AND+(CPCL/G06$+OR+CPCL/H04L))'

print(find_city(url50))

find_city(url)

next_link = start + find_city(url1)
while next_link != None:
	next_url = start + find_city(next_link)
	next_link = next_url

file.close()
