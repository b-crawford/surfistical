import pandas as pd

# constants
first_year = 2011

mens_womens = 'womens'

results = pd.DataFrame(columns = ['name',
 'nationality'])

events = pd.DataFrame(columns = ['name', 'country', 'location', 'date'])


for year in range(2011,2019):
    events1 = pd.read_csv('data/events_'+mens_womens+'_'+str(year)+'.csv')

    results1 = pd.read_csv('data/results_'+mens_womens+'_'+str(year)+'.csv')


    names = pd.Series([i.split('\n')[0].replace(' ','-').lower() for i in  results1['athlete-headshot-and-name']])
    nationalities = pd.Series([i.split('\n')[1].lower() for i in  results1['athlete-headshot-and-name']])


    results2 = results1.drop(['athlete-tour-rank', 'athlete-headshot-and-name', 'athlete-tour-points', 'athlete-tour-prize-money'],axis = 1)


    results2 = pd.concat([names, nationalities, results2], axis = 1)
    results2.rename(columns={0:'name',
                              1:'nationality'},
                     inplace=True)

    # results = results.merge(results2, how ='outer',left_on = ['name','nationality'],
    # right_on = ['name','nationality'])
    results = pd.merge(results,results2, how ='outer',on = ['name','nationality'],suffixes = ['',''])
    # results = pd.concat([results, results2], axis = 0, sort = False)
    events = pd.concat([events, events1], axis = 0, sort = False)


results.shape
events.shape


results.head()
