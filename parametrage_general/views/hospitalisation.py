from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from ..forms.hospitalisation import (
    TypeSejourForm,
    TypeChambreForm,
    ChambreForm,
    LitForm,
    TypeSoinForm,
    RegimeAlimentaireForm,
    MotifHospitalisationForm,
    TypeSortieForm,
    TarifSejourForm,
)

from ..models import (
    TypeSejour,
    TypeChambre,
    Chambre,
    Lit,
    TypeSoin,
    RegimeAlimentaire,
    MotifHospitalisation,
    TypeSortie,
    TarifSejour,
)


def _types_sejours_context(q=''):
    types_sejours = TypeSejour.objects.all()

    if q:
        types_sejours = types_sejours.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q)
        )

    types_sejours = types_sejours.order_by('ordre', 'nom')

    return {
        'types_sejours': types_sejours,
        'total_types_sejours': TypeSejour.objects.count(),
        'types_sejours_actifs': TypeSejour.objects.filter(actif=True).count(),
        'types_sejours_inactifs': TypeSejour.objects.filter(actif=False).count(),
        'q': q,
    }


@login_required
def liste_types_sejours(request):
    q = request.GET.get('q', '').strip()
    context = _types_sejours_context(q)
    context.update({
        'type_sejour_to_edit': None,
        'form': TypeSejourForm(),
        'modifier': False,
    })
    return render(
        request,
        'backend/parametrage_general/pages/hospitalisations/types_sejours.html',
        context
    )


@login_required
def ajouter_type_sejour(request):
    if request.method == 'POST':
        form = TypeSejourForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Le type de séjour a été ajouté avec succès.")
            return redirect('parametrage_general:liste_types_sejours')

        q = request.GET.get('q', '').strip()
        context = _types_sejours_context(q)
        context.update({
            'type_sejour_to_edit': None,
            'form': form,
            'modifier': False,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/types_sejours.html',
            context
        )

    return redirect('parametrage_general:liste_types_sejours')


@login_required
def modifier_type_sejour(request, pk):
    type_sejour = get_object_or_404(TypeSejour, pk=pk)

    if request.method == 'POST':
        form = TypeSejourForm(request.POST, instance=type_sejour)

        if form.is_valid():
            form.save()
            messages.success(request, "Le type de séjour a été modifié avec succès.")
            return redirect('parametrage_general:liste_types_sejours')

        q = request.GET.get('q', '').strip()
        context = _types_sejours_context(q)
        context.update({
            'type_sejour_to_edit': type_sejour,
            'form': form,
            'modifier': True,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/types_sejours.html',
            context
        )

    return redirect('parametrage_general:liste_types_sejours')


@login_required
def supprimer_type_sejour(request, pk):
    type_sejour = get_object_or_404(TypeSejour, pk=pk)

    if request.method == 'POST':
        try:
            type_sejour.delete()
            messages.success(request, "Le type de séjour a été supprimé avec succès.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer ce type de séjour car il est utilisé."
            )

    return redirect('parametrage_general:liste_types_sejours')


@login_required
def toggle_type_sejour(request, pk):
    type_sejour = get_object_or_404(TypeSejour, pk=pk)

    if request.method == 'POST':
        type_sejour.actif = not type_sejour.actif
        type_sejour.save(update_fields=['actif', 'updated_at'])

        if type_sejour.actif:
            messages.success(request, "Le type de séjour a été activé.")
        else:
            messages.success(request, "Le type de séjour a été désactivé.")

    return redirect('parametrage_general:liste_types_sejours')


def _types_chambres_context(q=''):
    types_chambres = TypeChambre.objects.all()

    if q:
        types_chambres = types_chambres.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q)
        )

    types_chambres = types_chambres.order_by('ordre', 'nom')

    return {
        'types_chambres': types_chambres,
        'total_types_chambres': TypeChambre.objects.count(),
        'types_chambres_actifs': TypeChambre.objects.filter(actif=True).count(),
        'types_chambres_inactifs': TypeChambre.objects.filter(actif=False).count(),
        'q': q,
    }


