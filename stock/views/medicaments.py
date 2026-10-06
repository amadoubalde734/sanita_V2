from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from stock.forms.medicaments import (
    FamilleMedicamentForm,
    MedicamentForm,
)
from stock.models.medicaments import (
    FamilleMedicament,
    Medicament,
)


# ============================================================
# MÉDICAMENTS
# ============================================================

@login_required
def medicament_list(request):

    # --------------------------------------------------------
    # LISTE DE BASE
    # --------------------------------------------------------

    medicaments = (
        Medicament.objects
        .select_related("famille")
        .order_by("nom")
    )

    # --------------------------------------------------------
    # RECHERCHE
    # --------------------------------------------------------

    recherche = request.GET.get(
        "q",
        "",
    ).strip()

    if recherche:

        medicaments = medicaments.filter(
            Q(code__icontains=recherche)
            | Q(code_cip__icontains=recherche)
            | Q(code_barre__icontains=recherche)
            | Q(nom__icontains=recherche)
        )

    # --------------------------------------------------------
    # FILTRE FAMILLE
    # --------------------------------------------------------

    famille_id = request.GET.get(
        "famille",
        "",
    ).strip()

    if famille_id:

        medicaments = medicaments.filter(
            famille_id=famille_id
        )

    # --------------------------------------------------------
    # FILTRE STATUT
    # --------------------------------------------------------

    actif = request.GET.get(
        "actif",
        "",
    ).strip()

    if actif == "1":

        medicaments = medicaments.filter(
            actif=True
        )

    elif actif == "0":

        medicaments = medicaments.filter(
            actif=False
        )

    # --------------------------------------------------------
    # FAMILLES DISPONIBLES POUR LE FILTRE
    # --------------------------------------------------------

    familles = (
        FamilleMedicament.objects
        .filter(
            actif=True,
            statut="actif",
        )
        .order_by("nom")
    )

    # --------------------------------------------------------
    # STATISTIQUES GLOBALES
    # --------------------------------------------------------
    #
    # Ces statistiques ne sont pas impactées par les filtres
    # de recherche afin d'afficher l'état réel du référentiel.
    #

    total_medicaments = (
        Medicament.objects.count()
    )

    medicaments_actifs = (
        Medicament.objects
        .filter(actif=True)
        .count()
    )

    medicaments_inactifs = (
        Medicament.objects
        .filter(actif=False)
        .count()
    )

    total_familles = (
        FamilleMedicament.objects.count()
    )

    # --------------------------------------------------------
    # CONTEXTE
    # --------------------------------------------------------

    context = {
        # Liste filtrée
        "medicaments": medicaments,

        # Filtres
        "familles": familles,
        "recherche": recherche,
        "famille_id": famille_id,
        "actif": actif,

        # Statistiques globales
        "total_medicaments": total_medicaments,
        "medicaments_actifs": medicaments_actifs,
        "medicaments_inactifs": medicaments_inactifs,
        "total_familles": total_familles,
    }

    return render(
        request,
        "backend/stock/pages/medicaments/list.html",
        context,
    )


# ============================================================
# APERÇU RÉFÉRENCE MÉDICAMENT
# ============================================================

