from django.urls import path
from .views import home
urlpatterns=[
    path('bus_data/', home, name='bus_data')
    # path('some_path/<int:pk>/', detail_view.as_view( ), name='abc')
]
