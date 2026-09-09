from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect


def root_redirect(request):
    return redirect('/dashboard/')


urlpatterns = [
    path('', root_redirect),

    path('portail/', include('front.urls')),

    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path(
    'cartes-sanitaires/',
    include(('cartes_sanitaires.urls', 'cartes_sanitaires'), namespace='cartes_sanitaires')
    ),
    path(
        'entreprises/',
        include(('entreprises.urls', 'entreprises'), namespace='entreprises')
    ),
    path('parametrage/', include(('parametrage_general.urls', 'parametrage_general'), namespace='parametrage_general')),

    path('administration/', include(('administration.urls', 'administration'), namespace='administration')),
    path('abonnement/', include(('abonnement.urls', 'abonnement'), namespace='abonnement')),
    path('audit/', include(('audit.urls', 'audit'), namespace='audit')),
    path('api/', include(('api.urls', 'api'), namespace='api')),
    path('cliniques/', include(('cliniques_partenaires.urls', 'cliniques_partenaires'), namespace='cliniques_partenaires')),
    path('consultations/', include(('consultations.urls', 'consultations'), namespace='consultations')),
    path('consultations_dentaires/', include(('consultations_dentaires.urls', 'consultations_dentaires'), namespace='consultations_dentaires')),
    path('documents/', include(('documents.urls', 'documents'), namespace='documents')),
    path('imagerie/', include(('imagerie.urls', 'imagerie'), namespace='imagerie')),
    path('laboratoires/', include(('laboratoires.urls', 'laboratoires'), namespace='laboratoires')),
    path('medecins/', include(('medecins.urls', 'medecins'), namespace='medecins')),
    path('medicaments/', include(('medicaments.urls', 'medicaments'), namespace='medicaments')),
    path('ordonnances/', include(('ordonnances.urls', 'ordonnances'), namespace='ordonnances')),
    path('patients/', include(('patients.urls', 'patients'), namespace='patients')),
    path('personnels/', include(('personnels.urls', 'personnels'), namespace='personnels')),
    path('infirmiers/', include(('infirmiers.urls', 'infirmiers'), namespace='infirmiers')),
    path('pharmacie/', include(('pharmacie.urls', 'pharmacie'), namespace='pharmacie')),
    path('stock/', include(('stock.urls', 'stock'), namespace='stock')),
    path('workflow/', include(('workflow.urls', 'workflow'), namespace='workflow')),
    
]


urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]