from django.db import models

from django.db.models import Avg, Max, Min

from django.db.models import Q

from django.utils.dateparse import *

from django.core.exceptions import ValidationError

from simple_history.models import HistoricalRecords

import copy

from django.contrib.auth.models import User, Group, Permission


class BasicModel(models.Model):
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):                 
        if self._state.adding is True : self.changeReason = 'Ajout'
        if self._state.adding is False : self.changeReason = 'Mise à jour'
        return super(BasicModel, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        self.changeReason = 'Suppression'        
        return super(BasicModel, self).delete(*args, **kwargs)
        

# Create your models here.
class AnneeScolaire(models.Model):
  
    nom = models.CharField(max_length=200)
    anneescolaire = models.IntegerField(default=0) 
    #history = HistoricalRecords()   
    def __str__(self):
        return self.nom
    

class Diplome(BasicModel):  #Author
    nom = models.CharField(max_length=200)     
    anneescolaire = models.ForeignKey(AnneeScolaire, on_delete=models.PROTECT) 
    history = HistoricalRecords()  
    def __str__(self):
        return self.nom +" "+self.anneescolaire.nom
    def get_eleves(self):
        return FiliereEleve.objects.filter(filiere__diplome__id=self.id)
    def get_periodes(self):
        return Periode.objects.filter(diplome__id=self.id).all()
    def get_filieres(self):
        return Filiere.objects.filter(diplome__id=self.id).all()
    def nommodeledb(self):
        return 'diplome/'+str(self.id)
    def nommodele(self):
        return 'Diplome'
    


class Filiere(BasicModel):  #Author
    nom = models.CharField(max_length=200)     
    diplome = models.ForeignKey(Diplome, on_delete=models.PROTECT)
    history = HistoricalRecords()   
    def __str__(self):
        return self.diplome.nom +" "+self.nom+" ("+self.diplome.anneescolaire.nom+")"
    def nommodele(self):
        return 'filiere '+str(self.nom)
    def nommodeledb(self):
        return 'filiere/'+str(self.id)
    
    
 #BookFormSet = inlineformset_factory(Diplome, Periode, fields=('title',))
# author = Author.objects.get(name='Mike Royko')
#formset = BookFormSet(instance=author)

class Periode(BasicModel): #Book
  
    nom = models.CharField(max_length=200)
    diplome= models.ForeignKey(Diplome, on_delete=models.PROTECT) 
    datedebut=models.DateTimeField()
    datefin=models.DateTimeField()
    history = HistoricalRecords()  
    def __str__(self):
        return self.diplome.nom+" "+self.nom +" "+self.diplome.anneescolaire.nom
    def nommodele(self):
        return 'Période'
    

class Personne(BasicModel):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    email = models.CharField(max_length=200,null=True, blank=True)
    #history = HistoricalRecords()
    
class Adresse(BasicModel):
    
    pays= models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    adresse1= models.CharField(max_length=200) 
    adresse2= models.CharField(max_length=200,null=True, blank=True) 
    adresse3= models.CharField(max_length=200,null=True, blank=True)   
    personne=models.ForeignKey(Personne,on_delete=models.CASCADE)
    history = HistoricalRecords()
    
    def nommodele(self):
        return 'Adresse'
    
     
class Eleve(Personne):
    filiere = models.ManyToManyField(Filiere, through="FiliereEleve")
    history = HistoricalRecords()
    def __str__(self):
        lastannscodip=FiliereEleve.objects.filter(eleve__id=self.id ).all().aggregate(Max('filiere__diplome__anneescolaire'))
        lastdip=FiliereEleve.objects.filter(eleve__id=self.id ).filter(filiere__diplome__anneescolaire__id=lastannscodip['filiere__diplome__anneescolaire__max']).first()
        if lastdip: return self.nom+" "+self.prenom +" ("+ str(lastdip.filiere.diplome.nom)+" "+lastdip.filiere.diplome.anneescolaire.nom+")"
        else : return " Aucune formation "
    def get_groupes(self):
        res="";
        for p in Inscription.objects.filter(eleve__id=self.id).all() :
            res=res+p.groupe.ue.nom +" ("+p.groupe.nom+"), "
        return res  
    def get_diplomes(self):
        res=""
        for d in FiliereEleve.objects.filter(eleve__id=self.id ).all():  
             res=res+"---"+d.filiere.diplome.nom +"  "+d.filiere.diplome.anneescolaire.nom
        return res   
    def nommodeledb(self):
        return 'eleve/'+str(self.id)
    def nommodele(self):
        return 'Eleve'
    def get_last_diplome(self):
        #lastdip=DiplomeEleve.objects.filter(eleve__id=self.id ).all().aggregate(Max('diplome__anneescolaire'))
       #
       #
       #
        lastannscodip=FiliereEleve.objects.filter(eleve__id=self.id ).all().aggregate(Max('filiere__diplome__anneescolaire'))
        lastdip=FiliereEleve.objects.filter(eleve__id=self.id ).filter(filiere__diplome__anneescolaire__id=lastannscodip['filiere__diplome__anneescolaire__max']).first()
        if lastdip: return str(lastdip.filiere.diplome.nom)+" "+lastdip.filiere.diplome.anneescolaire.nom
        else : return " Aucune formation "
    
    def save(self, *args, **kwargs):
    # Check how the current values differ from ._loaded_values. For example,
    # prevent changing the creator_id of the model. (This example doesn't
    # support cases where 'creator_id' is deferred).
        if self._state.adding :
            nbinscr=Eleve.objects.filter(nom=self.nom,prenom=self.prenom).count()
            if nbinscr>=1 : 
                raise ValueError("Cet élève existe déjà !")
            else : 
                super().save(*args, **kwargs)
                u, created  = User.objects.get_or_create(username=self.nom, email=self.email)
                if created:
                    u.set_password(self.nom)
                    u.save()  
                    new_group_ele,created= Group.objects.get_or_create(name='eleve')
                    new_group_ele.user_set.add(u)
        else :
            super().save(*args, **kwargs)       

class FiliereEleve(BasicModel):  
    filiere=models.ForeignKey(Filiere,on_delete=models.CASCADE)
    eleve=models.ForeignKey(Eleve,on_delete=models.CASCADE)
    history = HistoricalRecords()
    def nommodele(self):
        return 'filiere '+self.filiere.nom
    def nommodeledb(self):
        return 'eleve/'+str(self.eleve.id)
    def nommodeledb2(self):
        return 'filiere/'+str(self.filiere.id)

        
class Enseignant(Personne):
    history = HistoricalRecords()
    def __str__(self):
        return self.nom
    def get_groupes(self):
        res="";
        for p in Groupe.objects.filter(enseignants__id=self.id).all() :
            res=res+p.ue.nom +" ("+p.nom+"), "
        return res
    def nommodeledb(self):
        return 'enseignant/'+str(self.id)
    def nommodele(self):
        return 'Enseignant'

class UE(BasicModel):  
    nom = models.CharField(max_length=200)     
    descriptif = models.CharField(max_length=200,null=True, blank=True)     
    periode = models.ForeignKey(Periode, on_delete=models.PROTECT) 
    filieres= models.ManyToManyField(Filiere,through="UEFilieres")
    history = HistoricalRecords()
    def __str__(self):
        return self.nom+" ("+self.periode.diplome.nom+" "+self.periode.diplome.anneescolaire.nom+")"
    def get_groupes(self):
        res="";
        for p in Groupe.objects.filter(ue__id=self.id).all() :
            res=res+", "+ p.nom
        return res
    def nommodeledb(self):
        return 'UE/'+str(self.id)
    def nommodele(self):
        return 'UE'

class UEFilieres(models.Model):  
    ue=models.ForeignKey(UE,on_delete=models.PROTECT)
    filiere=models.ForeignKey(Filiere,on_delete=models.PROTECT)
    #history = HistoricalRecords()
    

class Groupe(BasicModel):  
    nom = models.CharField(max_length=200)     
    ue = models.ForeignKey(UE, on_delete=models.PROTECT) 
    enseignants= models.ManyToManyField(Enseignant, through="GroupesEnseignants")
    history = HistoricalRecords()
    def __str__(self):
        return self.ue.nom +" "+self.nom+" ("+self.ue.periode.diplome.nom+" "+ self.ue.periode.diplome.anneescolaire.nom+")"
    def get_nb_eleves(self):
        return Inscription.objects.filter(groupe__id=self.id).count()
    def nommodeledb(self):
        return 'groupe/'+str(self.id)
    
    
class GroupesEnseignants(models.Model):  
    groupe=models.ForeignKey(Groupe,on_delete=models.PROTECT)
    enseignant=models.ForeignKey(Enseignant,on_delete=models.PROTECT)
    #history = HistoricalRecords()
    def nommodele(self):
        return 'groupe'
    def nommodeledb(self):
        return 'groupe/'+str(self.groupe.id)
    def nommodeledb2(self):
        return 'enseignant/'+str(self.enseignant.id)
    def __str__(self): 
         return self.groupe.nom+" "+str(self.groupe.ue)

class Inscription(BasicModel):  
    groupe = models.ForeignKey(Groupe, on_delete=models.PROTECT) 
    eleve = models.ForeignKey(Eleve, on_delete=models.PROTECT) 
    history = HistoricalRecords()
   # enseignant= models.ForeignKey(Enseignant, on_delete=models.PROTECT) 
    def __str__(self):
        return self.groupe.ue.nom+" "+self.groupe.nom
    def nommodele(self):
        return 'inscription '+str(self.groupe.ue.periode.diplome.anneescolaire)
    def nommodeledb(self):
        return 'eleve/'+str(self.eleve.id)
    def nommodeledb2(self):
        return 'groupe/'+str(self.groupe.id)
    def save(self, *args, **kwargs):
    # Check how the current values differ from ._loaded_values. For example,
    # prevent changing the creator_id of the model. (This example doesn't
    # support cases where 'creator_id' is deferred).
        nbinscr=Inscription.objects.filter(groupe=self.groupe,eleve=self.eleve).count()
        if nbinscr>=1 : raise ValueError("L'élève est déjà inscrit au groupe "+str(self.groupe)+" !")
        else : super().save(*args, **kwargs)
    

class Salle(BasicModel):  
    nom = models.CharField(max_length=200)
    batiment = models.CharField(max_length=200,null=True, blank=True)     
    capacite = models.IntegerField(default=0)
    history = HistoricalRecords()     
    def __str__(self):
        return self.nom

class Cours(models.Model):  
    groupes = models.ManyToManyField(Groupe, through="CoursGroupes")
    salles= models.ManyToManyField(Salle,through="CoursSalles")
    datedebut=models.DateTimeField()
    datefin=models.DateTimeField()
    #duplication=models.BooleanField()
    #history = HistoricalRecords()
    def __str__(self): 
        str="";  
        str=str+" groupes :"     
        for eg in self.groupes.all() :
            str=str+eg.ue.nom +" "+eg.nom
            str=str+" "
        str=str+" salle :"
        for es in self.salles.all() :
            str=str+es.nom
        if self.datedebut.strftime('%d-%m-%Y') != self.datefin.strftime('%d-%m-%Y') :
            str=str+" "+self.datedebut.strftime('%d-%m-%Y %H:%M')+"\r\n "+self.datefin.strftime('%d-%m-%Y %H:%M')
        else : 
            str=str+" "+self.datedebut.strftime('%d-%m-%Y')+"\r\n "+self.datefin.strftime('%H:%M')+"-"+self.datefin.strftime('%H:%M')
        return str
               
    def verifResaSalle(self):
        datedebutcours=self.datedebut
        datefincours=self.datefin
        pb=False
        messerror='';
        for ts in self.salles.all():
            for c in CoursSalles.objects.filter( Q(salle__id=ts.id)).all() :             
              if self.id != c.cours.id :                     
                        if ((c.cours.datedebut>=datedebutcours and c.cours.datedebut<datefincours) or
                            (c.cours.datefin <=datefincours and c.cours.datefin>datedebutcours ) or 
                            (c.cours.datedebut<=datedebutcours and c.cours.datefin>=datefincours)) :
                                pb=True
                                #messerror=" chevauchement :"+str(c.cours)
                                messerror=" chevauchement "+str(c.cours)
        if pb is True :        
            raise ValueError(messerror) 
        
    def save(self, *args, **kwargs):
        super(Cours, self).save(*args, **kwargs)
        self.verifResaSalle()
    
    #def dnd(self, *args, **kwargs):   
        
        
    def dupliquer (self, *args, **kwargs):   
        #if self.duplication :
        datefinperiode=self.groupes.first().ue.periode.datefin                  
        i=7
        courtemp=Cours.objects.get(id=self.id)  
        while courtemp.datedebut<datefinperiode : 
            courtemp=Cours.objects.get(id=self.id)             
            courtemp.id=None      
            courtemp.datedebut=courtemp.datedebut+datetime.timedelta(days=i)
            courtemp.datefin=courtemp.datefin+datetime.timedelta(days=i) 
            courtemp.save()
            for sa in self.salles.all() :
                cs = CoursSalles(cours=courtemp,salle=sa)
                cs.save()
            for gr in self.groupes.all() :
                cg = CoursGroupes(cours=courtemp,groupe=gr)
                cg.save()            
            i=i+7
            
            try :
                courtemp.verifResaSalle() 
            except Exception as e :
                courtemp.delete() 
                return str(e) 
                
                #break            
           

             
             
            
       

#
class CoursGroupes(models.Model):  
    cours=models.ForeignKey(Cours,on_delete=models.CASCADE)
    groupe=models.ForeignKey(Groupe,on_delete=models.CASCADE)
    #history = HistoricalRecords()
    
class CoursSalles(models.Model):  
    cours=models.ForeignKey(Cours,on_delete=models.CASCADE)
    salle=models.ForeignKey(Salle,on_delete=models.CASCADE)
    
class Devoir(models.Model):  
    EXO = 'EXO'
    ORA = 'ORA'
    TYPE_DEVOIR = ((EXO, 'Exercices'),(ORA, 'Oral'),)
    
    cours=models.ForeignKey(Cours,on_delete=models.CASCADE,null=True, blank=True)
    type= models.CharField(max_length=3,choices=TYPE_DEVOIR,default=EXO,)
 
class Absence(models.Model):  
    JUSTI = 'JUSTI'
    PASJU = 'PASJU'
    TYPE_ABSENCE = ((JUSTI, 'Justifié'),(PASJU, 'Pas justifié'),)
    
    cours=models.ForeignKey(Cours,on_delete=models.CASCADE)
    eleve=models.ForeignKey(Eleve,on_delete=models.CASCADE)
    type= models.CharField(max_length=5,choices=TYPE_ABSENCE,default=PASJU,)  
    #history = HistoricalRecords()