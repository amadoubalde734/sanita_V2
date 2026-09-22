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


# ==========================================
# HELPERS — centralisent le calcul des querysets/stats,
# repris à l'identique dans liste/ajouter/modifier pour
# chaque entité, pour éviter la duplication.
# ==========================================
def _types_sejours_context(q=''):
    types = TypeSejour.objects.all()
    if q:
        types = types.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q)
        )
    types = types.order_by('ordre', 'nom')

    return {
        'types': types,
        'total_types': TypeSejour.objects.count(),
        'types_actifs': TypeSejour.objects.filter(actif=True).count(),
        'types_inactifs': TypeSejour.objects.filter(actif=False).count(),
        'q': q,
    }


def _types_chambres_context(q=''):
    types = TypeChambre.objects.all()
    if q:
        types = types.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q)
        )
    types = types.order_by('ordre', 'nom')

    return {
        'types': types,
        'total_types': TypeChambre.objects.count(),
        'types_actifs': TypeChambre.objects.filter(actif=True).count(),
        'types_inactifs': TypeChambre.objects.filter(actif=False).count(),
        'q': q,
    }


def _chambres_context(q=''):
    chambres = Chambre.objects.select_related(
        'etablissement', 'unite', 'unite__service', 'type_chambre'
    ).all()
    if q:
        chambres = chambres.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(etage__icontains=q) |
            models.Q(localisation__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(etablissement__nom__icontains=q) |
            models.Q(unite__nom__icontains=q) |
            models.Q(unite__service__nom__icontains=q) |
            models.Q(type_chambre__nom__icontains=q)
        )
    chambres = chambres.order_by('etablissement__nom', 'unite__nom', 'code')

    return {
        'chambres': chambres,
        'total_chambres': Chambre.objects.count(),
        'chambres_actives': Chambre.objects.filter(actif=True).count(),
        'chambres_inactives': Chambre.objects.filter(actif=False).count(),
        'q': q,
    }


def _lits_context(q=''):
    lits = Lit.objects.select_related(
        'chambre', 'chambre__etablissement', 'chambre__unite',
        'chambre__unite__service', 'chambre__type_chambre'
    ).all()
    if q:
        lits = lits.filter(
            models.Q(code__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(statut__icontains=q) |
            models.Q(chambre__code__icontains=q) |
            models.Q(chambre__nom__icontains=q) |
            models.Q(chambre__unite__nom__icontains=q) |
            models.Q(chambre__unite__service__nom__icontains=q) |
            models.Q(chambre__etablissement__nom__icontains=q)
        )
    lits = lits.order_by('chambre__etablissement__nom', 'chambre__unite__nom', 'chambre__code', 'code')

    return {
        'lits': lits,
        'total_lits': Lit.objects.count(),
        'lits_actifs': Lit.objects.filter(actif=True).count(),
        'lits_inactifs': Lit.objects.filter(actif=False).count(),
        'q': q,
    }


def _types_soins_context(q=''):
    types = TypeSoin.objects.all()
    if q:
        types = types.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(categorie__icontains=q) |
            models.Q(description__icontains=q)
        )
    types = types.order_by('ordre', 'nom')

    return {
        'types': types,
        'total_types': TypeSoin.objects.count(),
        'types_actifs': TypeSoin.objects.filter(actif=True).count(),
        'types_inactifs': TypeSoin.objects.filter(actif=False).count(),
        'q': q,
    }


def _regimes_context(q=''):
    regimes = RegimeAlimentaire.objects.all()
    if q:
        regimes = regimes.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q)
        )
    regimes = regimes.order_by('ordre', 'nom')

    return {
        'regimes': regimes,
        'total_regimes': RegimeAlimentaire.objects.count(),
        'regimes_actifs': RegimeAlimentaire.objects.filter(actif=True).count(),
        'regimes_inactifs': RegimeAlimentaire.objects.filter(actif=False).count(),
        'q': q,
    }


def _motifs_context(q=''):
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


