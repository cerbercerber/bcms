from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse

from django.template import loader
#from _overlapped import NULL

from .models import *

from .forms import *

from django.forms import inlineformset_factory

from django.contrib import messages

from django.http import JsonResponse

import pdb

import json

from django.urls import *

from django.contrib.auth.models import User, Group, Permission

from django.db.models import ProtectedError
# Create your views here.

import time
import pytz
import copy


def search(request):
    
    term=request.POST.get('term')
    #term="c"
    lele=Eleve.objects.filter(nom__contains=term)
    searchtab=[]
    entree={}
    for el in lele :
        entree={}
        entree['id'] = el.id
        entree['label'] = el.nom+" "+el.prenom+" ("+el.get_last_diplome()+")"
        entree['value'] = el.nom+" "+el.prenom
        entree['url'] = request.build_absolute_uri(reverse('bo:administratif2',kwargs={'modele':'eleve','oid':el.id}))
        entree['category'] = "Elève " 
        searchtab.append(entree)
    
    lens=Enseignant.objects.filter(nom__contains=term)
    entree={}
    for es in lens :
        entree={}
        entree['id'] = es.id
        entree['label'] = es.nom+" "+es.prenom
        entree['value'] = es.nom+" "+es.prenom
        entree['url'] = request.build_absolute_uri(reverse('bo:administratif2',kwargs={'modele':'enseignant','oid':es.id}))
        entree['category'] = "Enseignant " 
        searchtab.append(entree)
    
    lue=UE.objects.filter(nom__contains=term)
    entree={}
    for uu in lue :
        entree={}
        entree['id'] = uu.id
        entree['label'] = uu.nom+" "+str(uu.periode)
        entree['value'] = uu.nom+" "+str(uu.periode)
        entree['url'] = request.build_absolute_uri(reverse('bo:administratif2',kwargs={'modele':'UE','oid':uu.id}))
        entree['category'] = "UE " 
        searchtab.append(entree)
    

    return JsonResponse(searchtab,safe=False)


def deconnexion(request):
    #user = request.user
    #if user is not None :
    #    user.logout()
    logout(request)  
    return redirect('/bo/index',foo='bar')

def eleve(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='eleve').exists() :
            user=request.user        
            groupeeleve=Inscription.objects.filter(eleve__nom__contains=user.username)
            return render(request, 'bo/eleve.html',{"groupeeleve" : groupeeleve,'user':user,"ug":user.groups.all()}) 
    return deconnexion(request)

def enseignant(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='enseignant').exists() :
            user=request.user        
            groupeenseignant=Groupe.objects.filter(enseignants__nom__contains=user.username)
            return render(request, 'bo/enseignant.html',{"groupeenseignant" : groupeenseignant,'user':user,"ug":user.groups.all()}) 
    return deconnexion(request)


def edtresa(request,idcours):
 
 retjson=[]   
 #DND
 if request.POST.get("dndresize") :
       if idcours is not 0 :         
            instcours=Cours.objects.get(id=idcours) 
            oldcours=copy.copy(instcours)
            instcours.datedebut=datetime.datetime.strptime(request.POST.get("datedebut"), '%Y-%m-%d %H:%M').replace(tzinfo=utc)            
            instcours.datefin=datetime.datetime.strptime(request.POST.get("datefin"), '%Y-%m-%d %H:%M').replace(tzinfo=utc)      
            try :
                 instcours.save()
            except Exception as e:               
                 retjson={ 'error' : str(e)}
                 oldcours.pk=None
                 oldcours.save()
                 for sa in instcours.salles.all() :
                     cs = CoursSalles(cours=oldcours,salle=sa)
                     cs.save()
                 for gr in instcours.groupes.all() :
                     cg = CoursGroupes(cours=oldcours,groupe=gr)
                     cg.save()
                 instcours.delete()
            else :
                 retjson={ 'error' : "success"}
            return JsonResponse(retjson,safe=False)
 
 ## CREATTION MADAL
 else: 
    #MAJ RESA
    if request.POST.get("datedebut") :
         if idcours is not 0 :         
            instcours=Cours.objects.get(id=idcours) 
            cf=CoursForm(request.POST,instance=instcours);
         else :
            cf=CoursForm(request.POST)
         
         
         #sauv le cours  
         #if cf.is_valid() :
        
         
         if cf.is_valid() :
             instcours=cf.save(commit=False)
           #  instcours.datedebut= time.strptime(str(instcours.datedebut), '%Y-%m-%d %H:%M:%S') 
           #  instcours.datefin=  time.strptime(str(instcours.datefin), '%Y-%m-%d %H:%M:%S') 
             #instcours.verifResa()
             try :
                 instcours.save()
             except Exception as e:
                 retjson={ 'error' : str(instcours.datedebut)+ str(e)}
             else :       
                     #sauv le coursgroupe
                 if request.POST.getlist('groupes') :
                     cg=CoursGroupes.objects.filter(cours__id=idcours)
                     cg.delete()                             
                     listgro=request.POST.getlist('groupes');
                     for gro in listgro :
                        gr=Groupe.objects.get(id=gro)
                        cg=CoursGroupes(groupe=gr,cours=instcours)
                        cg.save()
                    
                 #sauv le courssallee
                 if request.POST.getlist('salles') :
                     cs=CoursSalles.objects.filter(cours__id=idcours)
                     cs.delete()                             
                     listsalle=request.POST.getlist('salles');
                     for sal in listsalle :
                        sa=Salle.objects.get(id=sal)
                        cg=CoursSalles(salle=sa,cours=instcours)
                        cg.save()                         
                    
                     try :
                          instcours.save()
                     except Exception as e:
                        instcours.delete()
                        retjson={ 'error' : str(instcours.datedebut)+ str(e)}
                     else : 
                        retjson={ 'error' : "success"}
         else :
            retjson={ 'error' : cf.errors}
         #else :
         #     messagetab.append({ 'error' : cf.errors});
         return JsonResponse(retjson,safe=False)
        
    #####DISPLAY FORM         
    else :
   
      if idcours is not 0 :         
         instcours=Cours.objects.get(id=idcours)       
         cf=CoursForm(instance=instcours);
      else :         
         cf=CoursForm
              
      return render(request, 'bo/administratifresa.html', {"coursform":cf, "idcours":idcours})  
  
          
             
     
      
    

