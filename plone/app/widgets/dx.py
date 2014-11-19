# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_callable
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from ZPublisher.Iterators import filestream_iterator
from datetime import date
from datetime import datetime
from os.path import basename
from os.path import join

from plone.app.textfield.widget import IRichTextWidget \
    as patextfield_IRichTextWidget
from plone.app.textfield.widget import RichTextWidget \
    as patextfield_RichTextWidget
from plone.app.textfield.value import RichTextValue
from plone.app.widgets.base import InputWidget
from plone.app.widgets.base import SelectWidget as BaseSelectWidget
from plone.app.widgets.base import TextareaWidget
from plone.app.widgets.base import FileWidget
from plone.app.widgets.base import dict_merge
from plone.app.widgets.interfaces import IFieldPermissionChecker
from plone.app.widgets.interfaces import IWidgetsLayer
from plone.app.widgets.utils import NotImplemented
from plone.app.widgets.utils import get_ajaxselect_options
from plone.app.widgets.utils import get_date_options
from plone.app.widgets.utils import get_datetime_options
from plone.app.widgets.utils import get_querystring_options
from plone.app.widgets.utils import get_relateditems_options
from plone.app.widgets.utils import get_tinymce_options
from plone.autoform.interfaces import WIDGETS_KEY
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.autoform.utils import resolveDottedName
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.utils import iterSchemata, getAdditionalSchemata
from plone.namedfile.utils import set_headers, stream_data
from plone.registry.interfaces import IRegistry
from plone.supermodel.utils import mergedTaggedValueDict
from plone.uuid.interfaces import IUUID
from tempfile import NamedTemporaryFile
from tempfile import gettempdir
from z3c.form.browser.select import SelectWidget as z3cform_SelectWidget
from z3c.form.browser.text import TextWidget as z3cform_TextWidget
from z3c.form.browser.widget import HTMLInputWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.converter import SequenceDataConverter
from z3c.form.converter import CollectionSequenceDataConverter
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import ISelectWidget
from z3c.form.interfaces import ITextWidget
from z3c.form.interfaces import IMultiWidget
from z3c.form.interfaces import IDataManager
from z3c.form.interfaces import NO_VALUE
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from z3c.form.widget import Widget
from zope.component import adapter
from zope.component import adapts
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import implements
from zope.interface import implementsOnly
from zope.interface import Interface
from zope.publisher.browser import TestRequest
from zope.publisher.interfaces import IPublishTraverse, NotFound
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IDate
from zope.schema.interfaces import IDatetime
from zope.schema.interfaces import IField
from zope.schema.interfaces import IList
from zope.schema.interfaces import ISequence
from zope.security.interfaces import IPermission

import pytz
import json
import fnmatch
import os
import time
import mimetypes

try:
    from plone.app.contenttypes.behaviors.collection import ICollection as IDXCollection  # noqa
    from plone.app.contenttypes.behaviors.richtext import IRichText  # noqa
    HAS_PAC = True
except ImportError:
    HAS_PAC = False


try:
    from z3c.relationfield.interfaces import IRelationChoice
    from z3c.relationfield.interfaces import IRelationList
except ImportError:  # pragma: no cover
    class IRelationChoice(Interface):
        pass

    class IRelationList(Interface):
        pass

try:
    from Products.CMFPlone.interfaces import IEditingSchema
except ImportError:
    IEditingSchema = Interface


class IDateField(IDate):
    """Marker interface for the DateField."""


class IDatetimeField(IDatetime):
    """Marker interface for the DatetimeField."""


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


class IRichTextWidget(patextfield_IRichTextWidget):
    """Marker interface for the TinyMCEWidget."""


class IFileUploadWidget(IMultiWidget):
    """Marker interface for the file upload widget.
    """


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
        if len(tmp) == 2 and ':' in tmp[1]:
            value += tmp[1].split(':')
        else:
            value += ['00', '00']

        # TODO: respect the selected zone from the widget and just fall back
        # to default_zone
        default_zone = self.widget.default_timezone
        zone = default_zone(self.widget.context)\
            if safe_callable(default_zone) else default_zone
        ret = datetime(*map(int, value))
        if zone:
            tzinfo = pytz.timezone(zone)
            ret = tzinfo.localize(ret)
        return ret


