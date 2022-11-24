# coding: utf-8

"""
Views Module
"""

# Django imports
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from datetime import timedelta
from django.utils.timezone import get_current_timezone

# Model imports
from .models import *

# Form imports
from .forms import *

from django.utils import timezone
from datetime import datetime


#@login_required
def index(request):
    """
    Sélection du film, index du site
    """
    # On room selection
    if request.method == "POST":  # si t'as submit

        event_id = request.POST.get("event")
        response = redirect(f"/event/{event_id}/")
        #response = redirect(f"/showing/{showing_id}")
        return response
    else:

        # Load template
        template = loader.get_template("seats/index.html")

        # Create form
        event_selection_form = EventSelectionForm()
        # Create avec FAb
        events = Event.objects.all()


        # # Get seats
        # rooms = Room.objects.all()
        # print("X" * 50)
        # print(rooms)

        # Fill context
        context = {
            "event_selection_form": event_selection_form,
            "events": events,
            #"showing_selection_form": showing_selection_form,
        }

        # Serve HTTP response
        return HttpResponse(template.render(context, request))


@login_required
def room(request, showing_id):
    """
    Affichage des sièges libres et occupés, sélection des sièges pour la réservation
    """
    # Load template
    template = loader.get_template("seats/room.html")
    # Get current room object
    showing = Showing.objects.get(pk = showing_id)
    room = showing.room
    # Get seats for this room
    seat_objects = room.seats.all()

    horaire = str(showing.date)
    resume_date = horaire.split()

    # Create a list of same size as the seat_objects list
    # You can disable a seat by putting available to False
    available = [True] * len(seat_objects)
    list_of_siege = [seat.id for seat in seat_objects]  # avoir l'index associé à available
    reservations = Reservation.objects.filter(showing_id=showing_id)  # showing_id c'est le paramètre de room

    # Creation d'une liste contenant l'id de tous les sièges déjà présents dans des réservations
    seat_reserved = [seat.id for reservation in reservations for seat in reservation.seat.all()]
    # for reservation in reservations:
    #    for seat in reservation.seat.all():
    #       print(seat.id)  # version fonctionnelle pour avoir les id des sieges occupés

    # Passage des valeurs de True à False en fonction des index des sièges réservés
    for seat in seat_reserved:
        if seat in list_of_siege:
            idx = list_of_siege.index(seat)
            available[idx] = False

    #available = [True, True, True, True, True, False, True, True, True, True]
    # Zip the two lists
    seats = zip(seat_objects, available)

    # Fill context
    context = {
        "title": showing.event,
        "showing": showing,
        "room": room,
        "seats": seats,
        "resume_date": resume_date[0],
        "resume_heure": resume_date[1],
    }

    # Serve HTTP response
    return HttpResponse(template.render(context, request))


@login_required
def seat_selection(request,showing_id, room_id, seat_ids=None):  # seats_id est un paramètre facultatif au cas ou aucun siege selectionnés
    """
    Validation de la réservation, résumé de la réservation
    """
    if seat_ids is None:
        return redirect(f"/showing/{showing_id}")

    else:
        # Load template
        template = loader.get_template("seats/seat_selection.html")
        #formulaire = CreationNouvelleReservation()

        #Transformation des identifiers des sièges en id des sièges sélectionnés
        seat_id_list = seat_ids.split(",")
        list_id_seat = []
        for seat_id in seat_id_list:
            s = Seat.objects.get(room__id=room_id, identifier = seat_id)
            list_id_seat.append(s.id)

        utilisateur_reservation = request.user.id
        seance_reservation = showing_id
        sieges_reserves = list_id_seat

        # Creation d'une nouvelle réservation
        reservation = Reservation(user_id=utilisateur_reservation, showing_id=seance_reservation)
        reservation.save()
        for sieges in sieges_reserves:
            s = Seat.objects.get(id=sieges)
            reservation.seat.add(s.id)
            reservation.save()

        resume_salle = reservation.showing.room.name
        horaire = str(reservation.showing.date)
        resume_date = horaire.split()
        resume_film = reservation.showing.event.title

        mail_user = str(request.user.email)
        corps_du_mail= f"""Bonjour {request.user.username}, voilà le résumé de votre réservation : 
Film : {resume_film}
Salle : {resume_salle}
Date : {resume_date[0]}
Heure : {resume_date[1]}
Sièges : {seat_id_list}
Merci d'avoir utilise Seats de la mort
Bien cordialement,

SdlM"""
        # send_mail(
        #     'Votre réservation est enregistrée',
        #     corps_du_mail,
        #     'reservations@SdlM.com',
        #     [mail_user],
        #     fail_silently=False,
        # )

        # Fill context
        context = {

            "seat_id_list": seat_id_list,
            "list_id_seat": list_id_seat,
            "showing_id": showing_id,
            "room_id": room_id,
            "resume_salle": resume_salle,
            "resume_date" : resume_date[0],
            "resume_heure": resume_date[1],
            "resume_film": resume_film,
        }
        #Send un email

        #from django.core.mail import send_mail

        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'from@example.com',
        #     ['to@example.com'],
        #     fail_silently=False,
        # )


        # Serve HTTP response
        return HttpResponse(template.render(context, request))



