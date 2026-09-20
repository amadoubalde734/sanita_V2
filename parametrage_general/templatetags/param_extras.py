from django import template

register = template.Library()


@register.filter
def has_item(a_list, value):
    """Vérifie si `value` est présent dans `a_list` (utilisable dans un {% if %})."""
    return value in (a_list or [])