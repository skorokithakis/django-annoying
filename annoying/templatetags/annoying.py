from django import template

from smart_if import smart_if


register = template.Library()

register.tag('if', smart_if)
