# -*- coding: utf-8 -*-
import json
from datetime import date
from datetime import datetime
from zope.interface import implementsOnly
from zope.component import adapts
from zope.component import providedBy
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.schema.interfaces import IDate
from zope.schema.interfaces import IDatetime
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IList
from zope.schema.interfaces import IVocabularyFactory
from z3c.form.browser.select import SelectWidget as z3cform_SelectWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import NO_VALUE
from z3c.form.widget import Widget
from z3c.form import interfaces as z3cform_interfaces
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.widgets import base


class IDatetimeWidget(z3cform_interfaces.ITextWidget):
    """Marker interface for the DatetimeWidget
    """


class IDateWidget(z3cform_interfaces.ITextWidget):
    """Marker interface for the DateWidget
    """


class ISelectWidget(z3cform_interfaces.ISelectWidget):
    """Marker interface for the SelectWidget
    """


class IAjaxSelectWidget(z3cform_interfaces.ITextWidget):
    """Marker interface for the Select2Widget
    """


class IQueryStringWidget(z3cform_interfaces.ITextWidget):
    """Marker interface for the QueryStringWidget
    """


class IRelatedItemsWidget(z3cform_interfaces.ITextWidget):
    """Marker interface for the RelatedItemsWidget
    """


class DatetimeWidgetConverter(BaseDataConverter):
    """Data converter for datetime stuff."""

    adapts(IDatetime, IDatetimeWidget)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return u''
        return '%d-%02d-%02d %s:%s' % (
            value.year, value.month, value.day, value.hour, value.minute)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        tmp = value.split(' ')
        if not tmp[0]:
            return None
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
        return '%d-%02d-%02d' % (value.year, value.month, value.day)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        return date(*map(int, value.split('-')))


class AjaxSelectWidgetConverter(BaseDataConverter):
    """Data converter for ICollection.
    """

    adapts(ICollection, IAjaxSelectWidget)

    def toWidgetValue(self, value):
        if not value:
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
        return collectionType(valueType and valueType(v) or v
                              for v in value.split(self.widget.separator))


class RelatedItemsDataConverter(BaseDataConverter):
    """Data converter for ICollection.
    """

    adapts(ICollection, IRelatedItemsWidget)

    def toWidgetValue(self, value):
        if not value:
            return u''
        return self.widget.separator.join(unicode(v.UID()) for v in value)

    def toFieldValue(self, value):
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]
        if not len(value):
            return self.field.missing_value
        catalog = getToolByName(self.widget.context, 'portal_catalog')
        value = value.split(self.widget.separator)
        value = [v.split('/')[0] for v in value]
        results = catalog(UID=value)
        return collectionType(item.getObject() for item in results)


class QueryStringDataConverter(BaseDataConverter):
    """data converter for ilist.
    """

    adapts(IList, IQueryStringWidget)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return u''
        return json.dumps(value)

    def toFieldValue(self, value):
        if value is self.field.missing_value:
            return self.field.missing_value
        return json.loads(value)


class NotImplemented(Exception):
    pass


class InputWidget(Widget):
    """
    """

    _base = base.InputWidget

    pattern_options = {}
    pattern = None

    def _base_args(self):
        if self.pattern is None:
            raise NotImplemented
        return {
            'name': self.name,
            'pattern': self.pattern,
            'pattern_options': self.pattern_options,
            'value': self.request.get(self.name, self.value),
        }

    def render(self):
        if self.mode != 'input':
            return super(InputWidget, self).render()
        return self._base(**self._base_args()).render()


class DateWidget(InputWidget):
    _widget_klass = base.InputWidget

    implementsOnly(IDateWidget)

    pattern = 'pickadate'
    pattern_options = InputWidget.pattern_options.copy()
    pattern_options['time'] = False

    def _widget_args(self):
        args = super(InputWidget, self)._widget_args()
        args['request'] = self.request
        args['pattern_options']['date'] = {'value': self.value}
        return args

    def extract(self, default=NO_VALUE):
        return self.request.form.get(self.name + '_date', default)

    def render(self):
        if self.mode != 'display':
            return super(DateWidget, self).render()

        if not self.value:
            return ''
        try:
            date_value = DateWidgetConverter(
                self.field, self).toFieldValue(self.value)
        except ValueError:
            return ''
        formatter = self.request.locale.dates.getFormatter("date", "short")
        if date_value.year > 1900:
            return formatter.format(date_value)
        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return date_value.ctime()


