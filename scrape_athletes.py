from requests_html import HTMLSession
import pandas as pd
import re
import datetime
import scrape_function


for mens_womens in ['mens', 'womens']:
    if mens_womens == 'mens':
        url = 'http://www.worldsurfleague.com/athletes?tourIds[]=1'
    else:
        url = 'http://www.worldsurfleague.com/athletes?tourIds%5B%5D=2'

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

    for i, link in enumerate(links):
        print(mens_womens + str(i))

        name = names[i]

        r = session.get(link)
        html = r.html.text

        stance = scrape_function.pull_data(html, 'Stance\n', '\n')
        first_season = scrape_function.pull_data(html, 'First season\n', '\n')
        current_age = scrape_function.pull_data(html,'Age\n(.*)','\n',string_split_end = 1)
        birthday = scrape_function.pull_data(html, 'Age\n(.*)','\n',string_split_start = -3)
        height_imperial = scrape_function.pull_data(html,'Height\n','\n',string_split_end = 4)
        height_metric = scrape_function.pull_data(html,' Height\n','\n',string_split_start = -2)
        weight_imperial = scrape_function.pull_data(html,'Weight\n','\n',string_split_end = 2)
        weight_metric = scrape_function.pull_data(html, 'Weight\n','\n',string_split_start = -2)
        hometown = scrape_function.pull_data(html, 'Hometown\n','\n')
        heat_wins = scrape_function.pull_data(html, 'Heat wins\n','\n')
        avg_heat_score = scrape_function.pull_data(html,'Avg. heat score\n','\n')
        rookie_year = scrape_function.pull_data(html, 'Rookie year\n', '\n')


        # we are not currenlty collecting data in the table at the bottom of the page

        row = [name,stance,first_season,current_age,birthday,height_imperial,
                height_metric,weight_imperial,weight_metric,hometown,heat_wins,
                avg_heat_score,rookie_year]

        df.iloc[i] = row

    year = str(datetime.datetime.now().year)
    filepath = 'data/athletes_' +mens_womens+'_'+year+'.csv'
    df.to_csv(filepath, index = False)
