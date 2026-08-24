from django.shortcuts import render


def index(request):
    return render(
        request,
        'cartes_sanitaires/index.html'
    )


def liste(request):
    return render(
        request,
        'backend/pages/cartes_sanitaires/liste.html'
    )


def nouvelle_carte(request):
    return render(
        request,
        'backend/pages/cartes_sanitaires/carte.html'
    )


def qrcode(request):
    return render(
        request,
        'backend/pages/cartes_sanitaires/generation_qrcode.html'
    )


def impression(request):
    return render(
        request,
        'backend/pages/cartes_sanitaires/impression_carte.html'
    )