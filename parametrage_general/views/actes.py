from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import (
    CategorieActeForm,
    ActeMedicalForm,
    TarifActeForm,
)

from ..models import (
    CategorieActe,
    ActeMedical,
    TarifActe,
)


# ==========================================
# HELPERS — évitent de recalculer les mêmes
# querysets/stats à chaque vue (liste/ajout/édition)
# ==========================================
def _categories_context(search_query=''):
    categories = CategorieActe.objects.all()
    if search_query:
        categories = categories.filter(nom__icontains=search_query)
    categories = categories.order_by('nom')

    total = CategorieActe.objects.count()
    actives = CategorieActe.objects.filter(actif=True).count()

    return {
        'categories': categories,
        'search_query': search_query,
        'total_categories': total,
        'active_categories': actives,
        'inactive_categories': total - actives,
    }


def _actes_context(search_query=''):
    actes = ActeMedical.objects.select_related('categorie').all()
    if search_query:
        actes = actes.filter(
            models.Q(code__icontains=search_query) |
            models.Q(libelle__icontains=search_query)
        )
    actes = actes.order_by('libelle')

    total = ActeMedical.objects.count()
    actives = ActeMedical.objects.filter(actif=True).count()

    return {
        'actes': actes,
        'categories': CategorieActe.objects.filter(actif=True).order_by('nom'),
        'search_query': search_query,
        'total_actes': total,
        'active_actes': actives,
        'inactive_actes': total - actives,
    }


def _tarifs_context(search_query=''):
    tarifs = TarifActe.objects.select_related('acte', 'etablissement').all()
    if search_query:
        tarifs = tarifs.filter(
            models.Q(acte__libelle__icontains=search_query) |
            models.Q(acte__code__icontains=search_query)
        )
    tarifs = tarifs.order_by('-date_debut')

    total = TarifActe.objects.count()
    actives = TarifActe.objects.filter(actif=True).count()

    return {
        'tarifs': tarifs,
        'search_query': search_query,
        'total_tarifs': total,
        'active_tarifs': actives,
        'inactive_tarifs': total - actives,
    }


