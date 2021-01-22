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
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


def populateDB(request):
    populateDatabase()
    return render(request, 'inicio.html', {'mensaje': 'Se ha generado correctamente la base de datos'})

def loadRS(request):
    loadDict()
    return render(request, 'inicio.html', {'mensaje': 'Se ha la relación de similitudes'})

def inicio(request):
    return render(request, 'inicio.html', {})

def pruebaWoosh(request):
    ix=open_dir('./Index')      
    with ix.searcher() as searcher:
        query = QueryParser("artista", ix.schema).parse('m.o.v.e')
        results = searcher.search(query)
    return render(request, 'inicio.html', {})
