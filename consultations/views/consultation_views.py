from django.shortcuts import render


def index(request):
    return render(request, 'consultations/index.html')


def consultation_list(request):
    return render(request, 'consultations/consultation/liste.html')


def consultation_add(request):
    return render(request, 'consultations/consultation/ajouter.html')


def consultation_detail(request):
    return render(request, 'consultations/consultation/detail.html')


def arret_travail_list(request):
    return render(request, 'consultations/arret_travail/index.html')


def orientation_list(request):
    return render(request, 'consultations/orientation/index.html')


def referement_list(request):
    return render(request, 'consultations/referement/index.html')
