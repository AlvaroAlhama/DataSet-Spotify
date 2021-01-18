from main.models import *
import csv
import random 

def deleteTables():  
    Puntuacion.objects.all().delete()
    Usuario.objects.all().delete()
    Cancion.objects.all().delete()
    Artista.objects.all().delete()

def populateArtista():
    print("Cargando artistas...")
        
    lista=[]
    with open('data2.csv', newline='', encoding='utf8') as File:
        reader = csv.reader(File)
        contador = 0
        for row in reader:
            if(contador != 0):
                artistas = row[3].replace("[","").replace("]","").replace("'","").split(", ")
                for a in artistas:
                    if Artista(nombre=a) not in lista:
                        lista.append(Artista(nombre=a))
                
            contador = contador + 1

    Artista.objects.bulk_create(lista)
    
    print("Artistas añadidos: " + str(Artista.objects.count()))
    print("---------------------------------------------------------") 
    
def populateCancion():
    print("Cargando canciones...")
        
    contador = 0
    lista_canciones=[]
    lista_artista={}
    diccionario_canciones = {}
    with open('data2.csv', newline='', encoding='utf8') as File:
        reader = csv.reader(File)
        for row in reader:
            if(contador != 0):
                id = contador - 1
                nombre = row[14]
                año = row[1]
                duracionms = row[5]
                duracion = float(duracionms)/60000
                popularidad = row[15]
                tempo = row[18].replace(';','')
                id_spotify = row[8]
                bailabilidad = row[4]
                explicito = row[7]

                lista_canciones.append(Cancion(id=id, nombre=nombre, año=año, duracion=duracion,
                popularidad=popularidad, tempo=tempo, id_spotify=id_spotify,
                bailabilidad=bailabilidad, explicito=explicito))

                diccionario_canciones[contador] = Cancion(id=id, nombre=nombre, año=año, duracion=duracion, popularidad=popularidad, tempo=tempo, id_spotify=id_spotify,
                bailabilidad=bailabilidad, explicito=explicito)

                lista_auxiliar = []
                artistas = row[3].replace("[","").replace("]","").replace("'","").split(", ")
                for a in artistas:
                    lista_auxiliar.append(Artista.objects.filter(nombre=a)[0])
                
                lista_artista[id] = lista_auxiliar

            contador = contador + 1

    Cancion.objects.bulk_create(lista_canciones)
    for cancion in Cancion.objects.all():
        cancion.artistas.set(lista_artista[cancion.id])
    
    print("Canciones añadidas: " + str(Cancion.objects.count()))
    print("---------------------------------------------------------")

    return diccionario_canciones
    


def populateUsuario():
    print("Cargando usuarios...")
       
    lista=[]
    for i in range(1,201):
        lista.append(Usuario(id=i))
    Usuario.objects.bulk_create(lista)
    
    print("Usuarios añadidos: " + str(Usuario.objects.count()))
    print("---------------------------------------------------------")

       
def populatePuntuacion(c):
    print("Cargando puntuaciones...")

    lista=[]
    num_canciones = Cancion.objects.count()
    for i in range(1,201):
        usuario = Usuario.objects.filter(id=i)[0]
        lista_canciones = []
        num_valoraciones = random.randrange(0,50)
        for j in range(num_valoraciones):
            valoracion = random.randrange(0,100)
            id_cancion = random.randrange(1, num_canciones)
            if id_cancion not in lista_canciones:
                lista.append(Puntuacion(id_cancion=c[id_cancion] , id_usuario=usuario, valoracion=valoracion))
                lista_canciones.append(id_cancion)
    Puntuacion.objects.bulk_create(lista)
    print("Puntuaciones añadidas: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")
    
    
def populateDatabase():
    deleteTables()
    populateArtista()
    c = populateCancion()
    populateUsuario()
    populatePuntuacion(c)
    print("Finished database population")
    
if __name__ == '__main__':
    populateDatabase()