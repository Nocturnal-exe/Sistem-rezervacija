from django.urls import path
from . import views

urlpatterns = [
    path("", views.pocetna, name="pocetna"),
]