from django.shortcuts import render


def famille_detail(request):
    return render(request, 'backend/pages/personnels/famille_detail.html')
