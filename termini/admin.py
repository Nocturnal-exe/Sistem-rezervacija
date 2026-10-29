from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Korisnik, Termin, Rezervacija

admin.site.site_header = "NEON//GYM"
admin.site.site_title = "NEON//GYM"
admin.site.index_title = "Upravljanje sistemom"


@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Dodatno", {"fields": ("uloga", "broj_telefona", "specijalnost")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Dodatno", {"fields": ("first_name", "last_name", "uloga", "specijalnost")}),
    )
    list_display = ("username", "first_name", "last_name", "uloga", "specijalnost", "is_active")
    list_filter = ("uloga", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")


@admin.register(Termin)
class TerminAdmin(admin.ModelAdmin):
    list_display = ("datum", "vrijeme_pocetka", "vrijeme_zavrsetka", "trener", "status")
    list_filter = ("datum", "trener", "status")
    ordering = ("-datum", "vrijeme_pocetka")


@admin.register(Rezervacija)
class RezervacijaAdmin(admin.ModelAdmin):
    list_display = ("klijent", "termin_datum", "termin_sat", "trener", "status", "datum_kreiranja")
    list_filter = ("status", "termin__datum", "termin__trener")
    search_fields = ("klijent__username", "klijent__first_name", "klijent__last_name")
    ordering = ("-termin__datum", "-termin__vrijeme_pocetka")

    @admin.display(description="Datum", ordering="termin__datum")
    def termin_datum(self, obj):
        return obj.termin.datum

    @admin.display(description="Sat", ordering="termin__vrijeme_pocetka")
    def termin_sat(self, obj):
        return obj.termin.vrijeme_pocetka.strftime("%H:%M")

    @admin.display(description="Trener", ordering="termin__trener")
    def trener(self, obj):
        return obj.termin.trener


admin.site.unregister(Group)