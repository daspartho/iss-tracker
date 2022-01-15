import json
import turtle
import urllib.request

def get_coordinates():
    response = urllib.request.urlopen("http://api.open-notify.org/iss-now.json")
    result = json.loads(response.read())   
    location = result["iss_position"]
    lat = float(location['latitude'])
    lon = float(location['longitude'])
    return lon, lat

def main():
    turtle.title('ISS Tracker')
    screen = turtle.Screen()
    screen.setup(1189, 848)
    screen.setworldcoordinates(-180,-90,180,90)
    screen.bgpic("map.gif")   
    screen.register_shape("iss.gif")
    iss = turtle.Turtle()
    iss.shape("iss.gif")
    iss.penup()
    
    while True:
        lon, lat = get_coordinates()
        iss.goto(lon, lat)

if __name__=='__main__':
    main()

