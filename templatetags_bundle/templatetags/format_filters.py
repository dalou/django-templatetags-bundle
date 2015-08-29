# encoding: utf-8

import json
import datetime
import re

from django import template
from django import forms
from django.template.defaultfilters import floatformat
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as django_now
from django.utils.translation import to_locale, get_language
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from django.forms.util import flatatt

from babel import Locale
from babel.numbers import format_number, format_decimal, format_percent

register = template.Library()

DEFAULT_CURRENCY = 'EUR'
# Send in data way to assets/js/input_format.js
CURRENCY_PATTERNS = {
    'EUR': { 'format': u'%s €', 'locale': 'fr_FR', 'spacing': ' ', 'decimal': ',', 'placeholder': 'EUR' },
    'USD': { 'format': u'$%s', 'locale': 'en_US', 'spacing': ',', 'decimal': '.', 'placeholder': 'USD' },
}

def price_format_decimal_to_currency(value, currency='EUR'):
    if value:
        try:
            if currency in CURRENCY_PATTERNS.keys():
                value = CURRENCY_PATTERNS[currency]['format'] % format_number(value, locale = CURRENCY_PATTERNS[currency]['locale'])
            else:
                return value
        except:
            return value
    return value

def price_format_currency_to_decimal(value, currency='EUR'):
    if value == None:
        return None
    value = unicode(value)
    if value.strip() == '':
        return None

    float_value = ""
    float_lock = False
    for c in value[::-1]:
        if c.isdigit():
            float_value += c
        if not float_lock and (c == '.' or c == ','):
            float_value += '.'
            float_lock = True

    try:
        return float(float_value[::-1]);
    except:
        return None

@register.filter
def percentage(value):
    if value or value == 0:
        kwargs = {
            'locale': to_locale(get_language()),
            'format': "#,##0.00 %",
        }
        return format_percent(value, **kwargs)


@register.filter
def smartdate(value):
    if isinstance(value, datetime.datetime):
        now = django_now()
    else:
        now = datetime.date.today()

    timedelta = value - now
    format = _(u"%(delta)s %(unit)s")
    delta = abs(timedelta.days)

    if delta > 30:
        delta = int(delta / 30)
        unit = _(u"mois")
    else:
        unit = _(u"jours")

    ctx = {
        'delta': delta,
        'unit': unit,
    }

    return format % ctx



@register.filter(name='formatted_price')
def formatted_price(value, currency='EUR'):
    return price_format_decimal_to_currency(value, currency)

@register.filter(name='formatted_float')
def formatted_float(value, currency='EUR'):
    return price_format_decimal_to_currency(value, currency)



@register.filter(name='sizify')
def sizify(file):
    """
    Simple kb/mb/gb size snippet for templates:

    {{ product.file.size|sizify }}
    """
    #value = ing(value)
    try:
        value = file.size
        if value < 512000:
            value = value / 1024.0
            ext = 'kb'
        elif value < 4194304000:
            value = value / 1048576.0
            ext = 'mb'
        else:
            value = value / 1073741824.0
            ext = 'gb'
        return '%s %s' % (str(round(value, 2)), ext)
    except:
        'n/a'
@register.filter
def file_sizify(value):
    return sizify(file)


@register.filter
def jsonify(obj):
    return json.dumps(obj)



@register.filter
def truncate_filename(value, args, maxchars=20, endchars='[...]'):

    """
    usage : {{ 'very_long_filename_display_blah_blah.zip'|truncate_filename:'20,...' }}
    result : very_long_file[...].zip
    """

    arg_list = [arg.strip() for arg in args.split(',')]
    # print arg_list
    if len(arg_list) == 1:
        maxchars = int(arg_list[0])
    if len(arg_list) == 2:
        endchars = arg_list[1]

    filename_ext = value.rsplit('.', 1)
    if len(filename_ext) >= 1:
        filename = filename_ext[0]
        ext = filename_ext[1]
    else:
        filename = value
        ext = ''

    if len(filename) > maxchars:
        return filename[:maxchars] + endchars + ext
    else:
        return value



tag_end_re = re.compile(r'(\w+)[^>]*>')
entity_end_re = re.compile(r'(\w+;)')

@register.filter
def truncatehtml(string, length, ellipsis='...'):
    """Truncate HTML string, preserving tag structure and character entities."""
    length = int(length)
    output_length = 0
    i = 0
    pending_close_tags = {}

    while output_length < length and i < len(string):
        c = string[i]

        if c == '<':
            # probably some kind of tag
            if i in pending_close_tags:
                # just pop and skip if it's closing tag we already knew about
                i += len(pending_close_tags.pop(i))
            else:
                # else maybe add tag
                i += 1
                match = tag_end_re.match(string[i:])
                if match:
                    tag = match.groups()[0]
                    i += match.end()

                    # save the end tag for possible later use if there is one
                    match = re.search(r'(</' + tag + '[^>]*>)', string[i:], re.IGNORECASE)
                    if match:
                        pending_close_tags[i + match.start()] = match.groups()[0]
                else:
                    output_length += 1 # some kind of garbage, but count it in

        elif c == '&':
            # possible character entity, we need to skip it
            i += 1
            match = entity_end_re.match(string[i:])
            if match:
                i += match.end()

            # this is either a weird character or just '&', both count as 1
            output_length += 1
        else:
            # plain old characters

            skip_to = string.find('<', i, i + length)
            if skip_to == -1:
                skip_to = string.find('&', i, i + length)
            if skip_to == -1:
                skip_to = i + length

            # clamp
            delta = min(skip_to - i,
                        length - output_length,
                        len(string) - i)

            output_length += delta
            i += delta

    output = [string[:i]]
    if output_length == length:
        output.append(ellipsis)

    for k in sorted(pending_close_tags.keys()):
        output.append(pending_close_tags[k])

    return "".join(output)


truncatehtml.is_safe = True