@login_required
def medicament_reference_preview(request):
    """
    Retourne la prochaine référence SANITA disponible
    pour une famille de médicaments.

    Exemple :

    ANT     -> ANT-00001
    ANT     -> ANT-00002
    ANTIF   -> ANTIF-00001
    """

    famille_id = request.GET.get(
        "famille",
        "",
    ).strip()

    # --------------------------------------------------------
    # AUCUNE FAMILLE
    # --------------------------------------------------------

    if not famille_id:

        return JsonResponse({
            "success": False,
            "reference": "",
            "message": "Aucune famille sélectionnée.",
        })

    # --------------------------------------------------------
    # RÉCUPÉRATION DE LA FAMILLE
    # --------------------------------------------------------

    try:

        famille = FamilleMedicament.objects.get(
            pk=famille_id,
            actif=True,
            statut="actif",
        )

    except FamilleMedicament.DoesNotExist:

        return JsonResponse({
            "success": False,
            "reference": "",
            "message": (
                "Famille introuvable ou inactive."
            ),
        })

    # --------------------------------------------------------
    # CODE FAMILLE
    # --------------------------------------------------------

    prefixe = famille.code.strip().upper()

    # --------------------------------------------------------
    # RECHERCHE DES RÉFÉRENCES EXISTANTES
    # --------------------------------------------------------
    #
    # Exemple :
    #
    # ANT-00001
    # ANT-00002
    # ANT-00015
    #
    # On recherche uniquement les médicaments appartenant
    # à cette famille et utilisant son préfixe.
    #

    medicaments = (
        Medicament.objects
        .filter(
            famille=famille,
            code__startswith=f"{prefixe}-",
        )
        .values_list(
            "code",
            flat=True,
        )
    )

    # --------------------------------------------------------
    # DERNIER NUMÉRO UTILISÉ
    # --------------------------------------------------------

    dernier_numero = 0

    for code in medicaments:

        try:

            numero = int(
                code.rsplit(
                    "-",
                    1,
                )[1]
            )

        except (
            ValueError,
            IndexError,
        ):

            continue

        if numero > dernier_numero:

            dernier_numero = numero

    # --------------------------------------------------------
    # PROCHAIN NUMÉRO
    # --------------------------------------------------------

    numero_suivant = (
        dernier_numero + 1
    )

    # --------------------------------------------------------
    # GÉNÉRATION DE LA RÉFÉRENCE
    # --------------------------------------------------------

    reference = (
        f"{prefixe}-{numero_suivant:05d}"
    )

    # --------------------------------------------------------
    # RÉPONSE JSON
    # --------------------------------------------------------

    return JsonResponse({
        "success": True,
        "reference": reference,
        "famille": famille.nom,
        "code_famille": prefixe,
    })


# ============================================================
# CRÉATION
# ============================================================

@login_required
def medicament_create(request):

    if request.method == "POST":

        form = MedicamentForm(
            request.POST
        )

        if form.is_valid():

            medicament = form.save()

            messages.success(
                request,
                (
                    f"Le médicament "
                    f"« {medicament.nom} » "
                    f"({medicament.code}) "
                    "a été créé avec succès."
                ),
            )

            return redirect(
                "stock:medicament_list"
            )

    else:

        form = MedicamentForm()

    context = {
        "form": form,
        "title": "Nouveau médicament",
        "medicament": None,
    }

    return render(
        request,
        "backend/stock/pages/medicaments/form.html",
        context,
    )


# ============================================================
# MODIFICATION
# ============================================================

@login_required
def medicament_update(request, pk):

    medicament = get_object_or_404(
        Medicament,
        pk=pk,
    )

    if request.method == "POST":

        form = MedicamentForm(
            request.POST,
            instance=medicament,
        )

        if form.is_valid():

            medicament = form.save()

            messages.success(
                request,
                (
                    f"Le médicament "
                    f"« {medicament.nom} » "
                    f"({medicament.code}) "
                    "a été modifié avec succès."
                ),
            )

            return redirect(
                "stock:medicament_list"
            )

    else:

        form = MedicamentForm(
            instance=medicament
        )

    context = {
        "form": form,
        "title": "Modifier le médicament",
        "medicament": medicament,
    }

    return render(
        request,
        "backend/stock/pages/medicaments/form.html",
        context,
    )


# ============================================================
# DÉTAIL
# ============================================================

@login_required
def medicament_detail(request, pk):

    medicament = get_object_or_404(
        Medicament.objects.select_related(
            "famille"
        ),
        pk=pk,
    )

    context = {
        "medicament": medicament,
    }

    return render(
        request,
        "backend/stock/pages/medicaments/detail.html",
        context,
    )


