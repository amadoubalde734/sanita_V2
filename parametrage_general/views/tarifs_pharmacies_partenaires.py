from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import TarifMedicamentPharmaciePartenaireForm

from ..models.tarifs_pharmacies_partenaires import (
    TarifMedicamentPharmaciePartenaire,
)

from ..models.pharmacie_partenaire import PharmaciePartenaire

from ..models.catalogue_pharmacies_partenaires import (
    CatalogueMedicamentPharmaciePartenaire,
)


# ============================================================
# TARIFS DES MÉDICAMENTS — PHARMACIES PARTENAIRES
# ============================================================


def liste_tarifs_medicaments_pharmacies_partenaires(request):

    # ========================================================
    # QUERYSET PRINCIPAL
    # ========================================================

    tarifs = (
        TarifMedicamentPharmaciePartenaire.objects
        .select_related(
            "catalogue",
            "catalogue__pharmacie",
            "catalogue__medicament",
            "catalogue__medicament__famille",
        )
        .order_by(
            "catalogue__pharmacie__nom",
            "catalogue__medicament__nom",
            "-date_debut",
        )
    )

    # ========================================================
    # FILTRES
    # ========================================================

    recherche = request.GET.get(
        "q",
        "",
    ).strip()

    pharmacie_id = request.GET.get(
        "pharmacie",
        "",
    ).strip()

    statut = request.GET.get(
        "statut",
        "",
    ).strip()

    # ========================================================
    # RECHERCHE
    # ========================================================

    if recherche:

        tarifs = tarifs.filter(
            Q(reference__icontains=recherche)
            | Q(
                catalogue__medicament__nom__icontains=recherche
            )
            | Q(
                catalogue__medicament__code__icontains=recherche
            )
            | Q(
                catalogue__medicament__code_cip__icontains=recherche
            )
            | Q(
                catalogue__pharmacie__nom__icontains=recherche
            )
            | Q(
                catalogue__pharmacie__code__icontains=recherche
            )
        )

    # ========================================================
    # FILTRE PHARMACIE
    # ========================================================

    if pharmacie_id:

        tarifs = tarifs.filter(
            catalogue__pharmacie_id=pharmacie_id
        )

    # ========================================================
    # FILTRE STATUT
    # ========================================================

    if statut == "actif":

        tarifs = tarifs.filter(
            actif=True
        )

    elif statut == "inactif":

        tarifs = tarifs.filter(
            actif=False
        )

    # ========================================================
    # FORMULAIRE
    # ========================================================

    form = TarifMedicamentPharmaciePartenaireForm()

    ouvrir_modal = False

    mode_formulaire = "ajout"

    tarif_modification_id = None

    # ========================================================
    # TRAITEMENT POST
    # ========================================================

    if request.method == "POST":

        action = request.POST.get(
            "action",
            "",
        ).strip()

        # ====================================================
        # AJOUT
        # ====================================================

        if action == "ajouter":

            form = TarifMedicamentPharmaciePartenaireForm(
                request.POST
            )

            if form.is_valid():

                tarif = form.save()

                messages.success(
                    request,
                    (
                        f"Le tarif « {tarif.reference} » "
                        f"du médicament "
                        f"« {tarif.catalogue.medicament.nom} » "
                        f"a été créé avec succès."
                    ),
                )

                return redirect(
                    "parametrage_general:"
                    "liste_tarifs_medicaments_pharmacies_partenaires"
                )

            ouvrir_modal = True

            mode_formulaire = "ajout"

        # ====================================================
        # MODIFICATION
        # ====================================================

        elif action == "modifier":

            tarif_id = request.POST.get(
                "tarif_id",
                "",
            ).strip()

            tarif_obj = get_object_or_404(
                TarifMedicamentPharmaciePartenaire,
                pk=tarif_id,
            )

            form = TarifMedicamentPharmaciePartenaireForm(
                request.POST,
                instance=tarif_obj,
            )

            if form.is_valid():

                tarif = form.save()

                messages.success(
                    request,
                    (
                        f"Le tarif « {tarif.reference} » "
                        "a été modifié avec succès."
                    ),
                )

                return redirect(
                    "parametrage_general:"
                    "liste_tarifs_medicaments_pharmacies_partenaires"
                )

            ouvrir_modal = True

            mode_formulaire = "modification"

            tarif_modification_id = tarif_obj.pk

    # ========================================================
    # OUVERTURE DIRECTE DE LA MODALE DE MODIFICATION
    #
    # Exemple :
    # ?modifier=15
    # ========================================================

    if request.method == "GET":

        modifier_id = request.GET.get(
            "modifier",
            "",
        ).strip()

        if modifier_id.isdigit():

            tarif_obj = get_object_or_404(
                TarifMedicamentPharmaciePartenaire.objects
                .select_related(
                    "catalogue",
                    "catalogue__pharmacie",
                    "catalogue__medicament",
                ),
                pk=int(modifier_id),
            )

            form = TarifMedicamentPharmaciePartenaireForm(
                instance=tarif_obj
            )

            ouvrir_modal = True

            mode_formulaire = "modification"

            tarif_modification_id = tarif_obj.pk

    # ========================================================
    # STATISTIQUES GLOBALES
    # ========================================================

    total_tarifs = (
        TarifMedicamentPharmaciePartenaire.objects.count()
    )

    total_tarifs_actifs = (
        TarifMedicamentPharmaciePartenaire.objects
        .filter(actif=True)
        .count()
    )

    total_tarifs_inactifs = (
        TarifMedicamentPharmaciePartenaire.objects
        .filter(actif=False)
        .count()
    )

    total_pharmacies = (
        TarifMedicamentPharmaciePartenaire.objects
        .values("catalogue__pharmacie_id")
        .distinct()
        .count()
    )

    # ========================================================
    # PHARMACIES DISPONIBLES
    #
    # Une pharmacie doit :
    # - être active ;
    # - avoir la gestion du catalogue active ;
    # - avoir la gestion des tarifs active.
    # ========================================================

    pharmacies = (
        PharmaciePartenaire.objects
        .filter(
            actif=True,
            gestion_catalogue_active=True,
            gestion_tarifs_active=True,
        )
        .order_by(
            "nom"
        )
    )

    # ========================================================
    # CATALOGUES DISPONIBLES
    #
    # On ne transmet au navigateur que les médicaments :
    # - actifs dans le catalogue ;
    # - appartenant à une pharmacie active ;
    # - dont la gestion du catalogue est active ;
    # - dont la gestion des tarifs est active.
    # ========================================================

    catalogues = (
        CatalogueMedicamentPharmaciePartenaire.objects
        .select_related(
            "pharmacie",
            "medicament",
        )
        .filter(
            actif=True,
            pharmacie__actif=True,
            pharmacie__gestion_catalogue_active=True,
            pharmacie__gestion_tarifs_active=True,
        )
        .order_by(
            "pharmacie__nom",
            "medicament__nom",
        )
    )

    # ========================================================
    # DONNÉES CATALOGUES POUR JAVASCRIPT
    # ========================================================

    catalogues_data = []

    for catalogue in catalogues:

        catalogues_data.append(
            {
                "id": catalogue.pk,

                "pharmacie_id": catalogue.pharmacie_id,

                "medicament": catalogue.medicament.nom,

                "conditionnement": (
                    catalogue.conditionnement
                    or ""
                ),

                "unite_vente": (
                    catalogue.unite_vente
                    or ""
                ),
            }
        )

    # ========================================================
    # CONTEXTE
    # ========================================================

    context = {

        "tarifs": tarifs,

        "pharmacies": pharmacies,

        "catalogues": catalogues,

        "catalogues_data": catalogues_data,

        "recherche": recherche,

        "pharmacie_id": pharmacie_id,

        "statut": statut,

        "form": form,

        "ouvrir_modal": ouvrir_modal,

        "mode_formulaire": mode_formulaire,

        "tarif_modification_id": tarif_modification_id,

        # ====================================================
        # STATISTIQUES
        # ====================================================

        "total_tarifs": total_tarifs,

        "total_tarifs_actifs": total_tarifs_actifs,

        "total_tarifs_inactifs": total_tarifs_inactifs,

        "total_pharmacies": total_pharmacies,
    }

    # ========================================================
    # RENDU
    # ========================================================

    return render(
        request,
        "backend/parametrage_general/pages/"
        "pharmacies_partenaires/tarifs/liste.html",
        context,
    )


