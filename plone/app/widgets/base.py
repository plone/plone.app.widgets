# -*- coding: utf-8 -*-

from copy import deepcopy
from lxml import etree

import json


def el_attrib(name):
    """Helper property methods to get/set/delete element property.

    :param name: [required] Name of the element property.
    :type name: string

    :returns: Property with getter/setter/deletter.
    :rtype: property
    """

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


def dict_merge(dict_a, dict_b):
    """Helper method which merges two dictionaries.

    Recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and b have a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.

    http://www.xormedia.com/recursively-merge-dictionaries-in-python

    :param dict_a: [required] First dictiornary.
    :type dict_a: dict

    :param dict_b: [required] Second dictiornary.
    :type dict_b: dict

    :returns: Merged dictionary.
    :rtype: dict
    """

    if not isinstance(dict_b, dict):
        return dict_b
    result = deepcopy(dict_a)
    for k, v in dict_b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


class BaseWidget(object):
    """Basic patterns widget."""

    _klass_prefix = 'pat-'
    klass = el_attrib('class')

    def __init__(self, el, pattern, pattern_options={}):
        """
        :param el: [required] element type (eg. input, div, textarea, a, ...).
        :type el: string

        :param pattern: [required] Pattern name.
        :type pattern: string

        :param pattern_options: Patterns options.
        :type pattern_options: dict
        """

        self.pattern = pattern
        self.el = etree.Element(el)
        if pattern:
            self.klass = self._klass_prefix + pattern
        self.pattern_options = pattern_options

    def update(self):
        """Updating pattern_options in element `data-*` attribute."""
        if self.pattern_options:
            self.el.attrib['data-' + self._klass_prefix + self.pattern] = \
                json.dumps(self.pattern_options)

    def render(self):
        """Renders the widget

        :returns: Widget's HTML.
        :rtype: string
        """

        self.update()
        return etree.tostring(self.el)


class DivWidget(BaseWidget):
    """Widget with `div` element."""

    def __init__(self, pattern, pattern_options={}):
        """
        :param pattern: [required] Pattern name.
        :type pattern: string

        :param pattern_options: Patterns options.
        :type pattern_options: dict

        """
        super(DivWidget, self).__init__('div', pattern, pattern_options)


class InputWidget(BaseWidget):
    """Widget with `input` element."""

    type = el_attrib('type')
    value = el_attrib('value')
    name = el_attrib('name')

    def __init__(self, pattern, pattern_options={}, type='text', name=None,
                 value=None):
        """
        :param pattern: [required] Pattern name.
        :type pattern: string

        :param pattern_options: Patterns options.
        :type pattern_options: dict

        :param type: `type` attribute of element.
        :type type: string

        :param name: `name` attribute of element.
        :type name: string

        :param value: `value` attribute of element.
        :type value: string
        """
        super(InputWidget, self).__init__('input', pattern, pattern_options)
        self.type = type
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value


class SelectWidget(BaseWidget):
    """Widget with `select` element."""

    name = el_attrib('name')
    _multiple = el_attrib('multiple')

    def __init__(self, pattern, pattern_options={}, items=[], name=None,
                 value=None, multiple=False):
        """
        :param pattern: [required] Pattern name.
        :type pattern: string

        :param pattern_options: Patterns options.
        :type pattern_options: dict

        :param items: List of value and title pairs which represents possible
                      options to choose from.
        :type items: list

        :param name: `name` attribute of element.
        :type name: string

        :param value: `value` attribute of element.
        :type value: string

        :param multiple: `multiple` attribute of element.
        :type multiple: bool
        """
        super(SelectWidget, self).__init__('select', pattern, pattern_options)
        self.el.text = ''
        self.items = items
        self.multiple = multiple
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value

    def _get_items(self):
        """Get list of possible options.

        :returns: List of value and title pairs.
        :rtype: list
        """

        for element in self.el.iter("option"):
            yield element.attrib['value'], element.text

    def _set_items(self, value):
        """Set options for element.

        :param value: List of value and title pairs which represents possible
                      options to choose from.
        :type value: list
        """
        for token, title in value:
            option = etree.SubElement(self.el, 'option')
            option.attrib['value'] = token
            option.text = title

    def _del_items(self):
        """Removing options from inside of elements."""
        for element in self.el.iter("option"):
            self.el.remove(element)

    items = property(_get_items, _set_items, _del_items)

    def _get_value(self):
        """Return selected option(s).

        :returns: Returns list of selected option(s) values.
        :rtype: list
        """
        value = []
        for element in self.el.iter("option"):
            if 'selected' in element.attrib and \
                    element.attrib['selected'] == 'selected':
                value.append(element.attrib['value'])
        return value

    def _set_value(self, value):
        """Select option(s).

        :param value: We are expecting option's value which should be selected.
        :type value: list or string
        """
        if isinstance(value, basestring):
            value = [value]

        for element in self.el.iter("option"):
            if element.attrib['value'] in value:
                element.attrib['selected'] = 'selected'
            elif 'selected' in element.attrib and \
                    element.attrib['selected'] == 'selected':
                del element.attrib['selected']

    def _del_value(self):
        """Unselect all selected options.
        """
        for element in self.el.iter("option"):
            if 'selected' in element.attrib and \
               element.attrib['selected'] == 'selected':
                del element.attrib['selected']

    value = property(_get_value, _set_value, _del_value)

    def _get_multiple(self):
        """Does element allows multiple items to be selected.

        :returns: `True` if allows multiple elements to be selected, otherwise
                  `False`.
        :rtype: bool
        """
        if self._multiple == 'multiple':
            return True
        return False

    def _set_multiple(self, value):
        """Make element accept multiple values.

        :param value: `True` if you want to set element as `multiple`,
                      otherwise `False`
        :type value: bool
        """
        if value:
            self._multiple = 'multiple'
        else:
            self._del_multiple()

    def _del_multiple(self):
        """Remove `multiple` attribute from element."""
        del self._multiple

    multiple = property(_get_multiple, _set_multiple, _del_multiple)


class TextareaWidget(BaseWidget):
    """Widget with `textarea` element."""

    name = el_attrib('name')

    def __init__(self, pattern, pattern_options={}, name=None, value=None):
        """
        :param pattern: [required] Pattern name.
        :type pattern: string

        :param pattern_options: Patterns options.
        :type pattern_options: dict

        :param name: `name` attribute of element.
        :type name: string

        :param value: `value` of element.
        :type value: string
        """
        super(TextareaWidget, self).__init__('textarea', pattern,
                                             pattern_options)
        self.el.text = ''
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value

    def _get_value(self):
        """
        :returns: Value of element.
        :rtype: string
        """
        return self.el.text

    def _set_value(self, value):
        """
        :param value: Set value of element.
        :type value: string
        """
        self.el.text = value

    def _del_value(self):
        """Set empty string as value of element."""
        self.el.text = ''

    value = property(_get_value, _set_value, _del_value)
