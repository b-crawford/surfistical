import pandas as pd
import numpy as np

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


# constants
first_year = 2011
last_year = 2018

mens_womens = 'mens'

results = pd.DataFrame(columns = ['name',
 'nationality'])

events = pd.DataFrame(columns = ['name', 'country', 'location', 'date'])


for year in range(first_year,last_year+1):
    events1 = pd.read_csv('data/events_'+mens_womens+'_'+str(year)+'.csv')

    results1 = pd.read_csv('data/results_'+mens_womens+'_'+str(year)+'.csv')


    names = pd.Series([i.split('\n')[0].replace(' ','-').lower() for i in  results1['athlete-headshot-and-name']])
    nationalities = pd.Series([i.split('\n')[1].lower() for i in  results1['athlete-headshot-and-name']])


    results2 = results1.drop(['athlete-tour-rank', 'athlete-headshot-and-name', 'athlete-tour-points', 'athlete-tour-prize-money'],axis = 1)


    results2 = pd.concat([names, nationalities, results2], axis = 1)
    results2.rename(columns={0:'name',
                              1:'nationality'},
                     inplace=True)

    results = pd.merge(results,results2, how ='outer',on = ['name','nationality'],suffixes = ['',''])
    events = pd.concat([events, events1], axis = 0, sort = False)


results.shape
events.shape


results.head()

events.head()

results = []
i = 0

event_name = events.iloc[i,0]

event_name_no_year = event_name[:-5]
relevant_spots = contest_spots.loc[contest_spots['contest'] == event_name_no_year]['spot_name'][0].split(', ')

indices = [i in relevant_spots for i in spots['spot-name']]
one_hot_spots.loc[indices]
one_hot_spots.loc[indices].sum()


event_country = events.iloc[i,1]
