from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from parametrage_general.models import ConfigurationEtablissement


@login_required
def dashboard(request):
    return render(request, 'backend/index.html')


@login_required
def index_global(request):

    config_etablissement = ConfigurationEtablissement.objects.first()

    return render(
        request,
        'backend/index_global.html',
        {
            'config_etablissement': config_etablissement
        }
    )