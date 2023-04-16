from django import template
from system.models import Entities, Files, RelationsFiles
from system.views import category_detail

register = template.Library()

@register.simple_tag()
def current_entities():
    return RelationsFiles.objects.all()