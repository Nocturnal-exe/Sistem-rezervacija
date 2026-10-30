from django.shortcuts import render

PAKETI = [
    {
        "naziv": "NEON BASIC",
        "opis": "Korištenje teretane",
        "cijene": [("1 mjesec", "XX KM"), ("15 dana", "XX KM"), ("Polugodišnja", "XX KM"), ("Godišnja", "XX KM")],
    },
    {
        "naziv": "NEON & SAUNA",
        "opis": "Korištenje teretane i saune",
        "cijene": [("1 mjesec", "XX KM"), ("15 dana", "XX KM"), ("Polugodišnja", "XX KM"), ("Godišnja", "XX KM")],
    },
    {
        "naziv": "NEON VIP",
        "opis": "Teretana, sauna, voda i peškir uz svaki trening",
        "cijene": [("1 mjesec", "XX KM"), ("Polugodišnja", "XX KM"), ("Godišnja", "XX KM")],
    },
    {
        "naziv": "NEON PRO",
        "opis": "Sve iz VIP paketa, protein i personalni trener",
        "cijene": [("1 mjesec", "XX KM"), ("Polugodišnja", "XX KM"), ("Godišnja", "XX KM")],
    },
    {
        "naziv": "STUDENT",
        "opis": "Teretana za studente i srednjoškolce, do 16h",
        "cijene": [("1 mjesec", "XX KM")],
    },
]


def cjenovnik(request):
    return render(request, "termini/cjenovnik.html", {
        "paketi": PAKETI,
        "podnaslov": "CJENOVNIK",
    })