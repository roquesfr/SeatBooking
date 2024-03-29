# Generated by Django 3.2.14 on 2022-07-20 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seats', '0002_event_reservation_showing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='showing_id',
            new_name='showing',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='reservation',
            name='seat',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='seats.seat'),
        ),
    ]
