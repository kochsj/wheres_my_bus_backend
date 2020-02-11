from django.shortcuts import render
from django.http import HttpResponse
import requests

# from rest_framework import generics
# from .your_models import YourModel
# from .serializers import YourSerializer
# from .permissions import IsAuthorOrReadOnly



def find_closest_stops(request, lat, lon):

    user_lat = float(lat) or 47.9365944 
    user_lon = float(lon) or -122.219628

    response = requests.get('http://api.pugetsound.onebusaway.org/api/where/stops-for-route/1_100275.json?key=TEST&version=2')
    bus_data = response.json()
    bus_stops = bus_data['data']['references']['stops']

    i = 0
    closest, next_closest = 1, 1
    index_of_closest, index_of_next_closest = 0, 0
    name_of_closest, name_of_next_closest = 'a', 'b'
    closest_direction, next_closest_direction = 'n', 's'
    for stop in bus_stops:

        difference_lat = abs(user_lat - stop['lat'])
        difference_lon = abs(user_lon - stop['lon'])
        difference = difference_lat + difference_lon

        if difference < closest:
            #change next closest
            next_closest = closest
            index_of_next_closest = index_of_closest
            name_of_next_closest = name_of_closest
            next_closest_direction = closest_direction

            #updating closest
            closest = difference
            index_of_closest = i
            name_of_closest = stop['name']
            closest_direction = stop['direction']

        print(i, ': ', difference)
        i+=1
    print('closest: ', name_of_closest, ' ', closest, ' degrees', 'direction: ', closest_direction)
    print('next_closest: ', name_of_next_closest, ' ', next_closest, ' degrees', 'direction: ', next_closest_direction)

    return HttpResponse(f'<h1>Success!\n User_lat: {lat}\n User_lon: {lon}\n name_of_closest: {name_of_closest}\n direction: {closest_direction}\n name_of_next_closest: {name_of_next_closest}\n direction: {next_closest_direction}</h1>')