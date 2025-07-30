"""Routes."""

from django.urls import path

from . import views

app_name = "evemap"

urlpatterns = [
    path("", views.index, name="index"),
    path("geospatial/<str:layer>/", views.geospatial, name="geospatial"),
]
