from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ModelForm
from django.shortcuts import render, redirect

from .models import Korisnik


class ProfilForma(ModelForm):
    class Meta:
        model = Korisnik
        fields = ("first_name", "last_name", "email", "broj_telefona")
        labels = {
            "first_name": "Ime",
            "last_name": "Prezime",
            "email": "Email",
            "broj_telefona": "Broj telefona",
        }


@login_required
def profil(request):
    forma = ProfilForma(instance=request.user)
    lozinka = PasswordChangeForm(request.user)

    if request.method == "POST":
        if "spremi_profil" in request.POST:
            forma = ProfilForma(request.POST, instance=request.user)
            if forma.is_valid():
                forma.save()
                messages.success(request, "Profil je sačuvan.")
                return redirect("profil")
        elif "promijeni_lozinku" in request.POST:
            lozinka = PasswordChangeForm(request.user, request.POST)
            if lozinka.is_valid():
                korisnik = lozinka.save()
                update_session_auth_hash(request, korisnik)
                messages.success(request, "Lozinka je promijenjena.")
                return redirect("profil")

    return render(request, "termini/profil.html", {
        "forma": forma,
        "lozinka": lozinka,
        "podnaslov": "PROFIL",
    })