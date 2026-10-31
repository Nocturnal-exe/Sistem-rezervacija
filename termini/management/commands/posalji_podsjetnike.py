import datetime
import time

from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from termini.models import Rezervacija

MINUTA_PRIJE = 15


def posalji():
    sada = datetime.datetime.now()
    granica = sada + datetime.timedelta(minutes=MINUTA_PRIJE)
    poslano = 0

    rezervacije = Rezervacija.objects.filter(
        status="aktivna", podsjetnik_poslan=False, termin__datum=sada.date()
    ).select_related("klijent", "termin", "termin__trener")

    for r in rezervacije:
        pocetak = datetime.datetime.combine(r.termin.datum, r.termin.vrijeme_pocetka)
        if not (sada < pocetak <= granica):
            continue
        if not r.klijent.email:
            continue

        trener = ""
        if r.termin.trener:
            trener = f"Trener: {r.termin.trener.get_full_name() or r.termin.trener.username}\n"

        send_mail(
            subject="NEON//GYM podsjetnik na trening",
            message=(
                f"Zdravo {r.klijent.first_name or r.klijent.username},\n\n"
                f"Tvoj trening počinje u {r.termin.vrijeme_pocetka.strftime('%H:%M')} "
                f"({r.termin.datum.strftime('%d.%m.%Y')}).\n"
                f"{trener}\nVidimo se!\nNEON//GYM"
            ),
            from_email=None,
            recipient_list=[r.klijent.email],
        )
        r.podsjetnik_poslan = True
        r.save(update_fields=["podsjetnik_poslan"])
        poslano += 1
    return poslano


class Command(BaseCommand):
    help = "Salje podsjetnik 15 minuta prije treninga. Sa --petlja radi stalno svake minute."

    def add_arguments(self, parser):
        parser.add_argument("--petlja", action="store_true")

    def handle(self, *args, **opcije):
        if not opcije["petlja"]:
            self.stdout.write(f"Poslano: {posalji()}")
            return
                self.stdout.write("Podsjetnici rade. Prekini sa Ctrl+C.")
        try:
            while True:
                n = posalji()
                if n:
                    self.stdout.write(f"Poslano: {n}")
                time.sleep(60)
        except KeyboardInterrupt:
            self.stdout.write("Podsjetnici zaustavljeni.")