class SelectWidgetConverterBase(object):

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: Value inserted by Select2 widget or default html
                      select/multi-select
        :type value: string | list

        :returns: List of items
        :rtype: list | tuple | set
        """
        separator = getattr(self.widget, 'separator', ';')
        if isinstance(value, basestring):
            value = value.strip()
            if value:
                value = value.split(separator)
            else:
                return self.field.missing_value
        elif value == (u'',):
            return self.field.missing_value
        return super(SelectWidgetConverterBase, self).toFieldValue(value)


class SequenceSelectWidgetConverter(
        SelectWidgetConverterBase, SequenceDataConverter):
    adapts(IField, ISelectWidget)


class SelectWidgetConverter(
        SelectWidgetConverterBase, CollectionSequenceDataConverter):
    adapts(ICollection, ISelectWidget)


class AjaxSelectWidgetConverter(BaseDataConverter):
    """Data converter for ICollection fields using the AjaxSelectWidget.
    """

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


class RelationChoiceRelatedItemsWidgetConverter(BaseDataConverter):
    """Data converter for RelationChoice fields using the RelatedItemsWidget.
    """

    adapts(IRelationChoice, IRelatedItemsWidget)

    def toWidgetValue(self, value):
        if not value:
            return self.field.missing_value
        return IUUID(value)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        try:
            catalog = getToolByName(self.widget.context, 'portal_catalog')
        except AttributeError:
            catalog = getToolByName(getSite(), 'portal_catalog')

        res = catalog(UID=value)
        if res:
            return res[0].getObject()
        else:
            return self.field.missing_value


class RelatedItemsDataConverter(BaseDataConverter):
    """Data converter for ICollection fields using the RelatedItemsWidget."""

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
        if IRelationList.providedBy(self.field):
            return separator.join([IUUID(o) for o in value if value])
        else:
            return separator.join(v for v in value if v)

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: List of UID's separated by separator defined
        :type value: string

        :returns: List of content objects
        :rtype: list | tuple | set
        """
        if not value:
            return self.field.missing_value

        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]

        separator = getattr(self.widget, 'separator', ';')
        value = value.split(separator)

        if IRelationList.providedBy(self.field):
            try:
                catalog = getToolByName(self.widget.context, 'portal_catalog')
            except AttributeError:
                catalog = getToolByName(getSite(), 'portal_catalog')

            objects = {item.UID: item.getObject()
                       for item in catalog(UID=value) if item}

            return collectionType(objects[uid]
                                  for uid in value
                                  if uid in objects.keys())
        else:
            return collectionType(v for v in value)


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
        if not value:
            return '[]'
        return json.dumps(value)

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: Query string.
        :type value: string

        :returns: Query string.
        :rtype: list
        """
        try:
            value = json.loads(value)
        except ValueError:
            value = None
        if not value:
            return self.field.missing_value
        return value


class FileUploadConverter(BaseDataConverter):
    """Converter for multi file widgets used on `schema.List` fields."""

    adapts(ISequence, IFileUploadWidget)

    def toWidgetValue(self, value):
        """Converts the value to a form used by the widget.
            For some reason this never gets called for File Uploads
            """
        return value

    def toFieldValue(self, value):
        """Converts the value to a storable form."""
        context = self.widget.context
        if not IAddForm.providedBy(self.widget.form):
            dm = queryMultiAdapter((context, self.field), IDataManager)
        else:
            dm = None

        current_field_value = (
            dm.query()
            if ((dm is not None) and self.field.interface.providedBy(context))
            else None
        )
        if not current_field_value or current_field_value == NO_VALUE:
            current_field_value = []
        if not isinstance(current_field_value, list):
            current_field_value = [current_field_value]
        current_field_set = set(current_field_value)
        retvalue = []
        value_type = self.field.value_type._type
        if not value:
            return value
        elif not isinstance(value, list):
            value = [value]
        for item in value:
            if item['new']:
                retvalue.append(value_type(data=item['file'].read(),
                                filename=item['name']))
            else:
                for existing_file in current_field_set:
                    if existing_file.filename == item['name']:
                        retvalue.append(existing_file)
        return retvalue


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


class DateWidget(BaseWidget, HTMLInputWidget):
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
            get_date_options(self.request),
            args['pattern_options'])

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
        if field_value is self.field.missing_value:
            return u''

        formatter = self.request.locale.dates.getFormatter(
            self._formater, "short")
        if field_value.year > 1900:
            return formatter.format(field_value)

        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return field_value.ctime()


class DatetimeWidget(DateWidget, HTMLInputWidget):
    """Datetime widget for z3c.form.

    :param default_timezone: A Olson DB/pytz timezone identifier or a callback
                             returning such an identifier.
    :type default_timezone: String or callback

    """

    _converter = DatetimeWidgetConverter
    _formater = 'dateTime'

    implementsOnly(IDatetimeWidget)

    pattern_options = DateWidget.pattern_options.copy()

    default_timezone = None

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
        if 'time' in args['pattern_options']:
            del args['pattern_options']['time']
        args['pattern_options'] = dict_merge(
            get_datetime_options(self.request),
            args['pattern_options'])

        return args


class SelectWidget(BaseWidget, z3cform_SelectWidget):
    """Select widget for z3c.form."""

    _base = BaseSelectWidget

    implementsOnly(ISelectWidget)

    pattern = 'select2'
    pattern_options = BaseWidget.pattern_options.copy()

    separator = ';'
    noValueToken = u''
    noValueMessage = u''
    multiple = None
    orderable = False
    required = True

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

        self.required = self.field.required
 
        options = args.setdefault('pattern_options', {})
        if self.multiple or ICollection.providedBy(self.field):
            options['multiple'] = args['multiple'] = self.multiple = True

        # ISequence represents an orderable collection
        if ISequence.providedBy(self.field) or self.orderable:
            options['orderable'] = True

        if self.multiple:
            options['separator'] = self.separator

        # Allow to clear field value if it is not required
        if not self.required:
            options['allowClear'] = True

        items = []
        for item in self.items():
            if not isinstance(item['content'], basestring):
                item['content'] = translate(
                    item['content'],
                    context=self.request,
                    default=item['value'])
            items.append((item['value'], item['content']))
        args['items'] = items
       
        return args

    def extract(self, default=NO_VALUE):
        """Override extract to handle delimited response values.
        Skip the vocabulary validation provided in the parent
        method, since it's not ever done for single selects."""
        if (self.name not in self.request and
                self.name + '-empty-marker' in self.request):
            return []
        return self.request.get(self.name, default)


