from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from ..forms.pharmacie_partenaire import PharmaciePartenaireForm
from ..models.pharmacie_partenaire import PharmaciePartenaire


# ============================================================
# CONTEXTE COMMUN
# ============================================================

def _get_pharmacies_partenaires_context(request):
    """
    Prépare les données communes utilisées par les différentes vues
    de gestion des pharmacies partenaires.
    """

    pharmacies = PharmaciePartenaire.objects.select_related(
        'ville'
    ).order_by('nom')

    # ------------------------------------------------------------
    # RECHERCHE
    # ------------------------------------------------------------

    search = request.GET.get('q', '').strip()

    if search:
        pharmacies = pharmacies.filter(
            Q(nom__icontains=search)
            | Q(code__icontains=search)
            | Q(telephone__icontains=search)
            | Q(email__icontains=search)
            | Q(pays__icontains=search)
            | Q(quartier__icontains=search)
            | Q(nom_responsable__icontains=search)
            | Q(telephone_responsable__icontains=search)
            | Q(ville__libelle__icontains=search)
        )

    # ------------------------------------------------------------
    # FILTRE STATUT PARTENARIAT
    # ------------------------------------------------------------

    statut = request.GET.get('statut', '').strip()

    if statut:
        pharmacies = pharmacies.filter(
            statut_partenariat=statut
        )

    # ------------------------------------------------------------
    # FILTRE ACTIVITÉ
    # ------------------------------------------------------------

    actif = request.GET.get('actif', '').strip()

    if actif == '1':
        pharmacies = pharmacies.filter(
            actif=True
        )

    elif actif == '0':
        pharmacies = pharmacies.filter(
            actif=False
        )

    # ------------------------------------------------------------
    # STATISTIQUES
    # ------------------------------------------------------------

    total = PharmaciePartenaire.objects.count()

    actives = PharmaciePartenaire.objects.filter(
        actif=True,
        statut_partenariat='active'
    ).count()

    inactives = PharmaciePartenaire.objects.filter(
        actif=False
    ).count()

    suspendues = PharmaciePartenaire.objects.filter(
        statut_partenariat='suspendue'
    ).count()

    return {
        'pharmacies': pharmacies,
        'search': search,
        'statut': statut,
        'actif': actif,
        'total': total,
        'actives': actives,
        'inactives': inactives,
        'suspendues': suspendues,
    }


# ============================================================
# LISTE
# ============================================================

@login_required
def liste_pharmacies_partenaires(request):
    """
    Affiche la liste des pharmacies partenaires.
    """

    context = _get_pharmacies_partenaires_context(request)

    # Formulaire vide utilisé par la modale "Ajouter"
    form = PharmaciePartenaireForm()

    context.update({
        'form': form,
        'mode': 'ajout',
        'titre_page': 'Ajouter une pharmacie partenaire',
    })

    return render(
        request,
        'backend/parametrage_general/pages/pharmacies_partenaires/liste.html',
        context
    )


# ============================================================
# AJOUT
# ============================================================

@login_required
def ajouter_pharmacie_partenaire(request):
    """
    Ajoute une nouvelle pharmacie partenaire.
    Le formulaire est affiché dans la page liste.
    """

    if request.method == 'POST':

        form = PharmaciePartenaireForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            pharmacie = form.save()

            messages.success(
                request,
                f"La pharmacie partenaire « {pharmacie.nom} » "
                "a été ajoutée avec succès."
            )

            return redirect(
                'parametrage_general:liste_pharmacies_partenaires'
            )

    else:

        form = PharmaciePartenaireForm()

    context = _get_pharmacies_partenaires_context(request)

    context.update({
        'form': form,
        'mode': 'ajout',
        'titre_page': 'Ajouter une pharmacie partenaire',
        'ouvrir_modal': True,
    })

    return render(
        request,
        'backend/parametrage_general/pages/pharmacies_partenaires/liste.html',
        context
    )


# ============================================================
# MODIFICATION
# ============================================================

@login_required
def modifier_pharmacie_partenaire(request, pk):
    """
    Modifie une pharmacie partenaire existante.
    Le formulaire est affiché dans la page liste.
    """

    pharmacie = get_object_or_404(
        PharmaciePartenaire,
        pk=pk
    )

    if request.method == 'POST':

        form = PharmaciePartenaireForm(
            request.POST,
            request.FILES,
            instance=pharmacie
        )

        if form.is_valid():

            pharmacie = form.save()

            messages.success(
                request,
                f"La pharmacie partenaire « {pharmacie.nom} » "
                "a été modifiée avec succès."
            )

            return redirect(
                'parametrage_general:details_pharmacie_partenaire',
                pk=pharmacie.pk
            )

    else:

        form = PharmaciePartenaireForm(
            instance=pharmacie
        )

    context = _get_pharmacies_partenaires_context(request)

    context.update({
        'form': form,
        'pharmacie': pharmacie,
        'mode': 'modification',
        'titre_page': 'Modifier la pharmacie partenaire',
        'ouvrir_modal': True,
    })

    return render(
        request,
        'backend/parametrage_general/pages/pharmacies_partenaires/liste.html',
        context
    )


# ============================================================
# DÉTAILS
# ============================================================

@login_required
def details_pharmacie_partenaire(request, pk):
    """
    Affiche les informations détaillées d'une pharmacie partenaire.
    """

    pharmacie = get_object_or_404(
        PharmaciePartenaire.objects.select_related(
            'ville'
        ),
        pk=pk
    )

    context = {
        'pharmacie': pharmacie,
    }

    return render(
        request,
        'backend/parametrage_general/pages/pharmacies_partenaires/details.html',
        context
    )


# ============================================================
# SUPPRESSION
# ============================================================

@login_required
def supprimer_pharmacie_partenaire(request, pk):
    """
    Supprime une pharmacie partenaire après confirmation POST.
    """

    pharmacie = get_object_or_404(
        PharmaciePartenaire,
        pk=pk
    )

    if request.method == 'POST':

        nom = pharmacie.nom

        pharmacie.delete()

        messages.success(
            request,
            f"La pharmacie partenaire « {nom} » "
            "a été supprimée avec succès."
        )

    return redirect(
        'parametrage_general:liste_pharmacies_partenaires'
    )


# ============================================================
# ACTIVATION / DÉSACTIVATION
# ============================================================

@login_required
def toggle_pharmacie_partenaire(request, pk):
    """
    Active ou désactive une pharmacie partenaire.
    """

    pharmacie = get_object_or_404(
        PharmaciePartenaire,
        pk=pk
    )

    if request.method != 'POST':

        return redirect(
            'parametrage_general:liste_pharmacies_partenaires'
        )

    pharmacie.actif = not pharmacie.actif

    pharmacie.save(
        update_fields=[
            'actif',
            'updated_at',
        ]
    )

    if pharmacie.actif:

        messages.success(
            request,
            f"La pharmacie partenaire « {pharmacie.nom} » "
            "a été activée."
        )

    else:

        messages.warning(
            request,
            f"La pharmacie partenaire « {pharmacie.nom} » "
            "a été désactivée."
        )

    return redirect(
        request.POST.get(
            'next',
            'parametrage_general:liste_pharmacies_partenaires'
        )
    )