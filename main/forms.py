#encoding:utf-8
from django import forms
from main.models import *

class CancionBusquedaForm(forms.Form):
    nombre = forms.CharField(label='Nombre de la Canción', widget=forms.TextInput, required=True)

class ArtistaBusquedaForm(forms.Form):
    nombre = forms.CharField(label='Nombre del Artista', widget=forms.TextInput, required=True)

class UsuarioBusquedaForm(forms.Form):
    idUsuario = forms.IntegerField(label='Id del Usuario', min_value=1, max_value=200, widget=forms.TextInput, required=True)

   