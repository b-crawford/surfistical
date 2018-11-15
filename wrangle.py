import pandas as pd
import numpy as np
from scrape_function import pull_data
from requests_html import HTMLSession
import re



# safe read csv files
def safe_read(filepath):
    try:
        tab = pd.read_csv(filepath)
        return(tab)
    except:
        return(None)

# constants
first_year = 2011
last_year = 2018

mens_womens = 'mens'


# spot data
spots = pd.read_csv('manual_data/spots.csv').fillna(' - ')
contest_spots =  pd.read_csv('manual_data/contest_spots.csv')

# one-hot encode spot spot characteristics
one_hot_spots = pd.DataFrame(spots['spot-name'])
one_hot_spots[['tide','bed','swell_direction','wind_direction']] = spots[['tide','bed','swell_direction','wind_direction']]

one_hot_spots['swell_direction_left'] = [i.split(' - ')[0] for i in spots['swell_direction']]
one_hot_spots['swell_direction_right'] = [i.split(' - ')[1] for i in spots['swell_direction']]

one_hot_spots['max_swell'] = [i[:-2] for i in spots['max_swell']]
one_hot_spots['min_swell'] = [i[:-2] for i in spots['min_swell']]
one_hot_spots['max_swell'] = pd.to_numeric(one_hot_spots['max_swell'])
one_hot_spots['min_swell'] = pd.to_numeric(one_hot_spots['min_swell'])

one_hot_spots['Right'] = ['right' in i.lower() for i in spots['type']]
one_hot_spots['Left'] = ['left' in i.lower() for i in spots['type']]
one_hot_spots['Peaky'] = ['peaky' in i.lower() or 'peaks' in i.lower() for i in spots['type']]

one_hot_spots['Reef'] = ['reef' in i.lower() for i in spots['type']]
one_hot_spots['Beach'] = ['beach' in i.lower() for i in spots['type']]
one_hot_spots['Point'] = ['point' in i.lower() for i in spots['type']]
one_hot_spots['Pier'] = ['pier' in i.lower() for i in spots['type']]


one_hot_spots = pd.concat([one_hot_spots['spot-name'] ,pd.get_dummies(one_hot_spots.drop(['spot-name'], axis = 1))], axis = 1)
one_hot_spots.head()


# combine all results into same dataframe
results = pd.DataFrame(columns = ['name','nationality'])
events = pd.DataFrame(columns = ['name', 'country', 'location', 'date'])
athletes = pd.DataFrame(columns = ['name','stance','first_season','current_age','birthday','height_imperial','height_metric',
 'weight_imperial','weight_metric','hometown','heat_wins','avg_heat_score','rookie_year'])


for year in range(first_year,last_year+1):
    events1 = safe_read('data/events_'+mens_womens+'_'+str(year)+'.csv')
    results1 = safe_read('data/results_'+mens_womens+'_'+str(year)+'.csv')
    athletes1 = safe_read('data/athletes_' +mens_womens+'_'+str(year)+'.csv')


    names = pd.Series([i.split('\n')[0].replace(' ','-').lower() for i in  results1['athlete-headshot-and-name']])
    nationalities = pd.Series([i.split('\n')[1].lower() for i in  results1['athlete-headshot-and-name']])


    results2 = results1.drop(['athlete-tour-rank', 'athlete-headshot-and-name', 'athlete-tour-points', 'athlete-tour-prize-money'],axis = 1)


    results2 = pd.concat([names, nationalities, results2], axis = 1)
    results2.rename(columns={0:'name',
                              1:'nationality'},
                     inplace=True)

    results = pd.merge(results,results2, how ='outer',on = ['name','nationality'],suffixes = ['',''])
    events = pd.concat([events, events1], axis = 0, sort = False)
    athletes = pd.concat([athletes, athletes1], axis = 0, sort = False)


# combine all athlete data into one:
athletes = athletes.fillna('')
athletes.head()

# Extract columns we are going to use:
athletes_use = pd.DataFrame(athletes['name'])
athletes_use['stance'] = athletes['stance']
athletes_use['birthyear'] = [i.split(', ')[1] for i in athletes['birthday']]
athletes_use['height'] = [i.split(' ')[0] for i in athletes['height_metric']]
athletes_use['weight'] = [i.split(' ')[0] for i in athletes['weight_metric']]
athletes_use['homecountry'] =  [i.split(', ')[-1:][0] for i in athletes['hometown']]
athletes_use[['rookie_year']] = athletes[['rookie_year']]

