from requests_html import HTMLSession
import pandas as pd
import numpy as np

year = 2014
mens_womens = 'womens'

# define the url to scrape from
if mens_womens == 'mens':
    url = 'http://www.worldsurfleague.com/athletes/tour/mct?year=' + str(year)
else:
    url = 'http://www.worldsurfleague.com/athletes/tour/wct?year=' + str(year)


# we will use the css tag of the first column's cells to work out where we are in the table:
css_class_of_first_column_cells = 'athlete-tour-rank'

# start a session and download table
session = HTMLSession()
r = session.get(url)
table = r.html.find('td')

# we use the css class of the first column to work out the number of columns in the table.
# we will also use the class tags as initial column names
colnames = []
for count, element in enumerate(table):
    if count != 0:
        if element.attrs['class'][0] == css_class_of_first_column_cells:
            ncol = count
            break
    colnames = colnames + [element.attrs['class'][0]]

nrow = int(len(table)/ncol)

# using these dimensions we create an empty dataframe:
dat = pd.DataFrame(index = range(nrow), columns = range(ncol))

# we now populate the frame:
row_index = -1
column_index = 0
for element in table:
    if element.attrs['class'][0] == css_class_of_first_column_cells: # move down a row if the class is the same as first row
        row_index = row_index + 1
        column_index = 0
    dat.loc[row_index, column_index] = element.text
    column_index = column_index+1

dat.columns = colnames

# unfortunately these column names are not very descriptive (every event is simply called athlete-event-place)
# we now scrape the event names



dat.head()
