import os
import pandas as pd
from requests_html import HTMLSession
import scrape_function

spots = pd.read_csv('manual_data/spots.csv')
new_cols = ['tide', 'type', 'bed', 'swell_direction', 'wind_direction',
            'max_swell', 'min_swell']

for col in new_cols:
    spots[col] = None

for j in range(len(spots)):
    url = spots.iloc[j,1]
    session = HTMLSession()
    r = session.get(url)

    html = r.html.text

    spots['tide'][j] = scrape_function.pull_data(html, 'Best Tide - ', '\n')
    spots['type'][j] = scrape_function.pull_data(html, 'Character / Type - ', '\n')
    spots['bed'][j]  = scrape_function.pull_data(html, 'Seabed - ', '\n')
    spots['swell_direction'][j] = scrape_function.pull_data(html, 'Swell Direction - ', '\n')
    spots['wind_direction'][j] = scrape_function.pull_data(html, 'Wind Direction - ', '\n')
    spots['max_swell'][j] = scrape_function.pull_data(html, 'Max Swell - ', '\n', string_split_end=1)
    spots['min_swell'][j] = scrape_function.pull_data(html, 'Min Swell - ', '\n')

cols = ['spot-name','url']+new_cols
row = pd.Series(['surf-ranch',None,'All Tides','Peaky Beachbreak','Sand',None,None,'6ft','3ft'],index=cols)
spots = spots.append(row, ignore_index=True)

spots.to_csv('manual_data/spots.csv', index = False)
