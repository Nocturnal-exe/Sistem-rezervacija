from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, trener, stranice, cijene, blog, profil

urlpatterns = [
    path("", views.pocetna, name="pocetna"),
    path("izbor-trenera/", views.izbor_trenera, name="izbor_trenera"),
    path("registracija/", views.registracija, name="registracija"),
    path(
        "prijava/",
        auth_views.LoginView.as_view(
            template_name="termini/auth.html",
            extra_context={"naslov": "PRIJAVA", "dugme": "Uđi u sistem"},
        ),
        name="prijava",
    ),
    path("lozinka/reset/", auth_views.PasswordResetView.as_view(
        template_name="termini/auth.html",
        extra_context={"naslov": "RESET LOZINKE", "dugme": "Pošalji link"},
        email_template_name="termini/email_reset.txt",
        subject_template_name="termini/email_reset_naslov.txt",
    ), name="password_reset"),
    path("lozinka/reset/poslano/", auth_views.PasswordResetDoneView.as_view(
        template_name="termini/poruka.html",
        extra_context={"naslov": "EMAIL POSLAN", "tekst": "Ako nalog sa tom email adresom postoji, poslali smo ti link za promjenu lozinke."},
    ), name="password_reset_done"),
    path("lozinka/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="termini/auth.html",
        extra_context={"naslov": "NOVA LOZINKA", "dugme": "Sačuvaj lozinku"},
    ), name="password_reset_confirm"),
    path("lozinka/reset/gotovo/", auth_views.PasswordResetCompleteView.as_view(
        template_name="termini/poruka.html",
        extra_context={"naslov": "LOZINKA PROMIJENJENA", "tekst": "Sada se možeš prijaviti novom lozinkom."},
    ), name="password_reset_complete"),
    path("odjava/", auth_views.LogoutView.as_view(), name="odjava"),
    path("rezervisi/", views.rezervisi, name="rezervisi"),
    path("moje-rezervacije/", views.moje_rezervacije, name="moje_rezervacije"),
    path("otkazi/<int:rezervacija_id>/", views.otkazi, name="otkazi"),
    path("trener/", trener.trener_panel, name="trener_panel"),
    path("trener/blokiraj/", trener.blokiraj, name="blokiraj"),
    path("trener/odblokiraj/", trener.odblokiraj, name="odblokiraj"),
    path("kontakt/", stranice.kontakt, name="kontakt"),
    path("o-nama/", stranice.o_nama, name="o_nama"),
    path("cjenovnik/", cijene.cjenovnik, name="cjenovnik"),
    path("profil/", profil.profil, name="profil"),
    path("blog/", blog.blog_lista, name="blog"),
    path("blog/<int:post_id>/", blog.blog_post, name="blog_post"),
]