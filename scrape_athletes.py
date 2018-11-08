from requests_html import HTMLSession
import pandas as pd
from html.parser import HTMLParser
import re
import numpy as np

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

df = pd.DataFrame(index = range(len(links)),columns=['name','stance','first_season','current_age','birthday','height_imperial',
        'height_metric','weight_imperial','weight_metric','hometown','heat_wins','avg_heat_score','rookie_year'])

# testing
link = links[2]
r = session.get(link)
html = r.html.text

def pull_data(start_term, end_term, string_split_start = 0, string_split_end = None):
    pull1 = re.search(start_term + '(.*)' + end_term, html)
    try:
        pull2 = pull1.group(1)
        split = pull2.split(' ')
        if string_split_end is None:
            string_split_end = len(split)
        pull3 = split[string_split_start:string_split_end]
        join = " ".join(pull3)
        return(join)
    except:
        return(None)


for i, link in enumerate(links):
    print(i)

    name = names[i]

    r = session.get(link)
    html = r.html.text

    stance = pull_data('Stance\n','\n')
    first_season =  pull_data('First season\n','\n')
    current_age = pull_data('Age\n(.*)','\n',string_split_end = 1)
    birthday = pull_data('Age\n(.*)','\n',string_split_start = -3)
    height_imperial = pull_data('Height\n','\n',string_split_end = 4)
    height_metric = pull_data('Height\n','\n',string_split_start = -2)
    weight_imperial = pull_data('Weight\n','\n',string_split_end = 2)
    weight_metric = pull_data('Weight\n','\n',string_split_start = -2)
    hometown = pull_data('Hometown\n','\n')
    heat_wins = pull_data('Heat wins\n','\n')
    avg_heat_score = pull_data('Avg. heat score\n','\n')
    rookie_year = pull_data('Rookie year\n','\n')


    # we are not currenlty collecting data in the table at the bottom of the page

    row = [name,stance,first_season,current_age,birthday,height_imperial,
            height_metric,weight_imperial,weight_metric,hometown,heat_wins,
            avg_heat_score,rookie_year]

    df.iloc[i] = row


df.head()