def _types_sortie_context(q=''):
    types = TypeSortie.objects.all()
    if q:
        types = types.filter(
            models.Q(code__icontains=q) |
            models.Q(nom__icontains=q) |
            models.Q(description__icontains=q)
        )
    types = types.order_by('ordre', 'nom')

    return {
        'types': types,
        'total_types': TypeSortie.objects.count(),
        'types_actifs': TypeSortie.objects.filter(actif=True).count(),
        'types_inactifs': TypeSortie.objects.filter(actif=False).count(),
        'q': q,
    }


def _tarifs_sejours_context(q=''):
    tarifs = TarifSejour.objects.select_related(
        'etablissement', 'type_sejour', 'type_chambre'
    ).all()
    if q:
        tarifs = tarifs.filter(
            models.Q(type_sejour__code__icontains=q) |
            models.Q(type_sejour__nom__icontains=q) |
            models.Q(type_chambre__code__icontains=q) |
            models.Q(type_chambre__nom__icontains=q) |
            models.Q(etablissement__nom__icontains=q) |
            models.Q(unite_facturation__icontains=q)
        )
    tarifs = tarifs.order_by('-date_debut')

    return {
        'tarifs': tarifs,
        'total_tarifs': TarifSejour.objects.count(),
        'tarifs_actifs': TarifSejour.objects.filter(actif=True).count(),
        'tarifs_inactifs': TarifSejour.objects.filter(actif=False).count(),
        'q': q,
    }


