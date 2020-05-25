from django import template

register = template.Library()

@register.filter(name='by_idx')
def by_idx(lst,idx):
    return lst[idx]

@register.filter(name='range')
def range(min=5):
    return range(min)