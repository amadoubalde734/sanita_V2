from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core.cache import cache
import secrets

from ..forms import (
    SocieteForm,
    VilleForm,
    SiteForm,
    DirectionForm,
    DepartementForm,
    ServiceForm,
    FonctionForm,
    SpecialiteForm,
    UniteMedicaleForm,
    ConfigurationEtablissementForm,
)

from ..models import (
    Societe,
    Ville,
    Site,
    Direction,
    Departement,
    Service,
    Fonction,
    Specialite,
    UniteMedicale,
    ConfigurationEtablissement,
)

@login_required
def index(request):
    config = ConfigurationEtablissement.objects.first()
    specialites = Specialite.objects.all().order_by('nom')
    unites_medicales = UniteMedicale.objects.filter(
        actif=True
    ).select_related(
        'site'
    ).prefetch_related(
        'specialites'
    ).order_by('nom')

    return render(
        request,
        'backend/parametrage_general/pages/index.html',
        {
            'config_etablissement': config,
            'specialites': specialites,
            'unites_medicales': unites_medicales,
        }
    )


@login_required
def ajouter_societe(request):
    form = SocieteForm()

    if request.method == "POST":
        form = SocieteForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.libelle) + '-' + secrets.token_urlsafe(8)
            instance.save()

            messages.success(
                request,
                f"La société '{instance.libelle}' a été ajoutée avec succès !"
            )

            return redirect(
                'parametrage_general:liste_societes'
            )

    societes = Societe.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_societes.html',
        {
            'societes': societes,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def modifier_societe(request, pk):
    societe = get_object_or_404(Societe, pk=pk)

    if request.method == "POST":
        form = SocieteForm(
            request.POST,
            instance=societe
        )

        if form.is_valid():
            instance = form.save()

            messages.success(
                request,
                f"La société '{instance.libelle}' a été modifiée avec succès !"
            )

            return redirect(
                'parametrage_general:liste_societes'
            )
    else:
        form = SocieteForm(instance=societe)

    societes = Societe.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_societes.html',
        {
            'societes': societes,
            'form': form,
            'modifier': True,
        }
    )


@login_required
def supprimer_societe(request, pk):
    societe = get_object_or_404(Societe, pk=pk)
    societe.delete()

    messages.success(
        request,
        "La société a été supprimée."
    )

    return redirect(
        'parametrage_general:liste_societes'
    )


@login_required
def liste_societes(request):
    societes = Societe.objects.all()
    form = SocieteForm()

    return render(
        request,
        'backend/parametrage_general/pages/liste_societes.html',
        {
            'societes': societes,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_ville(request):
    form = VilleForm()

    if request.method == "POST":
        form = VilleForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.libelle) + '-' + secrets.token_urlsafe(8)
            instance.save()

            messages.success(
                request,
                "La ville a été ajoutée avec succès !"
            )

            return redirect(
                'parametrage_general:ajouter_ville'
            )

    villes = Ville.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_villes.html',
        {
            'form': form,
            'villes': villes,
            'modifier': False,
        }
    )


@login_required
def modifier_ville(request, pk):
    ville = get_object_or_404(Ville, pk=pk)
    villes = Ville.objects.all()

    if request.method == "POST":
        form = VilleForm(
            request.POST,
            instance=ville
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La ville a été modifiée avec succès !"
            )

            return redirect(
                'parametrage_general:ajouter_ville'
            )
    else:
        form = VilleForm(instance=ville)

    return render(
        request,
        'backend/parametrage_general/pages/liste_villes.html',
        {
            'form': form,
            'villes': villes,
            'modifier': True,
            'ville_mod': ville,
        }
    )


@login_required
def supprimer_ville(request, pk):
    ville = get_object_or_404(Ville, pk=pk)
    ville.delete()

    messages.success(
        request,
        "La ville a été supprimée avec succès !"
    )

    return redirect(
        'parametrage_general:ajouter_ville'
    )


