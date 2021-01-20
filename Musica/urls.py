from django.urls import path
from django.contrib import admin
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio),
    path('populate/', views.populateDB),
    path('loadrs/', views.loadRS),
    path('prueba/', views.pruebaWoosh),
    ]
