from django.forms import ModelForm
from .models import *
from django import forms


from django.db.utils import OperationalError

#from django.forms import inlineformset_factory
from django.forms.models import *

class BasicForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)       
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
   
    def is_valid(self, *args, **kwargs):
        valid= super(ModelForm, self).is_valid()
        for visible in self.visible_fields():
            if visible.errors  :
                visible.field.widget.attrs['class'] = 'form-control is-invalid'
        return valid
        
class AdresseForm(BasicForm):
     class Meta:
        model = Adresse
        fields = '__all__'
     def nom():
         return 'Adresse'
# Create the form class.
class GroupeForm(BasicForm):
     class Meta:
        model = Groupe
        #fields = '__all__'
        fields = ['nom','ue']
      
class GroupeFormFilter (forms.Form):
    try :
         choicesens=[[0, 'Tous']] + [ (d.id, str(d)) for d in Enseignant.objects.all()]
         enseignantsfilter= forms.ChoiceField(choices=choicesens, label="Enseignant",                                      
                                         widget=forms.Select(attrs={'class': 'filter'}))
        
         choiceannsco=[[0, 'Tous']] + [ (d.id, str(d)) for d in AnneeScolaire.objects.all()]
         ue__diplome__anneescolairefilter= forms.ChoiceField(choices=choiceannsco, label="Année scolaire",                                      
                                         widget=forms.Select(attrs={'class': 'filter'}))  
         choicesdip=[[0, 'Tous']] + [ (d.id, str(d)) for d in Diplome.objects.all()]
         ue__periode__diplomefilter= forms.ChoiceField(choices=choicesdip, label="Diplome",                                      
                                         widget=forms.Select(attrs={'class': 'filter'}))
    except OperationalError: pass
        
    
                        

  
    
class EleveForm(BasicForm):
     class Meta:
        model = Eleve
        fields = '__all__'

class EleveFormFilter (forms.Form):
        
    try :
         choicesdip=[[0, 'Tous']] + [ (d.id, str(d)) for d in Diplome.objects.all()]
         choicesgroupes=[[0, 'Tous']] + [ (d.id, str(d)) for d in Groupe.objects.all()]
         filiere__diplomefilter= forms.ChoiceField(choices=choicesdip, label="Diplome",                                      
                                         widget=forms.Select(attrs={'class': 'filter'}))
         #groupefilter=forms.ChoiceField(choices=choicesgroupes, label="Groupe",                                      
         #                                widget=forms.Select(attrs={'class': 'filter'}))
         
    except OperationalError: pass    
    


class EnseignantForm(BasicForm):
     class Meta:
        model = Enseignant
        fields = '__all__' 
        

class PeriodeForm(BasicForm):
     class Meta:
        model = Enseignant
        fields = '__all__' 
                
class GroupesEnseignantsForm(BasicForm):
     class Meta:
        model = GroupesEnseignants
        fields = '__all__'           

class InscriptionForm(BasicForm):
     class Meta:
        model = Inscription
        fields = '__all__' 
                
     """def __init__(self, annee, *args, **kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)
        self.fields['groupe'].queryset = Groupe.objects.filter(ue__periode__diplome_anneescolaire=annee)   """      

class InscriptionFormSet2(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        my_arg = kwargs.pop("annee")
        super(InscriptionFormSet2, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['groupe'].queryset = Groupe.objects.filter(ue__periode__diplome_anneescolaire=annee)         

class UEForm(BasicForm):
     #creerGroupe=forms.BooleanField()
     class Meta:
        model = UE
        fields = '__all__' 
     
     '''
     def save(self, commit=True):
        # do something with self.cleaned_data['temp_id']
        uetemp=super(UEForm, self).save(commit=False)
        if Groupe.objects.filter(ue=uetemp).filter(nom='01').count()==0 :                  
            newgr=Groupe(nom='01',ue=uetemp);
            newgr.save();
        return super(UEForm, self).save(commit=True)
     '''
    

class UEFormFilter (forms.Form):
        
    try :
         choicedip=[[0, 'Tous']] + [ (d.id, str(d)) for d in Diplome.objects.all()]
         periode__diplomefilter= forms.ChoiceField(choices=choicedip, label="Diplome",                                      
                                         widget=forms.Select(attrs={'class': 'filter'}))
         choiceper=[[0, 'Tous']] + [ (d.id, str(d)) for d in Periode.objects.all()]
         periodefilter= forms.ChoiceField(choices=choiceper, label="Période",                                      
                                         widget=forms.Select(attrs={'class': 'filter'}))  
        
    except OperationalError: pass    
        
        
class DiplomeForm(BasicForm):
     class Meta:
        model = Diplome
        fields = '__all__' 

        
class DiplomeFormFilter (forms.Form):
    
    try :
        
         choiceannsco=[[0, 'Tous']] + [ (d.id, str(d)) for d in AnneeScolaire.objects.all()]
         anneescolairefilter= forms.ChoiceField(choices=choiceannsco, label="Année scolaire",                                      
                                         widget=forms.Select(attrs={'class': 'filter'})
                                         )
                                  
    
    except OperationalError: pass                                     
                          

class FiliereEleveForm(BasicForm):
     class Meta:
        model = FiliereEleve
        fields = '__all__'   
        
class FiliereForm(BasicForm):
     class Meta:
        model = Filiere
        fields = '__all__'

class SalleForm(BasicForm):
     class Meta:
        model = Salle
        fields = '__all__'

class PeriodeForm(BasicForm):
     class Meta:
        model = Periode
        fields = '__all__'
                
class CoursForm(BasicForm):
     class Meta:
        model = Cours
        fields = '__all__'      
########
#form set marche pas
########

#class BasicFormSet(BaseInlineFormSet):
#     def __init__(self, *args, **kwargs):
#        super(BaseInlineFormSet, self).__init__(*args, **kwargs)
#        for visible in self.form.fields():
#                        visible.field.widget.attrs['class'] = 'form-control'
            
        #for visible in self.visible_fields():
        #    visible.field.widget.attrs['class'] = 'form-control'
 
#class InscriptionsEleveFormset(BasicFormSet):
#     def __init__(self, *args, **kwargs):
#        super(BasicFormSet, self).__init__(*args, **kwargs)
        
    # def getform(i):
    #    formset=inlineformset_factory(Eleve, Inscription, fields=('groupe',))
    #    return formset(instance=i)           