# coding: utf-8

"""
URL Dispatcher
"""

from django.urls import path
from django.urls import include
from . import views

app_name = "seats"

urlpatterns = [
    # Base URL
    path("", views.index, name="index"),
    # Login/logout
    path("accounts/", include("django.contrib.auth.urls")),
    # Room page
    path("showing/<int:showing_id>/", views.room, name="room"),
    # Seat related URLs
    path("showing/<int:showing_id>/room/<int:room_id>/selection/<str:seat_ids>/", views.seat_selection, name="seat_selection"),
    path("showing/<int:showing_id>/room/<int:room_id>/selection/", views.seat_selection, name="seat_selection"),  # si aucun siege sélectionné
    # Page pour le staff pour ajouter des films, seances....
    path("staff/", views.staff, name="staff"),
    path("staff/new_event/", views.new_event, name="new_event"),
    path("staff/new_showing/", views.new_showing, name="new_showing"),
    #form d'inscription
    path("inscription/", views.inscription, name="inscription"),
    path("event/<int:event_id>/", views.choix_seance, name="choix_seance"),
    path("profil/", views.profil, name="profil"),
    path("reservation/", views.reservation, name="reservation"),
]
