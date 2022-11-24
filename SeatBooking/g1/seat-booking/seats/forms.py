# coding: utf-8

"""
# Forms module

Define custom forms used in the apps
"""

# Django imports
from django import forms
from .widgets import *
from django.forms.widgets import DateTimeInput
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
# Map models imports
from .models import *
from datetime import timezone


class SeatForm(forms.ModelForm):
    """
    Model form linked to Marker model
    """
    class Meta:
        model = Seat
        fields = ["identifier", "x", "y"]


class EventAddForm(forms.Form):
    """
    Formulaire d'ajout d' event/film
    """
    titre_film = forms.CharField(label='Titre du film', max_length=255)
    realisateur = forms.CharField(label='Réalisateur', max_length=255)
    annee = forms.CharField(label='Année', max_length=4)


class RoomSelectionForm(forms.Form):
    """
    Affichage des salles sous forme de liste déroulante
    """
    room = forms.ModelChoiceField(queryset=Room.objects.all().order_by('name'))


class EventSelectionForm(forms.Form):
    """
    Affichage des event/films sous forme de liste déroulante
    """
    event = forms.ModelChoiceField(queryset=Event.objects.all().order_by('title'))


class ShowingSelectionForm(forms.Form):
    """
    Affichage des séances sous forme de liste déroulante
    """

    showing = forms.ModelChoiceField(queryset=Showing.objects.all().order_by('event', 'date'))

    showing = forms.ModelChoiceField(queryset=Showing.objects.all())

    # def __init__(self, *args, **kwargs):
    #     event_id = kwargs.pop('event_id', None)
    #     super(ShowingSelectionForm, self).__init__(*args, **kwargs)
    #
    #     if event_id:
    #         self.fields['showing'].queryset = Showing.objects.filter(event=event_id).order_by('date')


class FormInscription(forms.Form):
    """
    Formulaire d'ajout d'un nouvel utilisateur
    """

    name = forms.CharField(label='Nom', max_length=40)
    prenom = forms.CharField(label='Prénom', max_length=40)
    pseudo = forms.CharField(label='Pseudo', max_length=40)
    mail = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe', max_length=40)


class ProfilForm(forms.Form):
    """
    Formulaire de modification d'un utilisateur
    """
    name = forms.CharField(label='Nom', max_length=40)
    prenom = forms.CharField(label='Prénom', max_length=40)
    pseudo = forms.CharField(label='Pseudo', max_length=40)
    mail = forms.EmailField(label='Email', max_length=100)


class ShowingAddForm(forms.Form):
    """
    Formulaire d'ajout d'une nouvelle séance
    """

    date = forms.DateField(widget=DatePickerInput)
    time = forms.TimeField(widget=TimePickerInput)
    event = forms.ModelChoiceField(queryset=Event.objects.all().order_by('id'))
    #event = forms.IntegerField(label='Film')
    room = forms.ModelChoiceField(queryset=Room.objects.all().order_by('id'))


    # class Meta:
    #     model = Showing


