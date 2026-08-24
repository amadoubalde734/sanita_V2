# parametrage_general/context_processors.py
from django.core.cache import cache
from .models import ConfigurationEtablissement

def configuration_etablissement(request):
    config = cache.get('config_etablissement')
    if config is None:
        config = ConfigurationEtablissement.objects.first()
        cache.set('config_etablissement', config, 3600)  # 1h
    return {
        'config_etablissement': config,
    }