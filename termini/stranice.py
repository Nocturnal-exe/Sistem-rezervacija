from django.shortcuts import render

KONTAKT = {
    "telefon": "+387 XX XXX XXX",
    "email": "email@primjer.ba",
    "adresa": "Ulica i broj, Grad",
    "radno_vrijeme": "Pon - Pet: 08:00 - 20:00",
}

O_NAMA = {
    "slogan": "TRENIRAJ SVIJETLIJE",
    "tekst": (
        "NEON//GYM je moderna teretana opremljena profesionalnim spravama "
        "i slobodnim tegovima za sve nivoe treninga. Naši treneri vode te "
        "korak po korak do cilja, bilo da gradiš snagu, mršaviš ili samo "
        "želiš ostati u formi. Termine rezervišeš online za par klikova, "
        "a trenera biraš sam."
    ),
    "programi": ["Snaga i masa", "Funkcionalni trening", "Kardio zona", "Istezanje i mobilnost"],
    "kartice": [
        {
            "naslov": "PERSONALNI TRENINZI",
            "slika": "kartica1.jpg",
            "ikona": "&#9733;",
            "tekst": (
                "Trening jedan na jedan sa trenerom po tvom izboru. Program se "
                "pravi prema tvojim ciljevima, a svaki termin rezervišeš "
                "unaprijed kroz naš sistem."
            ),
        },
        {
            "naslov": "GRUPNI TRENINZI",
            "slika": "kartica2.jpg",
            "ikona": "&#9829;",
            "tekst": (
                "Treniraj u dinamičnoj grupi uz stručno vođstvo. Motivacija "
                "ekipe i raznovrsne vježbe pomažu da ostaneš dosljedan i "
                "dosegneš nove rezultate."
            ),
        },
        {
            "naslov": "NEON KIDS",
            "slika": "kartica3.jpg",
            "ikona": "&#9786;",
            "tekst": (
                "Prostor za najmlađe, gdje uz igru i pokret razvijaju snagu, "
                "koordinaciju i zdrave navike. Programi su prilagođeni uzrastu "
                "i nivou aktivnosti djece i mladih."
            ),
        },
    ],
}


def kontakt(request):
    return render(request, "termini/kontakt.html", {
        "kontakt": KONTAKT,
        "podnaslov": "KONTAKT",
    })


def o_nama(request):
    return render(request, "termini/o_nama.html", {
        "o_nama": O_NAMA,
        "podnaslov": "O NAMA",
    })