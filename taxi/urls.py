from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('new', views.nouveau, name='nouveau'),
    path('reservations', views.reservations, name='reservations'),
    path('courses', views.courses, name='courses'),
    path('reservations/<int:reservation_id>/', views.detail, name='detail'),
    path('prendre/<int:reservation_id>/', views.prendre, name='prendre'),
    path('supprimer/<int:reservation_id>/', views.supprimer, name='supprimer'),
    path('terminer/<int:reservation_id>/', views.terminer, name='terminer'),
]
