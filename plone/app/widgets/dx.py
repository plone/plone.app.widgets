# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from datetime import date
from datetime import datetime
from plone.app.widgets.base import InputWidget
from plone.app.widgets.base import SelectWidget
from plone.app.widgets.base import TextareaWidget
from plone.app.widgets.base import dict_merge
from plone.app.widgets.interfaces import IFieldPermissionChecker
from plone.app.widgets.testing import TestRequest
from plone.app.widgets.utils import NotImplemented
from plone.app.widgets.utils import get_date_options
from plone.app.widgets.utils import get_datetime_options
from plone.app.widgets.utils import get_ajaxselect_options
from plone.app.widgets.utils import get_relateditems_options
from plone.app.widgets.utils import get_querystring_options
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.autoform.interfaces import WIDGETS_KEY
from plone.autoform.utils import resolveDottedName
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.utils import iterSchemata
from plone.supermodel.utils import mergedTaggedValueDict
from plone.uuid.interfaces import IUUID
from z3c.form.browser.select import SelectWidget as z3cform_SelectWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.interfaces import ISelectWidget
from z3c.form.interfaces import ITextAreaWidget
from z3c.form.interfaces import ITextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import Widget
from zope.component import adapts
from zope.component import queryUtility
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.interface import implementsOnly
from zope.security.interfaces import IPermission
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IDate
from zope.schema.interfaces import IDatetime
from zope.schema.interfaces import IList
from zope.schema.interfaces import ISequence

import json


class IDateWidget(ITextWidget):
    """Marker interface for the DateWidget."""


class IDatetimeWidget(ITextWidget):
    """Marker interface for the DatetimeWidget."""


class ISelectWidget(ISelectWidget):
    """Marker interface for the SelectWidget."""


class IAjaxSelectWidget(ITextWidget):
    """Marker interface for the Select2Widget."""


class IQueryStringWidget(ITextWidget):
    """Marker interface for the QueryStringWidget."""


class IRelatedItemsWidget(ITextWidget):
    """Marker interface for the RelatedItemsWidget."""


class ITinyMCEWidget(ITextAreaWidget):
    """Marker interface for the TinyMCEWidget."""


class DateWidgetConverter(BaseDataConverter):
    """Data converter for date fields."""

    adapts(IDate, IDateWidget)

    def toWidgetValue(self, value):
        """Converts from field value to widget.

        :param value: Field value.
        :type value: date

        :returns: Date in format `Y-m-d`
        :rtype: string
        """
        if value is self.field.missing_value:
            return u''
        return ('{value.year:}-{value.month:02}-{value.day:02}'
                ).format(value=value)

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: Value inserted by date widget.
        :type value: string

        :returns: `date.date` object.
        :rtype: date
        """
        if not value:
            return self.field.missing_value
        return date(*map(int, value.split('-')))


class DatetimeWidgetConverter(BaseDataConverter):
    """Data converter for datetime fields."""

    adapts(IDatetime, IDatetimeWidget)

    def toWidgetValue(self, value):
        """Converts from field value to widget.

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
        :type value: string

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


class AjaxSelectWidgetConverter(BaseDataConverter):
    """Data converter for ICollection."""

    adapts(ICollection, IAjaxSelectWidget)

    def toWidgetValue(self, value):
        """Converts from field value to widget.

        :param value: Field value.
        :type value: list |tuple | set

        :returns: Items separated using separator defined on widget
        :rtype: string
        """
        if not value:
            return self.field.missing_value
        separator = getattr(self.widget, 'separator', ';')
        return separator.join(unicode(v) for v in value)

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: Value inserted by AjaxSelect widget.
        :type value: string

        :returns: List of items
        :rtype: list | tuple | set
        """
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]
        if not len(value):
            return self.field.missing_value
        valueType = self.field.value_type._type
        if isinstance(valueType, tuple):
            valueType = valueType[0]
        separator = getattr(self.widget, 'separator', ';')
        return collectionType(valueType and valueType(v) or v
                              for v in value.split(separator))


class RelatedItemsDataConverter(BaseDataConverter):
    """Data converter for ICollection."""

    adapts(ICollection, IRelatedItemsWidget)

    def toWidgetValue(self, value):
        """Converts from field value to widget.

        :param value: List of catalog brains.
        :type value: list

        :returns: List of of UID separated by separator defined on widget.
        :rtype: string
        """
        if not value:
            return self.field.missing_value
        separator = getattr(self.widget, 'separator', ';')
        return separator.join([IUUID(o) for o in value if value])

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: List of UID's separated by separator defined
        :type value: string

        :returns: List of content objects
        :rtype: list | tuple | set
        """
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]

        if not len(value):
            return self.field.missing_value

        separator = getattr(self.widget, 'separator', ';')
        value = value.split(separator)
        value = [v.split('/')[0] for v in value]

        catalog = getToolByName(self.widget.context, 'portal_catalog')

        return collectionType(item.getObject()
                              for item in catalog(UID=value) if item)


