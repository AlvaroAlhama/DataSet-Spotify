from django.contrib import admin
from main.models import *

#registramos en el administrador de django los modelos 
admin.site.register(Artista)
admin.site.register(Cancion)
admin.site.register(Usuario)
admin.site.register(Puntuacion)