# -*- coding: utf-8 -*-

import json
from copy import deepcopy
from lxml import etree
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('plone')


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

    def __init__(self, pattern=None, pattern_options={}, el='input',
                 name=None):
        self.pattern = pattern
        self.el = etree.Element(el)
        if pattern:
            self.klass = self._klass_prefix + pattern
        self.name = name
        self.pattern_options = pattern_options

    def update(self):
        if self.pattern_options:
            self.el.attrib['data-pat-' + self.pattern] = \
                json.dumps(self.pattern_options)

    def render(self):
        self.update()
        return etree.tostring(self.el)


class InputWidget(BaseWidget):
    """
    """

    type = el_attrib('type')
    value = el_attrib('value')

    def __init__(self, pattern=None, pattern_options={}, name=None,
                 _type='text', value=None):
        super(InputWidget, self).__init__(pattern, pattern_options, 'input',
                                          name)
        self.type = _type
        self.value = value


class SelectWidget(BaseWidget):
    """
    """

    def __init__(self, pattern=None, pattern_options={}, name=None, options=[],
                 selected=None):
        super(SelectWidget, self).__init__(pattern, pattern_options, 'select',
                                           name)
        self.options = options
        self.selected = selected

    def get_options(self):
        for element in self.el.iter("option"):
            yield element.attrib['value'], element.text

    def set_options(self, value):
        if not value:
            self.el.text = ' '
            return
        for token, title in value:
            option = etree.SubElement(self.el, 'option')
            option.attrib['value'] = token
            option.text = title

    def del_options(self):
        for element in self.el.iter("option"):
            self.el.remove(element)

    options = property(get_options, set_options, del_options)

    def get_selected(self):
        for element in self.el.iter("option"):
            if 'selected' in element.attrib and \
               element.attrib['selected'] == 'selected':
                return element.attrib['value']

    def set_selected(self, value):
        if value is None:
            return
        for element in self.el.iter("option"):
            if element.attrib['value'] == value:
                element.attrib['selected'] = 'selected'
            elif 'selected' in element.attrib and \
                 element.attrib['selected'] == 'selected':
                del element.attrib['selected']

    def del_selected(self):
        for element in self.el.iter("option"):
            if 'selected' in element.attrib and \
               element.attrib['selected'] == 'selected':
                del element.attrib['selected']

    selected = property(get_selected, set_selected, del_selected)


class DateWidget(InputWidget):
    """
    """

    def __init__(self, pattern='pickadate', pattern_options={}, name=None,
                 _type='date', value=None, request=None, calendar='gregorian',
                 format_date_id='pickadate_date_format',
                 format_date_default='dd/mm/yyyy'):
        _pattern_options = {'date': {'format': format_date_default},
                            'time': 'false'}
        if request is not None:
            calendar = request.locale.dates.calendars[calendar]
            _pattern_options = dict_merge(_pattern_options, {
                'date': {
                    'monthsFull': calendar.getMonthNames(),
                    'monthsShort': calendar.getMonthAbbreviations(),
                    'weekdaysFull': calendar.getDayNames(),
                    'weekdaysShort': calendar.getDayAbbreviations(),
                    'today': translate(_(u"Today"), context=request),
                    'clear': translate(_(u"Clear"), context=request),
                    'format': translate(
                        format_date_id,
                        domain='plone.app.widgets',
                        context=request,
                        default=format_date_default),
                },
            })
        _pattern_options = dict_merge(_pattern_options, pattern_options)
        _pattern_options['date']['formatSubmit'] = 'dd-mm-yyyy'
        super(DateWidget, self).__init__(pattern, _pattern_options, name,
                                         _type, value)


class DatetimeWidget(DateWidget):
    """
    """

    def __init__(self, pattern='pickadate', pattern_options={}, name=None,
                 _type='datetime-local', value=None, request=None,
                 calendar='gregorian', format_date_id='pickadate_date_format',
                 format_date_default='dd/mm/yyyy',
                 format_time_id='pickadate_time_format',
                 format_time_default='HH:i'):
        timeOptions = pattern_options.get('time', {})
        super(DatetimeWidget, self).__init__(pattern, pattern_options, name,
                                             _type, value, request, calendar,
                                             format_date_id,
                                             format_date_default)
        self.pattern_options['time'] = timeOptions
        if isinstance(self.pattern_options['time'], dict):
            self.pattern_options['time']['formatSubmit'] = 'HH:i'


class Select2Widget(InputWidget):
    """
    """

    def __init__(self, pattern='select2', pattern_options={}, name=None,
                 _type='text', value=None):
        super(Select2Widget, self).__init__(pattern, pattern_options, name,
                                            _type, value)