@login_required
def liste_types_chambres(request):
    q = request.GET.get('q', '').strip()
    context = _types_chambres_context(q)
    context.update({
        'type_chambre_to_edit': None,
        'form': TypeChambreForm(),
        'modifier': False,
    })
    return render(
        request,
        'backend/parametrage_general/pages/hospitalisations/types_chambres.html',
        context
    )


@login_required
def ajouter_type_chambre(request):
    if request.method == 'POST':
        form = TypeChambreForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Le type de chambre a été ajouté avec succès.")
            return redirect('parametrage_general:liste_types_chambres')

        q = request.GET.get('q', '').strip()
        context = _types_chambres_context(q)
        context.update({
            'type_chambre_to_edit': None,
            'form': form,
            'modifier': False,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/types_chambres.html',
            context
        )

    return redirect('parametrage_general:liste_types_chambres')


@login_required
def modifier_type_chambre(request, pk):
    type_chambre = get_object_or_404(TypeChambre, pk=pk)

    if request.method == 'POST':
        form = TypeChambreForm(request.POST, instance=type_chambre)

        if form.is_valid():
            form.save()
            messages.success(request, "Le type de chambre a été modifié avec succès.")
            return redirect('parametrage_general:liste_types_chambres')

        q = request.GET.get('q', '').strip()
        context = _types_chambres_context(q)
        context.update({
            'type_chambre_to_edit': type_chambre,
            'form': form,
            'modifier': True,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/types_chambres.html',
            context
        )

    return redirect('parametrage_general:liste_types_chambres')


@login_required
def supprimer_type_chambre(request, pk):
    type_chambre = get_object_or_404(TypeChambre, pk=pk)

    if request.method == 'POST':
        try:
            type_chambre.delete()
            messages.success(request, "Le type de chambre a été supprimé avec succès.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer ce type de chambre car il est utilisé."
            )

    return redirect('parametrage_general:liste_types_chambres')


@login_required
def toggle_type_chambre(request, pk):
    type_chambre = get_object_or_404(TypeChambre, pk=pk)

    if request.method == 'POST':
        type_chambre.actif = not type_chambre.actif
        type_chambre.save(update_fields=['actif', 'updated_at'])

        if type_chambre.actif:
            messages.success(request, "Le type de chambre a été activé.")
        else:
            messages.success(request, "Le type de chambre a été désactivé.")

    return redirect('parametrage_general:liste_types_chambres')


def _chambres_context(q=''):
    chambres = Chambre.objects.select_related(
        'etablissement',
        'unite',
        'unite__site',
        'type_chambre'
    ).all()

    if q:
        chambres = chambres.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(etage__icontains=q) |
            models.Q(localisation__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(etablissement__nom_etablissement__icontains=q) |
            models.Q(unite__nom__icontains=q) |
            models.Q(unite__site__nom_site__icontains=q) |
            models.Q(type_chambre__nom__icontains=q)
        )

    chambres = chambres.order_by(
        'etablissement__nom_etablissement',
        'unite__nom',
        'code'
    )

    return {
        'chambres': chambres,
        'total_chambres': Chambre.objects.count(),
        'chambres_actives': Chambre.objects.filter(actif=True).count(),
        'chambres_inactives': Chambre.objects.filter(actif=False).count(),
        'q': q,
    }


@login_required
def liste_chambres(request):
    q = request.GET.get('q', '').strip()
    context = _chambres_context(q)
    context.update({
        'chambre_to_edit': None,
        'form': ChambreForm(),
        'modifier': False,
    })
    return render(
        request,
        'backend/parametrage_general/pages/hospitalisations/chambres.html',
        context
    )


@login_required
def ajouter_chambre(request):
    if request.method == 'POST':
        form = ChambreForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "La chambre a été ajoutée avec succès.")
            return redirect('parametrage_general:liste_chambres')

        q = request.GET.get('q', '').strip()
        context = _chambres_context(q)
        context.update({
            'chambre_to_edit': None,
            'form': form,
            'modifier': False,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/chambres.html',
            context
        )

    return redirect('parametrage_general:liste_chambres')


@login_required
def modifier_chambre(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)

    if request.method == 'POST':
        form = ChambreForm(request.POST, instance=chambre)

        if form.is_valid():
            form.save()
            messages.success(request, "La chambre a été modifiée avec succès.")
            return redirect('parametrage_general:liste_chambres')

        q = request.GET.get('q', '').strip()
        context = _chambres_context(q)
        context.update({
            'chambre_to_edit': chambre,
            'form': form,
            'modifier': True,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/chambres.html',
            context
        )

    return redirect('parametrage_general:liste_chambres')


@login_required
def supprimer_chambre(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)

    if request.method == 'POST':
        try:
            chambre.delete()
            messages.success(request, "La chambre a été supprimée avec succès.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer cette chambre car elle est utilisée."
            )

    return redirect('parametrage_general:liste_chambres')


@login_required
def toggle_chambre(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)

    if request.method == 'POST':
        chambre.actif = not chambre.actif
        chambre.save(update_fields=['actif', 'updated_at'])

        if chambre.actif:
            messages.success(request, "La chambre a été activée.")
        else:
            messages.success(request, "La chambre a été désactivée.")

    return redirect('parametrage_general:liste_chambres')


def _lits_context(q=''):
    lits = Lit.objects.select_related(
        'chambre',
        'chambre__etablissement',
        'chambre__unite',
        'chambre__unite__site',
        'chambre__type_chambre'
    ).all()

    if q:
        lits = lits.filter(
            models.Q(code__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(statut__icontains=q) |
            models.Q(chambre__code__icontains=q) |
            models.Q(chambre__nom__icontains=q) |
            models.Q(chambre__unite__nom__icontains=q) |
            models.Q(chambre__unite__site__nom_site__icontains=q) |
            models.Q(chambre__etablissement__nom_etablissement__icontains=q)
        )

    lits = lits.order_by(
        'chambre__etablissement__nom_etablissement',
        'chambre__unite__nom',
        'chambre__code',
        'code'
    )

    return {
        'lits': lits,
        'total_lits': Lit.objects.count(),
        'lits_actifs': Lit.objects.filter(actif=True).count(),
        'lits_inactifs': Lit.objects.filter(actif=False).count(),
        'q': q,
    }


@login_required
def liste_lits(request):
    q = request.GET.get('q', '').strip()
    context = _lits_context(q)
    context.update({
        'lit_to_edit': None,
        'form': LitForm(),
        'modifier': False,
    })
    return render(
        request,
        'backend/parametrage_general/pages/hospitalisations/lits.html',
        context
    )


@login_required
def ajouter_lit(request):
    if request.method == 'POST':
        form = LitForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Le lit a été ajouté avec succès.")
            return redirect('parametrage_general:liste_lits')

        q = request.GET.get('q', '').strip()
        context = _lits_context(q)
        context.update({
            'lit_to_edit': None,
            'form': form,
            'modifier': False,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/lits.html',
            context
        )

    return redirect('parametrage_general:liste_lits')


@login_required
def modifier_lit(request, pk):
    lit = get_object_or_404(Lit, pk=pk)

    if request.method == 'POST':
        form = LitForm(request.POST, instance=lit)

        if form.is_valid():
            form.save()
            messages.success(request, "Le lit a été modifié avec succès.")
            return redirect('parametrage_general:liste_lits')

        q = request.GET.get('q', '').strip()
        context = _lits_context(q)
        context.update({
            'lit_to_edit': lit,
            'form': form,
            'modifier': True,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/lits.html',
            context
        )

    return redirect('parametrage_general:liste_lits')


@login_required
def supprimer_lit(request, pk):
    lit = get_object_or_404(Lit, pk=pk)

    if request.method == 'POST':
        try:
            lit.delete()
            messages.success(request, "Le lit a été supprimé avec succès.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer ce lit car il est utilisé."
            )

    return redirect('parametrage_general:liste_lits')


@login_required
def toggle_lit(request, pk):
    lit = get_object_or_404(Lit, pk=pk)

    if request.method == 'POST':
        lit.actif = not lit.actif
        lit.save(update_fields=['actif', 'updated_at'])

        if lit.actif:
            messages.success(request, "Le lit a été activé.")
        else:
            messages.success(request, "Le lit a été désactivé.")

    return redirect('parametrage_general:liste_lits')


def _types_soins_context(q=''):
    types_soins = TypeSoin.objects.all()

    if q:
        types_soins = types_soins.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(categorie__icontains=q) |
            models.Q(description__icontains=q)
        )

    types_soins = types_soins.order_by('ordre', 'nom')

    return {
        'types_soins': types_soins,
        'total_types_soins': TypeSoin.objects.count(),
        'types_soins_actifs': TypeSoin.objects.filter(actif=True).count(),
        'types_soins_inactifs': TypeSoin.objects.filter(actif=False).count(),
        'q': q,
    }


@login_required
def liste_types_soins(request):
    q = request.GET.get('q', '').strip()
    context = _types_soins_context(q)
    context.update({
        'type_soin_to_edit': None,
        'form': TypeSoinForm(),
        'modifier': False,
    })
    return render(
        request,
        'backend/parametrage_general/pages/hospitalisations/types_soins.html',
        context
    )


@login_required
def ajouter_type_soin(request):
    if request.method == 'POST':
        form = TypeSoinForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Le type de soin a été ajouté avec succès.")
            return redirect('parametrage_general:liste_types_soins')

        q = request.GET.get('q', '').strip()
        context = _types_soins_context(q)
        context.update({
            'type_soin_to_edit': None,
            'form': form,
            'modifier': False,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/types_soins.html',
            context
        )

    return redirect('parametrage_general:liste_types_soins')


@login_required
def modifier_type_soin(request, pk):
    type_soin = get_object_or_404(TypeSoin, pk=pk)

    if request.method == 'POST':
        form = TypeSoinForm(request.POST, instance=type_soin)

        if form.is_valid():
            form.save()
            messages.success(request, "Le type de soin a été modifié avec succès.")
            return redirect('parametrage_general:liste_types_soins')

        q = request.GET.get('q', '').strip()
        context = _types_soins_context(q)
        context.update({
            'type_soin_to_edit': type_soin,
            'form': form,
            'modifier': True,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/types_soins.html',
            context
        )

    return redirect('parametrage_general:liste_types_soins')


@login_required
def supprimer_type_soin(request, pk):
    type_soin = get_object_or_404(TypeSoin, pk=pk)

    if request.method == 'POST':
        try:
            type_soin.delete()
            messages.success(request, "Le type de soin a été supprimé avec succès.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer ce type de soin car il est utilisé."
            )

    return redirect('parametrage_general:liste_types_soins')


@login_required
def toggle_type_soin(request, pk):
    type_soin = get_object_or_404(TypeSoin, pk=pk)

    if request.method == 'POST':
        type_soin.actif = not type_soin.actif
        type_soin.save(update_fields=['actif', 'updated_at'])

        if type_soin.actif:
            messages.success(request, "Le type de soin a été activé.")
        else:
            messages.success(request, "Le type de soin a été désactivé.")

    return redirect('parametrage_general:liste_types_soins')


def _regimes_alimentaires_context(q=''):
    regimes_alimentaires = RegimeAlimentaire.objects.all()

    if q:
        regimes_alimentaires = regimes_alimentaires.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q)
        )

    regimes_alimentaires = regimes_alimentaires.order_by('ordre', 'nom')

    return {
        'regimes_alimentaires': regimes_alimentaires,
        'total_regimes_alimentaires': RegimeAlimentaire.objects.count(),
        'regimes_alimentaires_actifs': RegimeAlimentaire.objects.filter(actif=True).count(),
        'regimes_alimentaires_inactifs': RegimeAlimentaire.objects.filter(actif=False).count(),
        'q': q,
    }


@login_required
def liste_regimes_alimentaires(request):
    q = request.GET.get('q', '').strip()
    context = _regimes_alimentaires_context(q)
    context.update({
        'regime_alimentaire_to_edit': None,
        'form': RegimeAlimentaireForm(),
        'modifier': False,
    })
    return render(
        request,
        'backend/parametrage_general/pages/hospitalisations/regimes.html',
        context
    )


@login_required
def ajouter_regime_alimentaire(request):
    if request.method == 'POST':
        form = RegimeAlimentaireForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Le régime alimentaire a été ajouté avec succès.")
            return redirect('parametrage_general:liste_regimes_alimentaires')

        q = request.GET.get('q', '').strip()
        context = _regimes_alimentaires_context(q)
        context.update({
            'regime_alimentaire_to_edit': None,
            'form': form,
            'modifier': False,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/regimes_alimentaires.html',
            context
        )

    return redirect('parametrage_general:liste_regimes_alimentaires')


@login_required
def modifier_regime_alimentaire(request, pk):
    regime_alimentaire = get_object_or_404(RegimeAlimentaire, pk=pk)

    if request.method == 'POST':
        form = RegimeAlimentaireForm(request.POST, instance=regime_alimentaire)

        if form.is_valid():
            form.save()
            messages.success(request, "Le régime alimentaire a été modifié avec succès.")
            return redirect('parametrage_general:liste_regimes_alimentaires')

        q = request.GET.get('q', '').strip()
        context = _regimes_alimentaires_context(q)
        context.update({
            'regime_alimentaire_to_edit': regime_alimentaire,
            'form': form,
            'modifier': True,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/regimes_alimentaires.html',
            context
        )

    return redirect('parametrage_general:liste_regimes_alimentaires')


@login_required
def supprimer_regime_alimentaire(request, pk):
    regime_alimentaire = get_object_or_404(RegimeAlimentaire, pk=pk)

    if request.method == 'POST':
        try:
            regime_alimentaire.delete()
            messages.success(request, "Le régime alimentaire a été supprimé avec succès.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer ce régime alimentaire car il est utilisé."
            )

    return redirect('parametrage_general:liste_regimes_alimentaires')


@login_required
def toggle_regime_alimentaire(request, pk):
    regime_alimentaire = get_object_or_404(RegimeAlimentaire, pk=pk)

    if request.method == 'POST':
        regime_alimentaire.actif = not regime_alimentaire.actif
        regime_alimentaire.save(update_fields=['actif', 'updated_at'])

        if regime_alimentaire.actif:
            messages.success(request, "Le régime alimentaire a été activé.")
        else:
            messages.success(request, "Le régime alimentaire a été désactivé.")

    return redirect('parametrage_general:liste_regimes_alimentaires')


def _motifs_hospitalisation_context(q=''):
    motifs = MotifHospitalisation.objects.all()

    if q:
        motifs = motifs.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q)
        )

    motifs = motifs.order_by('ordre', 'nom')

    return {
        'motifs': motifs,
        'total_motifs': MotifHospitalisation.objects.count(),
        'motifs_actifs': MotifHospitalisation.objects.filter(actif=True).count(),
        'motifs_inactifs': MotifHospitalisation.objects.filter(actif=False).count(),
        'q': q,
    }


@login_required
def liste_motifs_hospitalisation(request):
    q = request.GET.get('q', '').strip()
    context = _motifs_hospitalisation_context(q)
    context.update({
        'motif_to_edit': None,
        'form': MotifHospitalisationForm(),
        'modifier': False,
    })
    return render(
        request,
        'backend/parametrage_general/pages/hospitalisations/motifs.html',
        context
    )


@login_required
def ajouter_motif_hospitalisation(request):
    if request.method == 'POST':
        form = MotifHospitalisationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Le motif d'hospitalisation a été ajouté avec succès.")
            return redirect('parametrage_general:liste_motifs_hospitalisation')

        q = request.GET.get('q', '').strip()
        context = _motifs_hospitalisation_context(q)
        context.update({
            'motif_to_edit': None,
            'form': form,
            'modifier': False,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/motifs.html',
            context
        )

    return redirect('parametrage_general:liste_motifs_hospitalisation')


@login_required
def modifier_motif_hospitalisation(request, pk):
    motif = get_object_or_404(MotifHospitalisation, pk=pk)

    if request.method == 'POST':
        form = MotifHospitalisationForm(request.POST, instance=motif)

        if form.is_valid():
            form.save()
            messages.success(request, "Le motif d'hospitalisation a été modifié avec succès.")
            return redirect('parametrage_general:liste_motifs_hospitalisation')

        q = request.GET.get('q', '').strip()
        context = _motifs_hospitalisation_context(q)
        context.update({
            'motif_to_edit': motif,
            'form': form,
            'modifier': True,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/motifs.html',
            context
        )

    return redirect('parametrage_general:liste_motifs_hospitalisation')


@login_required
def supprimer_motif_hospitalisation(request, pk):
    motif = get_object_or_404(MotifHospitalisation, pk=pk)

    if request.method == 'POST':
        try:
            motif.delete()
            messages.success(request, "Le motif d'hospitalisation a été supprimé avec succès.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer ce motif d'hospitalisation car il est utilisé."
            )

    return redirect('parametrage_general:liste_motifs_hospitalisation')


@login_required
def toggle_motif_hospitalisation(request, pk):
    motif = get_object_or_404(MotifHospitalisation, pk=pk)

    if request.method == 'POST':
        motif.actif = not motif.actif
        motif.save(update_fields=['actif', 'updated_at'])

        if motif.actif:
            messages.success(request, "Le motif d'hospitalisation a été activé.")
        else:
            messages.success(request, "Le motif d'hospitalisation a été désactivé.")

    return redirect('parametrage_general:liste_motifs_hospitalisation')


def _types_sortie_context(q=''):
    types_sortie = TypeSortie.objects.all()

    if q:
        types_sortie = types_sortie.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q)
        )

    types_sortie = types_sortie.order_by('ordre', 'nom')

    return {
        'types_sortie': types_sortie,
        'total_types_sortie': TypeSortie.objects.count(),
        'types_sortie_actifs': TypeSortie.objects.filter(actif=True).count(),
        'types_sortie_inactifs': TypeSortie.objects.filter(actif=False).count(),
        'q': q,
    }


@login_required
def liste_types_sortie(request):
    q = request.GET.get('q', '').strip()
    context = _types_sortie_context(q)
    context.update({
        'type_sortie_to_edit': None,
        'form': TypeSortieForm(),
        'modifier': False,
    })
    return render(
        request,
        'backend/parametrage_general/pages/hospitalisations/types_sorties.html',
        context
    )


@login_required
def ajouter_type_sortie(request):
    if request.method == 'POST':
        form = TypeSortieForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Le type de sortie a été ajouté avec succès.")
            return redirect('parametrage_general:liste_types_sortie')

        q = request.GET.get('q', '').strip()
        context = _types_sortie_context(q)
        context.update({
            'type_sortie_to_edit': None,
            'form': form,
            'modifier': False,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/types_sorties.html',
            context
        )

    return redirect('parametrage_general:liste_types_sortie')


@login_required
def modifier_type_sortie(request, pk):
    type_sortie = get_object_or_404(TypeSortie, pk=pk)

    if request.method == 'POST':
        form = TypeSortieForm(request.POST, instance=type_sortie)

        if form.is_valid():
            form.save()
            messages.success(request, "Le type de sortie a été modifié avec succès.")
            return redirect('parametrage_general:liste_types_sortie')

        q = request.GET.get('q', '').strip()
        context = _types_sortie_context(q)
        context.update({
            'type_sortie_to_edit': type_sortie,
            'form': form,
            'modifier': True,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/types_sorties.html',
            context
        )

    return redirect('parametrage_general:liste_types_sortie')


@login_required
def supprimer_type_sortie(request, pk):
    type_sortie = get_object_or_404(TypeSortie, pk=pk)

    if request.method == 'POST':
        try:
            type_sortie.delete()
            messages.success(request, "Le type de sortie a été supprimé avec succès.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer ce type de sortie car il est utilisé."
            )

    return redirect('parametrage_general:liste_types_sortie')


@login_required
def toggle_type_sortie(request, pk):
    type_sortie = get_object_or_404(TypeSortie, pk=pk)

    if request.method == 'POST':
        type_sortie.actif = not type_sortie.actif
        type_sortie.save(update_fields=['actif', 'updated_at'])

        if type_sortie.actif:
            messages.success(request, "Le type de sortie a été activé.")
        else:
            messages.success(request, "Le type de sortie a été désactivé.")

    return redirect('parametrage_general:liste_types_sortie')


def _tarifs_sejours_context(q=''):
    tarifs = TarifSejour.objects.select_related(
        'etablissement',
        'type_sejour',
        'type_chambre'
    ).all()

    if q:
        tarifs = tarifs.filter(
            models.Q(etablissement__nom_etablissement__icontains=q) |
            models.Q(type_sejour__code__icontains=q) |
            models.Q(type_sejour__nom__icontains=q) |
            models.Q(type_chambre__code__icontains=q) |
            models.Q(type_chambre__nom__icontains=q) |
            models.Q(unite_facturation__icontains=q)
        )

    tarifs = tarifs.order_by(
        'etablissement__nom_etablissement',
        'type_sejour__nom',
        'type_chambre__nom',
        '-date_debut'
    )

    return {
        'tarifs': tarifs,
        'total_tarifs': TarifSejour.objects.count(),
        'tarifs_actifs': TarifSejour.objects.filter(actif=True).count(),
        'tarifs_inactifs': TarifSejour.objects.filter(actif=False).count(),
        'q': q,
    }


@login_required
def liste_tarifs_sejours(request):
    q = request.GET.get('q', '').strip()
    context = _tarifs_sejours_context(q)
    context.update({
        'tarif_to_edit': None,
        'form': TarifSejourForm(),
        'modifier': False,
    })
    return render(
        request,
        'backend/parametrage_general/pages/hospitalisations/tarifs.html',
        context
    )


@login_required
def ajouter_tarif_sejour(request):
    if request.method == 'POST':
        form = TarifSejourForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Le tarif de séjour a été ajouté avec succès.")
            return redirect('parametrage_general:liste_tarifs_sejours')

        q = request.GET.get('q', '').strip()
        context = _tarifs_sejours_context(q)
        context.update({
            'tarif_to_edit': None,
            'form': form,
            'modifier': False,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/tarifs.html',
            context
        )

    return redirect('parametrage_general:liste_tarifs_sejours')


@login_required
def modifier_tarif_sejour(request, pk):
    tarif = get_object_or_404(TarifSejour, pk=pk)

    if request.method == 'POST':
        form = TarifSejourForm(request.POST, instance=tarif)

        if form.is_valid():
            form.save()
            messages.success(request, "Le tarif de séjour a été modifié avec succès.")
            return redirect('parametrage_general:liste_tarifs_sejours')

        q = request.GET.get('q', '').strip()
        context = _tarifs_sejours_context(q)
        context.update({
            'tarif_to_edit': tarif,
            'form': form,
            'modifier': True,
        })
        return render(
            request,
            'backend/parametrage_general/pages/hospitalisations/tarifs.html',
            context
        )

    return redirect('parametrage_general:liste_tarifs_sejours')


@login_required
def supprimer_tarif_sejour(request, pk):
    tarif = get_object_or_404(TarifSejour, pk=pk)

    if request.method == 'POST':
        try:
            tarif.delete()
            messages.success(request, "Le tarif de séjour a été supprimé avec succès.")
        except ProtectedError:
            messages.error(
                request,
                "Impossible de supprimer ce tarif de séjour car il est utilisé."
            )

    return redirect('parametrage_general:liste_tarifs_sejours')


@login_required
def toggle_tarif_sejour(request, pk):
    tarif = get_object_or_404(TarifSejour, pk=pk)

    if request.method == 'POST':
        tarif.actif = not tarif.actif
        tarif.save(update_fields=['actif', 'updated_at'])

        if tarif.actif:
            messages.success(request, "Le tarif de séjour a été activé.")
        else:
            messages.success(request, "Le tarif de séjour a été désactivé.")

    return redirect('parametrage_general:liste_tarifs_sejours')