class AjaxSelectWidget(BaseWidget, z3cform_TextWidget):
    """Ajax select widget for z3c.form."""

    _base = InputWidget

    implementsOnly(IAjaxSelectWidget)

    pattern = 'select2'
    pattern_options = BaseWidget.pattern_options.copy()

    separator = ';'
    vocabulary = None
    vocabulary_view = '@@getVocabulary'
    orderable = False

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

        args['name'] = self.name
        args['value'] = self.value

        args.setdefault('pattern_options', {})

        field_name = self.field and self.field.__name__ or None

        context = self.context
        # We need special handling for AddForms
        if IAddForm.providedBy(getattr(self, 'form')):
            context = self.form

        vocabulary_name = self.vocabulary
        field = None
        if IChoice.providedBy(self.field):
            args['pattern_options']['maximumSelectionSize'] = 1
            field = self.field
        elif ICollection.providedBy(self.field):
            field = self.field.value_type
        if not vocabulary_name and field is not None:
            vocabulary_name = field.vocabularyName

        args['pattern_options'] = dict_merge(
            get_ajaxselect_options(context, args['value'], self.separator,
                                   vocabulary_name, self.vocabulary_view,
                                   field_name),
            args['pattern_options'])

        if field and getattr(field, 'vocabulary', None):
            form_url = self.request.getURL()
            source_url = "%s/++widget++%s/@@getSource" % (form_url, self.name)
            args['pattern_options']['vocabularyUrl'] = source_url

        # ISequence represents an orderable collection
        if ISequence.providedBy(self.field) or self.orderable:
            args['pattern_options']['orderable'] = True

        return args


