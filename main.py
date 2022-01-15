import json
import turtle
import urllib.request

def setup():
    turtle.title('ISS Tracker')
    screen = turtle.Screen()
    screen.setup(1189, 848)
    screen.setworldcoordinates(-180,-90,180,90)
    screen.bgpic("map.gif")   
    screen.register_shape("iss.gif")
    iss = turtle.Turtle()
    iss.shape("iss.gif")
    iss.penup()
    return iss

def astronaut_details():
    response = urllib.request.urlopen("http://api.open-notify.org/astros.json")
    result = json.loads(response.read())
    n= result["number"]
    print(f"There are currently {n} astronauts on the ISS: ")
    people = result["people"]
    
    for p in people:
        print(p['name'])

def get_coordinates():
    response = urllib.request.urlopen("http://api.open-notify.org/iss-now.json")
    result = json.loads(response.read())   
    location = result["iss_position"]
    lat = float(location['latitude'])
    lon = float(location['longitude'])
    return lon, lat

def main():
    iss = setup()
    astronaut_details()

    while True:
        lon, lat = get_coordinates()
        iss.goto(lon, lat)

if __name__=='__main__':
    main()

