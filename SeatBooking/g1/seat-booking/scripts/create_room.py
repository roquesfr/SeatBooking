# coding: utf-8

"""
# Module for creating rooms
"""

import string
from seats.models import Room
from seats.models import Seat

def run(*args):
    """
    Create a dense seat grid
    """
    room_name = args[0]

    nb_rows = 5
    nb_cols = 2
    seat_size = 64
    nb_letters = len(string.ascii_uppercase)

    room = Room(name = room_name)
    room.save()

    if nb_rows > 26:
        raise ValueError(f"Cannot create a room with more than {nb_letters} rows")

    for row in range(nb_rows):
        for col in range(nb_cols):
            x = row * seat_size 
            y = col * seat_size
            letter = string.ascii_uppercase[row]
            identifier = f"{letter}{col}"
            seat = Seat(room = room, identifier = identifier, x = x, y = y)
            seat.save()
