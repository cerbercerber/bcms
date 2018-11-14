from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse

from bo.models import *

def deconnexion(request):
    #user = request.user
    #if user is not None :
    #    user.logout()
    logout(request)  
    return redirect('fo:accueil')
# Create your views here.

def eleveconnected(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='eleve').exists() :
            user=request.user   
            elconn=Eleve.objects.get(email=user.email)
            return elconn
    return deconnexion(request)
        
def eleve(request):
    elconnected=eleveconnected(request)
    groupeeleve=[]
    for annsco in AnneeScolaire.objects.all() :
        groupeeleveannee=Inscription.objects.filter(groupe__ue__periode__diplome__anneescolaire__id=annsco.id,eleve=elconnected)
        groupeeleve.append({"annsco":annsco,"groupes" :groupeeleveannee })
                
    fileleve=FiliereEleve.objects.filter(eleve=elconnected)
    
            
            
    return render(request, 'fo/eleve.html',{"groupeeleve" : groupeeleve,"filiereeleve" : fileleve,'user':elconnected}) 


def eleveedt(request):
    elconnected=eleveconnected(request)
    inscrele=Inscription.objects.filter(eleve__id=elconnected.id).all(); 
    listgrou=[]
    for ie in inscrele :
        listgrou.append(ie.groupe.id)
    jsondata=Cours.objects.filter(groupes__in=listgrou) 
    data=[]
    for jd in jsondata :                       
        i=0
        for gr in jd.groupes.all() :
            if i!=0 : 
                strgr=strgr+", " 
            else :
                strgr=gr.ue.nom+"\n"+"groupes : "
            strgr=strgr+gr.nom
            i=i+1
        i=0
        strgr=strgr+"\nsalles : "
        for sa in jd.salles.all() :
            if i!=0 : 
                strgr=strgr+", " 
            else :
                strgr=strgr+sa.nom
        
        data.append(
        {
            'idcours' : jd.id,
            'title' : strgr,
            'start'  : jd.datedebut,
            'end'    : jd.datefin
        
        });
    return JsonResponse(data,safe=False)          

def enseignant(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='enseignant').exists() :
            user=request.user        
            groupeenseignant=Groupe.objects.filter(enseignants__nom__contains=user.username)
            return render(request, 'fo/enseignant.html',{"groupeenseignant" : groupeenseignant,'user':user,"ug":user.groups.all()}) 
    return deconnexion(request)

def index(request): 
  
    #init() 
   # deconnexion(request)      
    if request.POST.get('username') is not None:
    
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)               
            if user.groups.filter(name='eleve').exists() :
            #return render(request, 'frontoffice/connecte.html',{'user':user,"ug":user.groups.all()})
                return redirect('fo:eleve')
            else :
                return deconnexion(request)
        
       # Redirect to a success page.
            #...
        else:
            return render(request, 'fo/index.html',{"error":"oui"})
        # Return an 'invalid login' error message.
      #...
    else :
        return  render(request, 'fo/index.html')
    
    
    #return HttpResponse("Hello, world. You're at the chauss index.")
     #  latest_question_list = Question.objects.order_by('-pub_date')[:6]
    #context = {'latest_question_list': latest_question_list}
    #context="toto";
    #   return  render(request, 'fo/index.html')
