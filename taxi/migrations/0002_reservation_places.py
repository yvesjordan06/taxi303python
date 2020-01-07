# Generated by Django 3.0 on 2020-01-07 11:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('taxi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='places',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5),
                                                             django.core.validators.MinValueValidator(1)]),
        ),
    ]
