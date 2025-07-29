import os
import json
from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
from urllib.parse import urljoin
from pathlib import PurePosixPath
register = template.Library()


@register.filter(is_safe=True)
def replaceFilter(value, replaceStr):
    strArr = replaceStr.split('=>')
    old = strArr[0]
    new = strArr[1]
    return value


@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def is_false(arg):
    return arg is False


@register.filter
def get_type(value):
    return type(value)


@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))


@register.filter(name='json_loads')
def json_loads(value):
    return json.loads(value)


@register.filter
def replaceSpaceUnderscore(value):
    return value.replace(' ', '_')


@register.filter
def replaceUnderscoreSeparator(value):
    return value.replace('_', '-')


@register.filter
def hash(h, key):
    return h[key]


@register.simple_tag
def define(val=None):
    return val


@register.filter
def list_item(lst, i):
    try:
        return lst[i]
    except:
        return None


@register.filter
def to_str(value):
    """converts int to string"""
    return str(value)


@register.filter
def get_item(dictionary, key):
    is_vite = settings.IS_VITE
    if is_vite:
        if os.environ.get('CYPRESS_TEST_APP', '0') == '1':
            is_vite = False
    if is_vite:
        return f'http://localhost:3000/src/{key}'
    file_path = dictionary.get(key, '')
    sanitized_path = file_path.lstrip('/')
    static_url = urljoin(settings.STATIC_URL, sanitized_path)
    normalized_url = str(PurePosixPath(static_url))
    return normalized_url

#END OF QUBE
