from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.inscription, name='register'),
    path('logout', views.logout, name='logout'),

    path('reservations', views.reservations, name='reservations'),
    path('reservations/nouveau', views.reservations_nouveau, name='reservations.nouveau'),
    path('reservations/nouveau/<int:programme_id>', views.reservations_nouveau_withID, name='reservations.nouveau_id'),
    path('reservations/aujourdhui', views.reservations_jour, name='reservations.jour'),
    path('reservations/historique', views.reservations_historique, name='reservations.historique'),
    path('reservations/<int:reservation_id>/', views.detail, name='detail'),

    path('employer', views.employer, name='employer'),
    path('employer/nouveau', views.employer_nouveau, name='employer.nouveau'),
    path('employer/detail/<int:employer_id>', views.employer_detail, name='employer.detail'),
    path('employer/salaire', views.employer_salaire, name='employer.salaire'),

    path('expeditions', views.expedition, name='expeditions'),
    path('expeditions/nouveau', views.expedition_nouveau, name='expeditions.nouveau'),
    path('expeditions/terminer', views.expedition_terminer, name='expeditions.terminer'),

    path('programme', views.programme, name='programme'),
    path('programme/nouveau', views.programme_nouveau, name='programme.nouveau'),



    path('prendre/<int:reservation_id>/', views.prendre, name='prendre'),
    path('supprimer/<int:reservation_id>/', views.supprimer, name='supprimer'),
    path('terminer/<int:reservation_id>/', views.terminer, name='terminer'),
]