# ============================================================
# DÉTAILS D'UN TARIF
# ============================================================


def details_tarif_medicament_pharmacie_partenaire(
    request,
    pk,
):

    tarif = get_object_or_404(
        TarifMedicamentPharmaciePartenaire.objects
        .select_related(
            "catalogue",
            "catalogue__pharmacie",
            "catalogue__medicament",
            "catalogue__medicament__famille",
        ),
        pk=pk,
    )

    context = {
        "tarif": tarif,
    }

    return render(
        request,
        "backend/parametrage_general/pages/"
        "pharmacies_partenaires/tarifs/details.html",
        context,
    )


# ============================================================
# SUPPRESSION D'UN TARIF
# ============================================================


def supprimer_tarif_medicament_pharmacie_partenaire(
    request,
    pk,
):

    tarif = get_object_or_404(
        TarifMedicamentPharmaciePartenaire.objects
        .select_related(
            "catalogue",
            "catalogue__medicament",
        ),
        pk=pk,
    )

    if request.method == "POST":

        reference = tarif.reference

        medicament = tarif.catalogue.medicament.nom

        tarif.delete()

        messages.success(
            request,
            (
                f"Le tarif « {reference} » "
                f"du médicament « {medicament} » "
                "a été supprimé avec succès."
            ),
        )

    return redirect(
        "parametrage_general:"
        "liste_tarifs_medicaments_pharmacies_partenaires"
    )


# ============================================================
# ACTIVATION / DÉSACTIVATION D'UN TARIF
# ============================================================


def toggle_tarif_medicament_pharmacie_partenaire(
    request,
    pk,
):

    tarif = get_object_or_404(
        TarifMedicamentPharmaciePartenaire,
        pk=pk,
    )

    tarif.actif = not tarif.actif

    tarif.save(
        update_fields=[
            "actif",
            "date_modification",
        ]
    )

    if tarif.actif:

        messages.success(
            request,
            (
                f"Le tarif « {tarif.reference} » "
                "a été activé avec succès."
            ),
        )

    else:

        messages.success(
            request,
            (
                f"Le tarif « {tarif.reference} » "
                "a été désactivé avec succès."
            ),
        )

    return redirect(
        "parametrage_general:"
        "liste_tarifs_medicaments_pharmacies_partenaires"
    )