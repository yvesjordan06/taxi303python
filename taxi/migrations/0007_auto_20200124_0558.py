# Generated by Django 3.0.2 on 2020-01-24 05:58

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0006_auto_20200124_0519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='date_embauche',
            field=models.DateField(default=datetime.datetime(2020, 1, 24, 5, 58, 44, 799278, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='programme',
            name='heure_depart',
            field=models.TimeField(default=datetime.time(15, 0), max_length=64),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 24, 5, 58, 44, 803000, tzinfo=utc), verbose_name='Created at'),
        ),
    ]
