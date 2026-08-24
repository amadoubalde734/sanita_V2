from django.shortcuts import render


def rendez_vous_list(request):
    return render(request, 'consultations/rendez_vous/index.html')
