# -*- coding: utf-8 -*-

import json
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
        self.el.attrib[name] = value

    def _del(self):
        if name in self.el.attrib:
            del self.el.attrib[name]

    return property(_get, _set, _del)


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

    def get_pattern_options(self):
        if self.pattern and 'data-pat-' + self.pattern in self.el.attrib:
            return json.loads(self.el.attrib['data-pat-' + self.pattern])

    def set_pattern_options(self, value):
        if not self.pattern or len(value) == 0:
            return
        self.el.attrib['data-pat-' + self.pattern] = json.dumps(value)

    def del_pattern_options(self):
        if self.pattern and 'data-pat-' + self.pattern in self.el.attrib:
            del self.el.attrib['data-pat-' + self.pattern]

    pattern_options = property(
        get_pattern_options,
        set_pattern_options,
        del_pattern_options)

    def render(self):
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
        if value is None:
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
                 format_id='pickadate_date_format',
                 format_default='yyyy-mm-dd @'):
        _pattern_options = {'format': format_default}
        if request is not None:
            calendar = request.locale.dates.calendars[calendar]
            _pattern_options.update({
                'pickadate-monthsFull': calendar.getMonthNames(),
                'pickadate-monthsShort': calendar.getMonthAbbreviations(),
                'pickadate-weekdaysFull': calendar.getDayNames(),
                'pickadate-weekdaysShort': calendar.getDayAbbreviations(),
                'pickadate-today': translate(_(u"Today"), context=request),
                'pickadate-clear': translate(_(u"Clear"), context=request),
                'format': translate(
                    format_id,
                    domain='plone.app.widgets',
                    context=request,
                    default=format_default),
            })
        _pattern_options.update(pattern_options)
        _pattern_options['formatSubmit'] = 'yyyy-mm-dd'
        super(DateWidget, self).__init__(pattern, _pattern_options, name,
                                         _type, value)


class DatetimeWidget(DateWidget):
    """
    """

    def __init__(self, pattern='pickadate', pattern_options={}, name=None,
                 _type='datetime-local', value=None, request=None,
                 calendar='gregorian', format_id='pickadate_datetime_format',
                 format_default='yyyy-mm-dd @ HH:MM'):
        super(DatetimeWidget, self).__init__(pattern, pattern_options, name,
                                             _type, value, request, calendar,
                                             format_id, format_default)
        self.pattern_options['formatSubmit'] = 'yyyy-mm-dd HH:MM'


class Select2Widget(InputWidget):
    """
    """

    def __init__(self, pattern='select2', pattern_options={}, name=None,
                 _type='text', value=None):
        super(Select2Widget, self).__init__(pattern, pattern_options, name,
                                            _type, value)
