from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend
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

def home(request):
    reservations = Reservation.objects.all()

    return render(request, 'taxi/index.html', {
        'reservations': reservations,
    })


def detail(request, reservation_id):
    reservation = Reservation.objects.get(pk=reservation_id)
    return render(request, 'taxi/details_reservation.html', {'reservation': reservation})


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
                if user.est_chauffeur:
                    return redirect('courses')
                else:
                    return redirect('reservations')
    form = AuthForm()
    return render(request, 'taxi/login.html', {'form': form})


def reservations(request):
    _reservations = Reservation.objects.filter(client=request.user.client)
    return render(request, 'taxi/reservations.html', {'reservations': _reservations})


def nouveau(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post: Reservation = form.save(commit=False)
            post.client = request.user.client
            post.tarif = 300
            post.statut = 'en attente'
            post.created_at = timezone.now()
            post.save()
        return redirect('detail', reservation_id=post.id)
    else:
        form = PostForm()
        return render(request, 'taxi/nouvelle_reservation.html', {'form': form})


def courses(request):
    _reservations = Reservation.objects.all()
    return render(request, 'taxi/courses.html', {'reservations': _reservations})
