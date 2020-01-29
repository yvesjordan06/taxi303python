from django.contrib.auth import authenticate, login as SessionLogin, logout as SessionLogout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from .forms import AuthForm
from .models import *


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        print('this one hitted')

        user = Utilisateur.objects.get(username=username)

        if user.check_password(password):
            return user
        return None


# Create your views here.
@login_required
def home(request):
    user: Utilisateur = request.user

    if  not user.is_superuser and user.is_staff:
        return redirect("reservations")

    if not user.is_staff:
        return redirect("programme")
    res_todays = Reservation.objects.filter(date_depart=datetime.datetime.now().date())
    res_today = res_todays.count()
    res_prix = 0;
    for i in res_todays:
        res_prix += i.montant()

    colis_todays = Expedition.objects.all()
    colis_today = colis_todays.count()
    colis_prix = 0;
    for i in colis_todays:
        colis_prix += i.tarif

    employer_todays = Employe.objects.all()
    employer_today = employer_todays.count()
    employer_prix = 0;
    for i in employer_todays:
        employer_prix += i.salaire
    return render(request, 'taxi/admin/index.html', {
        'reservation_aujourdhui':res_today,
        'reservation_montant':res_prix,
        'colis': colis_today,
        'colis_montant': colis_prix,
        'employer': employer_today,
        'salaire': employer_prix,
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
            user: Utilisateur = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                SessionLogin(request, user)
                return redirect(home)
    form = AuthForm()
    return render(request, 'taxi/login.html', {'form': form})


def inscription(request):

    if request.method == "POST":
        form = request.POST
        print(form)
        first_name = form['first_name']
        last_name = form['last_name']
        telephone = form['telephone']
        password = form['password']
        cpassword = form['confirm_password']
        cni = form['cni']

        if cpassword != password:
            return redirect("register")

        try:
            user = Utilisateur.objects.get(cni__exact=cni)
        except:
            user = Utilisateur(
                first_name=first_name,
                last_name=last_name,
                telephone=telephone,
                cni=cni,
                is_staff=False,
            )
            user.set_password(password)
            user.save()

        client, created = Client.objects.get_or_create(user=user)

        SessionLogin(request, user)
        return redirect(home)
    form = AuthForm()
    return render(request, 'taxi/register.html', {'form': form})


@login_required
def reservations(request):
    user: Utilisateur = request.user
    reser = Reservation.objects.filter(date_depart=datetime.datetime.now().date()).filter(
        guichetier__isnull=True) if user.est_employer() else Reservation.objects.filter(client=user.client)



    return render(request, 'taxi/admin/reservations.html', {'reservations': reser, 'today':datetime.datetime.now().date()})


def reservations_jour(request):
    user: Utilisateur = request.user
    if not user.est_employer():
        return reservations(request)
    reser = Reservation.objects.filter(date_depart=datetime.datetime.now().date())
    return render(request, 'taxi/admin/reservations-du--jour.html', {'reservations': reser})


def reservations_historique(request):
    reser = Reservation.objects.all()
    user: Utilisateur = request.user
    if not user.is_superuser:
        return reservations_client(request)

    return render(request, 'taxi/admin/reservations-complet.html', {'reservations': reser})


def reservations_client(request):
    prog = Programme.objects.all()
    return render(request, 'taxi/reservations.html', {'programme': prog})

@login_required
def reservations_nouveau(request):

    if request.method == "POST":
        form = request.POST
        print(form)
        first_name = form['first_name'] or 'Client Inconnu'
        last_name = form['last_name'] or 'Client Inconnu'
        telephone = form['telephone'] or 'Client Inconnu'
        programme = form['programme']

        places = form['places']
        cni = form['cni']
        date: str = form['date']

        print(date)
        print(type(date))
        fdate = date.split('-')
        date: datetime.date = datetime.date(int(fdate[0]), int(fdate[1]), int(fdate[2]))
        try:
            user = Utilisateur.objects.get(cni__exact=cni)
        except:
            user = Utilisateur(
                first_name=first_name,
                last_name=last_name,
                telephone=telephone,
                cni=cni
            )
            user.set_password(cni)
            user.save()

        client, created = Client.objects.get_or_create(user=user)

        reser = Reservation(
            programme=Programme.objects.get(pk=programme),
            client=client,
            jour_depart=date.weekday(),
            places=places,
            date_depart=date
        )
        muser: Utilisateur = request.user

        if muser.est_employer() and (
                muser.is_superuser or muser.employe.poste == "GUICHETIER") and date == timezone.now().date():
            reser.guichetier = muser.employe
            p = Programme.objects.get(pk=programme)
            p.voiture.places_occuper = p.voiture.places_occuper + int(places)
            p.voiture.save()
            p.save()

        reser.save()

        return redirect('reservations')
    else:
        reser = Programme.objects.all()
        user: Utilisateur = request.user

        return render(request, 'taxi/admin/reservation-creer.html', {'reservations': reser})


def reservations_nouveau_withID(request, programme_id):
    reser = Programme.objects.all()
    return render(request, "taxi/admin/reservation-creer.html", {'programme': get_object_or_404(Programme, pk=programme_id), 'reservations': reser})

@login_required
def employer(request):
    user: Utilisateur = request.user
    if not user.is_superuser:
        return redirect('reservations')

    employee = Employe.objects.all()

    return render(request, 'taxi/admin/employe.html', {'employees': employee})


def employer_detail(request, employer_id):
    user: Utilisateur = request.user
    if not user.is_superuser:
        return redirect('reservations')

    return render(request, 'taxi/admin/detail-employe.html', {'employee': get_object_or_404(Employe, pk=employer_id)})


def employer_salaire(request, employer_id):
    user: Utilisateur = request.user
    if not user.is_superuser:
        return redirect('reservations')

    return render(request, 'taxi/admin/bulletin-employe.html', {'employee': get_object_or_404(Employe, pk=employer_id)})


def block_user(request, userid):
    user = get_object_or_404(Utilisateur, pk=userid)
    user.is_active = False
    user.save()
    return redirect()

def employer_nouveau(request):
    if request.method == "POST":
        form = request.POST
        print(form)
        first_name = form['first_name']
        last_name = form['last_name']
        telephone = form['telephone']
        poste = form['poste']
        salaire = form['salaire']
        date = form['date']
        cni = form['cni']

        a = Utilisateur.objects.filter(cni__exact=cni).union(Utilisateur.objects.filter(telephone__exact=telephone))
        if a.count() > 0: return redirect('employer')
        user = Utilisateur(first_name=first_name, last_name=last_name, cni=cni, telephone=telephone, is_staff=True)
        user.set_password(cni)
        user.save()
        employer = Employe(user=user, poste=poste, salaire=salaire)
        employer.save()
        print(user)
        return redirect('employer')

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
        user: Utilisateur = request.user
        if not user.is_superuser:
            return redirect('reservations')
        return render(request, 'taxi/admin/ajout-employe.html', {})


@login_required
def expedition(request):
    user: Utilisateur = request.user
    if not user.est_employer():
        return redirect('reservations')
    expedition = Expedition.objects.filter(livree=False)
    return render(request, 'taxi/admin/expeditions.html', {'expeditions':expedition})


@login_required
def expedition_nouveau(request):

    user: Utilisateur = request.user
    if not user.est_employer():
        return redirect('expeditions')

    if request.method == "POST":
        form = request.POST
        print(form)
        first_name = form['first_name'] or 'Client Inconnu'
        last_name = form['last_name'] or 'Client Inconnu'
        telephone = form['telephone'] or 'Client Inconnu'
        cni = form['cni']
        destination = form['destination']
        depart = form['depart']
        contenue = form['contenu']



        try:
            user = Utilisateur.objects.get(cni__exact=cni)
        except:
            user = Utilisateur(
                first_name=first_name,
                last_name=last_name,
                telephone=telephone,
                cni=cni
            )
            user.set_password(cni)
            user.save()

        client, created = Client.objects.get_or_create(user=user)

        colis = Colis(
            client=client,
            nom=contenue
        )
        colis.save()

        expedition = Expedition(
            colis=colis,
            depart=depart,
            arrive=destination,
            tarif=7000,
            livree=False
        )
        expedition.save()

        return redirect('expeditions')
    else:
      return render(request, 'taxi/admin/expedition-creer.html', {})

def gestion(request):

    user: Utilisateur = request.user
    if not user.est_employer():
        return redirect('reservations')

    return render(request, 'taxi/admin/gestion.html', {})


@login_required
def expedition_terminer(request):

    user: Utilisateur = request.user
    if not user.est_employer():
        return redirect('expeditions')

    return render(request, 'taxi/admin/expeditions-terminer.html', {'expeditions':Expedition.objects.filter(livree=True)})

def expedition_complet(request, id):

    user: Utilisateur = request.user
    if not user.est_employer():
        return redirect('expeditions')
    exp = get_object_or_404(Expedition, pk=id)
    exp.livree = True
    exp.save()

    #return render(request, 'taxi/admin/expeditions-terminer.html', {})
    return redirect('expeditions')

def expedition_supprimer(request, id):
    user: Utilisateur = request.user
    if not user.est_employer():
        return redirect('expeditions')

    exp = get_object_or_404(Expedition, pk=id)
    exp.delete()

    #return render(request, 'taxi/admin/expeditions-terminer.html', {})
    return redirect('expeditions')

def prendre(request, reservation_id):
    user: Utilisateur = request.user
    if not user.est_employer():
        return redirect('reservations')

    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.guichetier = user.employe
    reservation.statut = 'ACCEPTER'
    p = reservation.programme
    p.voiture.places_occuper = p.voiture.places_occuper + int(reservation.places)
    p.voiture.save()
    p.save()
    reservation.save()

    return redirect('reservations')


def terminer(request, reservation_id):
    user: Utilisateur = request.user
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.statut = 'TERMINER'
    user.chauffeur.voiture.places_occuper -= reservation.places
    user.chauffeur.statut = 'ON'
    reservation.save()
    user.chauffeur.voiture.save()
    user.chauffeur.save()
    user.save()

    return redirect(home)

def refuser(request, reservation_id):
    user: Utilisateur = request.user
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.statut = 'REFUSER'
    reservation.programme.voiture.places_occuper -= reservation.places
    reservation.programme.voiture.save()
    reservation.programme.save()
    reservation.save()

    return redirect("reservations")


def supprimer(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.delete()
    return redirect("reservations")


@login_required
def programme(request):


    programmes = Programme.objects.all()

    return render(request, 'taxi/admin/programme.html', {'programmes': programmes})


@login_required
def programme_nouveau(request):
    user: Utilisateur = request.user
    if not user.is_superuser:
        return redirect('reservations')
    if request.method == 'POST':
        form = request.POST
        print(form['heure'])
        p = Programme(
            depart=form['depart'],
            arrive=form['arrive'],
            type=form['type'],
            voiture=Voiture.objects.get(pk=form['voiture']),
            tarif=form['prix'],
            heure_depart=form['heure']
        )
        p.save()
        return redirect(programme)

    return render(request, 'taxi/admin/programme-creer.html', {'voitures': Voiture.objects.all()})

@login_required
def voiture_nouveau(request):
    user: Utilisateur = request.user
    if not user.is_superuser:
        return redirect('reservations')
    if request.method == 'POST':
        form = request.POST
        p = Voiture(
            marque=form['marque'],
            categorie=form['modele'],
            places=form['places'],
            matricule=form['matricule'],

        chauffeur_id=form['chauffeur'])

        p.save()
        return redirect('voiture')

    return render(request, 'taxi/admin/voiture-creer.html', {'chauffeurs': Employe.objects.filter(poste="CHAUFFEUR").filter(voiture__isnull=True)})

@login_required
def voiture(request):


    voiture = Voiture.objects.all()

    return render(request, 'taxi/admin/voiture.html', {'voitures': voiture})

def voiture_supprimer(request, reservation_id):
    reservation = get_object_or_404(Voiture, pk=reservation_id)
    reservation.delete()
    return redirect(voiture)

def programme_supprimer(request, reservation_id):
    reservation = get_object_or_404(Programme, pk=reservation_id)
    reservation.delete()
    return redirect(programme)