class RelatedItemsWidget(BaseWidget, z3cform_TextWidget):
    """RelatedItems widget for z3c.form."""

    _base = InputWidget

    implementsOnly(IRelatedItemsWidget)

    pattern = 'relateditems'
    pattern_options = BaseWidget.pattern_options.copy()

    separator = ';'
    vocabulary = None
    vocabulary_view = '@@getVocabulary'
    orderable = False

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

        args['name'] = self.name
        args['value'] = self.value
        args.setdefault('pattern_options', {})

        field = None
        if IChoice.providedBy(self.field):
            args['pattern_options']['maximumSelectionSize'] = 1
            field = self.field
        elif ICollection.providedBy(self.field):
            field = self.field.value_type

        vocabulary_name = self.vocabulary
        if not vocabulary_name:
            if field is not None and field.vocabularyName:
                vocabulary_name = field.vocabularyName
            else:
                vocabulary_name = 'plone.app.vocabularies.Catalog'

        field_name = self.field and self.field.__name__ or None
        args['pattern_options'] = dict_merge(
            get_relateditems_options(self.context, args['value'],
                                     self.separator, vocabulary_name,
                                     self.vocabulary_view, field_name),
            args['pattern_options'])

        if not self.vocabulary:  # widget vocab takes precedence over field
            if field and getattr(field, 'vocabulary', None):
                form_url = self.request.getURL()
                source_url = "%s/++widget++%s/@@getSource" % (
                    form_url, self.name)
                args['pattern_options']['vocabularyUrl'] = source_url

        return args


class QueryStringWidget(BaseWidget, z3cform_TextWidget):
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
            get_querystring_options(self.context, self.querystring_view),
            args['pattern_options'])

        return args


class RichTextWidget(BaseWidget, patextfield_RichTextWidget):
    """TinyMCE widget for z3c.form."""

    _base = TextareaWidget

    implementsOnly(IRichTextWidget)

    pattern_options = BaseWidget.pattern_options.copy()

    @property
    def pattern(self):
        """dynamically grab the actual pattern name so it will
           work with custom visual editors"""
        registry = getUtility(IRegistry)
        try:
            records = registry.forInterface(IEditingSchema, check=False,
                                            prefix='plone')
            return records.default_editor.lower()
        except AttributeError:
            return 'tinymce'

    def _base_args(self):
        args = super(RichTextWidget, self)._base_args()
        args['name'] = self.name
        properties = getToolByName(self.context, 'portal_properties')
        charset = properties.site_properties.getProperty('default_charset',
                                                         'utf-8')
        value = self.value and self.value.raw_encoded or ''
        args['value'] = (self.request.get(
            self.field.getName(), value)).decode(charset)

        args.setdefault('pattern_options', {})
        merged = dict_merge(get_tinymce_options(self.context, self.field, self.request),  # noqa
                            args['pattern_options'])
        args['pattern_options'] = merged['pattern_options']

        return args

    def render(self):
        """Render widget.

        :returns: Widget's HTML.
        :rtype: string
        """
        if self.mode != 'display':
            return super(RichTextWidget, self).render()

        if not self.value:
            return ''

        if isinstance(self.value, RichTextValue):
            return self.value.output

        return super(RichTextWidget, self).render()


