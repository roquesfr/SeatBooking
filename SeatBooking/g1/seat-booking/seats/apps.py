# coding: utf-8


"""
# Apps module

Define the app configuration
"""

from django.apps import AppConfig


class SeatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seats'
