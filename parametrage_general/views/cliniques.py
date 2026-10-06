from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from ..forms import EtablissementPartenaireForm
from ..models import EtablissementPartenaire


TEMPLATE_LISTE = 'backend/parametrage_general/pages/clinique/liste.html'
URL_LISTE = 'parametrage_general:liste_etablissements_partenaires'
LOGIN_URL = 'accounts:admin_login'


# ============================================================
# OUTIL : CONTEXTE COMMUN
# ============================================================

def _get_etablissements_context(request, form=None, form_action=None, ouvrir_modal=False):
    """
    Construit le contexte de la page des établissements partenaires :
    liste filtrée, statistiques, filtres et formulaire de la modale.
    """

    # ---------- Filtres (lus dans l'URL, conservés après une erreur) ----------
    recherche = request.GET.get('q', '').strip()
    type_selectionne = request.GET.get('type_partenaire', '').strip()
    statut_selectionne = request.GET.get('statut_partenaire', '').strip()

    # ---------- Liste ----------
    etablissements = (
        EtablissementPartenaire.objects
        .select_related('ville')
        .prefetch_related('specialites')
        .order_by('nom')
    )

    if recherche:
        etablissements = etablissements.filter(
            Q(nom__icontains=recherche)
            | Q(code__icontains=recherche)
            | Q(telephone__icontains=recherche)
            | Q(email__icontains=recherche)
            | Q(ville__libelle__icontains=recherche)
        )

    if type_selectionne:
        etablissements = etablissements.filter(type_partenaire=type_selectionne)

    if statut_selectionne:
        etablissements = etablissements.filter(statut_partenaire=statut_selectionne)

    # ---------- Statistiques (une seule requête SQL) ----------
    stats = EtablissementPartenaire.objects.aggregate(
        total=Count('pk'),
        actifs=Count('pk', filter=Q(statut_partenaire='actif')),
        inactifs=Count('pk', filter=Q(statut_partenaire='inactif')),
        suspendus=Count('pk', filter=Q(statut_partenaire='suspendu')),
    )

    return {
        # Liste
        'etablissements_partenaires': etablissements,

        # Statistiques
        'total_partenaires': stats['total'],
        'partenaires_actifs': stats['actifs'],
        'partenaires_inactifs': stats['inactifs'],
        'partenaires_suspendus': stats['suspendus'],

        # Filtres
        'types_partenaire': EtablissementPartenaire.TYPE_PARTENAIRE_CHOICES,
        'statuts_partenaire': EtablissementPartenaire.STATUT_PARTENAIRE_CHOICES,
        'recherche': recherche,
        'type_partenaire_selectionne': type_selectionne,
        'statut_partenaire_selectionne': statut_selectionne,

        # Modale
        'form': form or EtablissementPartenaireForm(),
        'form_action': form_action or reverse('parametrage_general:ajouter_etablissement_partenaire'),
        'ouvrir_modal': ouvrir_modal,
    }


# ============================================================
# LISTE
# ============================================================

@login_required(login_url=LOGIN_URL)
def liste_etablissements_partenaires(request):
    context = _get_etablissements_context(request)
    return render(request, TEMPLATE_LISTE, context)


# ============================================================
# AJOUTER
# ============================================================

@login_required(login_url=LOGIN_URL)
def ajouter_etablissement_partenaire(request):

    # Accès direct à l'URL : on renvoie vers la liste
    if request.method != 'POST':
        return redirect(URL_LISTE)

    form = EtablissementPartenaireForm(request.POST)

    if form.is_valid():
        partenaire = form.save()
        messages.success(
            request,
            f"L'établissement partenaire « {partenaire.nom} » a été créé avec succès.",
        )
        return redirect(URL_LISTE)

    # Erreurs : on réaffiche la liste avec la modale ouverte
    messages.error(request, "Le formulaire contient des erreurs. Veuillez les corriger.")

    context = _get_etablissements_context(
        request,
        form=form,
        ouvrir_modal=True,
    )
    return render(request, TEMPLATE_LISTE, context)


# ============================================================
# MODIFIER
# ============================================================

@login_required(login_url=LOGIN_URL)
def modifier_etablissement_partenaire(request, pk):

    partenaire = get_object_or_404(EtablissementPartenaire, pk=pk)
    form_action = reverse('parametrage_general:modifier_etablissement_partenaire', args=[pk])

    if request.method == 'POST':
        form = EtablissementPartenaireForm(request.POST, instance=partenaire)

        if form.is_valid():
            partenaire = form.save()
            messages.success(
                request,
                f"L'établissement partenaire « {partenaire.nom} » a été modifié avec succès.",
            )
            return redirect(URL_LISTE)

        messages.error(request, "Le formulaire contient des erreurs. Veuillez les corriger.")

    else:
        # Accès direct à l'URL : la modale s'ouvre pré-remplie
        form = EtablissementPartenaireForm(instance=partenaire)

    context = _get_etablissements_context(
        request,
        form=form,
        form_action=form_action,
        ouvrir_modal=True,
    )
    return render(request, TEMPLATE_LISTE, context)


# ============================================================
# SUPPRIMER
# ============================================================

@login_required(login_url=LOGIN_URL)
@require_POST
def supprimer_etablissement_partenaire(request, pk):

    partenaire = get_object_or_404(EtablissementPartenaire, pk=pk)
    nom = partenaire.nom

    partenaire.delete()

    messages.success(
        request,
        f"L'établissement partenaire « {nom} » a été supprimé avec succès.",
    )
    return redirect(URL_LISTE)


# ============================================================
# ACTIVER / DÉSACTIVER
# ============================================================

@login_required(login_url=LOGIN_URL)
def toggle_etablissement_partenaire(request, pk):

    partenaire = get_object_or_404(EtablissementPartenaire, pk=pk)

    partenaire.actif = not partenaire.actif
    partenaire.save(update_fields=['actif'])

    if partenaire.actif:
        messages.success(request, f"L'établissement partenaire « {partenaire.nom} » a été activé.")
    else:
        messages.warning(request, f"L'établissement partenaire « {partenaire.nom} » a été désactivé.")

    return redirect(URL_LISTE)