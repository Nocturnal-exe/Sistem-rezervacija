\# NEON//GYM



Web aplikacija za rezervaciju termina u teretani, napravljena u Djangu s cyberpunk neon izgledom. Počela je kao UML model u mom završnom radu, a onda sam htio vidjeti kako bi to izgledalo kao prava aplikacija. Dijagrami na dnu su zapravo plan po kojem je sve građeno.



\## Šta se u njoj može



Korisnik napravi nalog, izabere datum i sat, pa onda trenera. Uz svakog trenera piše je li slobodan ili zauzet u tom terminu. Rezervisati se može najviše tri termina odjednom, a svoje rezervacije korisnik može pregledati i otkazati. Ima i profil, promjenu lozinke i reset lozinke preko emaila.



Trener ima svoj panel gdje blokira i odblokira termine. Admin preko Django admina (koji sam sam preuredio i preveo na bosanski) vodi korisnike, termine, rezervacije i blog.



Prošle rezervacije se same označe kao završene, a 15 minuta prije treninga stiže podsjetnik emailom. Tu su još blog s paginacijom i stranice O nama, Cjenovnik i Kontakt.



\## Tehnologije



1\. Python 3 i Django

2\. SQLite baza

3\. Pillow za slike

4\. HTML, CSS i malo JavaScripta, bez vanjskih frameworka



\## Pokretanje



Potreban je instaliran Python.



```

git clone https://github.com/Nocturnal-exe/Sistem-rezervacija.git

cd Sistem-rezervacija

py -m pip install -r requirements.txt

py manage.py migrate

py manage.py createsuperuser

py manage.py runserver

```



Aplikacija se zatim otvara na http://127.0.0.1:8000/ a admin panel na http://127.0.0.1:8000/admin/



Trenere dodajete u adminu tako što korisniku postavite ulogu "trener".



\### Podsjetnici



Podsjetnike pokrećete u drugom cmd prozoru:



```

py manage.py posalji\_podsjetnike --petlja

```



Email se za sada samo ispisuje u konzoli, pravo slanje još nisam podesio.



\## Screenshotovi



\### Početna

!\[Početna](docs/pocetna.png)



\### Izbor trenera

!\[Izbor trenera](docs/izbor-trenera.png)



\### Moje rezervacije

!\[Moje rezervacije](docs/moje-rezervacije.png)



\### Trenerski panel

!\[Trenerski panel](docs/trener-panel.png)



\### Prijava

!\[Prijava](docs/prijava.png)



\### Profil

!\[Profil](docs/profil.png)



\### O nama

!\[O nama](docs/o-nama.png)



\### Cjenovnik

!\[Cjenovnik](docs/cjenovnik.png)



\### Blog

!\[Blog](docs/blog.png)



\### Kontakt

!\[Kontakt](docs/kontakt.png)



\### Admin panel

!\[Admin panel](docs/admin.png)



\## UML dijagrami



\### Dijagram slučajeva upotrebe

!\[Use case](docs/image1.png)



\### Dijagram klasa

!\[Klase](docs/image2.png)



\### Dijagram sekvence

!\[Sekvenca](docs/image3.png)



\### Dijagram aktivnosti

!\[Aktivnosti](docs/image4.png)



\### Dijagram stanja

!\[Stanja](docs/image5.png)



\## Autor



Hamza Fetić

