# -*- coding: utf-8 -*-

import json
from datetime import date
from datetime import datetime
from zope.interface import Interface
from zope.interface import implementsOnly
from zope.interface import implementer
from zope.component import adapts
from zope.component import adapter
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.schema.interfaces import IDate
from zope.schema.interfaces import IDatetime
from zope.schema.interfaces import ITextLine
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import ISequence
from zope.schema.interfaces import IList
from zope.schema.interfaces import IVocabularyFactory
from z3c.form.converter import BaseDataConverter
from z3c.form.widget import Widget
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IWidget
from z3c.form.interfaces import IFieldWidget
from plone.app.z3cform.widget import IDatetimeField
from plone.app.z3cform.widget import IDateField
from plone.registry.interfaces import IRegistry
from plone.app.querystring.interfaces import IQuerystringRegistryReader
from plone.app.widgets import base
from plone.app.widgets.interfaces import IWidgetsLayer


class IDatetimeWidget(IWidget):
    """Marker interface for the DatetimeWidget
    """


class IDateWidget(IWidget):
    """Marker interface for the DateWidget
    """


class ISelectWidget(IWidget):
    """Marker interface for the SelectWidget
    """


class ISelect2Widget(IWidget):
    """Marker interface for the Select2Widget
    """


class IQueryStringWidget(IWidget):
    """Marker interface for the QueryStringWidget
    """


class DatetimeWidgetConverter(BaseDataConverter):
    """Data converter for datetime stuff."""

    adapts(IDatetime, IDatetimeWidget)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return u''
        return '%s-%s-%s %s:%s' % (value.year,
                                   value.month,
                                   value.day,
                                   value.hour,
                                   value.minute)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        tmp = value.split(' ')
        value = tmp[0].split('-')
        value += tmp[1].split(':')
        return datetime(*map(int, value))


class DateWidgetConverter(BaseDataConverter):
    """Data converter for date stuff.
    """

    adapts(IDate, IDateWidget)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return u''
        return '%s-%s-%s' % (value.year,
                             value.month,
                             value.day)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        return date(*map(int, value.split('-')))


class Select2WidgetConverter(BaseDataConverter):
    """Data converter for ISequence.
    """

    adapts(ISequence, ISelect2Widget)

    def toWidgetValue(self, value):
        if self.field.missing_value and value in self.field.missing_value:
            return u''
        return self.widget.separator.join(unicode(v) for v in value)

    def toFieldValue(self, value):
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]
        if not len(value):
            return self.field.missing_value
        valueType = self.field.value_type._type
        if isinstance(valueType, tuple):
            valueType = valueType[0]
        return collectionType(valueType(v)
                              for v in value.split(self.widget.separator))


class QueryStringDataConverter(BaseDataConverter):

    adapts(IList, IQueryStringWidget)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return value
        return json.dumps(value)

    def toFieldValue(self, value):
        if value is self.field.missing_value:
            return value
        return json.loads(value)


class BaseWidget(Widget):
    """
    """

    _widget_klass = base.BaseWidget

    pattern = None
    pattern_options = {}

    def _widget_args(self):
        return {
            'name': self.name,
            'pattern': self.pattern,
            'pattern_options': self.pattern_options,
        }

    def render(self):
        if self.mode == 'display':
            return super(BaseWidget, self).render()
        return self._widget_klass(**self._widget_args()).render()


class InputWidget(BaseWidget):

    _widget_klass = base.InputWidget

    pattern_options = BaseWidget.pattern_options.copy()

    def _widget_args(self):
        args = super(InputWidget, self)._widget_args()
        # XXX: we might need to decode the value and encoding shouldn't be
        # hardcoded (value.decode('utf-8'))
        value = self.request.get(self.name, self.value)
        args['value'] = value
        return args


class SelectWidget(BaseWidget):

    _widget_klass = base.SelectWidget

    implementsOnly(ISelectWidget)

    pattern_options = BaseWidget.pattern_options.copy()

    def _widget_args(self):
        args = super(SelectWidget, self)._widget_args()

        options = None
        if self.field and self.field.vocabulary:
            options = []
            for term in self.field.vocabulary:
                options.append((term.token, term.title))
        elif self.field and self.field.vocabularyName:
            options = []
            for term in getUtility(IVocabularyFactory,
                                   self.field.vocabularyName)(self.context):
                options.append((term.token, term.title))
        args['options'] = options

        return args


class DatetimeWidget(InputWidget):

    _widget_klass = base.DatetimeWidget

    implementsOnly(IDatetimeWidget)

    pattern = 'pickadate'
    pattern_options = InputWidget.pattern_options.copy()

    def _widget_args(self):
        args = super(InputWidget, self)._widget_args()
        args['request'] = self.request
        return args


class DateWidget(DatetimeWidget):

    _widget_klass = base.DatetimeWidget

    implementsOnly(IDateWidget)

    pattern_options = DatetimeWidget.pattern_options.copy()


class Select2Widget(InputWidget):

    _widget_klass = base.Select2Widget

    implementsOnly(ISelect2Widget)

    pattern = 'select2'
    pattern_options = InputWidget.pattern_options.copy()
    separator = ';'
    ajax_vocabulary = None

    def _widget_args(self):
        args = super(Select2Widget, self)._widget_args()
        if self.ajax_vocabulary:
            portal_state = queryMultiAdapter((self.context, self.request),
                                             name=u'plone_portal_state')
            url = ''
            if portal_state:
                url += portal_state.portal_url()
            url += '/@@getVocabulary?name=' + self.ajax_vocabulary
            if 'pattern_options' not in args:
                args['pattern_options'] = {}
            args['pattern_options']['ajaxvocabulary'] = url
        return args


class QueryStringWidget(InputWidget):

    pattern = 'querystring'

    implementsOnly(IQueryStringWidget)

    def _widget_args(self):
        args = super(QueryStringWidget, self)._widget_args()

        registry = getUtility(IRegistry)
        config = IQuerystringRegistryReader(registry)()

        if 'pattern_options' not in args:
            args['pattern_options'] = {}
        args['pattern_options'].update(config)

        return args


@adapter(IDatetimeField, IWidgetsLayer)
@implementer(IFieldWidget)
def DateTimeFieldWidget(field, request):
    """IFieldWidget factory for DateTimeWidget."""
    return FieldWidget(field, DatetimeWidget(request))


@adapter(IDateField, IWidgetsLayer)
@implementer(IFieldWidget)
def DateFieldWidget(field, request):
    """IFieldWidget factory for DateWidget."""
    return FieldWidget(field, DateWidget(request))


@adapter(ICollection, Interface, IWidgetsLayer)
@implementer(IFieldWidget)
def SelectFieldWidget(field, source, request=None):
    """IFieldWidget factory for Select2Widget."""
    # BBB: emulate our pre-2.0 signature (field, request)
    if request is None:
        request = source
    return FieldWidget(field, SelectWidget(request))


@adapter(ISequence, ITextLine, IWidgetsLayer)
@implementer(IFieldWidget)
def Select2FieldWidget(field, value_type, request):
    """IFieldWidget factory for TagsWidget."""
    return FieldWidget(field, Select2Widget(request))
