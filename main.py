import json
import turtle
import urllib.request

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

    # Extract the ISS location
    location = result["iss_position"]
    lat = float(location['latitude'])
    lon = float(location['longitude'])

    return lon, lat

def main(trail=True):
    iss = setup()
    astronaut_details()

    while True:
        lon, lat = get_coordinates()

        # Update the ISS location on the map
        iss.goto(lon, lat)

        if trail==True:
            iss.dot(size=2) # Plot trail dots

if __name__=='__main__':
    main(trail=False)

