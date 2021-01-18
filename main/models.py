#encoding:utf-8
from django.db import models

class Artista(models.Model):
    nombre = models.CharField(max_length=60, verbose_name='Artista')

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="Id")

    def __str__(self):
        return self.id

class Cancion(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="Id")
    nombre = models.TextField(verbose_name='Nombre')
    año = models.IntegerField(verbose_name="Año")
    duracion = models.FloatField(verbose_name='Duración')
    popularidad = models.IntegerField(verbose_name='Popularidad')
    tempo = models.FloatField(verbose_name='Tempo')
    id_spotify = models.TextField(verbose_name='Id Spotify')
    bailabilidad = models.FloatField(verbose_name='Bailabilidad')
    explicito = models.IntegerField(verbose_name="Explicito")
    artistas = models.ManyToManyField(Artista, related_name='Artistas')

    def __str__(self):
        return self.nombre

class Puntuacion(models.Model):
    id_cancion = models.ForeignKey(Cancion, verbose_name="Id Canción", on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, verbose_name="Id Usuario", on_delete=models.CASCADE)
    valoracion = models.IntegerField(verbose_name="Valoración")

    def __str__(self):
        return str(self.id_cancion) + " " + str(self.id_usuario) + " " + str(self.valoracion)
    