class DatetimeWidget(DateWidget):
    _widget_klass = base.InputWidget

    implementsOnly(IDatetimeWidget)

    pattern_options = DateWidget.pattern_options.copy()

    def _widget_args(self):
        args = super(InputWidget, self)._widget_args()
        args['request'] = self.request
        value = self.value or u''
        value = value.split(' ')
        args['pattern_options']['date'] = {'value': value[0]}
        args['pattern_options']['time'] = {
            'value': value[1] if len(value) > 1 else '00:00'}
        return args

    def extract(self, default=NO_VALUE):
        date_value = self.request.form.get(self.name + '_date', default)
        time_value = self.request.form.get(self.name + '_time', '00:00')
        if date_value is default:
            return default

        return ' '.join([date_value, time_value])

    def render(self):
        if self.mode != 'display':
            return super(DateWidget, self).render()

        if not self.value:
            return ''
        try:
            date_value = DatetimeWidgetConverter(
                self.field, self).toFieldValue(self.value)
        except ValueError:
            return ''
        formatter = self.request.locale.dates.getFormatter("dateTime", "short")
        if date_value.year > 1900:
            return formatter.format(date_value)
        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return date_value.ctime()


class SelectWidget(InputWidget, z3cform_SelectWidget):

    _widget_klass = base.SelectWidget

    implementsOnly(ISelectWidget)

    pattern = 'select2'
    pattern_options = InputWidget.pattern_options.copy()

    def _widget_args(self):
        args = super(SelectWidget, self)._widget_args()

        options = []
        for item in self.items():
            options.append((item['value'], item['content']))
        args['options'] = options
        args['selected'] = self.value
        if self.multiple:
            args['multiple'] = 'multiple'

        return args


class AjaxSelectWidget(InputWidget):

    _base = base.InputWidget

    implementsOnly(IAjaxSelectWidget)

    pattern = 'select2'
    pattern_options = InputWidget.pattern_options.copy()

    separator = ';'
    vocabulary = None

    def _base_args(self):

        def get_portal():
            closest_site = getSite()
            if closest_site is not None:
                for potential_portal in closest_site.aq_chain:
                    if ISiteRoot in providedBy(potential_portal):
                        return potential_portal

        def get_portal_url():
            portal = get_portal()
            if portal:
                root = getNavigationRootObject(self.context, portal)
                if root:
                    return root.absolute_url()
            return ''

        args = super(AjaxSelectWidget, self)._widget_args()
        args['pattern_options']['separator'] = self.separator

        vocabulary_factory = getattr(self.field, 'vocabulary_factory', None)
        if not self.vocabulary:
            self.vocabulary = vocabulary_factory

        # get url which will be used to lookup vocabulary
        if self.vocabulary:
            vocabulary_url = '%s/@@getVocabulary?name=%s' % (
                get_portal_url(), self.vocabulary)
            args['pattern_options']['vocabularyUrl'] = vocabulary_url

            # initial values
            if self.value:
                vocabulary = queryUtility(IVocabularyFactory, self.vocabulary)
                if vocabulary:
                    initialValues = {}
                    vocabulary = vocabulary(self.context)
                    for value in self.value.split(self.separator):
                        term = vocabulary.getTerm(value)
                        initialValues[term.token] = term.title
                args['pattern_options']['initialValues'] = initialValues

        return args


class QueryStringWidget(InputWidget):

    pattern = 'querystring'
    pattern_options = InputWidget.pattern_options.copy()

    implementsOnly(IQueryStringWidget)

    def _base_args(self):
        args = super(QueryStringWidget, self)._widget_args()

        if 'pattern_options' not in args:
            args['pattern_options'] = {}
        args['pattern_options']['indexOptionsUrl'] = '%s/@@qsOptions' % (
            getSite().absolute_url())

        return args


class RelatedItemsWidget(AjaxSelectWidget):

    pattern = 'relateditems'
    pattern_options = AjaxSelectWidget.pattern_options.copy()

    implementsOnly(IRelatedItemsWidget)
