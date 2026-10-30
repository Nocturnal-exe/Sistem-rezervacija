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
        Korisnik, on_delete=models.SET_NULL, related_name="termini",
        limit_choices_to={"uloga": "trener"}, null=True, blank=True,
    )
    datum = models.DateField()
    vrijeme_pocetka = models.TimeField()
    vrijeme_zavrsetka = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUSI, default="slobodan")

    def __str__(self):
        return f"{self.datum} {self.vrijeme_pocetka}"

    class Meta:
        verbose_name = "Termin"
        verbose_name_plural = "Termini"
        unique_together = ("trener", "datum", "vrijeme_pocetka")


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
    termin = models.ForeignKey(
        Termin, on_delete=models.CASCADE, related_name="rezervacije",
    )
    datum_kreiranja = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUSI, default="aktivna")

    def __str__(self):
        return f"{self.klijent.username} - {self.termin}"

    class Meta:
        verbose_name = "Rezervacija"
        verbose_name_plural = "Rezervacije"


class Post(models.Model):
    naslov = models.CharField(max_length=200)
    slika = models.ImageField(upload_to="blog/", blank=True)
    kratak_opis = models.CharField(max_length=300, blank=True)
    tekst = models.TextField()
    datum = models.DateField(auto_now_add=True)
    objavljen = models.BooleanField(default=True)

    def __str__(self):
        return self.naslov

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Postovi"
        ordering = ["-datum", "-id"]