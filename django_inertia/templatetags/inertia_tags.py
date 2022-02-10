from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def inertia(context, app_id="app"):
    page = context["page"]
    return format_html('<div id="{}" data-page="{}"></div>', mark_safe(app_id), mark_safe(page))