# ==========================================
# TYPES DE SEJOURS
# ==========================================
@login_required
def liste_types_sejours(request):
    q = request.GET.get('q', '').strip()
    context = _types_sejours_context(q)
    context.update({'type_to_edit': None, 'form': TypeSejourForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/types.html', context)


@login_required
def ajouter_type_sejour(request):
    form = TypeSejourForm()

    if request.method == 'POST':
        form = TypeSejourForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le type de séjour a été ajouté avec succès.")
            return redirect('parametrage_general:liste_types_sejours')

    context = _types_sejours_context()
    context.update({'type_to_edit': None, 'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/types.html', context)


@login_required
def modifier_type_sejour(request, pk):
    type_sejour = get_object_or_404(TypeSejour, pk=pk)

    if request.method == 'POST':
        form = TypeSejourForm(request.POST, instance=type_sejour)
        if form.is_valid():
            form.save()
            messages.success(request, "Le type de séjour a été modifié avec succès.")
            return redirect('parametrage_general:liste_types_sejours')
    else:
        form = TypeSejourForm(instance=type_sejour)

    context = _types_sejours_context()
    context.update({'type_to_edit': type_sejour, 'form': form, 'modifier': True})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/types.html', context)


@login_required
def supprimer_type_sejour(request, pk):
    type_sejour = get_object_or_404(TypeSejour, pk=pk)

    if request.method == 'POST':
        try:
            type_sejour.delete()
            messages.success(request, "Le type de séjour a été supprimé avec succès.")
        except ProtectedError:
            messages.error(request, "Ce type de séjour ne peut pas être supprimé car il est utilisé.")

    return redirect('parametrage_general:liste_types_sejours')


@login_required
def toggle_type_sejour(request, pk):
    type_sejour = get_object_or_404(TypeSejour, pk=pk)
    type_sejour.actif = not type_sejour.actif
    type_sejour.save(update_fields=['actif', 'updated_at'])
    messages.success(request, "Le statut du type de séjour a été mis à jour.")
    return redirect('parametrage_general:liste_types_sejours')


# ==========================================
# TYPES DE CHAMBRES
# ==========================================
@login_required
def liste_types_chambres(request):
    q = request.GET.get('q', '').strip()
    context = _types_chambres_context(q)
    context.update({'type_to_edit': None, 'form': TypeChambreForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/types_chambres.html', context)


@login_required
def ajouter_type_chambre(request):
    form = TypeChambreForm()

    if request.method == 'POST':
        form = TypeChambreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le type de chambre a été ajouté avec succès.")
            return redirect('parametrage_general:liste_types_chambres')

    context = _types_chambres_context()
    context.update({'type_to_edit': None, 'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/types_chambres.html', context)


@login_required
def modifier_type_chambre(request, pk):
    type_chambre = get_object_or_404(TypeChambre, pk=pk)

    if request.method == 'POST':
        form = TypeChambreForm(request.POST, instance=type_chambre)
        if form.is_valid():
            form.save()
            messages.success(request, "Le type de chambre a été modifié avec succès.")
            return redirect('parametrage_general:liste_types_chambres')
    else:
        form = TypeChambreForm(instance=type_chambre)

    context = _types_chambres_context()
    context.update({'type_to_edit': type_chambre, 'form': form, 'modifier': True})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/types_chambres.html', context)


@login_required
def supprimer_type_chambre(request, pk):
    type_chambre = get_object_or_404(TypeChambre, pk=pk)

    if request.method == 'POST':
        try:
            type_chambre.delete()
            messages.success(request, "Le type de chambre a été supprimé avec succès.")
        except ProtectedError:
            messages.error(request, "Ce type de chambre ne peut pas être supprimé car il est utilisé.")

    return redirect('parametrage_general:liste_types_chambres')


@login_required
def toggle_type_chambre(request, pk):
    type_chambre = get_object_or_404(TypeChambre, pk=pk)
    type_chambre.actif = not type_chambre.actif
    type_chambre.save(update_fields=['actif', 'updated_at'])
    messages.success(request, "Le statut du type de chambre a été mis à jour.")
    return redirect('parametrage_general:liste_types_chambres')


# ==========================================
# CHAMBRES
# ==========================================
@login_required
def liste_chambres(request):
    q = request.GET.get('q', '').strip()
    context = _chambres_context(q)
    context.update({'chambre_to_edit': None, 'form': ChambreForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/chambres.html', context)


@login_required
def ajouter_chambre(request):
    form = ChambreForm()

    if request.method == 'POST':
        form = ChambreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La chambre a été ajoutée avec succès.")
            return redirect('parametrage_general:liste_chambres')

    context = _chambres_context()
    context.update({'chambre_to_edit': None, 'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/chambres.html', context)


@login_required
def modifier_chambre(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)

    if request.method == 'POST':
        form = ChambreForm(request.POST, instance=chambre)
        if form.is_valid():
            form.save()
            messages.success(request, "La chambre a été modifiée avec succès.")
            return redirect('parametrage_general:liste_chambres')
    else:
        form = ChambreForm(instance=chambre)

    context = _chambres_context()
    context.update({'chambre_to_edit': chambre, 'form': form, 'modifier': True})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/chambres.html', context)


@login_required
def supprimer_chambre(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)

    if request.method == 'POST':
        try:
            chambre.delete()
            messages.success(request, "La chambre a été supprimée avec succès.")
        except ProtectedError:
            messages.error(request, "Cette chambre ne peut pas être supprimée car elle est utilisée.")

    return redirect('parametrage_general:liste_chambres')


@login_required
def toggle_chambre(request, pk):
    chambre = get_object_or_404(Chambre, pk=pk)
    chambre.actif = not chambre.actif
    chambre.save(update_fields=['actif', 'updated_at'])
    messages.success(request, "Le statut de la chambre a été mis à jour.")
    return redirect('parametrage_general:liste_chambres')


# ==========================================
# LITS
# ==========================================
@login_required
def liste_lits(request):
    q = request.GET.get('q', '').strip()
    context = _lits_context(q)
    context.update({'lit_to_edit': None, 'form': LitForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/lits.html', context)


@login_required
def ajouter_lit(request):
    form = LitForm()

    if request.method == 'POST':
        form = LitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le lit a été ajouté avec succès.")
            return redirect('parametrage_general:liste_lits')

    context = _lits_context()
    context.update({'lit_to_edit': None, 'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/lits.html', context)


@login_required
def modifier_lit(request, pk):
    lit = get_object_or_404(Lit, pk=pk)

    if request.method == 'POST':
        form = LitForm(request.POST, instance=lit)
        if form.is_valid():
            form.save()
            messages.success(request, "Le lit a été modifié avec succès.")
            return redirect('parametrage_general:liste_lits')
    else:
        form = LitForm(instance=lit)

    context = _lits_context()
    context.update({'lit_to_edit': lit, 'form': form, 'modifier': True})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/lits.html', context)


@login_required
def supprimer_lit(request, pk):
    lit = get_object_or_404(Lit, pk=pk)

    if request.method == 'POST':
        try:
            lit.delete()
            messages.success(request, "Le lit a été supprimé avec succès.")
        except ProtectedError:
            messages.error(request, "Ce lit ne peut pas être supprimé car il est utilisé.")

    return redirect('parametrage_general:liste_lits')


@login_required
def toggle_lit(request, pk):
    lit = get_object_or_404(Lit, pk=pk)
    lit.actif = not lit.actif
    lit.save(update_fields=['actif', 'updated_at'])
    messages.success(request, "Le statut du lit a été mis à jour.")
    return redirect('parametrage_general:liste_lits')


# ==========================================
# TYPES DE SOINS
# ==========================================
@login_required
def liste_types_soins(request):
    q = request.GET.get('q', '').strip()
    context = _types_soins_context(q)
    context.update({'type_to_edit': None, 'form': TypeSoinForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/soins.html', context)


@login_required
def ajouter_type_soin(request):
    form = TypeSoinForm()

    if request.method == 'POST':
        form = TypeSoinForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le type de soin a été ajouté avec succès.")
            return redirect('parametrage_general:liste_types_soins')

    context = _types_soins_context()
    context.update({'type_to_edit': None, 'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/soins.html', context)


@login_required
def modifier_type_soin(request, pk):
    type_soin = get_object_or_404(TypeSoin, pk=pk)

    if request.method == 'POST':
        form = TypeSoinForm(request.POST, instance=type_soin)
        if form.is_valid():
            form.save()
            messages.success(request, "Le type de soin a été modifié avec succès.")
            return redirect('parametrage_general:liste_types_soins')
    else:
        form = TypeSoinForm(instance=type_soin)

    context = _types_soins_context()
    context.update({'type_to_edit': type_soin, 'form': form, 'modifier': True})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/soins.html', context)


@login_required
def supprimer_type_soin(request, pk):
    type_soin = get_object_or_404(TypeSoin, pk=pk)

    if request.method == 'POST':
        try:
            type_soin.delete()
            messages.success(request, "Le type de soin a été supprimé avec succès.")
        except ProtectedError:
            messages.error(request, "Ce type de soin ne peut pas être supprimé car il est utilisé.")

    return redirect('parametrage_general:liste_types_soins')


@login_required
def toggle_type_soin(request, pk):
    type_soin = get_object_or_404(TypeSoin, pk=pk)
    type_soin.actif = not type_soin.actif
    type_soin.save(update_fields=['actif', 'updated_at'])
    messages.success(request, "Le statut du type de soin a été mis à jour.")
    return redirect('parametrage_general:liste_types_soins')


# ==========================================
# REGIMES ALIMENTAIRES
# ==========================================
@login_required
def liste_regimes_alimentaires(request):
    q = request.GET.get('q', '').strip()
    context = _regimes_context(q)
    context.update({'regime_to_edit': None, 'form': RegimeAlimentaireForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/regimes.html', context)


@login_required
def ajouter_regime_alimentaire(request):
    form = RegimeAlimentaireForm()

    if request.method == 'POST':
        form = RegimeAlimentaireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le régime alimentaire a été ajouté avec succès.")
            return redirect('parametrage_general:liste_regimes_alimentaires')

    context = _regimes_context()
    context.update({'regime_to_edit': None, 'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/regimes.html', context)


@login_required
def modifier_regime_alimentaire(request, pk):
    regime = get_object_or_404(RegimeAlimentaire, pk=pk)

    if request.method == 'POST':
        form = RegimeAlimentaireForm(request.POST, instance=regime)
        if form.is_valid():
            form.save()
            messages.success(request, "Le régime alimentaire a été modifié avec succès.")
            return redirect('parametrage_general:liste_regimes_alimentaires')
    else:
        form = RegimeAlimentaireForm(instance=regime)

    context = _regimes_context()
    context.update({'regime_to_edit': regime, 'form': form, 'modifier': True})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/regimes.html', context)


@login_required
def supprimer_regime_alimentaire(request, pk):
    regime = get_object_or_404(RegimeAlimentaire, pk=pk)

    if request.method == 'POST':
        try:
            regime.delete()
            messages.success(request, "Le régime alimentaire a été supprimé avec succès.")
        except ProtectedError:
            messages.error(request, "Ce régime alimentaire ne peut pas être supprimé car il est utilisé.")

    return redirect('parametrage_general:liste_regimes_alimentaires')


@login_required
def toggle_regime_alimentaire(request, pk):
    regime = get_object_or_404(RegimeAlimentaire, pk=pk)
    regime.actif = not regime.actif
    regime.save(update_fields=['actif', 'updated_at'])
    messages.success(request, "Le statut du régime alimentaire a été mis à jour.")
    return redirect('parametrage_general:liste_regimes_alimentaires')


# ==========================================
# MOTIFS D'HOSPITALISATION
# ==========================================
@login_required
def liste_motifs_hospitalisation(request):
    q = request.GET.get('q', '').strip()
    context = _motifs_context(q)
    context.update({'motif_to_edit': None, 'form': MotifHospitalisationForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/motifs.html', context)


@login_required
def ajouter_motif_hospitalisation(request):
    form = MotifHospitalisationForm()

    if request.method == 'POST':
        form = MotifHospitalisationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le motif d'hospitalisation a été ajouté avec succès.")
            return redirect('parametrage_general:liste_motifs_hospitalisation')

    context = _motifs_context()
    context.update({'motif_to_edit': None, 'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/motifs.html', context)


@login_required
def modifier_motif_hospitalisation(request, pk):
    motif = get_object_or_404(MotifHospitalisation, pk=pk)

    if request.method == 'POST':
        form = MotifHospitalisationForm(request.POST, instance=motif)
        if form.is_valid():
            form.save()
            messages.success(request, "Le motif d'hospitalisation a été modifié avec succès.")
            return redirect('parametrage_general:liste_motifs_hospitalisation')
    else:
        form = MotifHospitalisationForm(instance=motif)

    context = _motifs_context()
    context.update({'motif_to_edit': motif, 'form': form, 'modifier': True})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/motifs.html', context)


@login_required
def supprimer_motif_hospitalisation(request, pk):
    motif = get_object_or_404(MotifHospitalisation, pk=pk)

    if request.method == 'POST':
        try:
            motif.delete()
            messages.success(request, "Le motif d'hospitalisation a été supprimé avec succès.")
        except ProtectedError:
            messages.error(request, "Ce motif ne peut pas être supprimé car il est utilisé.")

    return redirect('parametrage_general:liste_motifs_hospitalisation')


@login_required
def toggle_motif_hospitalisation(request, pk):
    motif = get_object_or_404(MotifHospitalisation, pk=pk)
    motif.actif = not motif.actif
    motif.save(update_fields=['actif', 'updated_at'])
    messages.success(request, "Le statut du motif d'hospitalisation a été mis à jour.")
    return redirect('parametrage_general:liste_motifs_hospitalisation')


# ==========================================
# TYPES DE SORTIE
# ==========================================
@login_required
def liste_types_sortie(request):
    q = request.GET.get('q', '').strip()
    context = _types_sortie_context(q)
    context.update({'type_to_edit': None, 'form': TypeSortieForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/sorties.html', context)


@login_required
def ajouter_type_sortie(request):
    form = TypeSortieForm()

    if request.method == 'POST':
        form = TypeSortieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le type de sortie a été ajouté avec succès.")
            return redirect('parametrage_general:liste_types_sortie')

    context = _types_sortie_context()
    context.update({'type_to_edit': None, 'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/sorties.html', context)


@login_required
def modifier_type_sortie(request, pk):
    type_sortie = get_object_or_404(TypeSortie, pk=pk)

    if request.method == 'POST':
        form = TypeSortieForm(request.POST, instance=type_sortie)
        if form.is_valid():
            form.save()
            messages.success(request, "Le type de sortie a été modifié avec succès.")
            return redirect('parametrage_general:liste_types_sortie')
    else:
        form = TypeSortieForm(instance=type_sortie)

    context = _types_sortie_context()
    context.update({'type_to_edit': type_sortie, 'form': form, 'modifier': True})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/sorties.html', context)


@login_required
def supprimer_type_sortie(request, pk):
    type_sortie = get_object_or_404(TypeSortie, pk=pk)

    if request.method == 'POST':
        try:
            type_sortie.delete()
            messages.success(request, "Le type de sortie a été supprimé avec succès.")
        except ProtectedError:
            messages.error(request, "Ce type de sortie ne peut pas être supprimé car il est utilisé.")

    return redirect('parametrage_general:liste_types_sortie')


@login_required
def toggle_type_sortie(request, pk):
    type_sortie = get_object_or_404(TypeSortie, pk=pk)
    type_sortie.actif = not type_sortie.actif
    type_sortie.save(update_fields=['actif', 'updated_at'])
    messages.success(request, "Le statut du type de sortie a été mis à jour.")
    return redirect('parametrage_general:liste_types_sortie')


# ==========================================
# TARIFS DE SEJOURS
# ==========================================
@login_required
def liste_tarifs_sejours(request):
    q = request.GET.get('q', '').strip()
    context = _tarifs_sejours_context(q)
    context.update({'tarif_to_edit': None, 'form': TarifSejourForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/tarifs.html', context)


@login_required
def ajouter_tarif_sejour(request):
    form = TarifSejourForm()

    if request.method == 'POST':
        form = TarifSejourForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le tarif de séjour a été ajouté avec succès.")
            return redirect('parametrage_general:liste_tarifs_sejours')

    context = _tarifs_sejours_context()
    context.update({'tarif_to_edit': None, 'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/tarifs.html', context)


@login_required
def modifier_tarif_sejour(request, pk):
    tarif = get_object_or_404(TarifSejour, pk=pk)

    if request.method == 'POST':
        form = TarifSejourForm(request.POST, instance=tarif)
        if form.is_valid():
            form.save()
            messages.success(request, "Le tarif de séjour a été modifié avec succès.")
            return redirect('parametrage_general:liste_tarifs_sejours')
    else:
        form = TarifSejourForm(instance=tarif)

    context = _tarifs_sejours_context()
    context.update({'tarif_to_edit': tarif, 'form': form, 'modifier': True})
    return render(request, 'backend/parametrage_general/pages/hospitalisation/tarifs.html', context)


@login_required
def supprimer_tarif_sejour(request, pk):
    tarif = get_object_or_404(TarifSejour, pk=pk)

    if request.method == 'POST':
        try:
            tarif.delete()
            messages.success(request, "Le tarif de séjour a été supprimé avec succès.")
        except ProtectedError:
            messages.error(request, "Ce tarif ne peut pas être supprimé car il est utilisé.")

    return redirect('parametrage_general:liste_tarifs_sejours')


@login_required
def toggle_tarif_sejour(request, pk):
    tarif = get_object_or_404(TarifSejour, pk=pk)
    tarif.actif = not tarif.actif
    tarif.save(update_fields=['actif', 'updated_at'])
    messages.success(request, "Le statut du tarif de séjour a été mis à jour.")
    return redirect('parametrage_general:liste_tarifs_sejours')