@login_required
def liste_villes(request):
    villes = Ville.objects.all()
    form = VilleForm()

    return render(
        request,
        'backend/parametrage_general/pages/liste_villes.html',
        {
            'villes': villes,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_site(request):
    form = SiteForm()

    if request.method == "POST":
        form = SiteForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom_site) + '-' + secrets.token_urlsafe(8)
            instance.save()

            messages.success(
                request,
                "Le site a été ajouté avec succès !"
            )

            return redirect(
                'parametrage_general:liste_sites'
            )

    sites = Site.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_sites.html',
        {
            'form': form,
            'sites': sites,
            'modifier': False,
        }
    )


@login_required
def modifier_site(request, pk):
    site = get_object_or_404(Site, pk=pk)

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['actif'] = 'actif' in request.POST

        form = SiteForm(
            post_data,
            instance=site
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Le site a été modifié avec succès !"
            )

            return redirect(
                'parametrage_general:liste_sites'
            )
    else:
        form = SiteForm(instance=site)

    sites = Site.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_sites.html',
        {
            'sites': sites,
            'form': form,
            'modifier': True,
            'site_to_edit': site,
        }
    )


@login_required
def supprimer_site(request, pk):
    site = get_object_or_404(Site, pk=pk)
    site.delete()

    messages.success(
        request,
        "Le site a été supprimé."
    )

    return redirect(
        'parametrage_general:liste_sites'
    )


