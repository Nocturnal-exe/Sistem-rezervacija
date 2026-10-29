import datetime
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Termin, Rezervacija
from .views import POCETNI_SAT, ZADNJI_SAT, parsiraj_datum, procitaj_sat


def samo_trener(view):
    @wraps(view)
    @login_required
    def omotac(request, *args, **kwargs):
        if request.user.uloga != "trener":
            messages.error(request, "Ova stranica je samo za trenere.")
            return redirect("pocetna")
        return view(request, *args, **kwargs)
    return omotac


def nazad_na(datum):
    return f"{reverse('trener_panel')}?datum={datum.isoformat()}"


@samo_trener
def trener_panel(request):
    danas = timezone.localdate()
    sada = datetime.datetime.now()
    datum = parsiraj_datum(request.GET.get("datum")) or danas
    if datum < danas:
        datum = danas

    aktivne = (
        Rezervacija.objects.filter(
            termin__trener=request.user,
            status="aktivna",
            termin__datum__gte=danas,
        )
        .select_related("klijent", "termin")
        .order_by("termin__datum", "termin__vrijeme_pocetka")
    )
    rezervacije = [
        r for r in aktivne
        if datetime.datetime.combine(r.termin.datum, r.termin.vrijeme_pocetka) > sada
    ]

    termini = {
        t.vrijeme_pocetka: t
        for t in Termin.objects.filter(trener=request.user, datum=datum)
    }
    rezervisani = set(
        Rezervacija.objects.filter(
            termin__trener=request.user, termin__datum=datum, status="aktivna"
        ).values_list("termin__vrijeme_pocetka", flat=True)
    )

    sati = []
    for h in range(POCETNI_SAT, ZADNJI_SAT):
        pocetak = datetime.time(h, 0)
        termin = termini.get(pocetak)
        zauzet = termin is not None and termin.status == "zauzet"
        rezervisan = pocetak in rezervisani
        sati.append({
            "sat": h,
            "pocetak": pocetak,
            "kraj": datetime.time(h + 1, 0),
            "rezervisan": rezervisan,
            "blokiran": zauzet and not rezervisan,
            "prosao": datum == danas and pocetak <= sada.time(),
        })

    return render(request, "termini/trener.html", {
        "datum": datum,
        "danas": danas,
        "sati": sati,
        "rezervacije": rezervacije,
    })


@samo_trener
@require_POST
def blokiraj(request):
    datum = parsiraj_datum(request.POST.get("datum"))
    sat = procitaj_sat(request.POST.get("sat"))
    if datum is None or sat is None:
        messages.error(request, "Neispravan termin.")
        return redirect("trener_panel")

    with transaction.atomic():
        termin, napravljen = Termin.objects.get_or_create(
            trener=request.user,
            datum=datum,
            vrijeme_pocetka=datetime.time(sat, 0),
            defaults={
                "vrijeme_zavrsetka": datetime.time(sat + 1, 0),
                "status": "zauzet",
            },
        )
        if not napravljen:
            if termin.status != "slobodan":
                messages.error(request, "Taj sat je već zauzet.")
                return redirect(nazad_na(datum))
            termin.status = "zauzet"
            termin.save()

    messages.success(request, "Sat je blokiran.")
    return redirect(nazad_na(datum))


@samo_trener
@require_POST
def odblokiraj(request):
    datum = parsiraj_datum(request.POST.get("datum"))
    sat = procitaj_sat(request.POST.get("sat"))
    if datum is None or sat is None:
        messages.error(request, "Neispravan termin.")
        return redirect("trener_panel")

    termin = Termin.objects.filter(
        trener=request.user,
        datum=datum,
        vrijeme_pocetka=datetime.time(sat, 0),
        status="zauzet",
    ).first()

    if termin is None:
        messages.error(request, "Taj sat nije blokiran.")
    elif termin.rezervacije.filter(status="aktivna").exists():
        messages.error(request, "Na tom satu postoji rezervacija klijenta.")
    else:
        termin.status = "slobodan"
        termin.save()
        messages.success(request, "Sat je ponovo slobodan.")

    return redirect(nazad_na(datum))