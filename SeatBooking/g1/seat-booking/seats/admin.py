# coding: utf-8

"""
Admin module
"""

from django.contrib import admin
from .models import *
from django.contrib import admin


class ShowingInline(admin.TabularInline):
    model = Showing
    extra = 3


class EventAdmin(admin.ModelAdmin):
    inlines = [ShowingInline]
    list_display = ('title','director' , 'year')
    list_filter = ('director' , 'year')
    ordering = ['title', 'director' , 'year']
    search_fields = ['title', 'director' , 'year']


class ShowingAdmin(admin.ModelAdmin):

    list_display = ('event', 'date', 'room')
    list_filter = ('event','room', 'date')
    ordering = ['event', "date", 'room']
    search_fields = ['event']


class RoomAdmin(admin.ModelAdmin):

    list_display = ('name',)
    list_filter = ('name',)
    ordering = ['name']
    search_fields = ['name']


class SeatAdmin(admin.ModelAdmin):
    list_display = ('identifier',)
    list_filter = ('room', 'x', 'y')
    ordering = ['room', 'x', 'y']
    search_fields = ['identifier', 'room', 'x', 'y']  # siège occupé ou non


class ReservationAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    ordering = ['showing', 'user', 'seat']
    search_fields = ['showing', 'user']  # siège occupé ou non


# Register custom models
admin.site.register(Room, RoomAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Showing, ShowingAdmin)
admin.site.register(Reservation)