@login_required
def liste_sites(request):
    sites = Site.objects.all()
    form = SiteForm()

    return render(
        request,
        'backend/parametrage_general/pages/liste_sites.html',
        {
            'sites': sites,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def liste_directions(request):
    directions = Direction.objects.all()
    form = DirectionForm()

    return render(
        request,
        'backend/parametrage_general/pages/liste_directions.html',
        {
            'directions': directions,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_direction(request):
    form = DirectionForm()

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['actif'] = 'actif' in post_data

        form = DirectionForm(post_data)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.save()

            messages.success(
                request,
                "La direction a été ajoutée avec succès !"
            )

            return redirect(
                'parametrage_general:liste_directions'
            )

    directions = Direction.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_directions.html',
        {
            'form': form,
            'directions': directions,
            'modifier': False,
        }
    )


@login_required
def modifier_direction(request, pk):
    direction = get_object_or_404(Direction, pk=pk)

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['actif'] = 'actif' in post_data

        form = DirectionForm(
            post_data,
            instance=direction
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La direction a été modifiée avec succès !"
            )

            return redirect(
                'parametrage_general:liste_directions'
            )
    else:
        form = DirectionForm(instance=direction)

    directions = Direction.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_directions.html',
        {
            'form': form,
            'directions': directions,
            'modifier': True,
            'direction_to_edit': direction,
        }
    )


@login_required
def supprimer_direction(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    direction.delete()

    messages.success(
        request,
        "La direction a été supprimée."
    )

    return redirect(
        'parametrage_general:liste_directions'
    )


@login_required
def toggle_direction(request, pk):
    direction = get_object_or_404(Direction, pk=pk)

    direction.actif = not direction.actif
    direction.save()

    status = "activée" if direction.actif else "désactivée"

    messages.success(
        request,
        f"La direction a été {status}."
    )

    return redirect(
        'parametrage_general:liste_directions'
    )


@login_required
def ajouter_departement(request):
    form = DepartementForm()

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['actif'] = 'actif' in post_data

        form = DepartementForm(post_data)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.save()

            messages.success(
                request,
                "Le département a été ajouté avec succès !"
            )

            return redirect(
                'parametrage_general:liste_departements'
            )

    departements = Departement.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_departements.html',
        {
            'form': form,
            'departements': departements,
            'modifier': False,
        }
    )


@login_required
def modifier_departement(request, pk):
    departement = get_object_or_404(
        Departement,
        pk=pk
    )

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['actif'] = 'actif' in post_data

        form = DepartementForm(
            post_data,
            instance=departement
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Le département a été modifié avec succès !"
            )

            return redirect(
                'parametrage_general:liste_departements'
            )
    else:
        form = DepartementForm(
            instance=departement
        )

    departements = Departement.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_departements.html',
        {
            'form': form,
            'departements': departements,
            'modifier': True,
            'departement_to_edit': departement,
        }
    )


@login_required
def supprimer_departement(request, pk):
    departement = get_object_or_404(
        Departement,
        pk=pk
    )

    departement.delete()

    messages.success(
        request,
        "Le département a été supprimé."
    )

    return redirect(
        'parametrage_general:liste_departements'
    )


@login_required
def toggle_departement(request, pk):
    departement = get_object_or_404(
        Departement,
        pk=pk
    )

    departement.actif = not departement.actif
    departement.save()

    status = "activé" if departement.actif else "désactivé"

    messages.success(
        request,
        f"Le département a été {status}."
    )

    return redirect(
        'parametrage_general:liste_departements'
    )


@login_required
def liste_departements(request):
    departements = Departement.objects.all()
    form = DepartementForm()

    return render(
        request,
        'backend/parametrage_general/pages/liste_departements.html',
        {
            'departements': departements,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_service(request):
    departements = Departement.objects.filter(actif=True)

    if request.method == "POST":
        form = ServiceForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.actif = 'actif' in request.POST
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.save()

            messages.success(
                request,
                "Le service a été ajouté avec succès !"
            )

            return redirect(
                'parametrage_general:liste_services'
            )
    else:
        form = ServiceForm()

    services = Service.objects.select_related(
        'departement'
    ).all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_services.html',
        {
            'form': form,
            'services': services,
            'departements': departements,
            'modifier': False,
        }
    )


@login_required
def modifier_service(request, pk):
    service = get_object_or_404(
        Service,
        pk=pk
    )

    departements = Departement.objects.filter(
        actif=True
    )

    if request.method == "POST":
        form = ServiceForm(
            request.POST,
            instance=service
        )

        if form.is_valid():
            instance = form.save(commit=False)
            instance.actif = 'actif' in request.POST
            instance.save()

            messages.success(
                request,
                "Le service a été modifié avec succès !"
            )

            return redirect(
                'parametrage_general:liste_services'
            )
    else:
        form = ServiceForm(
            instance=service
        )

    services = Service.objects.select_related(
        'departement'
    ).all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_services.html',
        {
            'form': form,
            'services': services,
            'departements': departements,
            'modifier': True,
            'service_to_edit': service,
        }
    )


@login_required
def supprimer_service(request, pk):
    service = get_object_or_404(
        Service,
        pk=pk
    )

    service.delete()

    messages.success(
        request,
        "Le service a été supprimé."
    )

    return redirect(
        'parametrage_general:liste_services'
    )


@login_required
def liste_services(request):
    services = Service.objects.select_related(
        'departement'
    ).all()

    departements = Departement.objects.filter(
        actif=True
    )

    form = ServiceForm()

    return render(
        request,
        'backend/parametrage_general/pages/liste_services.html',
        {
            'services': services,
            'departements': departements,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_fonction(request):
    services = Service.objects.filter(
        actif=True
    )

    if request.method == "POST":
        post_data = request.POST.copy()

        if 'actif' not in post_data:
            post_data['actif'] = False

        form = FonctionForm(post_data)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.save()

            messages.success(
                request,
                "La fonction a été ajoutée avec succès !"
            )

            return redirect(
                'parametrage_general:liste_fonctions'
            )
    else:
        form = FonctionForm()

    fonctions = Fonction.objects.select_related(
        'service'
    ).all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_fonctions.html',
        {
            'fonctions': fonctions,
            'services': services,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def modifier_fonction(request, pk):
    fonction = get_object_or_404(
        Fonction,
        pk=pk
    )

    services = Service.objects.filter(
        actif=True
    )

    if request.method == "POST":
        post_data = request.POST.copy()

        if 'actif' not in post_data:
            post_data['actif'] = False

        form = FonctionForm(
            post_data,
            instance=fonction
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La fonction a été modifiée avec succès !"
            )

            return redirect(
                'parametrage_general:liste_fonctions'
            )
    else:
        form = FonctionForm(
            instance=fonction
        )

    fonctions = Fonction.objects.select_related(
        'service'
    ).all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_fonctions.html',
        {
            'fonctions': fonctions,
            'services': services,
            'form': form,
            'modifier': True,
            'fonction_to_edit': fonction,
        }
    )


@login_required
def supprimer_fonction(request, pk):
    fonction = get_object_or_404(
        Fonction,
        pk=pk
    )

    fonction.delete()

    messages.success(
        request,
        "La fonction a été supprimée."
    )

    return redirect(
        'parametrage_general:liste_fonctions'
    )


@login_required
def liste_fonctions(request):
    fonctions = Fonction.objects.select_related(
        'service'
    ).all()

    services = Service.objects.filter(
        actif=True
    )

    form = FonctionForm()

    return render(
        request,
        'backend/parametrage_general/pages/liste_fonctions.html',
        {
            'fonctions': fonctions,
            'services': services,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def liste_specialites(request):
    specialites = Specialite.objects.all()
    form = SpecialiteForm()

    return render(
        request,
        'backend/parametrage_general/pages/liste_specialites.html',
        {
            'specialites': specialites,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_specialite(request):
    form = SpecialiteForm()

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['actif'] = 'actif' in post_data

        form = SpecialiteForm(post_data)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.save()

            messages.success(
                request,
                "La spécialité a été ajoutée avec succès !"
            )

            return redirect(
                'parametrage_general:liste_specialites'
            )

    specialites = Specialite.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_specialites.html',
        {
            'form': form,
            'specialites': specialites,
            'modifier': False,
        }
    )


@login_required
def modifier_specialite(request, pk):
    specialite = get_object_or_404(
        Specialite,
        pk=pk
    )

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['actif'] = 'actif' in post_data

        form = SpecialiteForm(
            post_data,
            instance=specialite
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "La spécialité a été modifiée avec succès !"
            )

            return redirect(
                'parametrage_general:liste_specialites'
            )
    else:
        form = SpecialiteForm(
            instance=specialite
        )

    specialites = Specialite.objects.all()

    return render(
        request,
        'backend/parametrage_general/pages/liste_specialites.html',
        {
            'specialites': specialites,
            'form': form,
            'modifier': True,
            'specialite_to_edit': specialite,
        }
    )


@login_required
def supprimer_specialite(request, pk):
    specialite = get_object_or_404(
        Specialite,
        pk=pk
    )

    specialite.delete()

    messages.success(
        request,
        "La spécialité a été supprimée."
    )

    return redirect(
        'parametrage_general:liste_specialites'
    )


@login_required
def toggle_specialite(request, pk):
    specialite = get_object_or_404(
        Specialite,
        pk=pk
    )

    specialite.actif = not specialite.actif
    specialite.save()

    status = "activée" if specialite.actif else "désactivée"

    messages.success(
        request,
        f"La spécialité a été {status}."
    )

    return redirect(
        'parametrage_general:liste_specialites'
    )


@login_required
def liste_unites_medicales(request):
    unites_medicales = UniteMedicale.objects.select_related(
        'site'
    ).prefetch_related(
        'specialites'
    ).all()

    sites = Site.objects.filter(
        actif=True
    ).order_by('nom_site')

    specialites = Specialite.objects.filter(
        actif=True
    ).order_by('nom')

    form = UniteMedicaleForm()

    return render(
        request,
        'backend/parametrage_general/pages/liste_unites_medicales.html',
        {
            'unites_medicales': unites_medicales,
            'sites': sites,
            'specialites': specialites,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def ajouter_unite_medicale(request):
    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['actif'] = 'actif' in request.POST

        form = UniteMedicaleForm(post_data)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = slugify(instance.nom) + '-' + secrets.token_urlsafe(8)
            instance.save()
            form.save_m2m()

            messages.success(
                request,
                f"L'unité médicale '{instance.nom}' a été ajoutée avec succès !"
            )

            return redirect(
                'parametrage_general:liste_unites_medicales'
            )
    else:
        form = UniteMedicaleForm()

    unites_medicales = UniteMedicale.objects.select_related(
        'site'
    ).prefetch_related(
        'specialites'
    ).all()

    sites = Site.objects.filter(
        actif=True
    ).order_by('nom_site')

    specialites = Specialite.objects.filter(
        actif=True
    ).order_by('nom')

    return render(
        request,
        'backend/parametrage_general/pages/liste_unites_medicales.html',
        {
            'unites_medicales': unites_medicales,
            'sites': sites,
            'specialites': specialites,
            'form': form,
            'modifier': False,
        }
    )


@login_required
def modifier_unite_medicale(request, pk):
    unite = get_object_or_404(
        UniteMedicale,
        pk=pk
    )

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data['actif'] = 'actif' in request.POST

        form = UniteMedicaleForm(
            post_data,
            instance=unite
        )

        if form.is_valid():
            instance = form.save(commit=False)
            instance.slug = unite.slug
            instance.save()
            form.save_m2m()

            messages.success(
                request,
                f"L'unité médicale '{instance.nom}' a été modifiée avec succès !"
            )

            return redirect(
                'parametrage_general:liste_unites_medicales'
            )
    else:
        form = UniteMedicaleForm(
            instance=unite
        )

    unites_medicales = UniteMedicale.objects.select_related(
        'site'
    ).prefetch_related(
        'specialites'
    ).all()

    sites = Site.objects.filter(
        actif=True
    ).order_by('nom_site')

    specialites = Specialite.objects.filter(
        actif=True
    ).order_by('nom')

    return render(
        request,
        'backend/parametrage_general/pages/liste_unites_medicales.html',
        {
            'unites_medicales': unites_medicales,
            'sites': sites,
            'specialites': specialites,
            'form': form,
            'modifier': True,
            'unite_to_edit': unite,
        }
    )


@login_required
def supprimer_unite_medicale(request, pk):
    unite = get_object_or_404(
        UniteMedicale,
        pk=pk
    )

    unite.delete()

    messages.success(
        request,
        "L'unité médicale a été supprimée."
    )

    return redirect(
        'parametrage_general:liste_unites_medicales'
    )


@login_required
def toggle_unite_medicale(request, pk):
    unite = get_object_or_404(
        UniteMedicale,
        pk=pk
    )

    unite.actif = not unite.actif
    unite.save()

    status = "activée" if unite.actif else "désactivée"

    messages.success(
        request,
        f"L'unité médicale a été {status}."
    )

    return redirect(
        'parametrage_general:liste_unites_medicales'
    )


@login_required
def configuration_etablissement(request):
    config = ConfigurationEtablissement.objects.first()

    return render(
        request,
        'backend/parametrage_general/pages/config_etablissement/configuration_etablissement.html',
        {
            'config': config
        }
    )


@login_required
def modifier_configuration_etablissement(request):
    config = ConfigurationEtablissement.objects.first()

    if request.method == "POST":
        form = ConfigurationEtablissementForm(
            request.POST,
            request.FILES,
            instance=config
        )

        if form.is_valid():
            config = form.save()

            cache.delete('config_etablissement')

            messages.success(
                request,
                "Configuration de l'établissement mise à jour."
            )

            return redirect(
                'parametrage_general:configuration_etablissement'
            )
    else:
        form = ConfigurationEtablissementForm(
            instance=config
        )

    return render(
        request,
        'backend/parametrage_general/pages/config_etablissement/modifier_configuration_etablissement.html',
        {
            'form': form,
            'config': config
        }
    )