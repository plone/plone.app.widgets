# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import TypesWidget
from Products.CMFCore.utils import getToolByName
from datetime import datetime
from plone.app.widgets.base import InputWidget
from plone.app.widgets.base import SelectWidget
from plone.app.widgets.base import TextareaWidget
from plone.app.widgets.base import dict_merge
from plone.app.widgets.interfaces import IFieldPermissionChecker
from plone.app.widgets.utils import NotImplemented
from plone.app.widgets.utils import get_date_options
from plone.app.widgets.utils import get_datetime_options
from plone.app.widgets.utils import get_ajaxselect_options
from plone.app.widgets.utils import get_relateditems_options
from plone.app.widgets.utils import get_querystring_options
from plone.uuid.interfaces import IUUID
from zope.interface import implements
from zope.component import adapts

import json


class BaseWidget(TypesWidget):
    """Base widget for Archetypes."""

    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro': 'patterns_widget',
        'pattern': None,
        'pattern_options': {},
    })

    def _base(self, pattern, pattern_options={}):
        """Base widget class."""
        raise NotImplemented

    def _base_args(self, context, field, request):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options

        :param context: Instance of content type.
        :type context: context

        :param request: Request object.
        :type request: request

        :param field: Instance of field of this widget.
        :type field: field

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        if self.pattern is None:
            raise NotImplemented("'pattern' option is not provided.")
        return {
            'pattern': self.pattern,
            'pattern_options': self.pattern_options,
        }

    def view(self, context, field, request):
        """Render widget on view.

        :returns: Fields value.
        :rtype: string
        """
        return field.getAccessor(context)()

    def edit(self, context, field, request):
        """Render widget on edit.

        :returns: Widget's HTML.
        :rtype: string
        """
        return self._base(**self._base_args(context, field, request)).render()


class DateWidget(BaseWidget):
    """Date widget for Archetypes."""

    _base = InputWidget

    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'pickadate',
        'pattern_options': {},
    })

    def _base_args(self, context, field, request):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        args = super(DateWidget, self)._base_args(context, field, request)
        args['name'] = field.getName()
        args['value'] = (request.get(field.getName(),
                                     field.getAccessor(context)()))

        if args['value'] and isinstance(args['value'], DateTime):
            args['value'] = ('{year:}-{month:02}-{day:02}').format(
                year=args['value'].year(),
                month=args['value'].month(),
                day=args['value'].day(),
            )

        elif args['value'] and isinstance(args['value'], datetime):
            args['value'] = ('{year:}-{month:02}-{day:02}').format(
                year=args['value'].year,
                month=args['value'].month,
                day=args['value'].day,
            )

        args.setdefault('pattern_options', {})
        args['pattern_options'] = dict_merge(
            args['pattern_options'],
            get_date_options(request))

        return args

    security = ClassSecurityInfo()
    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None):
        """Basic impl for form processing in a widget"""

        value = form.get(field.getName(), None)
        if not value:
            return empty_marker

        try:
            value = DateTime(datetime(*map(int, value.split('-'))))
        except:
            return empty_marker

        return value, {}


registerWidget(
    DateWidget,
    title='Date widget',
    description=('Date widget'),
    used_for=('Products.Archetypes.Field.DateTimeField',)
)


class DatetimeWidget(DateWidget):
    """Date widget for Archetypes."""

    _properties = DateWidget._properties.copy()
    _properties.update({
        'pattern': 'pickadate',
        'pattern_options': {},
    })

    def _base_args(self, context, field, request):
        """Method which will calculate _base class arguments.

        Returns (as python dictionary):
            - `pattern`: pattern name
            - `pattern_options`: pattern options
            - `name`: field name
            - `value`: field value

        :returns: Arguments which will be passed to _base
        :rtype: dict
        """
        args = super(DatetimeWidget, self)._base_args(context, field, request)
        args['name'] = field.getName()
        args['value'] = (request.get(field.getName(),
                                     field.getAccessor(context)()))

        if args['value'] and isinstance(args['value'], DateTime):
            args['value'] = ('{year:}-{month:02}-{day:02}').format(
                year=args['value'].year(),
                month=args['value'].month(),
                day=args['value'].day(),
            )

        elif args['value'] and isinstance(args['value'], datetime):
            args['value'] = ('{year:}-{month:02}-{day:02}').format(
                year=args['value'].year,
                month=args['value'].month,
                day=args['value'].day,
            )

        if args['value'] and len(args['value'].split(' ')) == 1:
            args['value'] += ' 00:00'

        args.setdefault('pattern_options', {})
        args['pattern_options'] = dict_merge(
            args['pattern_options'],
            get_datetime_options(request))

        return args

    security = ClassSecurityInfo()
    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None):
        """Basic impl for form processing in a widget"""

        value = form.get(field.getName(), None)
        if not value:
            return empty_marker, {}

        tmp = value.split(' ')
        if not tmp[0]:
            return empty_marker
        value = tmp[0].split('-')
        value += tmp[1].split(':')

        try:
            value = DateTime(datetime(*map(int, value)))
        except:
            return empty_marker, {}

        return value, {}


registerWidget(
    DatetimeWidget,
    title='Datetime widget',
    description=('Datetime widget'),
    used_for=('Products.Archetypes.Field.DateTimeField',)
)


