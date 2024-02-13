from django import forms
from django.forms import ModelForm
from datetime import date
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from .helper import helper
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




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
    
    
class BusquedaAvanzadaConcesionarioForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    telefono = forms.IntegerField(required=False)


class BusquedaAvanzadaEventoForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    
    
class MotoForm(forms.Form):
    nombre = forms.CharField(label="Nombre de la Moto",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")
    
    descripcion = forms.CharField(label="Descripcion",
                                  required=False,
                                  widget=forms.Textarea())
    
    modelo = forms.CharField(label="Nombre del modelo",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")
    
    año = forms.IntegerField()
    
    precio = forms.DecimalField(label="Precio", max_digits=5, decimal_places=2, required=False)

    
    
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
    marca = forms.ChoiceField(choices=MARCA,
                               initial="KA")
    
    def __init__(self, *args, **kwargs):
    
        super(MotoForm, self).__init__(*args, **kwargs)
        
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields["usuarios"] = forms.ChoiceField(
            choices=usuariosDisponibles,
            widget=forms.Select,
            required=True,
        )


class MotoActualizarNombreForm(forms.Form):
    nombre = forms.CharField(label="Nombre de Moto",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")
    
    


class ConcesionarioForm(forms.Form):
    nombre = forms.CharField(label="Nombre del Concesionario",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")
    
    ubicacion = forms.CharField(label="Ubicacion",
                                  required=False,
                                  widget=forms.Textarea())
    
    descripcion = forms.CharField(label="Descripcion",
                                  required=False,
                                  widget=forms.Textarea())
    
    
    
    
    telefono = forms.IntegerField()
    
    fecha_apertura = forms.DateField(label="Fecha Apertura",
                                        initial=datetime.date.today,
                                        widget= forms.SelectDateWidget(years=range(1990,2025))
                                        )
    
    def __init__(self, *args, **kwargs):
    
        super(ConcesionarioForm, self).__init__(*args, **kwargs)
        
        motosDisponibles = helper.obtener_motos_select()
        self.fields["motos"] = forms.ChoiceField(
            choices=motosDisponibles,
            widget=forms.Select,
            required=True,
        )


class ConcesionarioActualizarNombreForm(forms.Form):
    nombre = forms.CharField(label="Nombre de Concesionario",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")


class EventoForm(forms.Form):
    nombre = forms.CharField(label="Nombre del Evento",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")
    
    ubicacion = forms.CharField(label="Ubicacion",
                                  required=False,
                                  widget=forms.Textarea())
    
    descripcion = forms.CharField(label="Descripcion",
                                  required=False,
                                  widget=forms.Textarea())
    
    
    
    
    hora = forms.TimeField(label="Hora del Evento", required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
    
    fecha= forms.DateField(label="Fecha",
                                        initial=datetime.date.today,
                                        widget= forms.SelectDateWidget(years=range(1990,2025))
                                        )
    
    def __init__(self, *args, **kwargs):
    
        super(EventoForm, self).__init__(*args, **kwargs)
        
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields["usuarios"] = forms.ChoiceField(
            choices=usuariosDisponibles,
            widget=forms.Select,
            required=True,
        )
        
        

class RegistroForm(UserCreationForm): 
    roles = (                   
            (2, 'trabajador'),
            (3, 'cliente'),
            )   
    rol = forms.ChoiceField(choices=roles)  
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','rol')
        

class LoginForm(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    