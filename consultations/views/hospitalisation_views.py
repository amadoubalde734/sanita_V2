from django.shortcuts import render


def hospitalisation_list(request):
    return render(request, 'consultations/hospitalisation/index.html')
