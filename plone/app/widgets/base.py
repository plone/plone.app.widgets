# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from datetime import date
from lxml import etree
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('plone.app.widgets')
P_ = MessageFactory('plone')


def el_attrib(name):

    def _get(self):
        if name in self.el.attrib:
            value = self.el.attrib[name]
            if value.strip().startswith('[') or value.strip().startswith('{'):
                value = json.loads(value)
            return value

    def _set(self, value):
        if value is None:
            return
        if type(value) in (list, tuple):
            value = ' '.join(value)
        if type(value) in (dict, set):
            value = json.dumps(value)
        if type(value) is str:
            value = value.decode('utf8')
        self.el.attrib[name] = value

    def _del(self):
        if name in self.el.attrib:
            del self.el.attrib[name]

    return property(_get, _set, _del)


def dict_merge(a, b):
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and bhave a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.

    http://www.xormedia.com/recursively-merge-dictionaries-in-python
    '''
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


class BaseWidget(object):
    """
    """

    _klass_prefix = 'pat-'

    name = el_attrib('name')
    klass = el_attrib('class')

    def __init__(self, pattern, el, name, pattern_options={}):
        self.pattern = pattern
        self.el = etree.Element(el)
        if pattern:
            self.klass = self._klass_prefix + pattern
        self.name = name
        self.pattern_options = pattern_options

    def update(self):
        if self.pattern_options:
            self.el.attrib['data-' + self._klass_prefix + self.pattern] = \
                json.dumps(self.pattern_options)

    def render(self):
        self.update()
        return etree.tostring(self.el)


class InputWidget(BaseWidget):
    """
    """

    type = el_attrib('type')
    value = el_attrib('value')

    def __init__(self, pattern, name, pattern_options={},
                 type='text', value=None):
        super(InputWidget, self).__init__(pattern, 'input', name,
                                          pattern_options)
        self.type = type
        if value is not None:
            self.value = value


class SelectWidget(BaseWidget):
    """
    """

    def __init__(self, pattern, name, pattern_options={}, items=[],
                 value=None, multiple=False):
        super(SelectWidget, self).__init__(pattern, 'select', name,
                                           pattern_options)
        self.el.text = ''
        self.items = items
        self.multiple = multiple
        if value is not None:
            self.value = value

    def get_multiple(self):
        if self._multiple == 'multiple':
            return True
        return False

    def set_multiple(self, value):
        if value:
            self._multiple = 'multiple'
        else:
            del self._multiple

    def del_multiple(self):
        del self._multiple

    _multiple = el_attrib('multiple')
    multiple = property(get_multiple, set_multiple, del_multiple)

    def get_items(self):
        for element in self.el.iter("option"):
            yield element.attrib['value'], element.text

    def set_items(self, value):
        for token, title in value:
            option = etree.SubElement(self.el, 'option')
            option.attrib['value'] = token
            option.text = title

    def del_items(self):
        for element in self.el.iter("option"):
            self.el.remove(element)

    items = property(get_items, set_items, del_items)

    def get_value(self):
        if self.multiple:
            value = []
            for element in self.el.iter("option"):
                if 'selected' in element.attrib and \
                        element.attrib['selected'] == 'selected':
                    value.append(element.attrib['value'])
        else:
            value = None
            for element in self.el.iter("option"):
                if 'selected' in element.attrib and \
                        element.attrib['selected'] == 'selected':
                    value = element.attrib['value']
                    break
        return value

    def set_value(self, value):
        if self.multiple and type(value) not in (list, tuple):
            raise TypeError
        elif not self.multiple and not isinstance(value, basestring):
            raise TypeError
        for element in self.el.iter("option"):
            if self.multiple and element.attrib['value'] in value:
                element.attrib['selected'] = 'selected'
            elif not self.multiple and element.attrib['value'] == value:
                element.attrib['selected'] = 'selected'
            elif 'selected' in element.attrib and \
                    element.attrib['selected'] == 'selected':
                del element.attrib['selected']

    def del_value(self):
        for element in self.el.iter("option"):
            if 'selected' in element.attrib and \
               element.attrib['selected'] == 'selected':
                del element.attrib['selected']

    value = property(get_value, set_value, del_value)


class TextareaWidget(BaseWidget):
    """
    """

    def __init__(self, pattern, name, pattern_options={}, value=None):
        super(TextareaWidget, self).__init__(pattern, 'textarea', name,
                                             pattern_options)
        self.el.text = ''
        if value is not None:
            self.value = value

    def get_value(self):
        return self.el.text

    def set_value(self, value):
        self.el.text = value

    def del_value(self):
        self.el.text = ''

    value = property(get_value, set_value, del_value)


#class PickadatePatternWidget(InputWidget):
#    """
#    """
#
#    def __init__(self, name, pattern_options={}, type='date', value=None):
#        super(PickadatePatternWidget, self).__init__(
#            'pickadate', name, pattern_options, type, value)
#
# Date
#        _pattern_options = {'date': {'format': format_date or 'mmmm d, yyyy'},
#                            'time': 'false'}
#        if request is not None:
#            if format_date is None:
#                format_date = translate(
#                    _('pickadate_date_format', default='mmmm d, yyyy'),
#                    context=request)
#            calendar = request.locale.dates.calendars[calendar]
#            year = date.today().year
#            weekdaysFull = [
#                calendar.days.get(t, (None, None))[0]
#                for t in (7, 1, 2, 3, 4, 5, 6)]
#            weekdaysShort = [
#                calendar.days.get(t, (None, None))[1]
#                for t in (7, 1, 2, 3, 4, 5, 6)]
#            _pattern_options = dict_merge(_pattern_options, {
#                'date': {
#                    'selectYears': 200,
#                    'min': [year - 100, 1, 1],
#                    'max': [year + 20, 1, 1],
#                    'monthsFull': calendar.getMonthNames(),
#                    'monthsShort': calendar.getMonthAbbreviations(),
#                    'weekdaysFull': weekdaysFull,
#                    'weekdaysShort': weekdaysShort,
#                    'today': translate(P_(u"Today"), context=request),
#                    'clear': translate(P_(u"Clear"), context=request),
#                    'format': format_date,
#                },
#            })
#
# Datetime
#        timeOptions = pattern_options.get('time', {})
#        if isinstance(timeOptions, dict):
#            timeOptions['format'] = format_time or 'HH:i'
#            if request is not None:
#                if format_time is None:
#                    format_time = translate(
#                        _('pickadate_time_format', default='HH:i'),
#                        context=request)
#                timeOptions['format'] = format_time
#            timeOptions['formatSubmit'] = 'HH:i'
#        self.pattern_options['time'] = timeOptions