# ==========================================
# CATEGORIES D'ACTES
# ==========================================
@login_required
def liste_categories_actes(request):
    search_query = request.GET.get('q', '').strip()
    context = _categories_context(search_query)
    context.update({'form': CategorieActeForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/actes/categories.html', context)


@login_required
def ajouter_categorie_acte(request):
    form = CategorieActeForm()

    if request.method == 'POST':
        form = CategorieActeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie d'acte ajoutée avec succès.")
            return redirect('parametrage_general:liste_categories_actes')

    context = _categories_context()
    context.update({'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/actes/categories.html', context)


@login_required
def modifier_categorie_acte(request, pk):
    categorie = get_object_or_404(CategorieActe, pk=pk)

    if request.method == 'POST':
        form = CategorieActeForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie d'acte modifiée avec succès.")
            return redirect('parametrage_general:liste_categories_actes')
    else:
        form = CategorieActeForm(instance=categorie)

    context = _categories_context()
    context.update({'form': form, 'modifier': True, 'categorie_to_edit': categorie})
    return render(request, 'backend/parametrage_general/pages/actes/categories.html', context)


@login_required
def supprimer_categorie_acte(request, pk):
    categorie = get_object_or_404(CategorieActe, pk=pk)

    if request.method == 'POST':
        if categorie.actes.exists():
            messages.error(
                request,
                f"Impossible de supprimer « {categorie.nom} » : "
                "des actes médicaux y sont encore rattachés."
            )
        else:
            categorie.delete()
            messages.success(request, "Catégorie d'acte supprimée avec succès.")

    return redirect('parametrage_general:liste_categories_actes')


@login_required
def toggle_categorie_acte(request, pk):
    categorie = get_object_or_404(CategorieActe, pk=pk)
    categorie.actif = not categorie.actif
    categorie.save(update_fields=['actif'])
    status = "activée" if categorie.actif else "désactivée"
    messages.success(request, f"La catégorie a été {status}.")
    return redirect('parametrage_general:liste_categories_actes')


# ==========================================
# ACTES MEDICAUX
# ==========================================
@login_required
def liste_actes_medicaux(request):
    search_query = request.GET.get('q', '').strip()
    context = _actes_context(search_query)
    context.update({'form': ActeMedicalForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/actes/actes.html', context)


@login_required
def ajouter_acte_medical(request):
    form = ActeMedicalForm()

    if request.method == 'POST':
        form = ActeMedicalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Acte médical ajouté avec succès.')
            return redirect('parametrage_general:liste_actes_medicaux')

    context = _actes_context()
    context.update({'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/actes/actes.html', context)


@login_required
def modifier_acte_medical(request, pk):
    acte = get_object_or_404(ActeMedical, pk=pk)

    if request.method == 'POST':
        form = ActeMedicalForm(request.POST, instance=acte)
        if form.is_valid():
            form.save()
            messages.success(request, 'Acte médical modifié avec succès.')
            return redirect('parametrage_general:liste_actes_medicaux')
    else:
        form = ActeMedicalForm(instance=acte)

    context = _actes_context()
    context.update({'form': form, 'modifier': True, 'acte_to_edit': acte})
    return render(request, 'backend/parametrage_general/pages/actes/actes.html', context)


@login_required
def supprimer_acte_medical(request, pk):
    acte = get_object_or_404(ActeMedical, pk=pk)

    if request.method == 'POST':
        if acte.tarifs.exists():
            messages.error(
                request,
                f"Impossible de supprimer « {acte.libelle} » : "
                "des tarifs y sont encore rattachés."
            )
        else:
            acte.delete()
            messages.success(request, 'Acte médical supprimé avec succès.')

    return redirect('parametrage_general:liste_actes_medicaux')


@login_required
def toggle_acte_medical(request, pk):
    acte = get_object_or_404(ActeMedical, pk=pk)
    acte.actif = not acte.actif
    acte.save(update_fields=['actif'])
    status = "activé" if acte.actif else "désactivé"
    messages.success(request, f"L'acte a été {status}.")
    return redirect('parametrage_general:liste_actes_medicaux')


# ==========================================
# TARIFS D'ACTES
# ==========================================
@login_required
def liste_tarifs_actes(request):
    search_query = request.GET.get('q', '').strip()
    context = _tarifs_context(search_query)
    context.update({'form': TarifActeForm(), 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/actes/tarifs.html', context)


@login_required
def ajouter_tarif_acte(request):
    form = TarifActeForm()

    if request.method == 'POST':
        form = TarifActeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarif ajouté avec succès.')
            return redirect('parametrage_general:liste_tarifs_actes')

    context = _tarifs_context()
    context.update({'form': form, 'modifier': False})
    return render(request, 'backend/parametrage_general/pages/actes/tarifs.html', context)


@login_required
def modifier_tarif_acte(request, pk):
    tarif = get_object_or_404(TarifActe, pk=pk)

    if request.method == 'POST':
        form = TarifActeForm(request.POST, instance=tarif)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarif modifié avec succès.')
            return redirect('parametrage_general:liste_tarifs_actes')
    else:
        form = TarifActeForm(instance=tarif)

    context = _tarifs_context()
    context.update({'form': form, 'modifier': True, 'tarif_to_edit': tarif})
    return render(request, 'backend/parametrage_general/pages/actes/tarifs.html', context)


@login_required
def supprimer_tarif_acte(request, pk):
    tarif = get_object_or_404(TarifActe, pk=pk)

    if request.method == 'POST':
        tarif.delete()
        messages.success(request, 'Tarif supprimé avec succès.')

    return redirect('parametrage_general:liste_tarifs_actes')


@login_required
def toggle_tarif_acte(request, pk):
    tarif = get_object_or_404(TarifActe, pk=pk)
    tarif.actif = not tarif.actif
    tarif.save(update_fields=['actif'])
    status = "activé" if tarif.actif else "désactivé"
    messages.success(request, f"Le tarif a été {status}.")
    return redirect('parametrage_general:liste_tarifs_actes')