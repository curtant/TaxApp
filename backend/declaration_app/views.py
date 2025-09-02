from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CustomUserCreationForm, LoginForm
from anagrafica.models import DatiAnagrafici
import json

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            try:
                anagrafica = user.dati_anagrafici
                anagrafica.nome = "Mario"
                anagrafica.cognome = "Rossi"
                anagrafica.codice_fiscale = "RSSMRA80A01H501A" # Esempio
                anagrafica.save()
            except (AttributeError, DatiAnagrafici.DoesNotExist):
                pass

            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error_message = "Credenziali non valide."
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form, 'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    """
    Renderizza la dashboard principale.
    Passa i dati dell'utente e l'URL di logout al template per Vue.
    """
    try:
        anagrafica = request.user.dati_anagrafici
        first_name = anagrafica.nome
        last_name = anagrafica.cognome
    except DatiAnagrafici.DoesNotExist:
        first_name = request.user.username
        last_name = ""

    vue_data = {
        "userInfo": {
            "firstName": first_name,
            "lastName": last_name,
        },
        "logoutUrl": reverse('logout')
    }

    context = {
        'vue_data_json': json.dumps(vue_data)
    }
    return render(request, 'dashboard.html', context)
