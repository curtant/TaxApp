from django.urls import path
from .views import get_contribuente_form_html

app_name = 'anagrafica'

urlpatterns = [
    path('form/', get_contribuente_form_html, name='get_contribuente_form'),
]
