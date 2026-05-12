from django import template

from core.services import convert_xaf_price


register = template.Library()


@register.simple_tag
def converted_prices(amount):
    return convert_xaf_price(amount)