# ============================================================
# ACTIVATION / DÉSACTIVATION
# ============================================================

@login_required
def medicament_toggle(request, pk):

    medicament = get_object_or_404(
        Medicament,
        pk=pk,
    )

    if request.method != "POST":

        return redirect(
            "stock:medicament_list"
        )

    medicament.actif = not medicament.actif

    if medicament.actif:

        medicament.statut = "actif"

        message = (
            f"Le médicament « {medicament.nom} » "
            "a été activé."
        )

    else:

        medicament.statut = "inactif"

        message = (
            f"Le médicament « {medicament.nom} » "
            "a été désactivé."
        )

    medicament.save(
        update_fields=[
            "actif",
            "statut",
            "date_modification",
        ]
    )

    messages.success(
        request,
        message,
    )

    return redirect(
        "stock:medicament_list"
    )


# ============================================================
# FAMILLES DE MÉDICAMENTS
# ============================================================

@login_required
def famille_list(request):

    # --------------------------------------------------------
    # RECHERCHE
    # --------------------------------------------------------

    recherche = request.GET.get(
        "q",
        "",
    ).strip()

    # --------------------------------------------------------
    # FILTRE STATUT
    # --------------------------------------------------------

    actif_selectionne = request.GET.get(
        "actif",
        "",
    ).strip()

    # --------------------------------------------------------
    # LISTE DES FAMILLES
    # --------------------------------------------------------

    familles = (
        FamilleMedicament.objects
        .annotate(
            nombre_medicaments=Count(
                "medicaments"
            )
        )
        .order_by("nom")
    )

    # --------------------------------------------------------
    # RECHERCHE
    # --------------------------------------------------------

    if recherche:

        familles = familles.filter(
            Q(code__icontains=recherche)
            | Q(nom__icontains=recherche)
            | Q(description__icontains=recherche)
        )

    # --------------------------------------------------------
    # FILTRE STATUT
    # --------------------------------------------------------

    if actif_selectionne == "1":

        familles = familles.filter(
            actif=True
        )

    elif actif_selectionne == "0":

        familles = familles.filter(
            actif=False
        )

    # --------------------------------------------------------
    # STATISTIQUES
    # --------------------------------------------------------

    total_familles = (
        FamilleMedicament.objects.count()
    )

    familles_actives = (
        FamilleMedicament.objects
        .filter(actif=True)
        .count()
    )

    familles_inactives = (
        FamilleMedicament.objects
        .filter(actif=False)
        .count()
    )

    total_medicaments = (
        Medicament.objects.count()
    )

    # --------------------------------------------------------
    # FORMULAIRE
    # --------------------------------------------------------

    form = FamilleMedicamentForm()

    # --------------------------------------------------------
    # CONTEXTE
    # --------------------------------------------------------

    context = {
        "familles": familles,

        "recherche": recherche,
        "actif_selectionne": actif_selectionne,

        "total_familles": total_familles,
        "familles_actives": familles_actives,
        "familles_inactives": familles_inactives,
        "total_medicaments": total_medicaments,

        "form": form,

        "ouvrir_modal": False,
    }

    return render(
        request,
        "backend/stock/pages/medicaments/familles/list.html",
        context,
    )


# ============================================================
# CONTEXTE FAMILLES
# ============================================================

