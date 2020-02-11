from django.urls import path
from .views import find_closest_stops
urlpatterns=[
    path('bus_data/<lat>/<lon>', find_closest_stops, name='bus_data')
    # path('some_path/<int:pk>/', detail_view.as_view( ), name='abc')
]
