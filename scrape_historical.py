from requests_html import HTMLSession
import pandas as pd
import re


# define the function which pulls the grid off the page:
def url_to_table(url):
    # start a session and download table
    session = HTMLSession()
    r = session.get(url)
    table = r.html.find('td')

    # we use the css class of the first column to work out the
    # number of columns in the table. we will also use the class
    # tags as initial column names
    for count, element in enumerate(table):
        if count != 0:
            if element.attrs['class'][0] == css_class_of_first_column_cells:
                ncol = count
                break

    nrow = int(len(table)/ncol)

    # using these dimensions we create an empty dataframe:
    dat = pd.DataFrame(index=range(nrow), columns=range(ncol))

    # we now populate the frame:
    row_index = -1
    column_index = 0
    for element in table:
        if element.attrs['class'][0] == css_class_of_first_column_cells:
            # move down a row if the class is the same as first row
            row_index = row_index + 1
            column_index = 0
        dat.loc[row_index, column_index] = element.text
        column_index = column_index+1

    return(dat)


for mens_womens in ['mens', 'womans']:
    for year in range(2000, 2019, 1):
        print(mens_womens + ' ' + str(year))
        # define the url to scrape from
        if mens_womens == 'mens':
            url = 'http://www.worldsurfleague.com/athletes/tour/mct?sort=rank&year=' + str(year)
            event_url = 'http://www.worldsurfleague.com/events/' + str(year) + '/mct'
        else:
            url = 'http://www.worldsurfleague.com/athletes/tour/wct?sort=rank&year=' + str(year)
            event_url = 'http://www.worldsurfleague.com/events/' + str(year) + '/wct'

        # we will use the css tag of the first column's cells to work out where we are
        # in the table:
        css_class_of_first_column_cells = 'athlete-tour-rank'
        css_class_of_events = 'athlete-event-place'

        css_tag_of_event_name = '.tour-event-name'
        css_tag_of_event_location = '.tour-event-location'
        css_tag_of_event_dates = '.tour-event-range'

        # we first check if the page is displaying the data we are looking for:
        session = HTMLSession()
        r = session.get(url)
        table = r.html.find('.table-intro-primary span')

        last_updated = table[0].text
        year_updated = re.sub(r'.*, ', '', last_updated)

        if str(year) == year_updated:
            page1 = url_to_table(url)

            # they have a next button on the page so we go to next page and repeat the process:
            session = HTMLSession()
            r = session.get(url)
            next_button_list = r.html.find('.next a')
            if next_button_list:
                url = url + '&offset=51'
                page2 = url_to_table(url)
                dat = pd.concat([page1, page2])
            else:
                dat = page1.copy()

            # we now give the columns names which come from
            # the table in question but also the event names
            session = HTMLSession()
            r = session.get(url)
            table = r.html.find('td')

            colnames = []
            for count, element in enumerate(table):
                if count != 0:
                    if element.attrs['class'][0] == css_class_of_first_column_cells:
                        ncol = count
                        break
                colnames = colnames + [element.attrs['class'][0]]

            r = session.get(event_url)

            event_names = r.html.find(css_tag_of_event_name)
            event_names = [i.text for i in event_names]

            colnames2 = [i.replace(" ", "-") for i in event_names]

            event_location = r.html.find(css_tag_of_event_location)
            event_location = [i.text for i in event_location]

            event_date = r.html.find(css_tag_of_event_dates)
            event_date = [i.text for i in event_date]

            # now make a new colnames vector
            colnames = [i for i in colnames if i != css_class_of_events]
            colnames = colnames + colnames2

            dat.columns = colnames

            filepath = 'data/results_' + mens_womens + '_' + str(year) + '.csv'

            dat.to_csv(filepath, index=False)

            # Next we use the rest of the data from the events page to create an
            # events dataframe
            events = pd.DataFrame(
                {'name': event_names,
                 'location': event_location,
                 'date': event_date})

            filepath_events = 'data/events_' + mens_womens + '_' + str(year) + '.csv'

            events.to_csv(filepath_events, index=False)
