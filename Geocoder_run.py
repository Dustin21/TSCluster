from Geocoder import Geocoder
import pandas as pd

cis = pd.read_csv('data/CIS.csv')

test = Geocoder(cis).submit_request()
