from django import template

register = template.Library()

@register.simple_tag
def get_queue_info(shop, timeslots):
    return shop.checkQueue(timeslots)

@register.filter
def lengthrange(value):
    return range(len(value))