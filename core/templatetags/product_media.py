from django import template

from core.services import search_product_image

register = template.Library()


@register.simple_tag
def product_placeholder_image(product):
    return search_product_image(
        getattr(product, 'name', ''),
        getattr(product, 'category', ''),
    )
