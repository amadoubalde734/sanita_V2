from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import AyantDroit
from ..forms import AyantDroitForm


@login_required
def ayant_droit_list(request):
    ayants_droit = AyantDroit.objects.select_related('employe').all()
    return render(request, 'backend/pages/personnels/ayant_droit_list.html', {
        'ayants_droit': ayants_droit,
    })


@login_required
def ayant_droit_create(request, default_type=None):
    if request.method == 'POST':
        form = AyantDroitForm(request.POST, request.FILES)
        if form.is_valid():
            ayant_droit = form.save()
            messages.success(request, f"L'ayant droit {ayant_droit.nom} {ayant_droit.prenoms} a été ajouté avec succès.")
            return redirect('personnels:ayant_droit_list')
    else:
        initial = {}
        if default_type:
            initial['type'] = default_type
        form = AyantDroitForm(initial=initial)

    return render(request, 'backend/pages/personnels/ayant_droit_create.html', {
        'form': form,
        'default_type': default_type,
    })


@login_required
def enfant_create(request):
    return ayant_droit_create(request, default_type='ENFANT')


@login_required
def conjoint_create(request):
    return ayant_droit_create(request, default_type='CONJOINT')


@login_required
def autre_ayant_droit_create(request):
    return ayant_droit_create(request, default_type='AUTRE')
