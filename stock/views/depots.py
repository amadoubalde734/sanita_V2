from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from stock.forms.depots import DepotStockForm
from stock.models.depots import DepotStock


@login_required
def depot_list(request):
    depots = DepotStock.objects.select_related(
        "pharmacie"
    ).order_by(
        "pharmacie__nom",
        "nom",
    )

    recherche = request.GET.get("q", "").strip()
    pharmacie_id = request.GET.get("pharmacie", "").strip()
    statut = request.GET.get("statut", "").strip()
    principal = request.GET.get("principal", "").strip()

    if recherche:
        depots = depots.filter(
            Q(code__icontains=recherche)
            | Q(nom__icontains=recherche)
            | Q(lieu__icontains=recherche)
            | Q(pharmacie__nom__icontains=recherche)
        )

    if pharmacie_id:
        depots = depots.filter(
            pharmacie_id=pharmacie_id
        )

    if statut == "actif":
        depots = depots.filter(actif=True)

    elif statut == "inactif":
        depots = depots.filter(actif=False)

    if principal == "oui":
        depots = depots.filter(est_principal=True)

    elif principal == "non":
        depots = depots.filter(est_principal=False)

    context = {
        "depots": depots,
        "recherche": recherche,
        "pharmacie_id": pharmacie_id,
        "statut": statut,
        "principal": principal,
    }

    return render(
        request,
        "backend/stock/depots/list.html",
        context,
    )


@login_required
def depot_create(request):
    if request.method == "POST":
        form = DepotStockForm(request.POST)

        if form.is_valid():
            depot = form.save()

            messages.success(
                request,
                f"Le dépôt « {depot.nom} » a été créé avec succès.",
            )

            return redirect(
                "stock:depot_detail",
                pk=depot.pk,
            )
    else:
        form = DepotStockForm()

    context = {
        "form": form,
        "title": "Nouveau dépôt",
        "page_title": "Créer un dépôt",
        "submit_label": "Créer le dépôt",
    }

    return render(
        request,
        "backend/stock/depots/form.html",
        context,
    )


@login_required
def depot_detail(request, pk):
    depot = get_object_or_404(
        DepotStock.objects.select_related(
            "pharmacie"
        ),
        pk=pk,
    )

    context = {
        "depot": depot,
    }

    return render(
        request,
        "backend/stock/depots/detail.html",
        context,
    )


@login_required
def depot_update(request, pk):
    depot = get_object_or_404(
        DepotStock,
        pk=pk,
    )

    if request.method == "POST":
        form = DepotStockForm(
            request.POST,
            instance=depot,
        )

        if form.is_valid():
            depot = form.save()

            messages.success(
                request,
                f"Le dépôt « {depot.nom} » a été modifié avec succès.",
            )

            return redirect(
                "stock:depot_detail",
                pk=depot.pk,
            )
    else:
        form = DepotStockForm(
            instance=depot,
        )

    context = {
        "form": form,
        "depot": depot,
        "title": f"Modifier — {depot.nom}",
        "page_title": "Modifier le dépôt",
        "submit_label": "Enregistrer les modifications",
    }

    return render(
        request,
        "backend/stock/depots/form.html",
        context,
    )


@login_required
def depot_toggle(request, pk):
    depot = get_object_or_404(
        DepotStock,
        pk=pk,
    )

    if request.method != "POST":
        return redirect(
            "stock:depot_detail",
            pk=depot.pk,
        )

    depot.actif = not depot.actif

    if depot.actif:
        depot.statut = "actif"
        message = (
            f"Le dépôt « {depot.nom} » a été activé."
        )
    else:
        depot.statut = "inactif"
        message = (
            f"Le dépôt « {depot.nom} » a été désactivé."
        )

    depot.save(
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
        "stock:depot_detail",
        pk=depot.pk,
    )

