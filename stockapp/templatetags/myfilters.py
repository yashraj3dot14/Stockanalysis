from django import template
register = template.Library()

@register.filter
def get(mapping, key): #mapping is in form of dictionary, we are fetching data from dict. by passing key in func
    return mapping.get(key, '')