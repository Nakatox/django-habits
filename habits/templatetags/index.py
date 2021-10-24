from django import template

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter(name='index2')
def index2(string,str):
    return string in str