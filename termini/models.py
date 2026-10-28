from django.db import models
from django.contrib.auth.models import AbstractUser


class Korisnik(AbstractUser):
    ULOGE = [
        ("klijent", "Klijent"),
        ("trener", "Trener"),
        ("administrator", "Administrator"),
    ]
    uloga = models.CharField(max_length=20, choices=ULOGE, default="klijent")
    broj_telefona = models.CharField(max_length=20, blank=True)
    specijalnost = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Korisnik"
        verbose_name_plural = "Korisnici"


class Termin(models.Model):
    STATUSI = [("slobodan", "Slobodan"), ("zauzet", "Zauzet")]

    trener = models.ForeignKey(
        Korisnik, on_delete=models.CASCADE, related_name="termini",
        limit_choices_to={"uloga": "trener"},
    )
    datum = models.DateField()
    vrijeme_pocetka = models.TimeField()
    vrijeme_zavrsetka = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUSI, default="slobodan")

    def __str__(self):
        return f"{self.datum} {self.vrijeme_pocetka} ({self.trener.username})"

    class Meta:
        verbose_name = "Termin"
        verbose_name_plural = "Termini"


class Rezervacija(models.Model):
    STATUSI = [
        ("aktivna", "Aktivna"),
        ("otkazana", "Otkazana"),
        ("zavrsena", "Završena"),
        ("propustena", "Propuštena"),
    ]

    klijent = models.ForeignKey(
        Korisnik, on_delete=models.CASCADE, related_name="rezervacije",
        limit_choices_to={"uloga": "klijent"},
    )
    termin = models.OneToOneField(Termin, on_delete=models.CASCADE)
    datum_kreiranja = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUSI, default="aktivna")

    def __str__(self):
        return f"{self.klijent.username} - {self.termin}"

    class Meta:
        verbose_name = "Rezervacija"
        verbose_name_plural = "Rezervacije"