from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import DatiAnagrafici, Residenza, Contatti, DomicilioFiscale
from .forms import DatiAnagraficiForm, ResidenzaForm, ContattiForm, DomicilioFiscaleForm

@login_required
def get_contribuente_form_html(request):
    # Usa get_or_create per garantire che i profili esistano sempre
    anagrafica, _ = DatiAnagrafici.objects.get_or_create(user=request.user)
    residenza, _ = Residenza.objects.get_or_create(dati_anagrafici=anagrafica)
    contatti, _ = Contatti.objects.get_or_create(dati_anagrafici=anagrafica)
    
    # Gestisce il primo domicilio o ne crea uno di default
    domicilio, created = DomicilioFiscale.objects.get_or_create(
        dati_anagrafici=anagrafica,
        defaults={'data_validita': '2025-01-01'}
    )

    if request.method == 'POST':
        # Istanzia i form con i dati inviati e le istanze esistenti
        form_anagrafici = DatiAnagraficiForm(request.POST, instance=anagrafica)
        form_residenza = ResidenzaForm(request.POST, instance=residenza)
        form_contatti = ContattiForm(request.POST, instance=contatti)
        form_domicilio = DomicilioFiscaleForm(request.POST, instance=domicilio)

        # Valida e salva tutti i form
        if all([form_anagrafici.is_valid(), form_residenza.is_valid(), form_contatti.is_valid(), form_domicilio.is_valid()]):
            form_anagrafici.save()
            form_residenza.save()
            form_contatti.save()
            form_domicilio.save()
    else:
        # Istanzia i form con i dati presenti nel database
        form_anagrafici = DatiAnagraficiForm(instance=anagrafica)
        form_residenza = ResidenzaForm(instance=residenza)
        form_contatti = ContattiForm(instance=contatti)
        form_domicilio = DomicilioFiscaleForm(instance=domicilio)

    context = {
        'form_anagrafici': form_anagrafici,
        'form_residenza': form_residenza,
        'form_contatti': form_contatti,
        'form_domicilio': form_domicilio,
    }
    
    html_form = render_to_string('anagrafica/_contribuente_form.html', context, request=request)
    return JsonResponse({'html_form': html_form})
