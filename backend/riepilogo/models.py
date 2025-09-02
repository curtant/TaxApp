from django.db import models
from anagrafica.models import DatiAnagrafici

class RiepilogoAnnuale(models.Model):
    """
    Conserva i dati aggregati calcolati per un anno fiscale specifico.
    """
    dati_anagrafici = models.ForeignKey(DatiAnagrafici, on_delete=models.CASCADE, related_name='riepiloghi')
    anno = models.PositiveIntegerField()
    reddito_lordo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reddito_netto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    imposte_versate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rimborso_ottenuto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    potenziale_rimborso = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dati_simulati = models.BooleanField(default=True)

    class Meta:
        unique_together = ('dati_anagrafici', 'anno')
        ordering = ['anno']

    def __str__(self):
        return f"Riepilogo per {self.dati_anagrafici.user.username} - Anno {self.anno}"
