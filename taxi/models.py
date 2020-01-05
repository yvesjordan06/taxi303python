from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


class TaxiUser(AbstractUser):
    username = None
    email = None
    code = models.CharField(max_length=64)
    est_chauffeur = models.BooleanField(default=False)
    telephone = models.CharField(max_length=64, unique=True)
    matricule = models.CharField(max_length=8, blank=True, null=True)

    USERNAME_FIELD = 'telephone'


class Chauffeur(models.Model):
    user = models.OneToOneField(
        TaxiUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    statut = models.CharField(max_length=64)


class Client(models.Model):
    user = models.OneToOneField(
        TaxiUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class Voiture(models.Model):
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.SET_NULL, null=True, blank=True)
    marque = models.CharField(max_length=64)
    categorie = models.CharField(max_length=64)
    matricule = models.CharField(max_length=8, blank=False, null=False)
    places = models.IntegerField()
    places_occuper = models.IntegerField()


class Reservation(models.Model):
    depart = models.CharField(max_length=64)
    arrive = models.CharField(max_length=64)
    statut = models.CharField(max_length=64)
    tarif = models.IntegerField()
    heure_depart = models.DateTimeField('Date de depart', default=timezone.now)
    heure_arrive = models.DateTimeField('Date de depart', default=timezone.now, null=True, blank=True)
    client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE)
    chauffeur = models.ForeignKey(Chauffeur, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField('Created at', default=timezone.now)
    type = models.CharField(max_length=64)
