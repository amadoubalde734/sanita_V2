from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import (
    TypeConsultationForm,
    TarifConsultationForm,
    MotifConsultationForm,
    PosologieForm,
    VoieAdministrationForm,
    DosageForm,
    FormeForm,
)

from ..models import (
    TypeConsultation,
    TarifConsultation,
    MotifConsultation,
    Posologie,
    VoieAdministration,
    Dosage,
    Forme,
    TarifConsultation,
)


@login_required
def liste_types_consultation(request):
    search_query = request.GET.get('q', '').strip()

    types = TypeConsultation.objects.all()

    if search_query:
        types = types.filter(
            models.Q(code__icontains=search_query) |
            models.Q(nom__icontains=search_query) |
            models.Q(categorie__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    types = types.order_by('ordre', 'nom')

    total_types = TypeConsultation.objects.count()
    active_types = TypeConsultation.objects.filter(actif=True).count()
    inactive_types = total_types - active_types

    form = TypeConsultationForm()

    return render(
        request,
        'backend/parametrage_general/pages/consultations/types.html',
        {
            'types': types,
            'search_query': search_query,
            'total_types': total_types,
            'active_types': active_types,
            'inactive_types': inactive_types,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_type_consultation(request):
    form = TypeConsultationForm()

    if request.method == 'POST':
        form = TypeConsultationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Type de consultation ajouté avec succès.'
            )
            return redirect(
                'parametrage_general:liste_types_consultation'
            )

    types = TypeConsultation.objects.all().order_by('ordre', 'nom')
    total_types = TypeConsultation.objects.count()
    active_types = TypeConsultation.objects.filter(actif=True).count()
    inactive_types = total_types - active_types

    return render(
        request,
        'backend/parametrage_general/pages/consultations/types.html',
        {
            'types': types,
            'search_query': '',
            'total_types': total_types,
            'active_types': active_types,
            'inactive_types': inactive_types,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def modifier_type_consultation(request, pk):
    type_consultation = get_object_or_404(
        TypeConsultation,
        pk=pk
    )

    if request.method == 'POST':
        form = TypeConsultationForm(
            request.POST,
            instance=type_consultation
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Type de consultation modifié avec succès.'
            )
            return redirect(
                'parametrage_general:liste_types_consultation'
            )
    else:
        form = TypeConsultationForm(
            instance=type_consultation
        )

    types = TypeConsultation.objects.all().order_by('ordre', 'nom')
    total_types = TypeConsultation.objects.count()
    active_types = TypeConsultation.objects.filter(actif=True).count()
    inactive_types = total_types - active_types

    return render(
        request,
        'backend/parametrage_general/pages/consultations/types.html',
        {
            'types': types,
            'search_query': '',
            'total_types': total_types,
            'active_types': active_types,
            'inactive_types': inactive_types,
            'form': form,
            'modifier': True,
            'type_to_edit': type_consultation,
        }
    )


@login_required
def supprimer_type_consultation(request, pk):
    type_consultation = get_object_or_404(
        TypeConsultation,
        pk=pk
    )

    if request.method == 'POST':
        if type_consultation.tarifs.exists():
            messages.error(
                request,
                f"Impossible de supprimer « {type_consultation.nom} » : "
                "des tarifs y sont encore rattachés."
            )
        else:
            type_consultation.delete()
            messages.success(
                request,
                'Type de consultation supprimé avec succès.'
            )

    return redirect(
        'parametrage_general:liste_types_consultation'
    )


@login_required
def toggle_type_consultation(request, pk):
    type_consultation = get_object_or_404(
        TypeConsultation,
        pk=pk
    )

    type_consultation.actif = not type_consultation.actif
    type_consultation.save(update_fields=['actif'])

    status = (
        'activé'
        if type_consultation.actif
        else 'désactivé'
    )

    messages.success(
        request,
        f'Le type de consultation a été {status}.'
    )

    return redirect(
        'parametrage_general:liste_types_consultation'
    )


@login_required
def liste_tarifs_consultation(request):
    search_query = request.GET.get('q', '').strip()

    tarifs = TarifConsultation.objects.select_related(
        'type_consultation',
        'etablissement',
    )

    if search_query:
        tarifs = tarifs.filter(
            models.Q(
                type_consultation__nom__icontains=search_query
            ) |
            models.Q(
                type_consultation__code__icontains=search_query
            ) |
            models.Q(
                type_consultation__categorie__icontains=search_query
            ) |
            models.Q(
                etablissement__nom_etablissement__icontains=search_query
            )
        )

    tarifs = tarifs.order_by('-date_debut')

    total_tarifs = TarifConsultation.objects.count()
    active_tarifs = TarifConsultation.objects.filter(actif=True).count()
    inactive_tarifs = total_tarifs - active_tarifs

    form = TarifConsultationForm()

    return render(
        request,
        'backend/parametrage_general/pages/consultations/tarifs.html',
        {
            'tarifs': tarifs,
            'search_query': search_query,
            'total_tarifs': total_tarifs,
            'active_tarifs': active_tarifs,
            'inactive_tarifs': inactive_tarifs,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_tarif_consultation(request):
    form = TarifConsultationForm()

    if request.method == 'POST':
        form = TarifConsultationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Tarif de consultation ajouté avec succès.'
            )
            return redirect(
                'parametrage_general:liste_tarifs_consultation'
            )

    tarifs = TarifConsultation.objects.select_related(
        'type_consultation',
        'etablissement',
    ).order_by('-date_debut')

    total_tarifs = TarifConsultation.objects.count()
    active_tarifs = TarifConsultation.objects.filter(actif=True).count()
    inactive_tarifs = total_tarifs - active_tarifs

    return render(
        request,
        'backend/parametrage_general/pages/consultations/tarifs.html',
        {
            'tarifs': tarifs,
            'search_query': '',
            'total_tarifs': total_tarifs,
            'active_tarifs': active_tarifs,
            'inactive_tarifs': inactive_tarifs,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def modifier_tarif_consultation(request, pk):
    tarif = get_object_or_404(
        TarifConsultation,
        pk=pk
    )

    if request.method == 'POST':
        form = TarifConsultationForm(
            request.POST,
            instance=tarif
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Tarif de consultation modifié avec succès.'
            )
            return redirect(
                'parametrage_general:liste_tarifs_consultation'
            )
    else:
        form = TarifConsultationForm(
            instance=tarif
        )

    tarifs = TarifConsultation.objects.select_related(
        'type_consultation',
        'etablissement',
    ).order_by('-date_debut')

    total_tarifs = TarifConsultation.objects.count()
    active_tarifs = TarifConsultation.objects.filter(actif=True).count()
    inactive_tarifs = total_tarifs - active_tarifs

    return render(
        request,
        'backend/parametrage_general/pages/consultations/tarifs.html',
        {
            'tarifs': tarifs,
            'search_query': '',
            'total_tarifs': total_tarifs,
            'active_tarifs': active_tarifs,
            'inactive_tarifs': inactive_tarifs,
            'form': form,
            'modifier': True,
            'tarif_to_edit': tarif,
        }
    )


@login_required
def supprimer_tarif_consultation(request, pk):
    tarif = get_object_or_404(
        TarifConsultation,
        pk=pk
    )

    if request.method == 'POST':
        tarif.delete()
        messages.success(
            request,
            'Tarif de consultation supprimé avec succès.'
        )

    return redirect(
        'parametrage_general:liste_tarifs_consultation'
    )


@login_required
def toggle_tarif_consultation(request, pk):
    tarif = get_object_or_404(
        TarifConsultation,
        pk=pk
    )

    tarif.actif = not tarif.actif
    tarif.save(update_fields=['actif'])

    status = (
        'activé'
        if tarif.actif
        else 'désactivé'
    )

    messages.success(
        request,
        f'Le tarif de consultation a été {status}.'
    )

    return redirect(
        'parametrage_general:liste_tarifs_consultation'
    )


@login_required
def liste_motifs_consultation(request):
    search_query = request.GET.get('q', '').strip()

    motifs = MotifConsultation.objects.all()

    if search_query:
        motifs = motifs.filter(
            motif__icontains=search_query
        )

    motifs = motifs.order_by('motif')

    total_motifs = MotifConsultation.objects.count()
    active_motifs = MotifConsultation.objects.filter(actif=True).count()
    inactive_motifs = total_motifs - active_motifs

    form = MotifConsultationForm()

    return render(
        request,
        'backend/parametrage_general/pages/consultations/motifs.html',
        {
            'motifs': motifs,
            'search_query': search_query,
            'total_motifs': total_motifs,
            'active_motifs': active_motifs,
            'inactive_motifs': inactive_motifs,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_motif_consultation(request):
    form = MotifConsultationForm()

    if request.method == 'POST':
        form = MotifConsultationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Motif de consultation ajouté avec succès.'
            )
            return redirect(
                'parametrage_general:liste_motifs_consultation'
            )

    motifs = MotifConsultation.objects.all().order_by('motif')
    total_motifs = MotifConsultation.objects.count()
    active_motifs = MotifConsultation.objects.filter(actif=True).count()
    inactive_motifs = total_motifs - active_motifs

    return render(
        request,
        'backend/parametrage_general/pages/consultations/motifs.html',
        {
            'motifs': motifs,
            'search_query': '',
            'total_motifs': total_motifs,
            'active_motifs': active_motifs,
            'inactive_motifs': inactive_motifs,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def modifier_motif_consultation(request, pk):
    motif = get_object_or_404(
        MotifConsultation,
        pk=pk
    )

    if request.method == 'POST':
        form = MotifConsultationForm(
            request.POST,
            instance=motif
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Motif de consultation modifié avec succès.'
            )
            return redirect(
                'parametrage_general:liste_motifs_consultation'
            )
    else:
        form = MotifConsultationForm(
            instance=motif
        )

    motifs = MotifConsultation.objects.all().order_by('motif')
    total_motifs = MotifConsultation.objects.count()
    active_motifs = MotifConsultation.objects.filter(actif=True).count()
    inactive_motifs = total_motifs - active_motifs

    return render(
        request,
        'backend/parametrage_general/pages/consultations/motifs.html',
        {
            'motifs': motifs,
            'search_query': '',
            'total_motifs': total_motifs,
            'active_motifs': active_motifs,
            'inactive_motifs': inactive_motifs,
            'form': form,
            'modifier': True,
            'motif_to_edit': motif,
        }
    )


@login_required
def supprimer_motif_consultation(request, pk):
    motif = get_object_or_404(
        MotifConsultation,
        pk=pk
    )

    if request.method == 'POST':
        motif.delete()
        messages.success(
            request,
            'Motif de consultation supprimé avec succès.'
        )

    return redirect(
        'parametrage_general:liste_motifs_consultation'
    )


@login_required
def toggle_motif_consultation(request, pk):
    motif = get_object_or_404(
        MotifConsultation,
        pk=pk
    )

    motif.actif = not motif.actif
    motif.save(update_fields=['actif'])

    status = (
        'activé'
        if motif.actif
        else 'désactivé'
    )

    messages.success(
        request,
        f'Le motif de consultation a été {status}.'
    )

    return redirect(
        'parametrage_general:liste_motifs_consultation'
    )


@login_required
def liste_posologies(request):
    search_query = request.GET.get('q', '').strip()

    posologies = Posologie.objects.all()

    if search_query:
        posologies = posologies.filter(
            libelle__icontains=search_query
        )

    posologies = posologies.order_by('libelle')

    total_posologies = Posologie.objects.count()
    active_posologies = Posologie.objects.filter(actif=True).count()
    inactive_posologies = total_posologies - active_posologies

    form = PosologieForm()

    return render(
        request,
        'backend/parametrage_general/pages/consultations/posologies.html',
        {
            'posologies': posologies,
            'search_query': search_query,
            'total_posologies': total_posologies,
            'active_posologies': active_posologies,
            'inactive_posologies': inactive_posologies,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_posologie(request):
    form = PosologieForm()

    if request.method == 'POST':
        form = PosologieForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Posologie ajoutée avec succès.'
            )
            return redirect(
                'parametrage_general:liste_posologies'
            )

    posologies = Posologie.objects.all().order_by('libelle')
    total_posologies = Posologie.objects.count()
    active_posologies = Posologie.objects.filter(actif=True).count()
    inactive_posologies = total_posologies - active_posologies

    return render(
        request,
        'backend/parametrage_general/pages/consultations/posologies.html',
        {
            'posologies': posologies,
            'search_query': '',
            'total_posologies': total_posologies,
            'active_posologies': active_posologies,
            'inactive_posologies': inactive_posologies,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def modifier_posologie(request, pk):
    posologie = get_object_or_404(
        Posologie,
        pk=pk
    )

    if request.method == 'POST':
        form = PosologieForm(
            request.POST,
            instance=posologie
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Posologie modifiée avec succès.'
            )
            return redirect(
                'parametrage_general:liste_posologies'
            )
    else:
        form = PosologieForm(
            instance=posologie
        )

    posologies = Posologie.objects.all().order_by('libelle')
    total_posologies = Posologie.objects.count()
    active_posologies = Posologie.objects.filter(actif=True).count()
    inactive_posologies = total_posologies - active_posologies

    return render(
        request,
        'backend/parametrage_general/pages/consultations/posologies.html',
        {
            'posologies': posologies,
            'search_query': '',
            'total_posologies': total_posologies,
            'active_posologies': active_posologies,
            'inactive_posologies': inactive_posologies,
            'form': form,
            'modifier': True,
            'posologie_to_edit': posologie,
        }
    )


@login_required
def supprimer_posologie(request, pk):
    posologie = get_object_or_404(
        Posologie,
        pk=pk
    )

    if request.method == 'POST':
        posologie.delete()
        messages.success(
            request,
            'Posologie supprimée avec succès.'
        )

    return redirect(
        'parametrage_general:liste_posologies'
    )


@login_required
def toggle_posologie(request, pk):
    posologie = get_object_or_404(
        Posologie,
        pk=pk
    )

    posologie.actif = not posologie.actif
    posologie.save(update_fields=['actif'])

    status = (
        'activée'
        if posologie.actif
        else 'désactivée'
    )

    messages.success(
        request,
        f'La posologie a été {status}.'
    )

    return redirect(
        'parametrage_general:liste_posologies'
    )


@login_required
def liste_voies_administration(request):
    search_query = request.GET.get('q', '').strip()

    voies = VoieAdministration.objects.all()

    if search_query:
        voies = voies.filter(
            models.Q(code__icontains=search_query) |
            models.Q(nom__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    voies = voies.order_by('ordre', 'nom')

    total_voies = VoieAdministration.objects.count()
    active_voies = VoieAdministration.objects.filter(actif=True).count()
    inactive_voies = total_voies - active_voies

    form = VoieAdministrationForm()

    return render(
        request,
        'backend/parametrage_general/pages/consultations/voies.html',
        {
            'voies': voies,
            'search_query': search_query,
            'total_voies': total_voies,
            'active_voies': active_voies,
            'inactive_voies': inactive_voies,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_voie_administration(request):
    form = VoieAdministrationForm()

    if request.method == 'POST':
        form = VoieAdministrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Voie d'administration ajoutée avec succès."
            )
            return redirect(
                'parametrage_general:liste_voies_administration'
            )

    voies = VoieAdministration.objects.all().order_by('ordre', 'nom')
    total_voies = VoieAdministration.objects.count()
    active_voies = VoieAdministration.objects.filter(actif=True).count()
    inactive_voies = total_voies - active_voies

    return render(
        request,
        'backend/parametrage_general/pages/consultations/voies.html',
        {
            'voies': voies,
            'search_query': '',
            'total_voies': total_voies,
            'active_voies': active_voies,
            'inactive_voies': inactive_voies,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def modifier_voie_administration(request, pk):
    voie = get_object_or_404(
        VoieAdministration,
        pk=pk
    )

    if request.method == 'POST':
        form = VoieAdministrationForm(
            request.POST,
            instance=voie
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Voie d'administration modifiée avec succès."
            )
            return redirect(
                'parametrage_general:liste_voies_administration'
            )
    else:
        form = VoieAdministrationForm(
            instance=voie
        )

    voies = VoieAdministration.objects.all().order_by('ordre', 'nom')
    total_voies = VoieAdministration.objects.count()
    active_voies = VoieAdministration.objects.filter(actif=True).count()
    inactive_voies = total_voies - active_voies

    return render(
        request,
        'backend/parametrage_general/pages/consultations/voies.html',
        {
            'voies': voies,
            'search_query': '',
            'total_voies': total_voies,
            'active_voies': active_voies,
            'inactive_voies': inactive_voies,
            'form': form,
            'modifier': True,
            'voie_to_edit': voie,
        }
    )


@login_required
def supprimer_voie_administration(request, pk):
    voie = get_object_or_404(
        VoieAdministration,
        pk=pk
    )

    if request.method == 'POST':
        voie.delete()
        messages.success(
            request,
            "Voie d'administration supprimée avec succès."
        )

    return redirect(
        'parametrage_general:liste_voies_administration'
    )


@login_required
def toggle_voie_administration(request, pk):
    voie = get_object_or_404(
        VoieAdministration,
        pk=pk
    )

    voie.actif = not voie.actif
    voie.save(update_fields=['actif'])

    status = (
        'activée'
        if voie.actif
        else 'désactivée'
    )

    messages.success(
        request,
        f"La voie d'administration a été {status}."
    )

    return redirect(
        'parametrage_general:liste_voies_administration'
    )


@login_required
def liste_dosages(request):
    search_query = request.GET.get('q', '').strip()

    dosages = Dosage.objects.all()

    if search_query:
        dosages = dosages.filter(
            models.Q(code__icontains=search_query) |
            models.Q(nom__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    dosages = dosages.order_by('ordre', 'nom')

    total_dosages = Dosage.objects.count()
    active_dosages = Dosage.objects.filter(actif=True).count()
    inactive_dosages = total_dosages - active_dosages

    form = DosageForm()

    return render(
        request,
        'backend/parametrage_general/pages/consultations/dosages.html',
        {
            'dosages': dosages,
            'search_query': search_query,
            'total_dosages': total_dosages,
            'active_dosages': active_dosages,
            'inactive_dosages': inactive_dosages,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_dosage(request):
    form = DosageForm()

    if request.method == 'POST':
        form = DosageForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Dosage ajouté avec succès.'
            )
            return redirect(
                'parametrage_general:liste_dosages'
            )

    dosages = Dosage.objects.all().order_by('ordre', 'nom')
    total_dosages = Dosage.objects.count()
    active_dosages = Dosage.objects.filter(actif=True).count()
    inactive_dosages = total_dosages - active_dosages

    return render(
        request,
        'backend/parametrage_general/pages/consultations/dosages.html',
        {
            'dosages': dosages,
            'search_query': '',
            'total_dosages': total_dosages,
            'active_dosages': active_dosages,
            'inactive_dosages': inactive_dosages,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def modifier_dosage(request, pk):
    dosage = get_object_or_404(
        Dosage,
        pk=pk
    )

    if request.method == 'POST':
        form = DosageForm(
            request.POST,
            instance=dosage
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Dosage modifié avec succès.'
            )
            return redirect(
                'parametrage_general:liste_dosages'
            )
    else:
        form = DosageForm(
            instance=dosage
        )

    dosages = Dosage.objects.all().order_by('ordre', 'nom')
    total_dosages = Dosage.objects.count()
    active_dosages = Dosage.objects.filter(actif=True).count()
    inactive_dosages = total_dosages - active_dosages

    return render(
        request,
        'backend/parametrage_general/pages/consultations/dosages.html',
        {
            'dosages': dosages,
            'search_query': '',
            'total_dosages': total_dosages,
            'active_dosages': active_dosages,
            'inactive_dosages': inactive_dosages,
            'form': form,
            'modifier': True,
            'dosage_to_edit': dosage,
        }
    )


@login_required
def supprimer_dosage(request, pk):
    dosage = get_object_or_404(
        Dosage,
        pk=pk
    )

    if request.method == 'POST':
        dosage.delete()
        messages.success(
            request,
            'Dosage supprimé avec succès.'
        )

    return redirect(
        'parametrage_general:liste_dosages'
    )


@login_required
def toggle_dosage(request, pk):
    dosage = get_object_or_404(
        Dosage,
        pk=pk
    )

    dosage.actif = not dosage.actif
    dosage.save(update_fields=['actif'])

    status = (
        'activé'
        if dosage.actif
        else 'désactivé'
    )

    messages.success(
        request,
        f'Le dosage a été {status}.'
    )

    return redirect(
        'parametrage_general:liste_dosages'
    )


@login_required
def liste_formes(request):
    search_query = request.GET.get('q', '').strip()

    formes = Forme.objects.all()

    if search_query:
        formes = formes.filter(
            models.Q(code__icontains=search_query) |
            models.Q(nom__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    formes = formes.order_by('ordre', 'nom')

    total_formes = Forme.objects.count()
    active_formes = Forme.objects.filter(actif=True).count()
    inactive_formes = total_formes - active_formes

    form = FormeForm()

    return render(
        request,
        'backend/parametrage_general/pages/consultations/formes.html',
        {
            'formes': formes,
            'search_query': search_query,
            'total_formes': total_formes,
            'active_formes': active_formes,
            'inactive_formes': inactive_formes,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_forme(request):
    form = FormeForm()

    if request.method == 'POST':
        form = FormeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Forme pharmaceutique ajoutée avec succès.'
            )
            return redirect(
                'parametrage_general:liste_formes'
            )

    formes = Forme.objects.all().order_by('ordre', 'nom')
    total_formes = Forme.objects.count()
    active_formes = Forme.objects.filter(actif=True).count()
    inactive_formes = total_formes - active_formes

    return render(
        request,
        'backend/parametrage_general/pages/consultations/formes.html',
        {
            'formes': formes,
            'search_query': '',
            'total_formes': total_formes,
            'active_formes': active_formes,
            'inactive_formes': inactive_formes,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def modifier_forme(request, pk):
    forme = get_object_or_404(
        Forme,
        pk=pk
    )

    if request.method == 'POST':
        form = FormeForm(
            request.POST,
            instance=forme
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Forme pharmaceutique modifiée avec succès.'
            )
            return redirect(
                'parametrage_general:liste_formes'
            )
    else:
        form = FormeForm(
            instance=forme
        )

    formes = Forme.objects.all().order_by('ordre', 'nom')
    total_formes = Forme.objects.count()
    active_formes = Forme.objects.filter(actif=True).count()
    inactive_formes = total_formes - active_formes

    return render(
        request,
        'backend/parametrage_general/pages/consultations/formes.html',
        {
            'formes': formes,
            'search_query': '',
            'total_formes': total_formes,
            'active_formes': active_formes,
            'inactive_formes': inactive_formes,
            'form': form,
            'modifier': True,
            'forme_to_edit': forme,
        }
    )


@login_required
def supprimer_forme(request, pk):
    forme = get_object_or_404(
        Forme,
        pk=pk
    )

    if request.method == 'POST':
        forme.delete()
        messages.success(
            request,
            'Forme pharmaceutique supprimée avec succès.'
        )

    return redirect(
        'parametrage_general:liste_formes'
    )


@login_required
def toggle_forme(request, pk):
    forme = get_object_or_404(
        Forme,
        pk=pk
    )

    forme.actif = not forme.actif
    forme.save(update_fields=['actif'])

    status = (
        'activée'
        if forme.actif
        else 'désactivée'
    )

    messages.success(
        request,
        f'La forme pharmaceutique a été {status}.'
    )

    return redirect(
        'parametrage_general:liste_formes'
    )

