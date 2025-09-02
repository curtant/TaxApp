from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. Modello Principale: Dati Anagrafici
class DatiAnagrafici(models.Model):
    """
    Contiene i dati anagrafici essenziali del contribuente.
    Questo è il modello centrale collegato all'utente.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dati_anagrafici')
    codice_fiscale = models.CharField(max_length=16, unique=True, blank=True, null=True)
    cognome = models.CharField(max_length=50, blank=True)
    nome = models.CharField(max_length=50, blank=True)
    
    SESSO_CHOICES = [
        ('M', 'Maschio'),
        ('F', 'Femmina'),
    ]
    sesso = models.CharField(max_length=1, choices=SESSO_CHOICES, blank=True)
    data_nascita = models.DateField(null=True, blank=True)
    provincia_nascita = models.CharField(max_length=2, blank=True)
    comune_nascita = models.CharField(max_length=100, blank=True)
    fiscalmente_a_carico = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cognome} {self.nome} ({self.codice_fiscale})"

# 2. Modello per la Residenza
class Residenza(models.Model):
    """
    Modello dedicato esclusivamente ai dati di residenza,
    collegato ai dati anagrafici.
    """
    dati_anagrafici = models.OneToOneField(DatiAnagrafici, on_delete=models.CASCADE, related_name="residenza")
    provincia_residenza = models.CharField(max_length=2, blank=True, null=True)
    comune_residenza = models.CharField(max_length=100, blank=True, null=True)
    codice_catastale_residenza = models.CharField(max_length=4, blank=True, null=True)
    cap = models.CharField(max_length=5, blank=True, null=True)
    tipologia_via = models.CharField(max_length=20, blank=True, null=True)
    indirizzo = models.CharField(max_length=200, blank=True, null=True)
    numero_civico = models.CharField(max_length=10, blank=True, null=True)
    frazione = models.CharField(max_length=50, blank=True, null=True)
    data_variazione_residenza = models.DateField(blank=True, null=True)
    prima_dichiarazione = models.BooleanField(default=False)

    def __str__(self):
        return f"Residenza di {self.dati_anagrafici}"

# 3. Modello per i Contatti
class Contatti(models.Model):
    """
    Modello per i dati di contatto.
    """
    dati_anagrafici = models.OneToOneField(DatiAnagrafici, on_delete=models.CASCADE, related_name="contatti")
    telefono_cellulare = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Contatti di {self.dati_anagrafici}"

# 4. Modello per il Domicilio Fiscale
class DomicilioFiscale(models.Model):
    """
    Modello per i domicili fiscali, collegato ai dati anagrafici.
    Un contribuente può avere più domicili fiscali nel tempo.
    """
    dati_anagrafici = models.ForeignKey(DatiAnagrafici, on_delete=models.CASCADE, related_name="domicili_fiscali")
    provincia = models.CharField(max_length=2)
    comune = models.CharField(max_length=100)
    codice_catastale = models.CharField(max_length=4)
    casi_particolari_regionali = models.CharField(max_length=100, blank=True, null=True)
    fusione_comune = models.CharField(max_length=100, blank=True, null=True)
    data_validita = models.DateField()

    def __str__(self):
        return f"{self.comune} ({self.data_validita})"

# Segnale aggiornato per creare tutti i profili collegati quando un nuovo User viene registrato
@receiver(post_save, sender=User)
def create_full_profile(sender, instance, created, **kwargs):
    if created:
        anagrafica = DatiAnagrafici.objects.create(user=instance)
        Residenza.objects.create(dati_anagrafici=anagrafica)
        Contatti.objects.create(dati_anagrafici=anagrafica)
