# Generated by Django 3.2.14 on 2022-07-20 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seats', '0005_rename_seat_reservation_seats'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='seats',
            new_name='seat',
        ),
    ]