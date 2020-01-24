import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
# Create your models here.
from django.utils import timezone

TYPE_CHOICES = (
    ("CL", "Classique"),
    ("VIP", "VIP"),
)

JOURS_CHOICES = (
    ("0", "Lundi"),
    ("1", "Mardi"),
    ("2", "Mercredi"),
    ("3", "Jeudi"),
    ("4", "Vendredi"),
    ("5", "Samedi"),
    ("6", "Dimance"),
)

POSTE_CHOICES = (
    ("CHAUFFEUR", "Chauffeur"),
    ("GUICHETIER", "Guichetier"),
)

CHOICES_VILLE = (
    ("YDE","Yaounde"),
    ("DLA","Douala"),
    ("BAF","Baffoussam"),
    ("BDA","Bamenda"),
    ("BDJ","Bandjoun"),
)

CHOICES_HEURES = (
    ("6","6h"),
    ("10","10h"),
    ("14","14h"),
    ("19","19h"),
    ("22","22h"),
)

RESERVATION_STATUS = (
    ("ATTENTE", "Attente"),
    ("REFUSER", "Refuser"),
    ("ACCEPER", "Accepter"),
    ("EN COUR", "Encour"),
    ("TERMINER", "Terminer"),

)


class UserManager(BaseUserManager):
    def create_user(self, telephone, first_name, last_name, cni, password=None):
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
            cni=cni

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, first_name, last_name, cni, password):
        user = self.create_user(
            telephone,
            first_name,
            last_name,
            cni,
            password=password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff= True
        user.save(using=self._db)

        print(user.is_superuser);
        return user


class Utilisateur(AbstractUser):
    username = None
    email = None
    code = models.CharField(max_length=64)
    telephone = models.CharField(max_length=64, unique=True)
    cni = models.CharField(max_length=64, unique=True)
    is_admin = models.BooleanField(default=False)

    # matricule = models.CharField(max_length=8, blank=True, null=True)
    def est_employer(self):
        try:
            return self.employe is not None or self.is_superuser
        except:
            return False

    objects = UserManager()
    REQUIRED_FIELDS = ['first_name', 'last_name', 'cni']
    USERNAME_FIELD = 'telephone'
    EMAIL_FIELD = 'telephone'

    def __str__(self):
        return self.get_full_name()


class Employe(models.Model):
    user = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE
        # primary_key=True,
    )
    salaire = models.BigIntegerField(null=False, default='50000', )
    poste = models.CharField(max_length=32, null=False, choices=POSTE_CHOICES, default="CHAUFFEUR")
    date_embauche = models.DateField(default=timezone.now())

    def __str__(self):
        return self.user.get_full_name()


class Client(models.Model):
    user = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        # primary_key=True,
    )

    def __str__(self):
        return self.user.get_full_name()


class Voiture(models.Model):
    chauffeur = models.OneToOneField(Employe, on_delete=models.SET_NULL, null=True, blank=True)
    marque = models.CharField(max_length=64)
    categorie = models.CharField(max_length=64)
    matricule = models.CharField(max_length=8, blank=False, null=False)
    places = models.IntegerField(default=70)
    places_occuper = models.IntegerField(default=0)
    created_at = models.DateTimeField('Created at', default=timezone.now)

    def __str__(self):
        return f"{self.marque} {self.categorie} {self.places} Places "

    def place_dispo(self):
        return self.places - self.places_occuper

    def est_plein(self):
        return self.places == self.places_occuper

class Programme(models.Model):
    depart = models.CharField(max_length=64, choices=CHOICES_VILLE, null=False, )
    arrive = models.CharField(max_length=64, choices=CHOICES_VILLE, null=False, )
    type = models.CharField(max_length=64, choices=TYPE_CHOICES, null=False, default='CL')
    heure_depart = models.TimeField(max_length=64, default=datetime.time(15), )
    voiture = models.ForeignKey(Voiture, on_delete=models.SET_NULL, blank=True, null=True)
    tarif = models.IntegerField()

    def get_heure_depart_display(self):

        return f"{self.heure_depart.hour} H {self.heure_depart.minute if self.heure_depart.minute > 9 else '0'+str(self.heure_depart.minute)}" if self.heure_depart else "Pas d'horaire"
    def __str__(self):
        return f'Depart: {self.get_depart_display()}, Arrive: {self.get_arrive_display()}, Tarif: {self.tarif} FCFA, Heure: {self.get_heure_depart_display()}, Type: {self.get_type_display()}, Places: {self.voiture.place_dispo()}'

class Reservation(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, null=False, blank=False)
    places = models.IntegerField(default=1, validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE)
    guichetier = models.ForeignKey(Employe, null=True, on_delete=models.SET_NULL, default=None)
    created_at = models.DateTimeField('Created at', default=timezone.now())
    jour_depart = models.CharField(max_length=64, choices=JOURS_CHOICES, default=timezone.now().weekday())
    date_depart = models.DateField('Created at', default=timezone.now().date())
    statut = models.CharField(max_length=64, choices=RESERVATION_STATUS, null=False, default='ATTENTE')

    def __str__(self):
        return f"Client : {self.client.user}, Depart: {self.date_depart}, Par: {self.guichetier.user if self.guichetier else 'Aucun' }"

    def montant(self):
        return self.places * self.programme.tarif

    def _statut(self):
        return "En attente" if not self.guichetier else "Accepte"

    def est_aujourdhui(self):
        return (self.date_depart.day, self.date_depart.month, self.date_depart.year) == (timezone.now().day, timezone.now().month, timezone.now().year)

class Colis(models.Model):
    nom = models.CharField(max_length=64, choices=CHOICES_VILLE, null=False, )
    client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE)

class Expedition(models.Model):
    colis = models.ForeignKey(Colis, null=False, on_delete=models.CASCADE)
    depart = models.CharField(max_length=64, choices=CHOICES_VILLE, null=False, )
    arrive = models.CharField(max_length=64, choices=CHOICES_VILLE, null=False, )
    tarif = models.IntegerField()
    livree = models.BooleanField(default=False, blank=False)


