from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import CatalogueMedicamentPharmaciePartenaireForm
from ..models.catalogue_pharmacies_partenaires import (
    CatalogueMedicamentPharmaciePartenaire,
)
from ..models.pharmacie_partenaire import PharmaciePartenaire


# ============================================================
# CATALOGUE MÉDICAMENTS — PHARMACIES PARTENAIRES
# ============================================================


def liste_catalogue_medicaments_pharmacies_partenaires(request):

    catalogue = (
        CatalogueMedicamentPharmaciePartenaire.objects
        .select_related(
            "pharmacie",
            "medicament",
            "medicament__famille",
        )
        .order_by(
            "pharmacie__nom",
            "medicament__nom",
        )
    )

    recherche = request.GET.get("q", "").strip()
    pharmacie_id = request.GET.get("pharmacie", "").strip()
    statut = request.GET.get("statut", "").strip()

    # ========================================================
    # FILTRE RECHERCHE
    # ========================================================

    if recherche:
        catalogue = catalogue.filter(
            Q(medicament__nom__icontains=recherche)
            | Q(medicament__code__icontains=recherche)
            | Q(medicament__code_cip__icontains=recherche)
            | Q(nom_commercial__icontains=recherche)
            | Q(reference_interne__icontains=recherche)
            | Q(pharmacie__nom__icontains=recherche)
            | Q(pharmacie__code__icontains=recherche)
        )

    # ========================================================
    # FILTRE PHARMACIE
    # ========================================================

    if pharmacie_id:
        catalogue = catalogue.filter(
            pharmacie_id=pharmacie_id
        )

    # ========================================================
    # FILTRE STATUT
    # ========================================================

    if statut == "actif":

        catalogue = catalogue.filter(
            actif=True
        )

    elif statut == "inactif":

        catalogue = catalogue.filter(
            actif=False
        )

    elif statut == "disponible":

        catalogue = catalogue.filter(
            actif=True,
            disponible=True,
        )

    elif statut == "indisponible":

        catalogue = catalogue.filter(
            actif=True,
            disponible=False,
        )

    # ========================================================
    # PHARMACIES PARTENAIRES
    # ========================================================

    pharmacies = (
        PharmaciePartenaire.objects
        .filter(actif=True)
        .order_by("nom")
    )

    # ========================================================
    # FORMULAIRE
    # ========================================================

    form = CatalogueMedicamentPharmaciePartenaireForm()

    ouvrir_modal = False
    mode_formulaire = "ajout"
    catalogue_modification_id = None

    # ========================================================
    # TRAITEMENT POST
    # ========================================================

    if request.method == "POST":

        action = request.POST.get(
            "action",
            ""
        ).strip()

        # ====================================================
        # AJOUT
        # ====================================================

        if action == "ajouter":

            form = CatalogueMedicamentPharmaciePartenaireForm(
                request.POST
            )

            if form.is_valid():

                catalogue_obj = form.save()

                messages.success(
                    request,
                    (
                        f"Le médicament « "
                        f"{catalogue_obj.medicament.nom} » "
                        f"a été ajouté au catalogue de "
                        f"« {catalogue_obj.pharmacie.nom} »."
                    ),
                )

                return redirect(
                    "parametrage_general:"
                    "liste_catalogue_medicaments_pharmacies_partenaires"
                )

            ouvrir_modal = True
            mode_formulaire = "ajout"

        # ====================================================
        # MODIFICATION
        # ====================================================

        elif action == "modifier":

            catalogue_id = request.POST.get(
                "catalogue_id",
                ""
            ).strip()

            catalogue_obj = get_object_or_404(
                CatalogueMedicamentPharmaciePartenaire,
                pk=catalogue_id,
            )

            form = CatalogueMedicamentPharmaciePartenaireForm(
                request.POST,
                instance=catalogue_obj,
            )

            if form.is_valid():

                catalogue_obj = form.save()

                messages.success(
                    request,
                    (
                        f"Le médicament « "
                        f"{catalogue_obj.medicament.nom} » "
                        "a été mis à jour dans le catalogue."
                    ),
                )

                return redirect(
                    "parametrage_general:"
                    "liste_catalogue_medicaments_pharmacies_partenaires"
                )

            ouvrir_modal = True
            mode_formulaire = "modification"
            catalogue_modification_id = catalogue_obj.pk

    # ========================================================
    # OUVERTURE DIRECTE DE LA MODALE DE MODIFICATION
    #
    # Exemple :
    # ?modifier=15
    # ========================================================

    if request.method == "GET":

        modifier_id = request.GET.get(
            "modifier",
            ""
        ).strip()

        if modifier_id.isdigit():

            catalogue_obj = get_object_or_404(
                CatalogueMedicamentPharmaciePartenaire,
                pk=int(modifier_id),
            )

            form = CatalogueMedicamentPharmaciePartenaireForm(
                instance=catalogue_obj
            )

            ouvrir_modal = True
            mode_formulaire = "modification"
            catalogue_modification_id = catalogue_obj.pk

    # ========================================================
    # CONTEXTE
    # ========================================================

    context = {
        "catalogue": catalogue,
        "pharmacies": pharmacies,
        "recherche": recherche,
        "pharmacie_id": pharmacie_id,
        "statut": statut,

        "form": form,

        "ouvrir_modal": ouvrir_modal,
        "mode_formulaire": mode_formulaire,
        "catalogue_modification_id": catalogue_modification_id,
    }

    return render(
        request,
        "backend/parametrage_general/pages/"
        "pharmacies_partenaires/catalogue/liste.html",
        context,
    )


# ============================================================
# DÉTAILS
# ============================================================


def details_catalogue_medicament_pharmacie_partenaire(
    request,
    pk,
):

    catalogue = get_object_or_404(
        CatalogueMedicamentPharmaciePartenaire.objects.select_related(
            "pharmacie",
            "medicament",
            "medicament__famille",
        ),
        pk=pk,
    )

    return render(
        request,
        "backend/parametrage_general/pages/"
        "pharmacies_partenaires/catalogue/details.html",
        {
            "catalogue": catalogue,
        },
    )


# ============================================================
# SUPPRESSION
# ============================================================


def supprimer_catalogue_medicament_pharmacie_partenaire(
    request,
    pk,
):

    catalogue = get_object_or_404(
        CatalogueMedicamentPharmaciePartenaire,
        pk=pk,
    )

    if request.method == "POST":

        nom_medicament = catalogue.medicament.nom

        catalogue.delete()

        messages.success(
            request,
            (
                f"Le médicament « {nom_medicament} » "
                "a été retiré du catalogue."
            ),
        )

    return redirect(
        "parametrage_general:"
        "liste_catalogue_medicaments_pharmacies_partenaires"
    )


# ============================================================
# ACTIVATION / DÉSACTIVATION
# ============================================================


def toggle_catalogue_medicament_pharmacie_partenaire(
    request,
    pk,
):

    catalogue = get_object_or_404(
        CatalogueMedicamentPharmaciePartenaire,
        pk=pk,
    )

    catalogue.actif = not catalogue.actif

    catalogue.save(
        update_fields=["actif"]
    )

    if catalogue.actif:

        messages.success(
            request,
            (
                f"Le médicament « "
                f"{catalogue.medicament.nom} » "
                "est maintenant actif dans le catalogue."
            ),
        )

    else:

        messages.warning(
            request,
            (
                f"Le médicament « "
                f"{catalogue.medicament.nom} » "
                "a été désactivé du catalogue."
            ),
        )

    return redirect(
        "parametrage_general:"
        "liste_catalogue_medicaments_pharmacies_partenaires"
    )