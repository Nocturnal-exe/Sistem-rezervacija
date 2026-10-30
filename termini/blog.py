from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .models import Post

PO_STRANICI = 9

PRIMJERI = [
    {"naslov": "Primjer posta jedan", "kratak_opis": "Ovdje ide kratak opis posta. Dodaj pravi post kroz admin.", "slika": None},
    {"naslov": "Primjer posta dva", "kratak_opis": "Ovdje ide kratak opis posta. Dodaj pravi post kroz admin.", "slika": None},
    {"naslov": "Primjer posta tri", "kratak_opis": "Ovdje ide kratak opis posta. Dodaj pravi post kroz admin.", "slika": None},
]


def blog_lista(request):
    svi = Post.objects.filter(objavljen=True)
    paginator = Paginator(svi, PO_STRANICI)
    stranica = paginator.get_page(request.GET.get("stranica"))
    return render(request, "termini/blog.html", {
        "postovi": stranica,
        "primjeri": PRIMJERI,
        "podnaslov": "BLOG",
    })


def blog_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, objavljen=True)
    return render(request, "termini/blog_post.html", {
        "post": post,
        "podnaslov": "BLOG",
    })