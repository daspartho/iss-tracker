import json
import turtle
import urllib.request
import time

screen = turtle.Screen()
screen.setup(1189, 848)
screen.setworldcoordinates(-180,-90,180,90)

screen.bgpic("map.gif")
screen.register_shape("iss.gif")
iss = turtle.Turtle()
iss.shape("iss.gif")
#iss.setheading(45)
iss.penup()

while True:
    url="http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())

    location = result["iss_position"]
    lat = float(location['latitude'])
    lon = float(location['longitude'])
    
    iss.goto(lon, lat)
    if not iss.isdown():
        iss.pendown()
    #time.sleep(5)
