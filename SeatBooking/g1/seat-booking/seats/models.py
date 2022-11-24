# coding: utf-8

"""
# Models module

Define models that will be stored in the database


# Get Django user class
>>> user_type = settings.AUTH_USER_MODEL
"""

# MongoDB connector for django
from django.contrib.auth.models import User
from djongo import models

# Get django user model
from django.conf import settings
import datetime


class Room(models.Model):
    """
    Room class

    Define a room with seats.
    """
    name = models.CharField(max_length=255)

    # When displaying class object as a string,
    # display a custom string for readibility
    def __str__(self):
        return self.name


class Seat(models.Model):
    """
    Seat class

    Define a seat with an ID and a x and y position.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name = "seats", default = None)

    # Seat fields
    identifier = models.CharField(max_length=255)

    # Seat position
    x = models.FloatField()
    y = models.FloatField()

    # When displaying class object as a string,
    # display a custom string for readibility
    def __str__(self):
        return f"{self.identifier}"


class Event(models.Model):
    """
    Définit un évènement (film, pièce de théatre, concert)
    """
    title = models.CharField("Titre du film", max_length=255)
    director = models.CharField("Réalisateur", max_length=255)
    year = models.CharField("Année", max_length=4)

    def __str__(self):
        return f'{self.title} ({self.year}) : de {self.director}'


class Showing(models.Model):
    """
    Définit une séance ou un horaire de diffusion d'un évènement et une salle assignée
    """
    date = models.DateTimeField('Horaire séance')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name = "showings", default = None)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='showings', default = None)

    def __str__(self):
        return f'Séance pour {self.event} en salle {self.room}, le {self.date.strftime("%d-%m-%Y à %H:%M ")}'


class Reservation(models.Model):
    """
    Définit une réservation liée à l'utilisateur connecté, une séance et au(x) siège(s) sélectionnés
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "reservations", default = None)
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE, related_name = "reservations", default = None)
    seat = models.ManyToManyField(Seat)

    def __str__(self):
        seat = [siege for siege in self.seat.all()]
        s = [i.identifier for i in seat]
        return f"{self.user}, {self.showing}, {s}"




