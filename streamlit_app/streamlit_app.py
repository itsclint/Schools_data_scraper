#import python parkages 
from functools import cache
from typing import Tuple
import streamlit as st
import googlemaps
import time
import pandas as pd
import geopandas as gpd
import geopy
from shapely.geometry import Point, Polygon

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter



st.title("Schools Data Scrapper")

API_KEY = 'AIzaSyDr4i3TPaSc-7gruLAcKHVM6Bf8yYIRd9o'

#convert miles to meters
def miles_to_meters(miles):
    """
    converts miles to meters
    
    Arguments:
        miles: int
    Returns:
        meter equivalent of input argument   
    """
    try:
        return miles * 1_609.344

    except:
        return 0   



@cache
def get_map_data(coordinate):
    map_client = googlemaps.Client(API_KEY)

    Location = coordinate

    distance = miles_to_meters(5)

    schools_list = []

    response = map_client.places_nearby(
        location=Location,
        radius=10000,
        type='school'
        )
    schools_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')

    while next_page_token:
       time.sleep(5)
       response = map_client.places_nearby(
        location=Location,
        radius=1000,
        page_token=next_page_token
    )   

    schools_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')
    df = pd.DataFrame(schools_list)
    df['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df['place_id']

    return st.dataframe(df)   


Area = st.sidebar.text_input("Area", "lekki phase 1")
City = st.sidebar.text_input("City", "Lekki")
State = st.sidebar.text_input("Province", "Lagos")
Country = st.sidebar.text_input("Country", "Nigeria")

geolocator = Nominatim(user_agent="GTA Lookup")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
location = geolocator.geocode(Area+", "+City+", "+State+", "+Country)

lat = location.latitude
lon = location.longitude

map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

st.map(map_data, zoom=30)


coordinate = (lat,lon)

get_map_data(coordinate)





    



