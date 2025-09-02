from django.urls import path
from .views import summary_api_view

urlpatterns = [
    path('data/', summary_api_view, name='summary_api_data'),
]
