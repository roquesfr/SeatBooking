# Generated by Django 3.2.14 on 2022-07-20 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seats', '0004_auto_20220720_1428'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='seat',
            new_name='seats',
        ),
    ]
