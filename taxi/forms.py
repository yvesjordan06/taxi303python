from django import forms

from .models import Reservation, TaxiUser


class PostForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('depart', 'arrive', 'heure_arrive', 'type')


class AuthForm(forms.ModelForm):
    class Meta:
        model = TaxiUser
        fields = ('telephone', 'password')