def edt(request):
    
    modele=request.POST.get("modele");
    oid=request.POST.get("oid");
    
    
    """ modele="UE";
    oid=1
    start:"2018-07-01"
    end:"2018-08-12" 
    
    
    data = {"message": "Message",
            "modele" : modele,
            "oid" : oid}"""
    jsondata=[]
    
    if modele=="UE" :
        jsondata=Cours.objects.filter(groupes__ue__id=oid).distinct();
    elif modele=="eleve" :
        inscrele=Inscription.objects.filter(eleve__id=oid).all(); 
        listgrou=[]
        for ie in inscrele :
            listgrou.append(ie.groupe.id)                
        jsondata=Cours.objects.filter(groupes__in=listgrou)
    elif modele=="enseignant" :
        jsondata=Cours.objects.filter(groupes__enseignants__id=oid).distinct();
    elif modele=="diplome" :
        jsondata=Cours.objects.filter(groupes__ue__periode__diplome__id=oid).distinct();
    elif modele=="salle" :
        jsondata=Cours.objects.filter(salles__id=oid).distinct();
    elif modele=="groupe" :
        jsondata=Cours.objects.filter(groupes__id=oid).distinct();
            
    #export to json
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
     
    #print('----data ----')
    #print(data) 
    
    #pdb.set_trace()  
        
    return JsonResponse(data,safe=False)
 
def changeonformset(formset):
    for tempform in formset.forms :
        if tempform.empty_permitted and not tempform.has_changed():
            changeonformset=False
        else :
            changeonformset=True
            break
    return changeonformset
    
def saveFormset(request,formset): 
    
  if changeonformset(formset): 
    if formset.is_valid():
            try:                                          
                formset.save()
            except ValueError as e:
                   messages.error(request,formset.prefix+" : "+ str(e))                   
                   return False  
            except ProtectedError as e:
                        #messages.error(request, 'Impossible de supprimer cet objet '+ str(type(e))+" : "+str(e))
                        messerror=" ( "
                        for m in e.protected_objects :
                            messerror=messerror+m.nommodele()+" " + str(m) +" "   
                        messerror+=")"                                                
                        messages.error(request, 'Impossible de supprimer cet objet, il reste des objets liés ' + messerror)
                        return False
            
            
            else :
                messages.success(request, formset.prefix +' Enregistrement réussi')
                return True
            '''
            for tempform in formset.forms :
                numformset=' '.join(filter(lambda x: x.isdigit(), tempform.prefix))
                numformset=int(numformset)+1
                if tempform.is_valid() and not tempform.empty_permitted:
                    messages.success(request, str(tempform.instance.nommodele())+' enregistrement réussi')
            '''
    else: 
        for tempform in formset.forms :
            numformset=' '.join(filter(lambda x: x.isdigit(), tempform.prefix))
            numformset=int(numformset)+1
            for key,value in tempform.errors.items():
                messages.error(request,str(tempform.instance.nommodele())+" "+str(numformset)+" : "+key+" "+ value.as_text())
        return False                      
                         
def administratifliste(request,modele=None):
    
    if request.user.is_authenticated:
        if request.user.groups.filter(name='administratif').exists() :
            
            #if request.POST.get("modele") is not None :
            #    modele=request.POST.get("modele");
            
            formFilter="";
            #
            #determination modele et filtre
            #
            if modele is None or modele=="groupe" :
                 model=Groupe
                 modelForm=GroupeForm
                 formFilter=GroupeFormFilter(initial=request.POST)                                            
            elif modele=="eleve" :
                 model=Eleve
                 modelForm=EleveForm 
                 formFilter=EleveFormFilter(initial=request.POST)                               
            elif modele=="enseignant" :
                 model=Enseignant
                 modelForm=EnseignantForm
            elif modele=="diplome" :
                 model=Diplome
                 modelForm=DiplomeForm
                 formFilter=DiplomeFormFilter(initial=request.POST)      
            elif modele=="UE" :
                 model=UE
                 modelForm=UEForm
                 formFilter=UEFormFilter(initial=request.POST) 
            elif modele=="filiere" :
                 model=Filiere
                 modelForm=FiliereForm
            elif modele=="salle" :
                 model=Salle
                 modelForm=SalleForm   
            else :
                 return deconnexion(request)
             
              #TRAITEMENT SUPPRESSION
            if request.POST.get("Supprimer") :
                    tabdel=request.POST.getlist("delgroup[]");
                    groupesdel=model.objects.filter(id__in=tabdel)
                    try:
                        groupesdel.delete()
                    except ProtectedError as e:
                        #instances = e.args[1]
                        #messerror=", ".join([ instance.__str__() for instance in instances])
                        messerror=" ( "
                        for m in e.protected_objects :
                            messerror=messerror+m.nommodele()+" " + str(m) +" "   
                        messerror+=")"                                                
                        messages.error(request, 'Impossible de supprimer cet objet, il reste des objets liés ' + messerror)
                                          
                                                      
            #filter liste
            filterok=False
            if request.method == 'POST' :
                modeleliste=model.objects.all()  
                for filterkey,filtervalue in request.POST.items() :
                    if  filterkey.find("filter") !=-1 :
                            filterok=True
                            newfilterkey=filterkey.replace("filter","") 
                            if filtervalue!="0" :                           
                                kwargs = {
                                '{0}__{1}'.format(newfilterkey, 'id'): filtervalue,
                                }
                                modeleliste=modeleliste.filter(**kwargs)      
                            
            if not filterok :        
                modeleliste=model.objects.all()  
                
            return render(request, 'bo/administratifliste.html',{                                                                                                                                                                        
                                                         "modele":modele,
                                                         "modeleliste" : modeleliste,
                                                         "formFilter":formFilter,                                                                                                                                                                                                                         
                                                         }) 
                                                                      
    #else:
    return deconnexion(request)


