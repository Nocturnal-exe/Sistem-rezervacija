from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Korisnik, Termin, Rezervacija

admin.site.site_header = "Sistem za rezervaciju termina"
admin.site.site_title = "Rezervacije"
admin.site.index_title = "Upravljanje sistemom"


@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Dodatno", {"fields": ("uloga", "broj_telefona", "specijalnost")}),
    )


admin.site.register(Termin)
admin.site.register(Rezervacija)

admin.site.unregister(Group)