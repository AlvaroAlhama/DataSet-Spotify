# encoding:utf-8
from main.models import *
from main.populate import populateDatabase
from main.recommendations import loadDict
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import urllib.request
import lxml
from datetime import datetime
import csv


def populateDB(request):
    populateDatabase()
    return render(request, 'inicio.html', {'mensaje': 'Se ha generado correctamente la base de datos'})

def loadRS(request):
    loadDict()
    return render(request, 'inicio.html', {'mensaje': 'Se ha la relación de similitudes'})

def inicio(request):
    return render(request, 'inicio.html', {})

