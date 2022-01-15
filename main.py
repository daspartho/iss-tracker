import json
import turtle
import urllib.request
from math import radians, cos, sin, asin, sqrt
from geopy.geocoders import Nominatim
import time as time_module

def setup():
    turtle.title('ISS Tracker')

    # Setup the world map
    screen = turtle.Screen()
    screen.setup(1189, 848)
    screen.setworldcoordinates(-180,-90,180,90)
    screen.bgpic("map.gif") 

    # Setup ISS object
    screen.register_shape("iss.gif")
    iss = turtle.Turtle()
    iss.shape("iss.gif")
    iss.penup()

    return iss # return ISS object

def astronaut_details():
    # load the current status of astronauts on ISS in real-time
    response = urllib.request.urlopen("http://api.open-notify.org/astros.json")
    result = json.loads(response.read())

    # Extract and print the astronaut's details
    n= result["number"]
    print(f"There are currently {n} astronauts on the ISS: ")
    people = result["people"]
    for p in people:
        print(p['name'])

def get_coordinates():
    # load the current status of the ISS in real-time
    response = urllib.request.urlopen("http://api.open-notify.org/iss-now.json")
    result = json.loads(response.read())   

    # Extract the ISS location and time
    location = result["iss_position"]
    lat = float(location['latitude'])
    lon = float(location['longitude'])
    time = result["timestamp"]

    return lon, lat, time

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def calspeed(lon1, lat1, time1, lon2, lat2, time2):
    d = haversine(lon1, lat1, lon2, lat2)
    t = time2-time1 or 1 # incase of 0 time difference change to 1 to handle ZeroDivisionError
    return round((d/t)*3600, 2) # returns speed in kilometers per hour rounded upto 2nd decimal place

def getloc(lon, lat):
    geolocator = Nominatim(user_agent="geoapiExercises") # initialize Nominatim API
    location = geolocator.reverse(f'{lat},{lon}')
    if location==None:
        return 'Ocean' 
    address = location.raw['address']
    country = address.get('country', '')
    return country

def main(trail=True):
    iss = setup()
    astronaut_details()

    prevlon, prevlan, prevtime = get_coordinates() # initialize reference values

    while True:
        lon, lat, time = get_coordinates()
        speed = calspeed(prevlon, prevlan, prevtime, lon, lat, time)

        # Update the ISS location on the map
        iss.goto(lon, lat)

        if trail==True:
            iss.dot(size=2) # Plot trail dots

        # Output speed and country to terminal
        print(f'Speed: {speed} km/hr')
        print(f'Above {getloc(lon, lat)}')

        prevlon, prevlan, prevtime = lon, lat, time # update reference values
        time_module.sleep(5) # Referesh each 5 seconds

if __name__=='__main__':
    main(trail=False)