class FileUploadWidget(BaseWidget, z3cform_TextWidget):
    implementsOnly(IFileUploadWidget)

    _base = FileWidget
    _converter = FileUploadConverter

    pattern = 'fileupload'
    pattern_options = BaseWidget.pattern_options.copy()
    multiple = True
    maxNumberOfFiles = 1000

    def _base_args(self):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `multiple `: field multiple

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        args = super(FileUploadWidget, self)._base_args()
        url = '%s/++widget++%s/@@upload/' % (
                    self.request.getURL(),
                    self.name)
        args['name'] = self.name
        args.setdefault('pattern_options', {})
        args['pattern_options'] = {'url': url}
        self.cleanup()
        loaded = []
        extractName = self.name + "uploaded"
        if getattr(self.request, extractName, None) is not None:
            files = self.request[extractName]
            if files:
                extracted = json.loads(str(files))
                for extracted_file in extracted:
                    if extracted_file['name'] != extracted_file['title']:
                        tmpdir = gettempdir()
                        path = join(tmpdir, extracted_file['name'])
                        file_ = open(path, 'r+b')
                        file_.seek(0, 2)  # end of file
                        tmpsize = file_.tell()
                        file_.seek(0)
                        file_.close()
                        dl_url = '%s/++widget++%s/@@download/' % (
                                  self.request.getURL(),
                                  self.name) + (extracted_file['name'] +
                                                '?name=' +
                                                extracted_file['title'])
                        newfile = {'title': extracted_file['title'],
                                   'size': tmpsize,
                                   'url': dl_url,
                                   'name': extracted_file['name']}
                        loaded.append(newfile)

        if not IAddForm.providedBy(self.form):
            dm = queryMultiAdapter((self.context, self.field,), IDataManager)
        else:
            dm = None

        current_field_value = (
            dm.query()
            if ((dm is not None) and
                self.field.interface.providedBy(self.context))
            else None
        )
        if current_field_value and current_field_value != NO_VALUE:
            if not isinstance(current_field_value, list):
                current_field_value = [current_field_value]
            current_field_set = set(current_field_value)
            for item in current_field_set:
                dl_url = '%s/++widget++%s/@@downloadexisting/' % (
                             self.request.getURL(),
                             self.name) + item.filename
                info = {'name': item.filename,
                        'title': item.filename,
                        'size': item.getSize(),
                        'url': dl_url,
                        }
                loaded.append(info)
        args['pattern_options']['existing'] = loaded
        if self.maxNumberOfFiles == 1:
            self.multiple = False
        args['pattern_options']['maxNumberOfFiles'] = self.maxNumberOfFiles
        args['multiple'] = self.multiple
        return args

    def extract(self, default=NO_VALUE):
        """Extract all real FileUpload objects.
        """
        value = []
        extractName = self.name + "uploaded"
        if getattr(self.request, extractName, None) is not None:
            files = self.request[extractName]
            if files:
                extracted = json.loads(str(files))
                for extracted_file in extracted:
                    if extracted_file['name'] != extracted_file['title']:
                        tmpdir = gettempdir()
                        path = join(tmpdir, extracted_file['name'])
                        file_ = open(path, 'r+b')
                        newfile = {'name': extracted_file['title'],
                                   'file': file_, 'new': True,
                                   'temp': extracted_file['name']}
                        value.append(newfile)
                    else:
                        oldfile = {'name': extracted_file['name'],
                                   'file': None, 'new': False}
                        value.append(oldfile)
        return value

    def render(self):
        """Render widget.

        :returns: Widget's HTML.
        :rtype: string
        """
        if self.mode != 'display':
            return super(FileUploadWidget, self).render()

        if not IAddForm.providedBy(self.form):
            dm = queryMultiAdapter((self.context, self.field,), IDataManager)
        else:
            dm = None
        ret_value = '<div class="files">'
        current_field_value = (
            dm.query()
            if ((dm is not None) and
                self.field.interface.providedBy(self.context))
            else None
        )
        if current_field_value and current_field_value != NO_VALUE:
            if not isinstance(current_field_value, list):
                current_field_value = [current_field_value]
            current_field_set = set(current_field_value)
            for item in current_field_set:
                ret_value = ret_value + '<div class="existfileupload">'
                dl_url = '%s/++widget++%s/@@downloadexisting/' % (
                             self.request.getURL(),
                             self.name) + item.filename
                ret_value = ret_value + '<a href=' + dl_url + '>'
                ret_value = ret_value + '<span class="filename">' + item.filename + '</span>'
                size = self.formatSize(item.getSize())
                ret_value = ret_value + '<span class="filesize"> ' + size + '</span>'
                ret_value = ret_value + '</div>'
        ret_value = ret_value + '</div>'
        return ret_value

    def formatSize(self, numBytes):
        """
        Format a human readable file size
        """
        if numBytes > 1000000000:
            return str(int(round(numBytes / (1024 * 1024 * 1024)))) + ' GB'
        if numBytes > 1000000:
            return str(int(round(numBytes / (1024 * 1024)))) + ' MB'
        return str(int(round(numBytes / 1024))) + ' KB'

    def cleanup(self):
        """
        look through upload directory and remove old uploads
        (older than 2 hrs)
        """
        now = time.time()
        tmpdir = gettempdir()
        for filename in os.listdir(tmpdir):
            if fnmatch.fnmatch(filename, '*FileUpload'):
                filepath = os.path.join(tmpdir, filename)
                if (os.stat(filepath).st_mtime) < now - 2 * 60 * 60:
                    os.unlink(filepath)


