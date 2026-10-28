from django.shortcuts import render
from django.utils import timezone
from .models import Termin


def pocetna(request):
    termini = Termin.objects.filter(
        status="slobodan",
        datum__gte=timezone.localdate(),
    ).order_by("datum", "vrijeme_pocetka")
    return render(request, "termini/pocetna.html", {"termini": termini})