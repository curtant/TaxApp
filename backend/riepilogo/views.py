from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from anagrafica.models import DatiAnagrafici
from .logic import get_or_create_summary_data

@login_required
def summary_api_view(request):
    """
    Endpoint API che restituisce i dati di riepilogo per il frontend.
    """
    try:
        anagrafica = request.user.dati_anagrafici
        data = get_or_create_summary_data(anagrafica)
        return JsonResponse(data)
    except DatiAnagrafici.DoesNotExist:
        return JsonResponse({'error': 'Profilo non trovato'}, status=404)
