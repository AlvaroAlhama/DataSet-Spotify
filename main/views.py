# encoding:utf-8
from main.models import *
from main.populate import populateDatabase
from main.recommendations import *
from main.forms import *
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import urllib.request
import lxml
from datetime import datetime
import csv
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import shelve


def populateDB(request):
    populateDatabase()
    return render(request, 'inicio.html', {'mensaje': 'Se ha generado correctamente la base de datos'})

def loadRS(request):
    loadDict()
    return render(request, 'inicio.html', {'mensaje': 'Se ha la relación de similitudes'})

def inicio(request):
    return render(request, 'inicio.html', {})

def mostrarTodasCanciones(request):
    c = Cancion.objects.all()
    return render(request, 'mostrar_canciones.html', {'canciones': c})

def mostrarTodosArtistas(request):
    a = Artista.objects.all().order_by('nombre')
    return render(request, 'mostrar_artistas.html', {'artistas': a})

def mostrarCancionesPopulares(request):
    c = []
    for i in range(1999,2021):
        c.append(Cancion.objects.filter(año=i).order_by("popularidad")[:1][0])
    return render(request, 'mostrar_canciones_populares.html', {'canciones': c})

def mostrarCancionesExplicitas(request):
    c = Cancion.objects.filter(explicito=1)
    return render(request, 'mostrar_canciones_explicitas.html', {'canciones': c})

def busquedaCancion(request):
    formulario = CancionBusquedaForm()
    cancion = None
    mensaje = None
    if request.method == 'POST':
        formulario = CancionBusquedaForm(request.POST)

        if formulario.is_valid():
            cancion = Cancion.objects.filter(nombre=formulario.cleaned_data['nombre'])
            if len(cancion)==0:
                mensaje = 'Lo sentimos, no hay ninguna canción con ese nombre en nuestra BBDD'
    return render(request, 'mostrar_canciones.html', {'formulario': formulario, 'canciones': cancion, 'mensaje': mensaje})

def busquedaArtista(request):
    formulario = ArtistaBusquedaForm()
    artista = None
    mensaje = None
    if request.method == 'POST':
        formulario = ArtistaBusquedaForm(request.POST)

        if formulario.is_valid():
            artista = Artista.objects.filter(nombre=formulario.cleaned_data['nombre'])
            if len(artista)==0:
                mensaje = 'Lo sentimos, no hay ningún artista con ese nombre en nuestra BBDD'
    return render(request, 'mostrar_artistas.html', {'formulario': formulario, 'artistas': artista, 'mensaje': mensaje})

def busquedaArtistaURL(request, nombre):
    ix=open_dir('./Index')
    artista = {'nombre': None, 'albumnes': None, 'url_oficial': None, 'url_wiki': None, 'url_twitter': None, 'url_instagram':None}  
    mensaje = None    
    with ix.searcher() as searcher:
        query = QueryParser("artista", ix.schema).parse(nombre)
        results = searcher.search(query)
        artista['nombre'] = nombre
        if len(results)==0:
            mensaje = 'Lo sentimos, no tenemos más información de este artista.'
        else:
            if 'albumnes' in results[0].keys():
                artista['albumnes'] = results[0]['albumnes']
            if 'url_oficial' in results[0].keys():
                artista['url_oficial'] = results[0]['url_oficial']
            if 'url_wiki' in results[0].keys():
                artista['url_wiki'] = results[0]['url_wiki']
            if 'url_twitter' in results[0].keys():
                artista['url_twitter'] = results[0]['url_twitter']
            if 'url_instagram' in results[0].keys():
                artista['url_instagram'] = results[0]['url_instagram']
    a = Artista.objects.filter(nombre=nombre)
    if len(artista)>0:
        canciones = Cancion.objects.filter(artistas=a[0])
    return render(request, 'mostrar_artista.html', {'artista': artista, 'canciones': canciones, 'mensaje': mensaje})

def recomendacionUsuario(request):
    formulario = UsuarioBusquedaForm()
    items = None
    idUsuario = None
    if request.method == 'POST':
        formulario = UsuarioBusquedaForm(request.POST)
        if formulario.is_valid():
            idUsuario = formulario.cleaned_data['idUsuario']
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idUsuario))
            recommended = rankings[:3]
            canciones = []
            scores = []
            for re in recommended:
                canciones.append(Cancion.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(canciones,scores)

    return render(request,'canciones_recomendadas_usuario.html', {'formulario': formulario, 'items': items, 'idUsuario': idUsuario})

def recomendacionCancion(request):
    formulario = CancionBusquedaForm()
    items = None
    cancion = None
    if request.method == 'POST':
        formulario = CancionBusquedaForm(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data['nombre']
            cancion = nombre
            idCancion = Cancion.objects.filter(nombre=nombre)[0].pk
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idCancion), n=3)
            canciones = []
            scores = []
            for re in recommended:
                canciones.append(Cancion.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(canciones,scores)

    return render(request,'canciones_recomendadas_cancion.html', {'formulario': formulario, 'items': items, 'cancion': cancion})
