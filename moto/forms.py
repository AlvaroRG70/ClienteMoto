from django import forms
from django.forms import ModelForm
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm





class MotoBusquedaForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)