@login_required
def staff(request):
    """
    Page de liens pour les actions staff / administrateurs
    """
    if request.user.is_staff:
        template = loader.get_template("seats/staff.html")

        context = {

        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect("/accounts/login/")


@login_required
def new_event(request):
    """
    Page de création d'un nouvel Event (film à l'affiche)
    """
    if request.user.is_staff:
        template = loader.get_template("seats/new_event.html")
        if request.method == 'POST':
            form = EventAddForm(request.POST)
            if form.is_valid():
                film = Event(title=form.cleaned_data['titre_film'], director=form.cleaned_data['realisateur'], year=form.cleaned_data['annee'])
                film.save()

                return render(request, 'seats/staff.html')  # staff.html à supprimer
        else:
            form = EventAddForm()

            liste_label = []
            liste_input = []
            for champ in form:
                liste_input.append(champ)
                liste_label.append(champ.label)

            el_zipo = zip(liste_label, liste_input)

            context = {
                "el_zipo": el_zipo,
            }

            return render(request, 'seats/new_event.html', context)
    else:
        return redirect("/accounts/login/")


@login_required
def new_showing(request):
    """
    Page de création d'une nouvelle séance
    """
    if request.user.is_staff:

        template = loader.get_template("seats/new_showing.html")
        if request.method == 'POST':
            form = ShowingAddForm(request.POST)
            event_id = request.POST.get("event")
            room_id = request.POST.get("room")
            date = request.POST.get("date")
            time = request.POST.get("time")
            date_complete = date + " " + time
            tzinfo = get_current_timezone()
            date_object = datetime.strptime(date_complete, '%Y-%m-%d %H:%M')

            if form.is_valid():
                seance = Showing(event_id=event_id,
                                 room_id=room_id,
                                 date=date_object)
                seance.save()
                return redirect('/')
        else:  #se fait directement -> créer le le formualire
            form = ShowingAddForm()

            # liste_label = []
            # liste_input = []
            # for champ in form:
            #     liste_input.append(champ)
            #     liste_label.append(champ.label)
            #
            # el_zipo = zip(liste_label, liste_input)
            #
            # context = {
            #     "el_zipo": el_zipo,
            # }

            return render(request, 'seats/new_showing.html', {"form": form})

    else:
        return redirect("/accounts/login/")


def inscription(request):
    """
    Page de création d'un nouvel utilisateur (non-staff, non-admin)
    """

    template = loader.get_template("seats/inscription.html")
    if request.method == 'POST':
        form = FormInscription(request.POST)
        if form.is_valid():
            nouvel_user = User.objects.create_user(last_name=form.cleaned_data['name'],
                                                   first_name=form.cleaned_data['prenom'],
                                                   username=form.cleaned_data['pseudo'],
                                                   email= form.cleaned_data['mail'],
                                                   password= form.cleaned_data['password'])
            return redirect("/accounts/login")
    else:
        form = FormInscription()

        liste_label =[]
        liste_input = []
        for champ in form:
            liste_input.append(champ)
            liste_label.append(champ.label)

        el_zipo = zip(liste_label, liste_input)

        context = {
            "el_zipo": el_zipo,
        }

        return render(request, 'seats/inscription.html', context)


#@login_required
def choix_seance(request, event_id):
    """
    Page de vue et de sélection des séances futures pour le film choisi à la page précédente
    """
    # On room selection

    if request.method == "POST":  # si t'as submit

        showing_id = request.POST.get("showing")
        response = redirect(f"/showing/{showing_id}")
        return response
    else:

        # Load template
        template = loader.get_template("seats/choix_seance.html")
        now = timezone.now()
        # showing_selection_form = ShowingSelectionForm(event_id=event_id)
        showing_selection_form = ShowingSelectionForm()

        # Filtre des séances futures du film sélectionné
        showing_selection_form.fields['showing'].queryset = Showing.objects.filter(event=event_id).exclude(date__lt=now).order_by('date')

        showings = Showing.objects.filter(event=event_id).exclude(date__lt=now).order_by("date")

        context = {
            "showing_selection_form": showing_selection_form,
            "showings": showings,
        }
        return HttpResponse(template.render(context, request))

@login_required
def profil(request):
    """
    Page de modification des informations du profil (nom, prénom, nom d'utilisateur / pseudo, mail)
    """
    template = loader.get_template("seats/profil.html")
    if request.method == 'POST':
        form = ProfilForm(request.POST)
        if form.is_valid():
            modification = User.objects.get(pk=request.user.id)

            if form.cleaned_data['pseudo'] != request.user.username:
                modification.username = form.cleaned_data['pseudo']
            if form.cleaned_data['prenom'] != request.user.first_name:
                modification.first_name = form.cleaned_data['prenom']
            if form.cleaned_data['name'] != request.user.last_name:
                modification.last_name = form.cleaned_data['name']
            if form.cleaned_data['mail'] != request.user.email:
                modification.email = form.cleaned_data['mail']
            # if form.cleaned_data['pseudo'] == request.user.password:
            #     modification.password = form.cleaned_data['password']

            modification.save()

            return redirect("/profil")
    else:

        username = request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        dict = {"pseudo": username, "prenom": first_name, "name": last_name, "mail": email}
        form = ProfilForm(dict)

        liste_label = []
        liste_input = []
        for champ in form:
            liste_input.append(champ)
            liste_label.append(champ.label)

        el_zipo = zip(liste_label, liste_input)

        context = {
            "el_zipo": el_zipo,
        }

        return HttpResponse(template.render(context, request))
    #return render(request, 'seats/inscription.html', {'form': form})

@login_required
def reservation(request):
    """
    Page affichant les séances futures et les séances passées liées au compte utilisateur
    """
    template = loader.get_template("seats/reservation.html")

    now = timezone.now()

    # Recupération de toutes les réservations liées au compte connecté

    reservations = Reservation.objects.filter(user_id = request.user.id)

    liste_film = []
    liste_date = []
    liste_salle = []
    liste_siege = []

    liste_film2 = []
    liste_date2 = []
    liste_salle2 = []
    liste_siege2 = []


    #Remplissage des listes titre, date, salle et sièges des réservations passées

    for reservation in reservations:
        if reservation.showing.date <= now:
            liste_film.append(str(reservation.showing.event.title))
            liste_date.append(str(reservation.showing.date))
            liste_salle.append(str(reservation.showing.room.name))

            liste_siege_leretour =[]
            for siege in reservation.seat.all():
                liste_siege_leretour.append(siege.identifier)
            liste_siege.append(liste_siege_leretour)
        else:
            # Remplissage des listes titre, date, salle et sièges des réservations futures
            liste_film2.append(str(reservation.showing.event.title))
            liste_date2.append(str(reservation.showing.date))
            liste_salle2.append(str(reservation.showing.room.name))

            liste_siege_leretour = []
            for siege in reservation.seat.all():
                liste_siege_leretour.append(siege.identifier)
            liste_siege2.append(liste_siege_leretour)

    # zip des 4 listes passées
    le_zip = zip(liste_film, liste_date, liste_salle, liste_siege)
    # zip des 4 listes futures
    le_zip_turfu = zip(liste_film2, liste_date2, liste_salle2, liste_siege2)
    context = {
        "le_zip": le_zip,
        "le_zip_turfu": le_zip_turfu,
        "range_liste": range(len(liste_film)),
        #"reservations": reservations,
        #"reservation": reservation,
    }

    return HttpResponse(template.render(context, request))
