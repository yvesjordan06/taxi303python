from django import forms

from .models import Reservation, Utilisateur


class PostForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ('programme', 'places')


class AuthForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ('telephone', 'password')
