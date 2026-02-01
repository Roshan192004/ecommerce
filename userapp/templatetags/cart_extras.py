from django import template

register = template.Library()

@register.filter
def multiply(price, qty):
    return price * qty