class QueryStringDataConverter(BaseDataConverter):
    """Data converter for IList."""

    adapts(IList, IQueryStringWidget)

    def toWidgetValue(self, value):
        """Converts from field value to widget.

        :param value: Query string.
        :type value: list

        :returns: Query string converted to JSON.
        :rtype: string
        """
        if value is self.field.missing_value:
            return self.field.missing_value
        return json.dumps(value)

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: Query string.
        :type value: string

        :returns: Query string.
        :rtype: list
        """
        if value is self.field.missing_value:
            return self.field.missing_value
        return json.loads(value)


class BaseWidget(Widget):
    """Base widget for z3c.form."""

    pattern = None
    pattern_options = {}

    def _base(self, pattern, pattern_options={}):
        """Base widget class."""
        raise NotImplemented

    def _base_args(self):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        if self.pattern is None:
            raise NotImplemented("'pattern' option is not provided.")
        return {
            'pattern': self.pattern,
            'pattern_options': self.pattern_options.copy(),
        }

    def render(self):
        """Render widget.

        :returns: Widget's HTML.
        :rtype: string
        """
        if self.mode != 'input':
            return super(BaseWidget, self).render()
        return self._base(**self._base_args()).render()


class DateWidget(BaseWidget):
    """Date widget for z3c.form."""

    _base = InputWidget
    _converter = DateWidgetConverter
    _formater = 'date'

    implementsOnly(IDateWidget)

    pattern = 'pickadate'
    pattern_options = BaseWidget.pattern_options.copy()

    def _base_args(self):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        args = super(DateWidget, self)._base_args()
        args['name'] = self.name
        args['value'] = (self.request.get(self.name,
                                          self.value) or u'').strip()

        args.setdefault('pattern_options', {})
        args['pattern_options'] = dict_merge(
            args['pattern_options'],
            get_date_options(self.request))

        return args

    def render(self):
        """Render widget.

        :returns: Widget's HTML.
        :rtype: string
        """
        if self.mode != 'display':
            return super(DateWidget, self).render()

        if not self.value:
            return ''

        field_value = self._converter(
            self.field, self).toFieldValue(self.value)
        if field_value is self.fields.missing_value:
            return u''

        formatter = self.request.locale.dates.getFormatter(
            self._formater, "short")
        if field_value.year > 1900:
            return formatter.format(field_value)

        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return field_value.ctime()


class DatetimeWidget(DateWidget):
    """Datetime widget for z3c.form."""

    _converter = DatetimeWidgetConverter
    _formater = 'dateTime'

    implementsOnly(IDatetimeWidget)

    pattern_options = DateWidget.pattern_options.copy()

    def _base_args(self):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        args = super(DatetimeWidget, self)._base_args()

        if args['value'] and len(args['value'].split(' ')) == 1:
            args['value'] += ' 00:00'

        args.setdefault('pattern_options', {})
        args['pattern_options'] = dict_merge(
            args['pattern_options'],
            get_datetime_options(self.request))

        return args


class SelectWidget(BaseWidget, z3cform_SelectWidget):
    """Select widget for z3c.form."""

    _base = SelectWidget

    implementsOnly(ISelectWidget)

    pattern = 'select2'
    pattern_options = BaseWidget.pattern_options.copy()
    multiple = False

    def _base_args(self):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value
            - `multiple`: field multiple
            - `items`: field items from which we can select to

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        args = super(SelectWidget, self)._base_args()
        args['name'] = self.name
        args['value'] = self.value
        args['multiple'] = self.multiple

        items = []
        for item in self.items():
            items.append((item['value'], item['content']))
        args['items'] = items

        # ISequence represents an orderable collection
        if ISequence.providedBy(self.field):
            options = args.setdefault('pattern_options', {})
            options['orderable'] = True

        return args


class AjaxSelectWidget(BaseWidget):
    """Ajax select widget for z3c.form."""

    _base = InputWidget

    implementsOnly(IAjaxSelectWidget)

    pattern = 'select2'
    pattern_options = BaseWidget.pattern_options.copy()

    separator = ';'
    vocabulary = None
    vocabulary_view = '@@getVocabulary'

    def _base_args(self):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """

        args = super(AjaxSelectWidget, self)._base_args()

        vocabulary_factory = getattr(self.field, 'vocabulary_factory', None)
        if not self.vocabulary:
            self.vocabulary = vocabulary_factory

        args['name'] = self.name
        args['value'] = self.value

        options = args.setdefault('pattern_options', {})
        field_name = self.field and self.field.__name__ or None
        args['pattern_options'] = dict_merge(
            options,
            get_ajaxselect_options(self.context, args['value'], self.separator,
                                   self.vocabulary, self.vocabulary_view,
                                   field_name))
        # ISequence represents an orderable collection
        if ISequence.providedBy(self.field):
            args['pattern_options']['orderable'] = True

        return args


