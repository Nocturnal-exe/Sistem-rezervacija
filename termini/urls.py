from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.pocetna, name="pocetna"),
    path("izbor-trenera/", views.izbor_trenera, name="izbor_trenera"),
    path("registracija/", views.registracija, name="registracija"),
    path(
        "prijava/",
        auth_views.LoginView.as_view(
            template_name="termini/auth.html",
            extra_context={"naslov": "PRIJAVA", "dugme": "Uđi u sistem"},
        ),
        name="prijava",
    ),
    path("odjava/", auth_views.LogoutView.as_view(), name="odjava"),
    path("rezervisi/", views.rezervisi, name="rezervisi"),
    path("moje-rezervacije/", views.moje_rezervacije, name="moje_rezervacije"),
    path("otkazi/<int:rezervacija_id>/", views.otkazi, name="otkazi"),
]