from django.urls import path
from .views import dashboard_view, register_view, login_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    # Potresti voler impostare il login come pagina principale
    path('', login_view, name='home'),
]
