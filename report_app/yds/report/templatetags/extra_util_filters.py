from django import template


register = template.Library()


@register.filter(name='split_id_from_url')
def split_id_from_url(arg):
    return arg.split('/')[5]