def administratifdetail(request,oid=None,modele=None,mode=None): 
                
    if request.user.is_authenticated:
        if request.user.groups.filter(name='administratif').exists() :
            
            if modele is None or modele=="groupe" :
                 model=Groupe
                 modelForm=GroupeForm
            elif modele=="eleve" :
                 model=Eleve
                 modelForm=EleveForm 
            elif modele=="enseignant" :
                 model=Enseignant
                 modelForm=EnseignantForm
            elif modele=="diplome" :
                 model=Diplome
                 modelForm=DiplomeForm
            elif modele=="UE" :
                 model=UE
                 modelForm=UEForm
            elif modele=="filiere" :
                 model=Filiere
                 modelForm=FiliereForm
            elif modele=="salle" :
                 model=Salle
                 modelForm=SalleForm
            else :
                 return deconnexion(request)
             
           
           ################################################
                #CRER FORM INFO
           ###############################################
            modeleitem=""
            # liste de base                
            if oid is not None : 
                       groupeinstance= model.objects.get(id=oid)   
                       grfound=groupeinstance                                
                       formmodele = modelForm(instance=groupeinstance)
                       modeleitem=str(grfound)  
            else :
                       formmodele = modelForm()                
            ##############################################
                   # sauvegarde form info
            #############################################             
            if request.POST.get("Enregistrerinf") :  
             
                    if oid is not None :  formmodele = modelForm(request.POST,instance=groupeinstance)    
                    else : formmodele=modelForm(request.POST)
               
                    if formmodele.is_valid():
                        if modele=="eleve" :
                            
                            #delete diplome  eleve
                            dipleledel=FiliereEleve.objects.filter(eleve__id=oid)
                            dipleledel.delete()
                            # save many many with select 2
                            new_eleve = formmodele.save(commit=False) 
                            new_eleve.save()                         
                            tabdipid=request.POST.getlist('filiere')
                            listdip=Filiere.objects.filter(id__in=tabdipid)
                            for dip in listdip :                     
                                de=FiliereEleve(eleve=new_eleve, filiere=dip)
                                de.save()                                
                            newoid=new_eleve.pk
                            
                        elif modele=="UE" :
                            #filiere
                            uefil=UEFilieres.objects.filter(ue__id=oid)
                            uefil.delete()
                            new_ue = formmodele.save(commit=False)   
                            new_ue.save()                        
                            tabdipid=request.POST.getlist('filieres')
                            listdip=Filiere.objects.filter(id__in=tabdipid)
                            for dip in listdip :                     
                                de=UEFilieres(ue=new_ue, filiere=dip)
                                de.save()                                                            
                            newoid=new_ue.pk
                            #groupe 01
                            if Groupe.objects.filter(ue=new_ue).filter(nom='01').count()==0 :                  
                                newgr=Groupe(nom='01',ue=new_ue);
                                newgr.save();
                       #     messages.success(request, 'Enregistrement réussi Informations')
                        else :
                            objsave=formmodele.save()
                            newoid=objsave.pk
                        messages.success(request, 'Enregistrement réussi')
                        if oid is None :
                            return redirect('bo:administratif2',modele=modele,oid=newoid)
                    else :
                        for key,value in formmodele.errors.items():
                                messages.error(request,key+" "+ value.as_text())     
                        #return redirect('bo:administratif4',modele=modele,mode='add')
                    
                    
            inlineformset1="vide"
            inlineformset2 ="vide"
            inlineformset3="vide"
            formsettitre1=""
            formsettitre2=""
            formsettitre3=""
            listeformset1=[]
            listeformsettitre1=""
            listeformset2=[]
            listeformsettitre2=""
            
            listefs=[]
            listelistefs=[]
            
            ''''
            if oid is None :
                gform = modelForm()
            else:
                grfound=model.objects.get(id=oid);
                formmodele = modelForm(instance=grfound)  
                modeleitem=str(grfound)  
            '''                         
                #######
                #DIPLOME#
                #######
            if oid is not None :
                if modele=="diplome" :
                    
                    PeriodeDiplomeFormset = inlineformset_factory(Diplome, Periode, fields=('nom','datedebut','datefin',),form=PeriodeForm)                                             
                    if  request.POST.get('Enregistrer2')  :
                        inlineformset1 = PeriodeDiplomeFormset(request.POST,instance=grfound)
                        if saveFormset(request,inlineformset1) :
                            inlineformset1 = PeriodeDiplomeFormset(instance=grfound)  
                    else :
                        inlineformset1 = PeriodeDiplomeFormset(instance=grfound)                                                      
                    listefs.append({'titre':"Périodes","formset":inlineformset1,'numtab':"2"})
                  
                    DiplomeFiliereFormSet = inlineformset_factory(Diplome, Filiere,fields=('nom',),form=FiliereForm)                                                   
                    if request.POST.get('Enregistrer3')  : 
                        inlineformset2 = DiplomeFiliereFormSet(request.POST,instance=grfound)
                        if saveFormset(request,inlineformset2) :
                            inlineformset2 = DiplomeFiliereFormSet(instance=grfound)
                    else :
                        inlineformset2 = DiplomeFiliereFormSet(instance=grfound)                    
                    listefs.append({'titre':"Filières","formset":inlineformset2,'numtab':"3"})
                    
                    for fifi in Filiere.objects.filter(diplome__id=oid) :    
                        tempprefix="filierel" +str(fifi.id)                    
                        FiliereEleveFormSet= inlineformset_factory(Filiere, FiliereEleve, fields=('eleve',),form=FiliereEleveForm)   
                        if  request.POST.get('Enregistrer4')  :
                            formsethtmltemp = FiliereEleveFormSet(request.POST,instance=fifi,prefix=tempprefix,queryset=FiliereEleve.objects.filter(filiere__id=fifi.id))
                            if saveFormset(request,formsethtmltemp) :
                                    formsethtmltemp = FiliereEleveFormSet(instance=fifi,prefix=tempprefix,queryset=FiliereEleve.objects.filter(filiere__id=fifi.id))              
                        else :                           
                            formsethtmltemp = FiliereEleveFormSet(instance=fifi,prefix=tempprefix,queryset=FiliereEleve.objects.filter(filiere__id=fifi.id))                                                             
                        listeformset1.append({'titre':fifi.nom ,'formset':formsethtmltemp})
                    
                    listelistefs.append({'titre':"Elèves","listformset":listeformset1,'numtab':"4"});        
                    #DiplomeEleveFormSet = inlineformset_factory(Diplome, DiplomeEleve, fields=('eleve',),form=DiplomeEleveForm)       
                    #inlineformset2 = DiplomeEleveFormSet(instance=grfound)
                    #formsettitre2="Elèves"
                elif modele=="eleve" :
                    
                     #ifo=InscriptionsEleveFormset();
                    #formset=ifo.getform(instance=grfound)
                    '''
                    InscriptionFormSet = inlineformset_factory(Eleve, Inscription, fields=('groupe',),form=InscriptionForm)                         
                    if request.POST.get('Enregistrer2') :
                         inlineformset1 = InscriptionFormSet(request.POST,instance=grfound)
                         saveFormset(request,inlineformset1);
                    inlineformset1 = InscriptionFormSet(instance=grfound)                                     
                    listefs.append({'titre':"Inscriptions simples","formset":inlineformset1,'numtab':"2"});
                    '''
                    
                    AdresseFormSet = inlineformset_factory(Eleve, Adresse, fields=('pays','ville','adresse1','adresse2','adresse3'),form=AdresseForm)                         
                    if request.POST.get('Enregistrer2') :
                        inlineformset1 = AdresseFormSet(request.POST,instance=grfound)
                        if saveFormset(request,inlineformset1) :
                            inlineformset1 = AdresseFormSet(request.POST,instance=grfound)
                    else :
                        inlineformset1 = AdresseFormSet(instance=grfound)                                     
                    listefs.append({'titre':"Adresse","formset":inlineformset1,'numtab':"2"});
                    
                    InscriptionFormSet = inlineformset_factory(Eleve, Inscription, fields=('groupe',),form=InscriptionForm)  
                    for annsco in AnneeScolaire.objects.all() :
                                tempprefix="inscriptions" +str(annsco.id)
                                if  request.POST.get('Enregistrer3')  :
                                    formsethtmltemp = InscriptionFormSet(request.POST,instance=grfound,prefix=tempprefix,queryset=Inscription.objects.filter(groupe__ue__periode__diplome__anneescolaire=annsco.id))
                                    if saveFormset(request,formsethtmltemp):                     
                                        formsethtmltemp = InscriptionFormSet(instance=grfound,prefix=tempprefix,queryset=Inscription.objects.filter(groupe__ue__periode__diplome__anneescolaire=annsco.id))                           
                                else :
                                        formsethtmltemp = InscriptionFormSet(instance=grfound,prefix=tempprefix,queryset=Inscription.objects.filter(groupe__ue__periode__diplome__anneescolaire=annsco.id))                
                                #filtrer les select par anne scolaire                                
                                for form in formsethtmltemp:
                                        form.fields['groupe'].queryset = Groupe.objects.filter(ue__periode__diplome__anneescolaire=annsco)
                                listeformset1.append({'titre':annsco.nom ,'formset':formsethtmltemp})
                    
                    listelistefs.append({'titre':"Inscriptions complexes","listformset":listeformset1,'numtab':"3"});                  
                                       
                elif modele=="groupe" :
                            
                    GroupesEnseignantsFormSet = inlineformset_factory(Groupe, GroupesEnseignants, fields=('enseignant',),form=GroupesEnseignantsForm)                       
                    if request.POST.get('Enregistrer2')  :
                        inlineformset2 = GroupesEnseignantsFormSet(request.POST,instance=grfound)
                        if saveFormset(request,inlineformset1) :
                            inlineformset2 = GroupesEnseignantsFormSet(instance=grfound)  
                    else :
                        inlineformset2 = GroupesEnseignantsFormSet(instance=grfound)                    
                    listefs.append({'titre':"Enseignants","formset":inlineformset2,'numtab':"2"});   
                    
                    InscriptionFormSet = inlineformset_factory(Groupe, Inscription, fields=('eleve',),form=InscriptionForm)
                    if request.POST.get('Enregistrer3') :                       
                        inlineformset1 = InscriptionFormSet(request.POST,instance=grfound) 
                        if saveFormset(request,inlineformset1) :
                             inlineformset1 = InscriptionFormSet(instance=grfound)            
                    else :
                        inlineformset1 = InscriptionFormSet(instance=grfound)                      
                    listefs.append({'titre':"Inscriptions","formset":inlineformset1,'numtab':"3"});   
                    
                elif modele=="enseignant" :   
                                                                     
                    GroupesEnseignantsFormSet = inlineformset_factory(Enseignant, GroupesEnseignants, fields=('groupe',),form=GroupesEnseignantsForm)       
                    if  request.POST.get('Enregistrer2') :                      
                        inlineformset1 = GroupesEnseignantsFormSet(request.POST,instance=grfound)
                        if saveFormset(request,inlineformset1) :
                            inlineformset1 = GroupesEnseignantsFormSet(instance=grfound)    
                    else :
                        inlineformset1 = GroupesEnseignantsFormSet(instance=grfound)                    
                    listefs.append({'titre':"Groupes","formset":inlineformset1,'numtab':"2"});   
                    
                    for annsco in AnneeScolaire.objects.all() :
                                tempprefix="groupesel" +str(annsco.id)
                                if  request.POST.get('Enregistrer3') :                                                                       
                                    formsethtmltemp = GroupesEnseignantsFormSet(request.POST,instance=grfound,prefix=tempprefix,queryset=GroupesEnseignants.objects.filter(groupe__ue__periode__diplome__anneescolaire=annsco.id))
                                    if saveFormset(request,formsethtmltemp) :
                                        formsethtmltemp = GroupesEnseignantsFormSet(instance=grfound,prefix=tempprefix,queryset=GroupesEnseignants.objects.filter(groupe__ue__periode__diplome__anneescolaire=annsco.id))                                                                    
                                else :                                  
                                    formsethtmltemp = GroupesEnseignantsFormSet(instance=grfound,prefix=tempprefix,queryset=GroupesEnseignants.objects.filter(groupe__ue__periode__diplome__anneescolaire=annsco.id))                                                        
                                listeformset1.append({'titre':annsco.nom ,'formset':formsethtmltemp})                   
                    listelistefs.append({'titre':"Inscriptions","listformset":listeformset1,'numtab':"3"}); 
                
                
                elif modele=="UE" :
                                                                            
                    GroupesUEFormSet = inlineformset_factory(UE, Groupe, fields=('nom',),form=GroupeForm )   
                    if  request.POST.get('Enregistrer2') :     
                        inlineformset1 = GroupesUEFormSet(request.POST,instance=grfound)
                        if saveFormset(request,inlineformset1) :
                              inlineformset1 = GroupesUEFormSet(instance=grfound)     
                    else :
                        inlineformset1 = GroupesUEFormSet(instance=grfound)                                         
                    listefs.append({'titre':"Groupes","formset":inlineformset1,'numtab':"2"});  
                                                          
                    GroupesUEFormset = inlineformset_factory(Groupe, Inscription, fields=('eleve',),form=InscriptionForm)                                  
                    for grue in Groupe.objects.filter(ue=grfound) :
                                tempprefix="groupesue" +str(grue.id)
                                if  request.POST.get('Enregistrer3') :                                      
                                    tempGroupesUEFormset = GroupesUEFormset(request.POST,instance=grue,prefix=tempprefix)
                                    if saveFormset(request,tempGroupesUEFormset) :
                                         tempGroupesUEFormset = GroupesUEFormset(instance=grue,prefix=tempprefix)   
                                else :                                   
                                    tempGroupesUEFormset = GroupesUEFormset(instance=grue,prefix=tempprefix)    
                                listeformset1.append({'titre':grue.nom ,'formset':tempGroupesUEFormset})
                    listelistefs.append({'titre':"Inscriptions","listformset":listeformset1,'numtab':"3"});             
                    
                    GroupesEnseignantsFormSet = inlineformset_factory(Groupe, GroupesEnseignants, fields=('enseignant',),form=GroupesEnseignantsForm)                                    
                    for grue in Groupe.objects.filter(ue=grfound) :
                                tempprefix="groupesenseignant" +str(grue.id)
                                if request.POST.get('Enregistrer4') :                                    
                                    tempGroupesEnseignantsFormSet = GroupesEnseignantsFormSet(request.POST,instance=grue,prefix=tempprefix)
                                    if saveFormset(request,tempGroupesEnseignantsFormSet) : 
                                         tempGroupesEnseignantsFormSet = GroupesEnseignantsFormSet(instance=grue,prefix=tempprefix)   
                                else :                                  
                                    tempGroupesEnseignantsFormSet = GroupesEnseignantsFormSet(instance=grue,prefix=tempprefix)                                                                    
                                listeformset2.append({'titre':grue.nom ,'formset':tempGroupesEnseignantsFormSet})
                    listelistefs.append({'titre':"Enseignants","listformset":listeformset2,'numtab':"4"}); 

                
            
           
            return render(request, 'bo/administratifdetail.html',{                                                                                                                                                                        
                                                         "oid" : oid,"modele":modele,"modeleitem":modeleitem,"mode":mode,
                                                         "formmodele" : formmodele,
                                                         "listefs":listefs,
                                                         "listelistefs":listelistefs                                                                                                                                                                                                                           
                                                         }) 

