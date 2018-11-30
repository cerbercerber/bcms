from django.urls import path

from . import views

app_name = 'bo'
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index2'),
    path('login', views.login, name='login'),
    #path('eleve', views.eleve, name='eleve'),
    path('administratif', views.administratifliste, name='administratif'),
    path('administratif/<str:modele>/<int:oid>', views.administratifdetail, name='administratif2'),
    path('administratif/<str:modele>', views.administratifliste, name='administratif3'),
    #path('administratif/<str:modele>', views.administratif, name='administratif3'),
    path('administratif/<str:modele>/<str:mode>', views.administratifdetail, name='administratif4'),
    
    path('search', views.search, name='search'),
    
    path('administratifedt/<str:mode>', views.edt, name='edt'),
    path('administratifedtresa/<int:idcours>', views.edtresa, name='edtresa'), 
    path('administratifedtresadup/<int:idcours>', views.edtresadup, name='edtresadup'), 
    
    path('administratifedtsuppresa/<int:idcours>',views.edtresasup, name='edtresasup'),
    #path('frontoffice/administratif/<int:grid>', views.connecteadministratif, name='connectadministratif2'),
    #path('enseignant', views.enseignant, name='enseignant'),
    path('deconnexion', views.deconnexion, name='deconnexion'),    
    
   # path('frontoffice/administratif/groupe/int:pk', views.connecteadministratif, name='connectadministratif'),
  #  path('list', views.list, name='list')     
]