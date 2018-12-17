from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse

from bo.models import *

import datetime

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
    #groupes
    listgroupeeleveannee=[]
    for annsco in AnneeScolaire.objects.all() :
        groupeeleveannee=Inscription.objects.filter(groupe__ue__periode__diplome__anneescolaire__id=annsco.id,eleve=elconnected)
        listgroupeeleveannee.append({"annsco":annsco,"groupes" :groupeeleveannee })
    #filiere            
    fileleve=FiliereEleve.objects.filter(eleve=elconnected)
   
   #devoir
   #controle 
    listecontroledatenext={}
    listedevoirsdatenext={}  
    groupeeleve=Inscription.objects.filter(eleve=elconnected)   
    
    today = datetime.datetime.now()
    start = today - datetime.timedelta(days=today.weekday())
    end = start + datetime.timedelta(days=5)
    
    if request.POST.get( "nbsemainesuivantes") :
        nbsemsuiv=request.POST.get( "nbsemainesuivantes")
        nbjoursuiv=7*nbsemsuiv
        start=start + timedelta(days=nbjoursuiv)
        end=end + timedelta(days=nbjoursuiv)
    
    dateexa= start    
    while dateexa<=end :
        listecontrolenext=[]
        listedevoirsnext=[]
        for ge in groupeeleve:          
            listecontrole=Controle.objects.filter(cours__groupes__id=ge.groupe.id)
            listedevoirs=Devoir.objects.filter(cours__groupes__id=ge.groupe.id)
            for cont in listecontrole:
                if cont.cours.datedebut.strftime('%d-%m-%Y')==dateexa.strftime('%d-%m-%Y') :
                    listecontrolenext.append(cont)      
            for dev in listedevoirs:
                if dev.cours.datedebut.strftime('%d-%m-%Y')==dateexa.strftime('%d-%m-%Y') :
                    listedevoirsnext.append(dev)                        
        if  listecontrolenext:      
                listecontroledatenext[dateexa.strftime('%d-%m-%Y')]=listecontrolenext
        if  listedevoirsnext:      
                listedevoirsdatenext[dateexa.strftime('%d-%m-%Y')]=listedevoirsnext
        dateexa=dateexa + datetime.timedelta(1)        
      

    
    #notes
    #listenotes=Note.objects.none()   
    listenotes=Note.objects.filter(eleve=elconnected)
                       
    return render(request, 'fo/eleve.html',{"groupeeleve" : listgroupeeleveannee,
                                            "filiereeleve" : fileleve,
                                            "listedevoirs":listedevoirs,
                                            "start":start.strftime('%d-%m-%Y'),"end":end.strftime('%d-%m-%Y'),
                                            'listecontroledatenext':listecontroledatenext, 'listedevoirsdatenext':listedevoirsdatenext,                                            
                                            'listenotes':listenotes,
                                            'user':elconnected}) 


def eleveedt(request):
    
    mode= request.POST.get("mode")
    disp=request.POST.get("disp")
    data=[]
    elconnected=eleveconnected(request)
    inscrele=Inscription.objects.filter(eleve__id=elconnected.id).all(); 
           
    if mode=="controle" :     
       for ie in inscrele :
           controles=Controle.objects.filter(cours__groupes=ie.groupe).all()
           for cont in controles :
               if cont :
                    data.append(
                    {
                    'idcours' : cont.id,
                    'title' : cont.type+" "+cont.texte +"("+str(cont.bareme)+" "+str(cont.classant)+ ")",
                    'start'  : cont.cours.datedebut,
                    'end'    : cont.cours.datefin,
                    'type' : 'controle'
                    });
    
    elif mode=="devoir" :
       for ie in inscrele :
           devoirs=Devoir.objects.filter(cours__groupes=ie.groupe).all()
           for dev in devoirs :
               if dev :
                    data.append(
                    {
                    'idcours' : dev.id,
                    'title' : dev.type+" "+dev.texte,
                    'start'  : dev.cours.datedebut,
                    'end'    : dev.cours.datefin,
                    'type' : 'devoir'
                    });
    
    elif mode=="edt":
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
            nbdevoirs=Devoir.objects.filter(cours=jd).count()
            nbcont=Controle.objects.filter(cours=jd).count()
            data.append(
            {
                'idcours' : jd.id,
                'title' : strgr,
                'start'  : jd.datedebut,
                'end'    : jd.datefin,
                'nbdevoirs' :nbdevoirs,
                'nbcont' :nbcont,
                "type":"edt"
            
            });
            
    if disp=="liste" : 
            datatab=[];
            for jd in data :                  
           
                datecours=jd["start"].strftime('%d-%m-%Y')
                heurecours=jd["start"].strftime('%Hh%M')
                heurecours=heurecours +"-"+jd["end"].strftime('%Hh%M')
                if request.POST.get("start") :
                    debdate=request.POST.get("start").replace(" GMT+0000","")
                    enddate=request.POST.get("end").replace(" GMT+0000","")
                    datedebdate=datetime.datetime.strptime(debdate, "%a %b %d %Y %H:%M:%S")
                    dateenddate=datetime.datetime.strptime(enddate, "%a %b %d %Y %H:%M:%S")
                    datedebdate=datedebdate.replace(tzinfo=utc)
                    dateenddate=dateenddate.replace(tzinfo=utc)
                    
                   
                        
                    if jd["start"]>datedebdate and jd["end"]<=dateenddate :                      
                        if jd["end"].strftime('%d-%m-%Y') != datecours : datecours+"-"+jd["end"].strftime('%d-%m-%Y')
                        datatab.append(
                               {
                            'idcours' : jd["idcours"],
                            'title' : jd["title"],
                            'start'  : datecours,
                            'end'    : heurecours
                        
                        }); 
                else :           
                     datatab.append(
                                       {
                                   'idcours' : jd["idcours"],
                            'title' : jd["title"],
                            'start'  : datecours,
                            'end'    : heurecours
                                });
            listdata ={"data":datatab}
            return JsonResponse(listdata,safe=False)
            
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
    if request.user.is_authenticated: return redirect('fo:eleve')    
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
