import django
from django import template

from smart_if import smart_if


register = template.Library()


try:
    if int(django.get_version()[-5:]) < 11806:
        register.tag('if', smart_if)
except ValueError:
    pass
