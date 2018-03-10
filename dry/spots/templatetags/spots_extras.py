from django import template

register = template.Library()


@register.filter(name='strip_newlines')
def cut(value):
    return value.replace('\n', ' ').replace('\r', '')
