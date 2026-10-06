from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from ..models import PharmacieInterne
from ..forms import PharmacieInterneForm


# ============================================================
# OUTIL : CONTEXTE COMMUN
# ============================================================

def _get_pharmacies_internes_context(
    form=None,
    modifier=False,
    pharmacie_to_edit=None,
    recherche="",
    site_selectionne="",
    statut_selectionne=""
):
    """
    Prépare le contexte commun utilisé par la page
    de gestion des pharmacies internes.
    """

    pharmacies = (
        PharmacieInterne.objects
        .select_related(
            "site",
            "unite_medicale",
        )
        .order_by("nom")
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
            | Q(nom_responsable__icontains=recherche)
            | Q(site__nom_site__icontains=recherche)
            | Q(unite_medicale__nom__icontains=recherche)
        )

    # --------------------------------------------------------
    # Filtre site
    # --------------------------------------------------------

    if site_selectionne:

        pharmacies = pharmacies.filter(
            site_id=site_selectionne
        )

    # --------------------------------------------------------
    # Filtre statut
    # --------------------------------------------------------

    if statut_selectionne == "active":

        pharmacies = pharmacies.filter(
            actif=True
        )

    elif statut_selectionne == "inactive":

        pharmacies = pharmacies.filter(
            actif=False
        )

    # --------------------------------------------------------
    # Statistiques
    # --------------------------------------------------------

    total_pharmacies = PharmacieInterne.objects.count()

    pharmacies_actives = (
        PharmacieInterne.objects
        .filter(actif=True)
        .count()
    )

    pharmacies_inactives = (
        PharmacieInterne.objects
        .filter(actif=False)
        .count()
    )

    pharmacies_stock_actif = (
        PharmacieInterne.objects
        .filter(
            actif=True,
            gestion_stock_active=True
        )
        .count()
    )

    pharmacies_dispensation_active = (
        PharmacieInterne.objects
        .filter(
            actif=True,
            gestion_dispensation_active=True
        )
        .count()
    )

    if form is None:
        form = PharmacieInterneForm()

    return {
        "pharmacies_internes": pharmacies,

        "total_pharmacies": total_pharmacies,
        "pharmacies_actives": pharmacies_actives,
        "pharmacies_inactives": pharmacies_inactives,
        "pharmacies_stock_actif": pharmacies_stock_actif,
        "pharmacies_dispensation_active": (
            pharmacies_dispensation_active
        ),

        "sites": (
            PharmacieInterne._meta
            .get_field("site")
            .remote_field
            .model
            .objects
            .filter(actif=True)
            .order_by("nom_site")
        ),

        "recherche": recherche,
        "site_selectionne": site_selectionne,
        "statut_selectionne": statut_selectionne,

        "form": form,
        "modifier": modifier,
        "pharmacie_to_edit": pharmacie_to_edit,
    }


# ============================================================
# LISTE
# ============================================================

def liste_pharmacies_internes(request):

    recherche = request.GET.get(
        "q",
        ""
    ).strip()

    site = request.GET.get(
        "site",
        ""
    ).strip()

    statut = request.GET.get(
        "statut",
        ""
    ).strip()

    context = _get_pharmacies_internes_context(
        recherche=recherche,
        site_selectionne=site,
        statut_selectionne=statut,
    )

    return render(
        request,
        "backend/parametrage_general/pages/pharmacie_interne/liste.html",
        context
    )


# ============================================================
# AJOUT
# ============================================================

def ajouter_pharmacie_interne(request):

    if request.method == "POST":

        form = PharmacieInterneForm(
            request.POST
        )

        if form.is_valid():

            pharmacie = form.save()

            messages.success(
                request,
                (
                    f"La pharmacie interne « {pharmacie.nom} » "
                    "a été créée avec succès."
                )
            )

            return redirect(
                "parametrage_general:liste_pharmacies_internes"
            )

    else:

        form = PharmacieInterneForm()

    context = _get_pharmacies_internes_context(
        form=form
    )

    return render(
        request,
        "backend/parametrage_general/pages/pharmacie_interne/liste.html",
        context
    )


# ============================================================
# MODIFICATION
# ============================================================

def modifier_pharmacie_interne(request, pk):

    pharmacie = get_object_or_404(
        PharmacieInterne,
        pk=pk
    )

    if request.method == "POST":

        form = PharmacieInterneForm(
            request.POST,
            instance=pharmacie
        )

        if form.is_valid():

            pharmacie = form.save()

            messages.success(
                request,
                (
                    f"La pharmacie interne « {pharmacie.nom} » "
                    "a été modifiée avec succès."
                )
            )

            return redirect(
                "parametrage_general:liste_pharmacies_internes"
            )

    else:

        form = PharmacieInterneForm(
            instance=pharmacie
        )

    context = _get_pharmacies_internes_context(
        form=form,
        modifier=True,
        pharmacie_to_edit=pharmacie
    )

    return render(
        request,
        "backend/parametrage_general/pages/pharmacie_interne/liste.html",
        context
    )


# ============================================================
# DÉTAILS
# ============================================================

def details_pharmacie_interne(request, pk):

    pharmacie = get_object_or_404(
        PharmacieInterne.objects.select_related(
            "site",
            "unite_medicale",
        ),
        pk=pk
    )

    return render(
        request,
        "backend/parametrage_general/pages/pharmacie_interne/details.html",
        {
            "pharmacie": pharmacie,
        }
    )


# ============================================================
# SUPPRESSION
# ============================================================

def supprimer_pharmacie_interne(request, pk):

    pharmacie = get_object_or_404(
        PharmacieInterne,
        pk=pk
    )

    if request.method == "POST":

        nom = pharmacie.nom

        pharmacie.delete()

        messages.success(
            request,
            (
                f"La pharmacie interne « {nom} » "
                "a été supprimée avec succès."
            )
        )

    return redirect(
        "parametrage_general:liste_pharmacies_internes"
    )


# ============================================================
# ACTIVATION / DESACTIVATION
# ============================================================

def toggle_pharmacie_interne(request, pk):

    pharmacie = get_object_or_404(
        PharmacieInterne,
        pk=pk
    )

    pharmacie.actif = not pharmacie.actif

    pharmacie.save(
        update_fields=["actif"]
    )

    if pharmacie.actif:

        messages.success(
            request,
            (
                f"La pharmacie interne « {pharmacie.nom} » "
                "a été activée."
            )
        )

    else:

        messages.warning(
            request,
            (
                f"La pharmacie interne « {pharmacie.nom} » "
                "a été désactivée."
            )
        )

    return redirect(
        "parametrage_general:liste_pharmacies_internes"
    )