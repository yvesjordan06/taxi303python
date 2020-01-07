from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from django.utils import timezone

TYPE_CHOICES = (
    ("CL", "Classique"),
    ("DP", "Depot"),
    ("CR", "Course"),
    ("MR", "Marriage"),
    ("LT", "Location"),
)

STATUT_CHOICES = (
    ("ON", "Disponible"),
    ("OFF", "Indisponible"),

)

RESERVATION_STATUS = (
    ("ATTENTE", "Attente"),
    ("EN COUR", "Encour"),
    ("TERMINER", "Terminer"),

)


class UserManager(BaseUserManager):
    def create_user(self, telephone, first_name, last_name, est_chauffeur=False, password=None):
        if not telephone:
            raise ValueError('Users must have a phone number')
        if not first_name:
            raise ValueError('Users must have a first_name')
        if not last_name:
            raise ValueError('Users must have a last_name')

        user = self.model(
            telephone=telephone,
            first_name=first_name,
            last_name=last_name,
            est_chauffeur=est_chauffeur
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, first_name, last_name, est_chauffeur, password):
        user = self.create_user(
            telephone,
            first_name,
            last_name,
            est_chauffeur,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class TaxiUser(AbstractUser):
    username = None
    email = None
    code = models.CharField(max_length=64)
    est_chauffeur = models.BooleanField(default=False)
    telephone = models.CharField(max_length=64, unique=True)
    # matricule = models.CharField(max_length=8, blank=True, null=True)

    objects = UserManager()
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'telephone'

    def __str__(self):
        return self.get_full_name()


class Chauffeur(models.Model):
    user = models.OneToOneField(
        TaxiUser,
        on_delete=models.CASCADE,
        # primary_key=True,
    )
    statut = models.CharField(max_length=3, choices=STATUT_CHOICES, null=False, default='ON')

    def __str__(self):
        return self.user.get_full_name()


class Client(models.Model):
    user = models.OneToOneField(
        TaxiUser,
        on_delete=models.CASCADE,
        # primary_key=True,
    )

    def __str__(self):
        return self.user.get_full_name()


class Voiture(models.Model):
    chauffeur = models.OneToOneField(Chauffeur, on_delete=models.SET_NULL, null=True, blank=True)
    marque = models.CharField(max_length=64)
    categorie = models.CharField(max_length=64)
    matricule = models.CharField(max_length=8, blank=False, null=False)
    places = models.IntegerField(default=5)
    places_occuper = models.IntegerField(default=0)

    def __str__(self):
        return self.marque + ' ' + self.categorie

    def place_dispo(self):
        return self.places - self.places_occuper

    def est_plein(self):
        return self.places == self.places_occuper


class Reservation(models.Model):
    depart = models.CharField(max_length=64)
    arrive = models.CharField(max_length=64)
    statut = models.CharField(max_length=10, choices=RESERVATION_STATUS, null=False, default='ATTENTE')
    places = models.IntegerField(default=1, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    tarif = models.IntegerField()
    heure_depart = models.DateTimeField('Date de depart', default=timezone.now)
    heure_arrive = models.DateTimeField('Date de depart', default=timezone.now, null=True, blank=True)
    client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE)
    chauffeur = models.ForeignKey(Chauffeur, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField('Created at', default=timezone.now)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, null=False, default='CL')
