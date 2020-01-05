from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('new', views.nouveau, name='nouveau'),
    path('reservations', views.reservations, name='reservations'),
    path('courses', views.courses, name='courses'),
    path('reservations/<int:reservation_id>/', views.detail, name='detail'),
]
