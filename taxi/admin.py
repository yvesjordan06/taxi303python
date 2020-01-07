from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import *


# Register your models here.


# Register your models here.


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = TaxiUser
        fields = ('password', 'first_name', 'last_name', 'telephone', 'est_chauffeur')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = TaxiUser
        fields = ('first_name', 'last_name', 'telephone', 'est_chauffeur')


class VoitureAdmin(ModelAdmin):
    empty_value_display = '-VIDE-'

    list_display = ('marque', 'categorie', 'chauffeur', 'places', 'places_occuper')


class Chauffer(ModelAdmin):
    empty_value_display = '-VIDE-'

    list_display = ('marque', 'categorie', 'voiture')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('telephone', 'est_chauffeur', 'first_name', 'last_name',)
    list_filter = ('est_chauffeur',)
    fieldsets = (
        (None, {'fields': ('telephone', 'est_chauffeur')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        # ('Permissions', {'fields': ('est_chauffeur',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telephone', 'est_chauffeur', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    search_fields = ('telephone',)
    ordering = ('telephone',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(TaxiUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

# admin.site.register(TaxiUser)
admin.site.register(Chauffeur)
admin.site.register(Client)
admin.site.register(Voiture, VoitureAdmin)
admin.site.register(Reservation)