def administratif(request,oid=None,modele=None,mode=None):
    
      
    if request.user.is_authenticated:
        if request.user.groups.filter(name='administratif').exists() :
            
            #if request.POST.get("modele") is not None :
            #    modele=request.POST.get("modele");
            
            formFilter="";
            #
            #determination modele et filtre
            #
            if modele is None or modele=="groupe" :
                 model=Groupe
                 modelForm=GroupeForm
                 formFilter=GroupeFormFilter(initial=request.POST)                                            
            elif modele=="eleve" :
                 model=Eleve
                 modelForm=EleveForm 
                 formFilter=EleveFormFilter(initial=request.POST)                               
            elif modele=="enseignant" :
                 model=Enseignant
                 modelForm=EnseignantForm
            elif modele=="diplome" :
                 model=Diplome
                 modelForm=DiplomeForm
                 formFilter=DiplomeFormFilter(initial=request.POST)      
            elif modele=="UE" :
                 model=UE
                 modelForm=UEForm
                 formFilter=UEFormFilter(initial=request.POST)    
            else :
                 return deconnexion(request)
             
            
              
              
            #traitement POST
            #TRAITEMENT AJOUT MODIFICATION 
            if request.method == 'POST' : 
     
                 ##############################################
                   # sauvegarde form info
                 #############################################
                if request.POST.get("Enregistrerinf") :
                    
                    
                    if oid is not None : 
                       groupeinstance= model.objects.get(id=oid)                                   
                       form = modelForm(request.POST,instance=groupeinstance)
                    else :
                        form = modelForm(request.POST)
                   
                    if form.is_valid():
                        if modele=="eleve" :
                            
                            #delete diplome  eleve
                            dipleledel=FiliereEleve.objects.filter(eleve__id=oid)
                            dipleledel.delete()
                            # save many many with select 2
                            new_eleve = form.save(commit=False) 
                            new_eleve.save()                         
                            tabdipid=request.POST.getlist('filiere')
                            listdip=Filiere.objects.filter(id__in=tabdipid)
                            for dip in listdip :                     
                                de=FiliereEleve(eleve=new_eleve, filiere=dip)
                                de.save()                                
                            newoid=new_eleve.pk
                            
                        elif modele=="UE" :
                            #filiere
                            uefil=UEFilieres.objects.filter(ue__id=oid)
                            uefil.delete()
                            new_ue = form.save(commit=False)   
                            new_ue.save()                        
                            tabdipid=request.POST.getlist('filieres')
                            listdip=Filiere.objects.filter(id__in=tabdipid)
                            for dip in listdip :                     
                                de=UEFilieres(ue=new_ue, filiere=dip)
                                de.save()                                                            
                            newoid=new_ue.pk
                            #groupe 01
                            if Groupe.objects.filter(ue=new_ue).filter(nom='01').count()==0 :                  
                                newgr=Groupe(nom='01',ue=new_ue);
                                newgr.save();
                       #     messages.success(request, 'Enregistrement réussi Informations')
                        else :
                            objsave=form.save()
                            newoid=objsave.pk
                        messages.success(request, 'Enregistrement réussi')
                        if oid is None :
                            return redirect('bo:administratif2',modele=modele,oid=newoid)
                    else :
                        for key,value in form.errors.items():
                                messages.error(request,key+" "+ value.as_text())     
                        return redirect('bo:administratif4',modele=modele,mode='add')

                    
                                                                           
            #TRAITEMENT SUPPRESSION
            if request.POST.get("Supprimer") :
                    tabdel=request.POST.getlist("delgroup[]");
                    groupesdel=model.objects.filter(id__in=tabdel)
                    groupesdel.delete()
                    
            #fin traitement formulaire
            user=request.user        
           
            
            #filter liste
            filterok=False
            if request.method == 'POST' :
                modeleliste=model.objects.all()  
                for filterkey,filtervalue in request.POST.items() :
                    if  filterkey.find("filter") !=-1 :
                            filterok=True
                            newfilterkey=filterkey.replace("filter","") 
                            if filtervalue!="0" :                           
                                kwargs = {
                                '{0}__{1}'.format(newfilterkey, 'id'): filtervalue,
                                }
                                modeleliste=modeleliste.filter(**kwargs) 
                            #else :  
                            #    groupes=model.objects.all()       
                            #groupes=model.objects.filter(newfilterkey=filtervalue)            
                            
            if not filterok :        
                modeleliste=model.objects.all()             
                    
            #fin filtrer liste    
            
            modeleitem=""
            # liste de base
            formmodele = modelForm()
            inlineformset1="vide"
            inlineformset2 ="vide"
            inlineformset3="vide"
            formsettitre1=""
            formsettitre2=""
            formsettitre3=""
            listeformset1=[]
            listeformsettitre1=""
            listeformset2=[]
            listeformsettitre2=""
            
            listefs=[]
            listelistefs=[]
            
            if oid is None :
                gform = modelForm()
            else:
                grfound=model.objects.get(id=oid);
                formmodele = modelForm(instance=grfound)  
                modeleitem=str(grfound)                           
                #######
                #DIPLOME#
                #######
                if modele=="diplome" :
                    
                    PeriodeDiplomeFormset = inlineformset_factory(Diplome, Periode, fields=('nom','datedebut','datefin',),form=PeriodeForm)                                             
                    if  request.POST.get('Enregistrer2')  :
                        inlineformset1 = PeriodeDiplomeFormset(request.POST,instance=grfound)
                        saveFormset(request,inlineformset1);
                    inlineformset1 = PeriodeDiplomeFormset(instance=grfound)                                                      
                    listefs.append({'titre':"Périodes","formset":inlineformset1,'numtab':"2"})
                  
                    DiplomeFiliereFormSet = inlineformset_factory(Diplome, Filiere,fields=('nom',),form=FiliereForm)                                                   
                    if request.POST.get('Enregistrer3')  : 
                        inlineformset2 = DiplomeFiliereFormSet(request.POST,instance=grfound)
                        saveFormset(request,inlineformset2);
                    inlineformset2 = DiplomeFiliereFormSet(instance=grfound)                    
                    listefs.append({'titre':"Filières","formset":inlineformset2,'numtab':"3"})
                    
                    for fifi in Filiere.objects.filter(diplome__id=oid) :    
                        tempprefix="filierel" +str(fifi.id)                    
                        FiliereEleveFormSet= inlineformset_factory(Filiere, FiliereEleve, fields=('eleve',),form=FiliereEleveForm)   
                        if  request.POST.get('Enregistrer4')  :
                            formsethtmltemp = FiliereEleveFormSet(request.POST,instance=fifi,prefix=tempprefix,queryset=FiliereEleve.objects.filter(filiere__id=fifi.id))
                            if formsethtmltemp.is_valid():
                                formsethtmltemp.save()
                        
                        formsethtmltemp = FiliereEleveFormSet(instance=fifi,prefix=tempprefix,queryset=FiliereEleve.objects.filter(filiere__id=fifi.id))                                                             
                        listeformset1.append({'titre':fifi.nom ,'formset':formsethtmltemp})
                    
                    listelistefs.append({'titre':"Elèves","listformset":listeformset1,'numtab':"4"});        
                    #DiplomeEleveFormSet = inlineformset_factory(Diplome, DiplomeEleve, fields=('eleve',),form=DiplomeEleveForm)       
                    #inlineformset2 = DiplomeEleveFormSet(instance=grfound)
                    #formsettitre2="Elèves"
                elif modele=="eleve" :
                    
                     #ifo=InscriptionsEleveFormset();
                    #formset=ifo.getform(instance=grfound)
                    InscriptionFormSet = inlineformset_factory(Eleve, Inscription, fields=('groupe',),form=InscriptionForm)                         
                    if request.POST.get('Enregistrer2') :
                         inlineformset1 = ff(request.POST,instance=grfound)
                         saveFormset(request,inlineformset1);
                    inlineformset1 = InscriptionFormSet(instance=grfound)                                     
                    listefs.append({'titre':"Inscriptions simples","formset":inlineformset1,'numtab':"2"});
                    
                    for annsco in AnneeScolaire.objects.all() :
                                tempprefix="groupesel" +str(annsco.id)
                                if  request.POST.get('Enregistrer3')  :
                                    formsethtmltemp = InscriptionFormSet(request.POST,instance=grfound,prefix=tempprefix,queryset=Inscription.objects.filter(groupe__ue__periode__diplome__anneescolaire=annsco.id))
                                    saveFormset(request,formsethtmltemp);                           
                                formsethtmltemp = InscriptionFormSet(instance=grfound,prefix=tempprefix,queryset=Inscription.objects.filter(groupe__ue__periode__diplome__anneescolaire=annsco.id))                           
                                #filtrer les select par anne scolaire                                
                                for form in formsethtmltemp:
                                        form.fields['groupe'].queryset = Groupe.objects.filter(ue__periode__diplome__anneescolaire=annsco)
                                listeformset1.append({'titre':annsco.nom ,'formset':formsethtmltemp})
                    
                    listelistefs.append({'titre':"Inscriptions complexes","listformset":listeformset1,'numtab':"3"});                  
                                       
                elif modele=="groupe" :
                            
                    GroupesEnseignantsFormSet = inlineformset_factory(Groupe, GroupesEnseignants, fields=('enseignant',),form=GroupesEnseignantsForm)                       
                    if request.POST.get('Enregistrer2')  :
                        inlineformset2 = GroupesEnseignantsFormSet(request.POST,instance=grfound)
                        saveFormset(request,inlineformset1);
                    inlineformset2 = GroupesEnseignantsFormSet(instance=grfound)                    
                    listefs.append({'titre':"Enseignants","formset":inlineformset2,'numtab':"2"});   
                    
                    InscriptionFormSet = inlineformset_factory(Groupe, Inscription, fields=('eleve',),form=InscriptionForm)
                    if request.POST.get('Enregistrer3') :                       
                        inlineformset1 = InscriptionFormSet(request.POST,instance=grfound) 
                        saveFormset(request,inlineformset1);
                    inlineformset1 = InscriptionFormSet(instance=grfound)                      
                    listefs.append({'titre':"Inscriptions","formset":inlineformset1,'numtab':"3"});   
                    
                elif modele=="enseignant" :   
                                                                     
                    GroupesEnseignantsFormSet = inlineformset_factory(Enseignant, GroupesEnseignants, fields=('groupe',),form=GroupesEnseignantsForm)       
                    if  request.POST.get('Enregistrer2') :                      
                        inlineformset1 = GroupesEnseignantsFormSet(request.POST,instance=grfound)
                        saveFormset(request,inlineformset1);
                    inlineformset1 = GroupesEnseignantsFormSet(instance=grfound)                    
                    listefs.append({'titre':"Groupes","formset":inlineformset1,'numtab':"2"});   
                    
                    for annsco in AnneeScolaire.objects.all() :
                                tempprefix="groupesel" +str(annsco.id)
                                if  request.POST.get('Enregistrer3') :                                                                       
                                    formsethtmltemp = GroupesEnseignantsFormSet(request.POST,instance=grfound,prefix=tempprefix,queryset=GroupesEnseignants.objects.filter(groupe__ue__periode__diplome__anneescolaire=annsco.id))
                                    saveFormset(request,formsethtmltemp);                                     
                                formsethtmltemp = GroupesEnseignantsFormSet(instance=grfound,prefix=tempprefix,queryset=GroupesEnseignants.objects.filter(groupe__ue__periode__diplome__anneescolaire=annsco.id))                                                        
                                listeformset1.append({'titre':annsco.nom ,'formset':formsethtmltemp})                   
                    listelistefs.append({'titre':"Inscriptions","listformset":listeformset1,'numtab':"3"}); 
                
                
                elif modele=="UE" :
                                                                            
                    GroupesEnseignantsFormSet = inlineformset_factory(UE, Groupe, fields=('nom',),form=GroupeForm )   
                    if  request.POST.get('Enregistrer2') :     
                        inlineformset1 = GroupesEnseignantsFormSet(request.POST,instance=grfound)
                        saveFormset(request,inlineformset1);
                    inlineformset1 = GroupesEnseignantsFormSet(instance=grfound)                                         
                    listefs.append({'titre':"Groupes","formset":inlineformset1,'numtab':"2"});  
                                                          
                    GroupesUEFormset = inlineformset_factory(Groupe, Inscription, fields=('eleve',),form=InscriptionForm)                                  
                    for grue in Groupe.objects.filter(ue=grfound) :
                                tempprefix="groupesue" +str(grue.id)
                                if  request.POST.get('Enregistrer3') :                                      
                                    tempGroupesUEFormset = GroupesUEFormset(request.POST,instance=grue,prefix=tempprefix)
                                    saveFormset(request,tempGroupesUEFormset);                                      
                                tempGroupesUEFormset = GroupesUEFormset(instance=grue,prefix=tempprefix)    
                                listeformset1.append({'titre':grue.nom ,'formset':tempGroupesUEFormset})
                    listelistefs.append({'titre':"Inscriptions","listformset":listeformset1,'numtab':"3"});             
                    
                    GroupesEnseignantsFormSet = inlineformset_factory(Groupe, GroupesEnseignants, fields=('enseignant',),form=GroupesEnseignantsForm)                                    
                    for grue in Groupe.objects.filter(ue=grfound) :
                                tempprefix="groupesenseignant" +str(grue.id)
                                if request.POST.get('Enregistrer4') :                                    
                                    tempGroupesEnseignantsFormSet = GroupesEnseignantsFormSet(request.POST,instance=grue,prefix=tempprefix)
                                    saveFormset(request,tempGroupesEnseignantsFormSet);                                   
                                tempGroupesEnseignantsFormSet = GroupesEnseignantsFormSet(instance=grue,prefix=tempprefix)                                                                    
                                listeformset2.append({'titre':grue.nom ,'formset':tempGroupesEnseignantsFormSet})
                    listelistefs.append({'titre':"Enseignants","listformset":listeformset2,'numtab':"4"}); 

                
            
           
            return render(request, 'bo/administratif.html',{                                                                                                                                                                        
                                                         "oid" : oid,"modele":modele,"modeleitem":modeleitem,"mode":mode,
                                                         "formmodele" : formmodele,"modeleliste" : modeleliste,
                                                         "formFilter":formFilter,  
                                                         "listefs":listefs,
                                                         "listelistefs":listelistefs                                                                                                                                                                                                                           
                                                         }) 
            
                                                                                                                 
                                                         #"formset3":inlineformset3,"formset2":inlineformset2,"formset1":inlineformset1, 
                                                         #"formsettitre1":formsettitre1,"formsettitre2":formsettitre2,"formsettitre3":formsettitre3, 
                                                         
                                                         #"listeformset1" :listeformset1,"listeformset2" :listeformset2,
                                                         #"listeformsettitre1":listeformsettitre1, "listeformsettitre2":listeformsettitre2 
                                                            
    #else:
    return deconnexion(request)