# note we are not using avg heat score or heat wins as they refer to the very
# contests we are training the system on

# merge with all athletes in result set:
all_athletes = pd.DataFrame(results['name'])
athletes_use = pd.merge(athletes_use,all_athletes, how ='outer',on = ['name'],suffixes = ['',''])

athletes_use.head()
# see what data is missing:
athletes_use = athletes_use.replace('',np.nan, regex=True)
athletes_use.isna().sum()

athletes_use.loc[athletes_use['birthyear'].isna(),].head()

# try and gather missing data from Wikipedia:
missing = athletes_use.loc[athletes_use.isna().any(axis = 1)].reset_index(drop = True)
complete = athletes_use.loc[~athletes_use.isna().any(axis = 1)]


missing.iloc[64]

for i in range(len(missing)):
    # i = 64
    name = '_'.join([j.capitalize() for j in missing['name'][i].split('-')])
    # print('{:.1f}% complete'.format(100*(i+1)/len(missing)))

    url = 'https://en.wikipedia.org/wiki/'+name

    session = HTMLSession()
    r = session.get(url)

    html = r.html.text
    html = re.sub('[^A-Za-z0-9]+', ' ', html)

    stance = pull_data(html, 'Stance', 'foot', string_split_end=2)
    born = pull_data(html, 'Born', 'age', string_split_end=2)
    height = pull_data(html, 'Height', ' m ')
    weight = pull_data(html, 'Weight', ' kg ')
    hometown = pull_data(html, "Born", "Residence", string_split_start=-2)

    if 'in' in height: # sometimes inches are on the wikipedia page aswell
        height = height.split('in')[-1:][0]

    if 'lb' in weight: # sometimes inches are on the wikipedia page aswell
        weight = weight.split('lb')[-1:][0]

    if len(hometown) ==1: # sometimes hometown is only one letter
        hometown = pull_data(html, "Born", "Residence", string_split_start=-3)

    if len(born) <4: # sometimes hometown is only one letter
        born = pull_data(html, 'Born', 'age',string_split_start=3,string_split_end=4)

    try: # sometimes birthyear is not numeric
        born =  int(born)
    except:
        born = np.nan

    try: # sometimes birthyear is not numeric
        weight =  int(weight)
    except:
        weight = np.nan

    if weight > 150:
        weight = np.nan

    if born > 1970: # if theyre really old its probably not them
        row = [stance,born,height,weight,hometown, None]
    else:
        row = [None,None,None,None,None, None]

    missing = missing.fillna('')
    for k in range(len(row)):
        if missing.iloc[i,k+1] =='':
            missing.iloc[i,k+1] = row[k]

athletes_use = pd.concat([missing,complete]).reset_index(drop=True)

home_countries_conversion = {   'Carioca':'Brazil',
                                'Central Coast NSW Australia':'Australia',
                                'Florianopolis':'Brazil',
                                'US': 'USA',
                                'States':'USA'}

athletes_use = athletes_use.replace({'homecountry':home_countries_conversion})

chunk = -1
chunk = chunk +1
athletes_use.iloc[(chunk*5):(chunk+1)*5]

athletes_use.iloc[14,5]
# wierd homecountries:



# WRANGLE:

)output = []
i = 4

# gather event information
event_name = events.iloc[i,0]
event_country = events.iloc[i,1]

# gather spot information
event_name_no_year = event_name[:-5]
relevant_spots = list(contest_spots.loc[contest_spots['contest'] == event_name_no_year]['spot_name'])[0].split(', ')
indices = [i in relevant_spots for i in spots['spot-name']]
spot_chars = [np.mean(one_hot_spots.loc[indices]['max_swell']),np.mean(one_hot_spots.loc[indices]['min_swell'])]+[int(i >0) for i in one_hot_spots.drop(['spot-name','max_swell','min_swell'], axis = 1).loc[indices].sum()]
spot_chars_names = one_hot_spots.columns[1:]

# gather athlete information
col_index = i+2
use_dat = results.iloc[:,:col_index]

use_dat.head()

j = 0
athlete = use_dat.iloc[j,0]
athlete
