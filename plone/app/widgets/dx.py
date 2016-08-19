# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_callable
from datetime import date
from datetime import datetime
from lxml import etree
from plone.app.textfield.interfaces import IRichText
from plone.app.textfield.value import RichTextValue
from plone.app.textfield.widget import IRichTextWidget as patextfield_IRichTextWidget  # noqa
from plone.app.textfield.widget import RichTextWidget as patextfield_RichTextWidget  # noqa
from plone.app.widgets.base import InputWidget
from plone.app.widgets.base import SelectWidget as BaseSelectWidget
from plone.app.widgets.base import TextareaWidget
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
from plone.app.widgets.utils import get_widget_form
from plone.autoform.interfaces import WIDGETS_KEY
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.autoform.utils import resolveDottedName
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.utils import iterSchemata, getAdditionalSchemata
from plone.registry.interfaces import IRegistry
from plone.supermodel.utils import mergedTaggedValueDict
from plone.uuid.interfaces import IUUID
from z3c.form.browser.select import SelectWidget as z3cform_SelectWidget
from z3c.form.browser.text import TextWidget as z3cform_TextWidget
from z3c.form.browser.widget import HTMLInputWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.converter import CollectionSequenceDataConverter
from z3c.form.converter import SequenceDataConverter
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import ISelectWidget
from z3c.form.interfaces import ITextWidget
from z3c.form.interfaces import NO_VALUE
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from z3c.form.widget import Widget
from zope.component import adapter
from zope.component import adapts
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import implements
from zope.interface import implementsOnly
from zope.publisher.browser import TestRequest
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

try:
    from plone.app.contenttypes.behaviors.collection import ICollection as IDXCollection  # noqa
    from plone.app.contenttypes.behaviors import richtext  # noqa
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
            return separator.join([IUUID(o) for o in value if o])
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
            valueType = getattr(self.field.value_type, '_type', unicode)
            return collectionType(valueType(v) for v in value)


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
            # Time gets set in parent class to false. Remove.
            del args['pattern_options']['time']
        if 'time' in self.pattern_options:
            # Re-apply custom set time options.
            args['pattern_options']['time'] = self.pattern_options['time']
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

    def update(self):
        super(AjaxSelectWidget, self).update()
        field = getattr(self, 'field', None)
        if ICollection.providedBy(self.field):
            field = self.field.value_type
        if (not self.vocabulary and field is not None and
                getattr(field, 'vocabularyName', None)):
            self.vocabulary = field.vocabularyName

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
        form = get_widget_form(self)
        # We need special handling for AddForms
        if IAddForm.providedBy(form):
            context = form

        vocabulary_name = self.vocabulary
        field = None
        if IChoice.providedBy(self.field):
            args['pattern_options']['maximumSelectionSize'] = 1
            field = self.field
        elif ICollection.providedBy(self.field):
            field = self.field.value_type

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
    vocabulary_override = False
    vocabulary_view = '@@getVocabulary'
    orderable = False

    def update(self):
        super(RelatedItemsWidget, self).update()
        field = getattr(self, 'field', None)
        if ICollection.providedBy(self.field):
            field = self.field.value_type
        if (not self.vocabulary and field is not None and
                getattr(field, 'vocabularyName', None)):
            self.vocabulary = field.vocabularyName
            self.vocabulary_override = True
        else:
            self.vocabulary = 'plone.app.vocabularies.Catalog'

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
        field_name = self.field and self.field.__name__ or None

        context = self.context
        form = get_widget_form(self)
        # We need special handling for AddForms
        if IAddForm.providedBy(form):
            context = form

        args['pattern_options'] = dict_merge(
            get_relateditems_options(context, args['value'],
                                     self.separator, vocabulary_name,
                                     self.vocabulary_view, field_name,
                                     widget=self),
            args['pattern_options'])

        if not self.vocabulary_override:  # widget vocab precedence over field
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
        merged_options = dict_merge(get_tinymce_options(self.context,
                                                        self.field,
                                                        self.request),  # noqa
                                    args['pattern_options'])
        args['pattern_options'] = merged_options

        return args

    def render(self):
        """Render widget.

        :returns: Widget's HTML.
        :rtype: string
        """
        if self.mode != 'display':
            # MODE "INPUT"
            rendered = ''
            allowed_mime_types = self.allowedMimeTypes()
            if not allowed_mime_types or len(allowed_mime_types) <= 1:
                # Display textarea with default widget
                rendered = super(RichTextWidget, self).render()
            else:
                # Let pat-textarea-mimetype-selector choose the widget

                # Initialize the widget without a pattern
                base_args = self._base_args()
                pattern_options = base_args['pattern_options']
                del base_args['pattern']
                del base_args['pattern_options']
                textarea_widget = self._base(None, None, **base_args)
                textarea_widget.klass = ''
                mt_pattern_name = '{}{}'.format(
                    self._base._klass_prefix,
                    'textareamimetypeselector'
                )

                # Initialize mimetype selector pattern
                # TODO: default_mime_type returns 'text/html', regardless of
                # settings. fix in plone.app.textfield
                value_mime_type = self.value.mimeType if self.value\
                    else self.field.default_mime_type
                mt_select = etree.Element('select')
                mt_select.attrib['id'] = '{}_text_format'.format(self.id)
                mt_select.attrib['name'] = '{}.mimeType'.format(self.name)
                mt_select.attrib['class'] = mt_pattern_name
                mt_select.attrib['{}{}'.format('data-', mt_pattern_name)] =\
                    json.dumps({
                        'textareaName': self.name,
                        'widgets': {
                            'text/html': {  # TODO: currently, we only support
                                            # richtext widget config for
                                            # 'text/html', no other mimetypes.
                                'pattern': self.pattern,
                                'patternOptions': pattern_options
                            }
                        }
                    })

                # Create a list of allowed mime types
                for mt in allowed_mime_types:
                    opt = etree.Element('option')
                    opt.attrib['value'] = mt
                    if value_mime_type == mt:
                        opt.attrib['selected'] = 'selected'
                    opt.text = mt
                    mt_select.append(opt)

                # Render the combined widget
                rendered = '{}\n{}'.format(
                    textarea_widget.render(),
                    etree.tostring(mt_select)
                )
            return rendered

        if not self.value:
            return ''

        if isinstance(self.value, RichTextValue):
            return self.value.output

        return super(RichTextWidget, self).render()


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

    @adapter(getSpecification(richtext.IRichText['text']), IFormLayer)
    @implementer(IFieldWidget)
    def RichTextFieldWidget(field, request):
        return FieldWidget(field, RichTextWidget(request))
else:
    # expose RichTextFieldWidget factory for non-PAC plone 4 sites:
    @adapter(IRichText, IWidgetsLayer)
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
                    if widget:
                        widget.update()
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
