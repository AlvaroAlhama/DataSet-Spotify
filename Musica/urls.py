from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio),
    path('populate/', views.populateDB),
    path('loadrs/', views.loadRS),
    path('mostrarcanciones/', views.mostrarTodasCanciones),
    path('mostrarartistas/', views.mostrarTodosArtistas),
    path('mostrarexplicito/', views.mostrarCancionesExplicitas),
    path('mostrarpopulares/', views.mostrarCancionesPopulares),
    path('busquedacancion/', views.busquedaCancion),
    path('busquedaartista/', views.busquedaArtista),
    path('artista/<str:nombre>', views.busquedaArtistaURL),
    path('recomendarcancionusuario/', views.recomendacionUsuario),
    path('recomendarcancion/', views.recomendacionCancion),
    ]
