from django import template

register = template.Library()

@register.filter(name="total")
def total(milestones):

    total=0
    for x in milestones:
        total += x.cost

    return total
