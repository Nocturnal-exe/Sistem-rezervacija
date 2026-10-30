import datetime

from django.db.models import Q

from .models import Rezervacija


def zavrsi_prosle():
    sada = datetime.datetime.now()
    Rezervacija.objects.filter(status="aktivna").filter(
        Q(termin__datum__lt=sada.date())
        | Q(termin__datum=sada.date(), termin__vrijeme_zavrsetka__lte=sada.time())
    ).update(status="zavrsena")


def broj_aktivnih(klijent):
    zavrsi_prosle()
    return Rezervacija.objects.filter(klijent=klijent, status="aktivna").count()