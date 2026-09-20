from django.shortcuts import render


def index(request):
	return render(request, 'backend/patients/index.html')