class SelectWidget(BaseWidget):
    """Select widget for Archetypes."""

    _base = SelectWidget

    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'select2',
        'pattern_options': {},
        'separator': ';',
        'multiple': False,
        'orderable': False,
    })

    def _base_args(self, context, field, request):
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
        args = super(SelectWidget, self)._base_args(context, field, request)
        args['name'] = field.getName()
        args['value'] = (request.get(field.getName(),
                                     field.getAccessor(context)()))
        args['multiple'] = self.multiple

        items = []
        for item in field.Vocabulary(context).items():
            items.append((item[0], item[1]))
        args['items'] = items

        options = args.setdefault('pattern_options', {})

        if self.separator:
            options['separator'] = self.separator

        if self.orderable and self.multiple:
            options = args.setdefault('pattern_options', {})
            options['orderable'] = True

        return args


registerWidget(
    SelectWidget,
    title='Select widget',
    description=('Select widget'),
    used_for=('Products.Archetypes.Field.SelectField',)
)


class AjaxSelectWidget(BaseWidget):
    """Ajax select widget for Archetypes."""

    _base = InputWidget

    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'select2',
        'pattern_options': {},
        'separator': ';',
        'vocabulary': None,
        'vocabulary_view': '@@getVocabulary',
        'orderable': False,
    })

    def _base_args(self, context, field, request):
        args = super(AjaxSelectWidget, self)._base_args(context, field,
                                                        request)

        vocabulary_factory = getattr(field, 'vocabulary_factory', None)
        if not self.vocabulary:
            self.vocabulary = vocabulary_factory

        args['name'] = field.getName()
        args['value'] = self.separator.join(request.get(
            field.getName(), field.getAccessor(context)()))

        options = args.setdefault('pattern_options', {})
        args['pattern_options'] = dict_merge(
            options,
            get_ajaxselect_options(context, args['value'], self.separator,
                                   self.vocabulary, self.vocabulary_view,
                                   field.getName()))

        if self.orderable:
            options = args.setdefault('pattern_options', {})
            options['orderable'] = True

        return args

    security = ClassSecurityInfo()
    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None):
        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker
        value = value.strip().split(self.separator)
        return value, {}


registerWidget(
    AjaxSelectWidget,
    title='Ajax select widget',
    description=('Ajax select widget'),
    used_for=('Products.Archetypes.Field.LinesField',))


class RelatedItemsWidget(BaseWidget):
    """Related items widget for Archetypes."""

    _base = InputWidget

    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'relateditems',
        'pattern_options': {},
        'separator': ';',
        'vocabulary': 'plone.app.vocabularies.Catalog',
        'vocabulary_view': '@@getVocabulary',
    })

    def _base_args(self, context, field, request):
        args = super(RelatedItemsWidget, self)._base_args(context, field,
                                                          request)

        value = request.get(field.getName(), None)
        if value is None:
            value = [IUUID(o) for o in field.getAccessor(context)() if o]
        else:
            value = [v.split('/')[0]
                     for v in value.strip().split(self.separator)]

        vocabulary_factory = getattr(field, 'vocabulary_factory', None)
        if not self.vocabulary:
            self.vocabulary = vocabulary_factory

        args['name'] = field.getName()
        args['value'] = self.separator.join(value)

        args.setdefault('pattern_options', {})
        args['pattern_options'] = dict_merge(
            args['pattern_options'],
            get_relateditems_options(context, args['value'], self.separator,
                                     self.vocabulary, self.vocabulary_view,
                                     field.getName()))

        return args

    security = ClassSecurityInfo()
    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None):
        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker
        value = [v.split('/')[0] for v in value.strip().split(self.separator)]
        return value, {}


registerWidget(
    RelatedItemsWidget,
    title='Related items widget',
    description=('Related items widget'),
    used_for='Products.Archetypes.Field.ReferenceField')


class QueryStringWidget(BaseWidget):
    """Query string widget for Archetypes."""

    _base = TextareaWidget

    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'querystring',
        'pattern_options': {},
        'querystring_view': '@@qsOptions',
    })

    def _base_args(self, context, field, request):
        args = super(QueryStringWidget, self)._base_args(
            context, field, request)

        args['name'] = field.getName()
        args['value'] = request.get(field.getName(), json.dumps(
            [dict(c) for c in field.getRaw(context)]
        ))

        args.setdefault('pattern_options', {})
        args['pattern_options'] = dict_merge(
            args['pattern_options'],
            get_querystring_options(context, self.querystring_view))

        return args

    security = ClassSecurityInfo()
    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker
        value = json.loads(value)
        return value, {}


registerWidget(
    QueryStringWidget,
    title='Querystring widget',
    description=('Querystring widget'),
    used_for='archetypes.querywidget.field.QueryField')


class TinyMCEWidget(BaseWidget):
    """TinyMCE widget for Archetypes."""

    _base = TextareaWidget

    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'tinymce',
        'pattern_options': {},
    })

    def _base_args(self, context, field, request):
        args = super(TinyMCEWidget, self)._base_args(context, field, request)
        args['name'] = field.getName()
        properties = getToolByName(context, 'portal_properties')
        charset = properties.site_properties.getProperty('default_charset',
                                                         'utf-8')
        args['value'] = (request.get(field.getName(),
                                     field.getAccessor(context)())
                         ).decode(charset)
        return args


registerWidget(
    TinyMCEWidget,
    title='TinyMCE widget',
    description=('TinyMCE widget'),
    used_for='Products.Archetypes.Field.TextField')


class ATFieldPermissionChecker(object):
    implements(IFieldPermissionChecker)
    adapts(IBaseObject)

    def __init__(self, context):
        self.context = context

    def validate(self, field_name):
        field = self.context.getField(field_name)
        if field is not None:
            return field.checkPermission('w', self.context)
        raise AttributeError('No such field: {}'.format(field_name))
