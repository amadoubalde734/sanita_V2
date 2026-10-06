from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Pharmacie
from ..forms import PharmacieForm


# ============================================================
# OUTIL : CONTEXTE COMMUN
# ============================================================

def _get_pharmacies_context(
    form=None,
    modifier=False,
    pharmacie_to_edit=None,
    recherche='',
    type_pharmacie_selectionne='',
    statut_partenaire_selectionne=''
):
    """
    Prépare le contexte commun utilisé par la page
    de gestion des pharmacies.
    """

    pharmacies = (
        Pharmacie.objects
        .select_related(
            'ville',
            'site',
            'unite_medicale',
            'etablissement_partenaire',
        )
        .order_by('nom')
    )

    # --------------------------------------------------------
    # Recherche
    # --------------------------------------------------------

    if recherche:
        pharmacies = pharmacies.filter(
            Q(nom__icontains=recherche)
            | Q(code__icontains=recherche)
            | Q(telephone__icontains=recherche)
            | Q(email__icontains=recherche)
            | Q(ville__libelle__icontains=recherche)
        )

    # --------------------------------------------------------
    # Filtre type
    # --------------------------------------------------------

    if type_pharmacie_selectionne:
        pharmacies = pharmacies.filter(
            type_pharmacie=type_pharmacie_selectionne
        )

    # --------------------------------------------------------
    # Filtre partenariat
    # --------------------------------------------------------

    if statut_partenaire_selectionne:
        pharmacies = pharmacies.filter(
            statut_partenaire=statut_partenaire_selectionne
        )

    # --------------------------------------------------------
    # Statistiques
    # --------------------------------------------------------

    total_pharmacies = Pharmacie.objects.count()

    pharmacies_actives = (
        Pharmacie.objects
        .filter(actif=True)
        .count()
    )

    pharmacies_inactives = (
        Pharmacie.objects
        .filter(actif=False)
        .count()
    )

    pharmacies_independantes = (
        Pharmacie.objects
        .filter(type_pharmacie='independante')
        .count()
    )

    pharmacies_partenaires = (
        Pharmacie.objects
        .exclude(statut_partenaire='non_partenaire')
        .count()
    )

    if form is None:
        form = PharmacieForm()

    return {
        'pharmacies': pharmacies,

        'total_pharmacies': total_pharmacies,
        'pharmacies_actives': pharmacies_actives,
        'pharmacies_inactives': pharmacies_inactives,
        'pharmacies_independantes': pharmacies_independantes,
        'pharmacies_partenaires': pharmacies_partenaires,

        'types_pharmacie': Pharmacie.TYPE_PHARMACIE_CHOICES,
        'statuts_partenaire': Pharmacie.STATUT_PARTENAIRE_CHOICES,

        'recherche': recherche,
        'type_pharmacie_selectionne': type_pharmacie_selectionne,
        'statut_partenaire_selectionne': statut_partenaire_selectionne,

        'form': form,
        'modifier': modifier,
        'pharmacie_to_edit': pharmacie_to_edit,
    }


# ============================================================
# LISTE
# ============================================================

def liste_pharmacies(request):

    recherche = request.GET.get(
        'q',
        ''
    ).strip()

    type_pharmacie = request.GET.get(
        'type_pharmacie',
        ''
    ).strip()

    statut_partenaire = request.GET.get(
        'statut_partenaire',
        ''
    ).strip()

    context = _get_pharmacies_context(
        recherche=recherche,
        type_pharmacie_selectionne=type_pharmacie,
        statut_partenaire_selectionne=statut_partenaire,
    )

    return render(
        request,
        'backend/parametrage_general/pages/pharmacie/liste.html',
        context
    )


# ============================================================
# AJOUT
# ============================================================

def ajouter_pharmacie(request):

    if request.method == 'POST':

        form = PharmacieForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            pharmacie = form.save()

            messages.success(
                request,
                (
                    f"La pharmacie « {pharmacie.nom} » "
                    "a été créée avec succès."
                )
            )

            return redirect(
                'parametrage_general:liste_pharmacies'
            )

    else:

        form = PharmacieForm()

    context = _get_pharmacies_context(
        form=form
    )

    return render(
        request,
        'backend/parametrage_general/pages/pharmacie/liste.html',
        context
    )


# ============================================================
# MODIFICATION
# ============================================================

def modifier_pharmacie(request, pk):

    pharmacie = get_object_or_404(
        Pharmacie,
        pk=pk
    )

    if request.method == 'POST':

        form = PharmacieForm(
            request.POST,
            request.FILES,
            instance=pharmacie
        )

        if form.is_valid():

            pharmacie = form.save()

            messages.success(
                request,
                (
                    f"La pharmacie « {pharmacie.nom} » "
                    "a été modifiée avec succès."
                )
            )

            return redirect(
                'parametrage_general:liste_pharmacies'
            )

    else:

        form = PharmacieForm(
            instance=pharmacie
        )

    context = _get_pharmacies_context(
        form=form,
        modifier=True,
        pharmacie_to_edit=pharmacie
    )

    return render(
        request,
        'backend/parametrage_general/pages/pharmacie/liste.html',
        context
    )


# ============================================================
# SUPPRESSION
# ============================================================

def supprimer_pharmacie(request, pk):

    pharmacie = get_object_or_404(
        Pharmacie,
        pk=pk
    )

    if request.method == 'POST':

        nom = pharmacie.nom

        pharmacie.delete()

        messages.success(
            request,
            (
                f"La pharmacie « {nom} » "
                "a été supprimée avec succès."
            )
        )

    return redirect(
        'parametrage_general:liste_pharmacies'
    )


# ============================================================
# ACTIVATION / DESACTIVATION
# ============================================================

def toggle_pharmacie(request, pk):

    pharmacie = get_object_or_404(
        Pharmacie,
        pk=pk
    )

    pharmacie.actif = not pharmacie.actif

    pharmacie.save(
        update_fields=['actif']
    )

    if pharmacie.actif:

        messages.success(
            request,
            (
                f"La pharmacie « {pharmacie.nom} » "
                "a été activée."
            )
        )

    else:

        messages.warning(
            request,
            (
                f"La pharmacie « {pharmacie.nom} » "
                "a été désactivée."
            )
        )

    return redirect(
        'parametrage_general:liste_pharmacies'
    )