def _famille_list_context(
    form=None,
    recherche="",
    actif_selectionne="",
    ouvrir_modal=False,
):
    """
    Prépare le contexte commun de la page des familles.

    Utilisé notamment lorsque le formulaire du modal
    contient des erreurs de validation.
    """

    familles = (
        FamilleMedicament.objects
        .annotate(
            nombre_medicaments=Count(
                "medicaments"
            )
        )
        .order_by("nom")
    )

    if recherche:

        familles = familles.filter(
            Q(code__icontains=recherche)
            | Q(nom__icontains=recherche)
            | Q(description__icontains=recherche)
        )

    if actif_selectionne == "1":

        familles = familles.filter(
            actif=True
        )

    elif actif_selectionne == "0":

        familles = familles.filter(
            actif=False
        )

    total_familles = (
        FamilleMedicament.objects.count()
    )

    familles_actives = (
        FamilleMedicament.objects
        .filter(actif=True)
        .count()
    )

    familles_inactives = (
        FamilleMedicament.objects
        .filter(actif=False)
        .count()
    )

    total_medicaments = (
        Medicament.objects.count()
    )

    if form is None:

        form = FamilleMedicamentForm()

    return {
        "familles": familles,

        "recherche": recherche,
        "actif_selectionne": actif_selectionne,

        "total_familles": total_familles,
        "familles_actives": familles_actives,
        "familles_inactives": familles_inactives,
        "total_medicaments": total_medicaments,

        "form": form,

        "ouvrir_modal": ouvrir_modal,
    }


# ============================================================
# CRÉATION FAMILLE
# ============================================================

@login_required
def famille_create(request):

    if request.method != "POST":

        return redirect(
            "stock:famille_list"
        )

    form = FamilleMedicamentForm(
        request.POST
    )

    if form.is_valid():

        famille = form.save()

        messages.success(
            request,
            (
                f"La famille "
                f"« {famille.nom} » "
                "a été créée avec succès."
            ),
        )

        return redirect(
            "stock:famille_list"
        )

    # --------------------------------------------------------
    # ERREUR DE VALIDATION
    # --------------------------------------------------------

    recherche = request.POST.get(
        "q",
        "",
    ).strip()

    actif_selectionne = request.POST.get(
        "actif",
        "",
    ).strip()

    context = _famille_list_context(
        form=form,
        recherche=recherche,
        actif_selectionne=actif_selectionne,
        ouvrir_modal=True,
    )

    return render(
        request,
        "backend/stock/pages/medicaments/familles/list.html",
        context,
    )


# ============================================================
# MODIFICATION FAMILLE
# ============================================================

@login_required
def famille_update(request, pk):

    famille = get_object_or_404(
        FamilleMedicament,
        pk=pk,
    )

    if request.method != "POST":

        return redirect(
            "stock:famille_list"
        )

    form = FamilleMedicamentForm(
        request.POST,
        instance=famille,
    )

    if form.is_valid():

        famille = form.save()

        messages.success(
            request,
            (
                f"La famille "
                f"« {famille.nom} » "
                "a été modifiée avec succès."
            ),
        )

        return redirect(
            "stock:famille_list"
        )

    # --------------------------------------------------------
    # ERREUR DE VALIDATION
    # --------------------------------------------------------

    recherche = request.POST.get(
        "q",
        "",
    ).strip()

    actif_selectionne = request.POST.get(
        "actif",
        "",
    ).strip()

    context = _famille_list_context(
        form=form,
        recherche=recherche,
        actif_selectionne=actif_selectionne,
        ouvrir_modal=True,
    )

    # Permet au JavaScript de savoir qu'il s'agit
    # d'une modification.
    context["famille"] = famille

    return render(
        request,
        "backend/stock/pages/medicaments/familles/list.html",
        context,
    )


# ============================================================
# ACTIVATION / DÉSACTIVATION FAMILLE
# ============================================================

@login_required
def famille_toggle(request, pk):

    famille = get_object_or_404(
        FamilleMedicament,
        pk=pk,
    )

    if request.method != "POST":

        return redirect(
            "stock:famille_list"
        )

    famille.actif = not famille.actif

    if famille.actif:

        famille.statut = "actif"

        message = (
            f"La famille « {famille.nom} » "
            "a été activée."
        )

    else:

        famille.statut = "inactif"

        message = (
            f"La famille « {famille.nom} » "
            "a été désactivée."
        )

    famille.save(
        update_fields=[
            "actif",
            "statut",
            "date_modification",
        ]
    )

    messages.success(
        request,
        message,
    )

    return redirect(
        "stock:famille_list"
    )