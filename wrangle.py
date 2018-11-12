import pandas as pd
import numpy as np

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
athletes
athletes.head()

one_hot_athletes = pd.DataFrame(athletes['name'])









# WRANGLE:

output = []
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
