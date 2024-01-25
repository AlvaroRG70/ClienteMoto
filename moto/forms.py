from django import forms
from django.forms import ModelForm
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm





class MotoBusquedaForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)


class BusquedaAvanzadaMotoForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    MARCA = [
        ("KA","Kawasaki"),
        ("YA","Yamaha"),
        ("DU","Ducati"),
        ("HO","Honda"),
        ("BM","BMW"),
        ("TR","Triumph"),
        ("SZ","Suzuki"),
        ("KT","KTM"),
    ]
    
    marca = forms.MultipleChoiceField(choices=MARCA,
                                required=False,
                                widget=forms.CheckboxSelectMultiple()
                               )
    anyo = forms.IntegerField(required=False)
    precio = forms.IntegerField(required=False)