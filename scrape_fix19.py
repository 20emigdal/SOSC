import requests
from bs4 import BeautifulSoup
import csv

headers = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15" }

file = open('cities2019_0.csv','w')
writer = csv.writer(file)

def find_city(link):
	response = requests.get(link, headers = headers)
	soup = BeautifulSoup(response.text, 'html.parser')
	tables = soup.find_all('table')
	num = 3
	if '**Please see images for: ' in soup.get_text():
		num = 4
	row = tables[num].find('tr')
	inventors = row.find('td').contents
	cities = []
	for i in range(len(inventors)):
		if '(' in inventors[i] and ')' in inventors[i]:
			chunk = inventors[i]
			city = chunk[2:(len(chunk)-1)].strip(')')
			cities.append(city)
	print(cities)
	writer.writerow(cities)

for i in range(1600,1700):
	url = 'https://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=' + str(i+1) + '&f=G&l=50&d=PTXT&p=1&S1=((((%22San+Francisco%22.ASCI.)+AND+%40AD%3E%3D20190101%3C%3D20191231)+AND+US.INCO.)+AND+(G06$.CPCL.+OR+H04L.CPCL.))&OS=AC/%22San+Francisco%22+and+APD/1/1/2019-%3E12/31/2019+and+ICN/US+and+(CPCL/G06$+or+CPCL/H04L)&RS=(((AC/%22San+Francisco%22+AND+APD/20190101-%3E20191231)+AND+ICN/US)+AND+(CPCL/G06$+OR+CPCL/H04L))'
	print(i)
	find_city(url)
	
file.close()
