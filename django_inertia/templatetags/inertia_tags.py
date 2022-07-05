import json

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def inertia(context: template.Context, app_id: str = "app"):
    page = context[settings.INERTIA_PAGE_CONTEXT]
    return format_html(
        "<div id=\"{}\" data-page='{}'></div>", mark_safe(app_id), mark_safe(json.dumps(page))
    )
