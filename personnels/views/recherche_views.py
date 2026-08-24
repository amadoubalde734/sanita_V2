from django.shortcuts import render


def recherche_employe(request):
    return render(request, 'backend/pages/personnels/employe_recherche.html')