def init():
    
    from django.db.utils import OperationalError
    #from django.core.management import call_command
    #call_command('makemigrations')
    #call_command('migrate')
    
    try:
        User.objects.get(username='cerede')            
    except User.DoesNotExist:     
        User.objects.create_superuser(username='cerede', email='cerede@google.fr', password='kddcy8kx')
    #except OperationalError:
    #    User.objects.create_superuser(username='cerede', email='cerede@google.fr', password='kddcy8kx')
    
      
    # creation user admin1 
    u,created = User.objects.get_or_create(username='admin1', email='admin1@gooogle.fr')
    if created:
        u.set_password('kddcy8kx')
        u.save()
    
      #creation roles
    new_group_adm, created = Group.objects.get_or_create(name='administratif')
    if created :
        new_group_adm.user_set.add(u);
    new_group_ens, created = Group.objects.get_or_create(name='enseignant')
    new_group_ele, created = Group.objects.get_or_create(name='eleve')
    
    
    AnneeScolaire.objects.get_or_create(anneescolaire=2017,nom='2017-2018')
    AnneeScolaire.objects.get_or_create(anneescolaire=2018,nom='2018-2019')
   

def index(request): 
  
    init() 
   # deconnexion(request)      
    if request.POST.get('username') is not None:
    
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)    
            
            if user.groups.filter(name='eleve').exists() :
            #return render(request, 'frontoffice/connecte.html',{'user':user,"ug":user.groups.all()})
                return redirect('bo:eleve')
        
            if user.groups.filter(name='enseignant').exists() :
                return redirect('bo:enseignant')
            
            if user.groups.filter(name='administratif').exists() :
                return redirect('bo:administratif')
            
            # Redirect to a success page.
            #...
        else:
            return render(request, 'bo/index.html',{"error":"oui"})
        # Return an 'invalid login' error message.
      #...
    else :
        deconnexion(request)  
    #return HttpResponse("Hello, world. You're at the chauss index.")
     #  latest_question_list = Question.objects.order_by('-pub_date')[:6]
    #context = {'latest_question_list': latest_question_list}
    #context="toto";
        return  render(request, 'bo/index.html')

# Create your views here.
