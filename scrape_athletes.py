from requests_html import HTMLSession
import pandas as pd
from html.parser import HTMLParser
import re


mens_url = 'http://www.worldsurfleague.com/athletes?tourIds[]=1'
womens_url = 'http://www.worldsurfleague.com/athletes?tourIds%5B%5D=2'

url = mens_url

session = HTMLSession()
r = session.get(url)
links = r.html.absolute_links
list(links)

links = [i for i in links
        if 'athletes' in i
        and not 'filter' in i
        and not 'rankings' in i
        and not 'year' in i
        and len(i.replace("http://www.worldsurfleague.com/athletes","")) >1 ]

names = [i.split('/')[-1] for i in links]

links = [y for x,y in sorted(zip(names,links))]
names = [x for x,y in sorted(zip(names,links))]

link = links[0]

r = session.get(link)
html = r.html.text

stance = re.search('Stance\n(.*)\n', html).group(1)
first_season = re.search('First season\n(.*)\n', html).group(1)
current_age = re.search('Age\n(.*)\n', html).group(1).split(" ")[0]
birthday = re.search('Age\n(.*)\n', html).group(1).split(" ")[-3:]
height_imperial = re.search('Height\n(.*)\n', html).group(1).split(" ")[:4]
height_metric = re.search('Height\n(.*)\n', html).group(1).split(" ")[-2:]
weight_imperial = re.search('Weight\n(.*)\n', html).group(1).split(" ")[:2]
weight_metric = re.search('Weight\n(.*)\n', html).group(1).split(" ")[-2:]
hometown = re.search('Hometown\n(.*)\n', html).group(1)
heat_wins = re.search('Heat wins\n(.*)\n', html).group(1)
avg_heat_score = re.search('Avg. heat score\n(.*)\n', html).group(1)
rookie_year = re.search('Rookie year\n(.*)\n', html).group(1)

# we are not currenlty collecting data in the table at the bottom of the page
