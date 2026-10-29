import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Korisnik, Termin, Rezervacija

POCETNI_SAT = 8
ZADNJI_SAT = 20


class RegistracijaForma(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Korisnik
        fields = ("username", "first_name", "last_name", "email")


def parsiraj_datum(tekst):
    try:
        return datetime.date.fromisoformat(tekst)
    except (TypeError, ValueError):
        return None


def pocetna(request):
    danas = timezone.localdate()
    datum = parsiraj_datum(request.GET.get("datum")) or danas
    if datum < danas:
        datum = danas

    zauzeti = set(
        Termin.objects.filter(datum=datum, status="zauzet")
        .values_list("vrijeme_pocetka", flat=True)
    )
    sada = timezone.localtime().time()

    sati = []
    for h in range(POCETNI_SAT, ZADNJI_SAT):
        pocetak = datetime.time(h, 0)
        sati.append({
            "sat": h,
            "pocetak": pocetak,
            "kraj": datetime.time(h + 1, 0),
            "zauzet": pocetak in zauzeti,
            "prosao": datum == danas and pocetak <= sada,
        })

    return render(request, "termini/pocetna.html", {
        "datum": datum,
        "danas": danas,
        "sati": sati,
    })


def registracija(request):
    forma = RegistracijaForma(request.POST or None)
    if request.method == "POST" and forma.is_valid():
        korisnik = forma.save()
        login(request, korisnik)
        return redirect("pocetna")
    return render(request, "termini/auth.html", {
        "form": forma,
        "naslov": "REGISTRACIJA",
        "dugme": "Kreiraj nalog",
    })


@login_required
@require_POST
def rezervisi(request):
    datum = parsiraj_datum(request.POST.get("datum"))
    try:
        sat = int(request.POST.get("sat"))
    except (TypeError, ValueError):
        sat = None

    if datum is None or sat is None or not (POCETNI_SAT <= sat < ZADNJI_SAT):
        messages.error(request, "Neispravan termin.")
        return redirect("pocetna")

    nazad = f"/?datum={datum.isoformat()}"
    pocetak = datetime.time(sat, 0)
    kraj = datetime.time(sat + 1, 0)

    if datetime.datetime.combine(datum, pocetak) <= datetime.datetime.now():
        messages.error(request, "Taj termin je već prošao.")
        return redirect(nazad)

    try:
        with transaction.atomic():
            termin, napravljen = Termin.objects.get_or_create(
                datum=datum,
                vrijeme_pocetka=pocetak,
                defaults={"vrijeme_zavrsetka": kraj, "status": "zauzet"},
            )
            if not napravljen:
                if termin.status != "slobodan":
                    raise IntegrityError("zauzet")
                termin.status = "zauzet"
                termin.save()
            Rezervacija.objects.create(klijent=request.user, termin=termin)
    except IntegrityError:
        messages.error(request, "Termin je u međuvremenu zauzet.")
        return redirect(nazad)

    messages.success(request, "Termin je uspješno rezervisan.")
    return redirect(nazad)


@login_required
def moje_rezervacije(request):
    rezervacije = (
        Rezervacija.objects.filter(klijent=request.user)
        .select_related("termin")
        .order_by("-termin__datum", "-termin__vrijeme_pocetka")
    )
    sada = datetime.datetime.now()
    for r in rezervacije:
        pocetak = datetime.datetime.combine(r.termin.datum, r.termin.vrijeme_pocetka)
        r.moze_otkazati = r.status == "aktivna" and pocetak > sada
    return render(request, "termini/moje.html", {"rezervacije": rezervacije})


@login_required
@require_POST
def otkazi(request, rezervacija_id):
    rezervacija = get_object_or_404(
        Rezervacija, id=rezervacija_id, klijent=request.user
    )
    pocetak = datetime.datetime.combine(
        rezervacija.termin.datum, rezervacija.termin.vrijeme_pocetka
    )

    if rezervacija.status != "aktivna":
        messages.error(request, "Ova rezervacija se ne može otkazati.")
    elif pocetak <= datetime.datetime.now():
        messages.error(request, "Termin je već prošao.")
    else:
        with transaction.atomic():
            rezervacija.status = "otkazana"
            rezervacija.save()
            rezervacija.termin.status = "slobodan"
            rezervacija.termin.save()
        messages.success(request, "Rezervacija je otkazana.")

    return redirect("moje_rezervacije")