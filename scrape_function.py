import re
from pdb import set_trace as bp

def pull_data(html,start_term, end_term, string_split_start = 0, string_split_end = None):
    pull1 = re.search(start_term + '(.*)' + end_term, html)
    try:
        pull2 = pull1.group(1)
        split = pull2.split(' ')
        if string_split_end is None:
            pull3 = split[string_split_start:len(split)]
        else:
            pull3 = split[string_split_start:string_split_end]
        join = " ".join(pull3)
        return(join)
    except:
        return('Test')


# 
#
# # testing
# import pandas as pd
# from requests_html import HTMLSession
# mens_womens ='mens'
# i=1
#
# if mens_womens == 'mens':
#     url = 'http://www.worldsurfleague.com/athletes?tourIds[]=1'
# else:
#     url = 'http://www.worldsurfleague.com/athletes?tourIds%5B%5D=2'
#
# session = HTMLSession()
# r = session.get(url)
# links = r.html.absolute_links
# list(links)
#
# links = [i for i in links
#         if 'athletes' in i
#         and not 'filter' in i
#         and not 'rankings' in i
#         and not 'year' in i
#         and len(i.replace("http://www.worldsurfleague.com/athletes","")) >1 ]
#
# names = [i.split('/')[-1] for i in links]
#
# links = [y for x,y in sorted(zip(names,links))]
# names = [x for x,y in sorted(zip(names,links))]
#
# df = pd.DataFrame(index = range(len(links)),columns=['name','stance','first_season','current_age','birthday','height_imperial',
#         'height_metric','weight_imperial','weight_metric','hometown','heat_wins','avg_heat_score','rookie_year'])
#
#
# link = links[i]
# r = session.get(link)
# html = r.html.text
#
# name = names[i]
#
#
# start_term = 'Height\n'
# end_term = '\n'
# string_split_start = -2
# string_split_end = None
#
# pull1 = re.search(start_term + '(.*)' + end_term, html)
# pull1
#
#
# pull2 = pull1.group(1)
# split = pull2.split(' ')
# if string_split_end is None:
#     pull3 = split[string_split_start:len(split)]
# else:
#     pull3 = split[string_split_start:string_split_end]
# join = " ".join(pull3)
#
# pull_data(html,'Height\n','\n',string_split_start = -2)
#
# pull_data(html,'Height\n','\n',string_split_end = 4)