class RelatedItemsWidget(BaseWidget):
    """RelatedItems widget for z3c.form."""

    _base = InputWidget

    implementsOnly(IRelatedItemsWidget)

    pattern = 'relateditems'
    pattern_options = BaseWidget.pattern_options.copy()

    separator = ';'
    vocabulary = 'plone.app.vocabularies.Catalog'
    vocabulary_view = '@@getVocabulary'

    def _base_args(self):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """

        args = super(RelatedItemsWidget, self)._base_args()

        vocabulary_factory = getattr(self.field, 'vocabulary_factory', None)
        if not self.vocabulary:
            self.vocabulary = vocabulary_factory

        args['name'] = self.name
        args['value'] = self.value

        args.setdefault('pattern_options', {})
        field_name = self.field and self.field.__name__ or None
        args['pattern_options'] = dict_merge(
            args['pattern_options'],
            get_relateditems_options(self.context, args['value'],
                                     self.separator, self.vocabulary,
                                     self.vocabulary_view,
                                     field_name))

        return args


class QueryStringWidget(BaseWidget):
    """QueryString widget for z3c.form."""

    _base = InputWidget

    implementsOnly(IQueryStringWidget)

    pattern = 'querystring'
    pattern_options = BaseWidget.pattern_options.copy()

    querystring_view = '@@qsOptions'

    def _base_args(self):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        args = super(QueryStringWidget, self)._base_args()
        args['name'] = self.name
        args['value'] = self.value

        args.setdefault('pattern_options', {})
        args['pattern_options'] = dict_merge(
            args['pattern_options'],
            get_querystring_options(self.context, self.querystring_view))

        return args


class TinyMCEWidget(BaseWidget):
    """TinyMCE widget for z3c.form."""

    _base = TextareaWidget

    implementsOnly(ITextAreaWidget)

    pattern = 'tinymce'
    pattern_options = BaseWidget.pattern_options.copy()

    def _base_args(self):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        args = super(TinyMCEWidget, self)._base_args()

        args['name'] = self.name
        args['value'] = self.value

        return args


DEFAULT_PERMISSION = 'Modify portal content'


class DXFieldPermissionChecker(object):
    implements(IFieldPermissionChecker)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context
        self._mock_request = TestRequest()

    def validate(self, field_name, vocabulary_name=None):
        context = self.context
        checker = getSecurityManager().checkPermission
        for schema in iterSchemata(context):
            if field_name in schema:
                # If a vocabulary name was specified and it does not
                # match the vocabulary name for the field or widget,
                # fail.
                field = schema[field_name]
                if vocabulary_name and (
                   vocabulary_name != getattr(field, 'vocabulary', None) and
                   vocabulary_name != getattr(field, 'vocabularyName', None)):
                    # Determine the widget to check for vocabulary there
                    widgets = mergedTaggedValueDict(schema, WIDGETS_KEY)
                    widget = widgets.get(field_name)
                    if widget:
                        widget = (isinstance(widget, basestring) and
                                  resolveDottedName(widget) or widget)
                        widget = widget and widget(field, self._mock_request)
                    else:
                        widget = queryMultiAdapter((field, self._mock_request),
                                                   IFieldWidget)
                    if getattr(widget, 'vocabulary', None) != vocabulary_name:
                        return False
                # Create mapping of all schema permissions
                permissions = mergedTaggedValueDict(schema,
                                                    WRITE_PERMISSIONS_KEY)
                permission_name = permissions.get(field_name, None)
                if permission_name is not None:
                    permission = queryUtility(IPermission,
                                              name=permission_name)
                    if permission:
                        return checker(permission.title, context)
                # If the field is in the schema, but no permission is
                # specified, fall back to the default edit permission
                return checker(DEFAULT_PERMISSION, context)
        else:
            raise AttributeError('No such field: {}'.format(field_name))
