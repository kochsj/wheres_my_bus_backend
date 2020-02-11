from django.shortcuts import render
from django.http import HttpResponse
import requests
import time

# from rest_framework import generics
# from .your_models import YourModel
# from .serializers import YourSerializer
# from .permissions import IsAuthorOrReadOnly



def find_closest_stops(request, lat, lon):

    user_lat = float(lat) or 47.9365944 
    user_lon = float(lon) or -122.219628

    bus_id = '1_100275'
     
    response = requests.get(f'http://api.pugetsound.onebusaway.org/api/where/stops-for-route/{bus_id}.json?key=TEST&version=2')
    bus_data = response.json()
    bus_stops = bus_data['data']['references']['stops']

    i = 0
    closest, next_closest = 1, 1
    closest_stop_id, next_closest_stop_id = 0, 0
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
            next_closest_stop_id = closest_stop_id

            #updating closest
            closest = difference
            index_of_closest = i
            name_of_closest = stop['name']
            closest_direction = stop['direction']
            closest_stop_id = stop['id']

        # print(i, ': ', difference)
        i+=1

    # print('closest: ', name_of_closest, ' ', closest, ' degrees', 'direction: ', closest_direction)
    # print('next_closest: ', name_of_next_closest, ' ', next_closest, ' degrees', 'direction: ', next_closest_direction)

    closest_arrival = find_estimated_arrival(closest_stop_id, bus_id)
    next_closest_arrival = find_estimated_arrival(next_closest_stop_id, bus_id)


    return HttpResponse(f'<h1>Success!\n User_lat: {lat}\n User_lon: {lon}\n name_of_closest: {name_of_closest}\n direction: {closest_direction}\n closest_stop_id: {closest_stop_id} closest_minutes: {closest_arrival} name_of_next_closest: {name_of_next_closest}\n direction: {next_closest_direction} next_closest_stop_id: {next_closest_stop_id} next_closest_minutes: {next_closest_arrival}</h1>')

def find_estimated_arrival(stop_id, bus_id):

    bus_id = bus_id or '1_100275'
    url = f'http://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/{stop_id}.json?key=TEST'

    response = requests.get(url)
    stop_data = response.json()
    list_of_arrivals = stop_data['data']['entry']['arrivalsAndDepartures']

    arrival_time = 0
    current_time = ((time.time()) *1000)

    for arrival in list_of_arrivals:
        if arrival['routeId'] == bus_id:
            if arrival['predictedArrivalTime'] != 0:
                arrival_time = arrival['predictedArrivalTime']
            else:
                arrival_time = arrival['scheduledArrivalTime']
            
        if arrival_time > current_time:
            return ((arrival_time - current_time)//60000)


