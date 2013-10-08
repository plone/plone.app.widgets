# -*- coding: utf-8 -*-

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from datetime import date
from datetime import datetime
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.widgets import base
from plone.app.widgets import utils
from z3c.form import interfaces as z3cform_interfaces
from z3c.form.browser.select import SelectWidget as z3cform_SelectWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import NO_VALUE
from z3c.form.widget import Widget
from zope.component import adapts
from zope.component import providedBy
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.interface import implementsOnly
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IDate
from zope.schema.interfaces import IDatetime
from zope.schema.interfaces import IList
from zope.schema.interfaces import IVocabularyFactory

import json

_ = MessageFactory('plone.app.widgets')
_plone = MessageFactory('plone')


class NotImplemented(Exception):
    pass


class IDatetimeWidget(z3cform_interfaces.ITextWidget):
    """Marker interface for the DatetimeWidget."""


class IDateWidget(z3cform_interfaces.ITextWidget):
    """Marker interface for the DateWidget."""


class ISelectWidget(z3cform_interfaces.ISelectWidget):
    """Marker interface for the SelectWidget."""


class IAjaxSelectWidget(z3cform_interfaces.ITextWidget):
    """Marker interface for the Select2Widget."""


class IQueryStringWidget(z3cform_interfaces.ITextWidget):
    """Marker interface for the QueryStringWidget."""


class IRelatedItemsWidget(z3cform_interfaces.ITextWidget):
    """Marker interface for the RelatedItemsWidget."""


class DatetimeWidgetConverter(BaseDataConverter):
    """Data converter for datetime stuff."""

    adapts(IDatetime, IDatetimeWidget)

    def toWidgetValue(self, value):
        """Coverts from field value to widget.

        :param value: Field value.
        :type value: datetime

        :returns: Datetime in format `Y-m-d H:M`
        :rtype: string
        """
        if value is self.field.missing_value:
            return u''
        return ('{value.year:}-{value.month:02}-{value.day:02} '
                '{value.hour:02}:{value.minute:02}').format(value=value)

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: Value inserted by datetime widget.
        :param value: string

        :returns: `datetime.datetime` object.
        :rtype: datetime
        """
        if not value:
            return self.field.missing_value
        tmp = value.split(' ')
        if not tmp[0]:
            return self.field.missing_value
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


class BaseWidget(Widget):
    """Base pattern widget for z3c.form."""

    pattern = None
    pattern_options = {}

    def _base_args(self):
        """
        """
        if self.pattern is None:
            raise NotImplemented("'pattern' options not provided.")
        return {
            'pattern': self.pattern,
            'pattern_options': self.pattern_options,
        }

    def render(self):
        """
        :returns:
        :rtype: string
        """
        if self.mode != 'input':
            return super(BaseWidget, self).render()
        return self._base(**self._base_args()).render()


class DatetimeWidget(BaseWidget):
    """Datetime pattern widget for z3c.form."""

    _base = base.InputWidget

    implementsOnly(IDatetimeWidget)

    pattern = 'pickadate'
    pattern_options = BaseWidget.pattern_options.copy()

    def _base_args(self):
        args = super(DatetimeWidget, self)._base_args()
        args['name'] = self.name

        value = (self.request.get(self.name, self.value) or u'').strip()
        if len(value.split(' ')) == 1:
            value += ' 00:00'
        args['value'] = value

        today = date.today()
        args.setdefault('pattern_options', {})
        _pattern_options_calendar = utils.get_calendar_options(self.request)
        _pattern_options_defaults = {
            'selectYears': 200,
            'min': [today.year - 100, 1, 1],
            'max': [today.year + 20, 1, 1],
            'format_date': translate(
                _('pickadate_date_format', default='mmmm d, yyyy'),
                context=self.request),
            'format_time': translate(
                _('pickadate_time_format', default='h:i a'),
                context=self.request),
            'placeholderDate': translate(_plone('Enter date...'),
                                         context=self.request),
            'placeholderTime': translate(_plone('Enter time...'),
                                         context=self.request),
            'today': translate(_plone(u"Today"), context=self.request),
            'clear': translate(_plone(u"Clear"), context=self.request),
        }

        args['pattern_options'] = base.dict_merge(
            args['pattern_options'],
            _pattern_options_defaults)

        args['pattern_options'] = base.dict_merge(
            args['pattern_options'],
            _pattern_options_calendar)

        return args

    def render(self):
        if self.mode != 'display':
            return super(DatetimeWidget, self).render()

        if not self.value:
            return ''

        field_value = DatetimeWidgetConverter(
            self.field, self).toFieldValue(self.value)
        if field_value is self.fields.missing_value:
            return u''

        formatter = self.request.locale.dates.getFormatter("dateTime", "short")
        if field_value.year > 1900:
            return formatter.format(field_value)

        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return field_value.ctime()


class DateWidget(DatetimeWidget):

    implementsOnly(IDateWidget)

    pattern_options = DatetimeWidget.pattern_options.copy()

    def _widget_args(self):
        args = super(DateWidget, self)._base_args()
        args['pattern_options']['time'] = False
        del args['pattern_options']['format_time']
        return args

    def render(self):
        if self.mode != 'display':
            return super(DateWidget, self).render()

        if not self.value:
            return ''

        field_value = DateWidgetConverter(
            self.field, self).toFieldValue(self.value)
        if field_value is self.fields.missing_value:
            return u''

        formatter = self.request.locale.dates.getFormatter("date", "short")
        if field_value.year > 1900:
            return formatter.format(field_value)

        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return field_value.ctime()


class SelectWidget(BaseWidget, z3cform_SelectWidget):

    _base_klass = base.SelectWidget

    implementsOnly(ISelectWidget)

    pattern = 'select2'
    pattern_options = BaseWidget.pattern_options.copy()

    def _base_args(self):
        args = super(SelectWidget, self)._base_args()

        options = []
        for item in self.items():
            options.append((item['value'], item['content']))
        args['options'] = options
        args['selected'] = self.value
        if self.multiple:
            args['multiple'] = 'multiple'

        return args


class AjaxSelectWidget(BaseWidget):

    _base = base.InputWidget

    implementsOnly(IAjaxSelectWidget)

    pattern = 'select2'
    pattern_options = BaseWidget.pattern_options.copy()

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
                        try:
                            term = vocabulary.getTerm(value)
                            initialValues[term.token] = term.title
                        except LookupError:
                            initialValues[value] = value
                args['pattern_options']['initialValues'] = initialValues

        return args


class QueryStringWidget(BaseWidget):

    pattern = 'querystring'
    pattern_options = BaseWidget.pattern_options.copy()

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