@implementer(IFieldWidget)
def FileUploadFieldWidget(field, request):
    return FieldWidget(field, FileUploadWidget(request))


class Upload(BrowserView):
    """Upload a file via ++widget++widget_name/@@upload"""

    implements(IPublishTraverse)

    def __call__(self):

        if hasattr(self.request, "REQUEST_METHOD"):
            # TODO: we should check errors in the creation process, and
            # broadcast those to the error template in JS
            if self.request["REQUEST_METHOD"] == "POST":
                if getattr(self.request, self.context.name, None) is not None:
                    files = self.request[self.context.name]
                    uploaded = self.upload([files])
                    if uploaded:
                        return json.dumps({'files': uploaded})
                return json.dumps({'files': []})

    def upload(self, files):
        loaded = []
        fileid = self.request[self.context.name + 'fileids']
        for item in files:
            if item.filename:
                filename = safe_unicode(item.filename)
                item.seek(0, 2)  # end of file
                tmpsize = item.tell()
                tmpfile = NamedTemporaryFile(suffix='FileUpload', delete=False)
                item.seek(0)
                tmpfile.write(item.read())
                tmpfile.close()
                dlname = basename(tmpfile.name)
                dl_url = '%s/@@download/' % (
                         self.request.URL1) + dlname + '?name=' + filename
                info = {'name': dlname,
                        'title': filename,
                        'size': tmpsize,
                        'url': dl_url,
                        'fileid': fileid,
                        }
                loaded.append(info)
            return loaded


class DownloadExisting(BrowserView):
    """Download a file via ++widget++widget_name/@@downloadexisting/filename"""

    implements(IPublishTraverse)

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.filename = None

    def publishTraverse(self, request, name):

        if self.filename is None:  # ../@@download/filename
            self.filename = name
        else:
            raise NotFound(self, name, request)

        return self

    def __call__(self):

        if self.context.form is not None:
            content = aq_inner(self.context.form.getContent())
        else:
            content = aq_inner(self.context.context)
        field = aq_inner(self.context.field)

        dm = queryMultiAdapter((content, field,), IDataManager)
        file_list = dm.query()
        if file_list == NO_VALUE:
            return None
        file_ = None
        if not isinstance(file_list, list):
            file_list = [file_list]
        for curr_file in file_list:
            if curr_file.filename == self.filename:
                file_ = curr_file
        filename = getattr(file_, 'filename', '')
        if not file_:
            return None
        set_headers(file_, self.request.response, filename=filename)
        return stream_data(file_)


