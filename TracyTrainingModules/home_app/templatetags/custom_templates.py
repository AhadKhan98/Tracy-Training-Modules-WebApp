from django import template

register = template.Library()

@register.filter(name='by_idx')
def by_idx(lst,idx):
    return lst[idx]