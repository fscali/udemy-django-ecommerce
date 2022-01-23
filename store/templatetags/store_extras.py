from django import template

register = template.Library()


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def currency(amount):
    return f'${amount:.2f}'


@register.filter
def mult(arg1, arg2):
    return arg1 * arg2