class Download(BrowserView):
    """Download a file via ++widget++widget_name/@@download/filename"""

    implements(IPublishTraverse)

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.filename = None

    def publishTraverse(self, request, name):

        if self.filename is None:  # ../@@download/filename
            self.filename = name
        else:
            raise NotFound(self, name, request)

        return self

    def __call__(self):

        if getattr(self.request, "name", None) is not None:
            filename = self.request['name']
        tmpdir = gettempdir()
        filepath = os.path.join(tmpdir, self.filename)
        try:
            file_ = open(filepath)
        except IOError:
            return

        file_.seek(0, 2)  # end of file
        tmpsize = file_.tell()
        file_.seek(0)
        contenttype = 'application/octet-stream'
        filename = safe_unicode(filename)
        if filename:
            extension = os.path.splitext(filename)[1].lower()
            contenttype = mimetypes.types_map.get(extension,
                                                  'application/octet-stream')
        self.request.response.setHeader("Content-Type", contenttype)
        self.request.response.setHeader("Content-Length", tmpsize)
        if filename is not None:
            self.request.response.setHeader("Content-Disposition",
                                            "attachment; filename=\"%s\""
                                             % filename)
        return filestream_iterator(filepath, 'rb')


@implementer(IFieldWidget)
def DateFieldWidget(field, request):
    return FieldWidget(field, DateWidget(request))


@implementer(IFieldWidget)
def DatetimeFieldWidget(field, request):
    return FieldWidget(field, DatetimeWidget(request))


@implementer(IFieldWidget)
def SelectFieldWidget(field, request):
    return FieldWidget(field, SelectWidget(request))


@implementer(IFieldWidget)
def AjaxSelectFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, AjaxSelectWidget(request))


@implementer(IFieldWidget)
def RelatedItemsFieldWidget(field, request, extra=None):
    if extra is not None:
        request = extra
    return FieldWidget(field, RelatedItemsWidget(request))


if HAS_PAC:
    @adapter(getSpecification(IDXCollection['query']), IFormLayer)
    @implementer(IFieldWidget)
    def QueryStringFieldWidget(field, request):
        return FieldWidget(field, QueryStringWidget(request))

    @adapter(getSpecification(IRichText['text']), IFormLayer)
    @implementer(IFieldWidget)
    def RichTextFieldWidget(field, request):
        return FieldWidget(field, RichTextWidget(request))


class MockRequest(TestRequest):
    implements(IWidgetsLayer)


class DXFieldPermissionChecker(object):
    """
    """

    implements(IFieldPermissionChecker)
    adapts(IDexterityContent)

    DEFAULT_PERMISSION = 'Modify portal content'

    def __init__(self, context):
        self.context = context
        self._request = MockRequest()

    def _get_schemata(self):
        return iterSchemata(self.context)

    def validate(self, field_name, vocabulary_name=None):
        context = self.context
        checker = getSecurityManager().checkPermission
        schemata = self._get_schemata()
        for schema in schemata:
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
                        widget = widget and widget(field, self._request)
                    else:
                        widget = queryMultiAdapter((field, self._request),
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
                return checker(self.DEFAULT_PERMISSION, context)
        else:
            raise AttributeError('No such field: {0}'.format(field_name))


class DXAddViewFieldPermissionChecker(DXFieldPermissionChecker):
    """Permission checker for when we just have an add view"""

    adapts(IAddForm)

    def __init__(self, view):
        self.context = view.context
        # This may fail for views that aren't DefaultAddForm or
        # DefaultAddView sub-classes, but they can register their own
        # more specific adapters, if needed.
        self.fti = getattr(view, 'fti', None)
        if self.fti is None:
            self.fti = view.ti
        self._request = view.request

    def _get_schemata(self):
        fti = self.fti
        yield fti.lookupSchema()
        for schema in getAdditionalSchemata(portal_type=fti.getId()):
            yield schema
