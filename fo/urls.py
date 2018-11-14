from django.urls import path

from . import views

app_name = 'fo'
urlpatterns = [
    path('', views.index, name='index'),
    path('', views.index, name='accueil'),
    path('eleve', views.eleve, name='eleve'),
    path('index', views.index, name='index2'),
    path('login', views.login, name='login'),   
    path('deconnexion', views.deconnexion, name='deconnexion'),
    path('eleveedt', views.eleveedt, name='edt'),
 
    
   # path('frontoffice/administratif/groupe/int:pk', views.connecteadministratif, name='connectadministratif'),
  #  path('list', views.list, name='list')     
]
