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


def procitaj_sat(tekst):
    try:
        sat = int(tekst)
    except (TypeError, ValueError):
        return None
    if POCETNI_SAT <= sat < ZADNJI_SAT:
        return sat
    return None


def trener_zauzet(trener, datum, pocetak):
    return Termin.objects.filter(
        trener=trener, datum=datum, vrijeme_pocetka=pocetak, status="zauzet"
    ).exists()


def pocetna(request):
    danas = timezone.localdate()
    datum = parsiraj_datum(request.GET.get("datum")) or danas
    if datum < danas:
        datum = danas

    broj_trenera = Korisnik.objects.filter(uloga="trener", is_active=True).count()
    zauzeto_po_satu = {}
    for t in Termin.objects.filter(datum=datum, status="zauzet", trener__isnull=False):
        zauzeto_po_satu[t.vrijeme_pocetka] = zauzeto_po_satu.get(t.vrijeme_pocetka, 0) + 1

    sada = timezone.localtime().time()
    sati = []
    for h in range(POCETNI_SAT, ZADNJI_SAT):
        pocetak = datetime.time(h, 0)
        sati.append({
            "sat": h,
            "pocetak": pocetak,
            "kraj": datetime.time(h + 1, 0),
            "zauzet": broj_trenera == 0 or zauzeto_po_satu.get(pocetak, 0) >= broj_trenera,
            "prosao": datum == danas and pocetak <= sada,
        })

    return render(request, "termini/pocetna.html", {
        "datum": datum,
        "danas": danas,
        "sati": sati,
    })


@login_required
def izbor_trenera(request):
    datum = parsiraj_datum(request.GET.get("datum"))
    sat = procitaj_sat(request.GET.get("sat"))
    if datum is None or sat is None:
        messages.error(request, "Neispravan termin.")
        return redirect("pocetna")

    pocetak = datetime.time(sat, 0)
    if datetime.datetime.combine(datum, pocetak) <= datetime.datetime.now():
        messages.error(request, "Taj termin je već prošao.")
        return redirect("pocetna")

    treneri = []
    for trener in Korisnik.objects.filter(uloga="trener", is_active=True).order_by("first_name", "username"):
        treneri.append({
            "id": trener.id,
            "ime": trener.get_full_name() or trener.username,
            "specijalnost": trener.specijalnost,
            "zauzet": trener_zauzet(trener, datum, pocetak),
        })

    return render(request, "termini/izbor_trenera.html", {
        "datum": datum,
        "sat": sat,
        "pocetak": pocetak,
        "kraj": datetime.time(sat + 1, 0),
        "treneri": treneri,
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
    sat = procitaj_sat(request.POST.get("sat"))
    trener = Korisnik.objects.filter(
        id=request.POST.get("trener") or 0, uloga="trener", is_active=True
    ).first()

    if datum is None or sat is None or trener is None:
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
                trener=trener,
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
        messages.error(request, "Taj trener je u međuvremenu zauzet.")
        return redirect(nazad)

    messages.success(request, "Termin je uspješno rezervisan.")
    return redirect(nazad)


@login_required
def moje_rezervacije(request):
    rezervacije = (
        Rezervacija.objects.filter(klijent=request.user)
        .select_related("termin", "termin__trener")
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