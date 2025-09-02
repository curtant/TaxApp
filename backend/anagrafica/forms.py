from django import forms
from django.db import models
from .models import DatiAnagrafici, Residenza, Contatti, DomicilioFiscale

def get_default_widgets(model):
    """
    Funzione helper per applicare 'form-control' solo ai campi di testo concreti,
    ignorando i campi di relazione.
    """
    widgets = {}
    for field in model._meta.get_fields():
        # Controlliamo che il campo sia concreto e del tipo giusto
        if field.concrete and isinstance(field, (models.CharField, models.EmailField, models.TextField)):
            widgets[field.name] = forms.TextInput(attrs={'class': 'form-control'})
    return widgets

class DatiAnagraficiForm(forms.ModelForm):
    class Meta:
        model = DatiAnagrafici
        exclude = ['user']
        widgets = {
            **get_default_widgets(DatiAnagrafici), # Applica stile di default
            'data_nascita': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sesso': forms.Select(attrs={'class': 'form-select'}),
            'fiscalmente_a_carico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ResidenzaForm(forms.ModelForm):
    class Meta:
        model = Residenza
        exclude = ['dati_anagrafici']
        widgets = {
            **get_default_widgets(Residenza), # Applica stile di default
            'data_variazione_residenza': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'prima_dichiarazione': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ContattiForm(forms.ModelForm):
    class Meta:
        model = Contatti
        exclude = ['dati_anagrafici']
        widgets = get_default_widgets(Contatti) # Applica stile di default

class DomicilioFiscaleForm(forms.ModelForm):
    class Meta:
        model = DomicilioFiscale
        exclude = ['dati_anagrafici']
        widgets = {
            **get_default_widgets(DomicilioFiscale), # Applica stile di default
            'data_validita': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
