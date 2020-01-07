from django.contrib.auth import authenticate, login as SessionLogin, logout as SessionLogout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import PostForm, AuthForm
from .models import *


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        print('this one hitted')

        user = TaxiUser.objects.get(username=username)

        if user.check_password(password):
            return user
        return None


# Create your views here.
@login_required
def home(request):
    if not request.user.est_chauffeur:
        return redirect('reservations')
    else:
        return redirect('courses')
    reservations = Reservation.objects.all()

    return render(request, 'taxi/index.html', {
        'reservations': reservations,
    })


@login_required
def detail(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    return render(request, 'taxi/details_reservation.html', {'reservation': reservation})


def logout(request):
    SessionLogout(request)
    return redirect('login')


def login(request):
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.data:
            print('form is valid')
            username: str = request.POST['telephone']
            password: str = request.POST['password']
            print(username)
            print(password)
            user: TaxiUser = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                SessionLogin(request, user)
                return redirect(home)
    form = AuthForm()
    return render(request, 'taxi/login.html', {'form': form})


def inscription(request):
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.data:
            print('form is valid')
            username: str = request.POST['telephone']
            password: str = request.POST['password']
            print(username)
            print(password)
            user: TaxiUser = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                SessionLogin(request, user)
                return redirect(home)
    form = AuthForm()
    return render(request, 'taxi/login.html', {'form': form})


@login_required
def reservations(request):
    _reservations = Reservation.objects.filter(client=request.user.client).order_by('-created_at')
    return render(request, 'taxi/reservations.html', {'reservations': _reservations})


@login_required
def nouveau(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():

            post: Reservation = form.save(commit=False)
            type = post.type
            tarif = 250
            places = post.places
            if type == 'DP':
                tarif = 2500 * places
            elif type == 'CR':
                tarif = 3000
            elif type == 'MR':
                tarif = 50000
            elif type == 'LT':
                tarif = 35000
            else:
                tarif = tarif * places

            post.client = request.user.client
            post.tarif = tarif
            post.statut = 'ATTENTE'
            post.created_at = timezone.now()
            post.save()
        return redirect('reservations')
    else:
        form = PostForm()
        return render(request, 'taxi/nouvelle_reservation.html', {'form': form})


@login_required
def courses(request):
    user: TaxiUser = request.user
    if not user.est_chauffeur:
        return redirect('reservations')

    _mes_reservations = Reservation.objects.filter(chauffeur=user.chauffeur, statut__exact='EN COUR')
    places_dispo = user.chauffeur.voiture.places - user.chauffeur.voiture.places_occuper
    if places_dispo == user.chauffeur.voiture.places:
        _reservations = Reservation.objects.filter(chauffeur__isnull=True, places__lte=places_dispo,
                                                   statut__exact='ATTENTE', ).union(_mes_reservations)
    else:
        _reservations = Reservation.objects.filter(chauffeur__isnull=True, places__lte=places_dispo, type='CL',
                                                   statut__exact='ATTENTE').union(_mes_reservations)

    if user.chauffeur.statut == 'OFF':
        _reservations = Reservation.objects.filter(chauffeur=user.chauffeur, statut__exact='EN COUR')

    return render(request, 'taxi/courses.html', {'reservations': _reservations.order_by('-created_at')})


def prendre(request, reservation_id):
    user: TaxiUser = request.user
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.chauffeur = user.chauffeur
    reservation.statut = 'EN COUR'
    user.chauffeur.voiture.places_occuper += reservation.places
    if reservation.type != 'CL' or user.chauffeur.voiture.est_plein():
        user.chauffeur.statut = 'OFF'
    reservation.save()
    user.chauffeur.voiture.save()
    user.chauffeur.save()
    user.save()

    return redirect(home)


def terminer(request, reservation_id):
    user: TaxiUser = request.user
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.statut = 'TERMINER'
    user.chauffeur.voiture.places_occuper -= reservation.places
    user.chauffeur.statut = 'ON'
    reservation.save()
    user.chauffeur.voiture.save()
    user.chauffeur.save()
    user.save()

    return redirect(home)


def supprimer(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.delete()
    return redirect(home)
