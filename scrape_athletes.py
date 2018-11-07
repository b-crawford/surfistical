from requests_html import HTMLSession
import pandas as pd

url = 'http://www.worldsurfleague.com/athletes?tourIds[]=1'

session = HTMLSession()
r = session.get(url)
links = r.html.absolute_links
links
