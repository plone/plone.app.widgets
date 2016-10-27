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
from plone.app.widgets.utils import get_tinymce_options
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
            get_date_options(request),
            args['pattern_options'])

        if 'date' in args['pattern_options'] and \
           'firstDay' in args['pattern_options']['date'] and \
           callable(args['pattern_options']['date']['firstDay']):
            args['pattern_options']['date']['firstDay'] = \
                args['pattern_options']['date']['firstDay']()

        return args

    security = ClassSecurityInfo()
    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None):
        """Basic impl for form processing in a widget"""

        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker

        value = value.split('-')
        if value[0] == '':
            # empty value, clear any previous value
            return None, {}

        try:
            value = DateTime(datetime(*map(int, value)))
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
            args['value'] = (
                '{year:}-{month:02}-{day:02} {hour:02}:{minute:02}'
            ).format(
                year=args['value'].year(),
                month=args['value'].month(),
                day=args['value'].day(),
                hour=args['value'].hour(),
                minute=args['value'].minute(),
            )

        elif args['value'] and isinstance(args['value'], datetime):
            args['value'] = (
                '{year:}-{month:02}-{day:02} {hour:02}:{minute:02}'
            ).format(
                year=args['value'].year,
                month=args['value'].month,
                day=args['value'].day,
                hour=args['value'].hour,
                minute=args['value'].minute,
            )

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
            get_datetime_options(request),
            args['pattern_options'])

        return args

    security = ClassSecurityInfo()
    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None):
        """Basic impl for form processing in a widget"""

        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker

        tmp = value.split(' ')
        if not tmp[0]:
            # empty: clear, not preserve, any previous value
            return None, {}
        value = tmp[0].split('-')
        if len(tmp) == 2 and ':' in tmp[1]:
            value += tmp[1].split(':')
        else:
            value += ['00', '00']

        try:
            value = DateTime(datetime(*map(int, value)))
        except:
            return empty_marker

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

        args.setdefault('pattern_options', {})

        if self.separator:
            args['pattern_options']['separator'] = self.separator

        if self.multiple and self.orderable:
            args['pattern_options']['orderable'] = True

        return args

    security = ClassSecurityInfo()
    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None):
        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker
        if self.multiple and isinstance(value, basestring):
            value = value.strip().split(self.separator)
        return value, {}

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
        value = request.get(field.getName(), field.getAccessor(context)())
        if isinstance(value, basestring):
            value = value.strip().split(self.separator)
        args['value'] = self.separator.join(value)

        args.setdefault('pattern_options', {})
        args['pattern_options'] = dict_merge(
            get_ajaxselect_options(context, args['value'], self.separator,
                                   self.vocabulary, self.vocabulary_view,
                                   field.getName()),
            args['pattern_options'])

        if self.orderable:
            args['pattern_options']['orderable'] = True

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


class KeywordsWidget(AjaxSelectWidget):
    """Keywords widget for Archetypes."""

    _base = InputWidget

    _properties = AjaxSelectWidget._properties.copy()
    _properties.update({
        'vocabulary': 'plone.app.vocabularies.Keywords',
    })

    def _base_args(self, context, field, request):
        args = super(KeywordsWidget, self)._base_args(context, field,
                                                      request)

        membership = getToolByName(context, 'portal_membership')
        user = membership.getAuthenticatedMember()

        site_properties = getToolByName(
            context, 'portal_properties')['site_properties']
        allowRolesToAddKeywords = site_properties.getProperty(
            'allowRolesToAddKeywords', None)

        allowNewItems = False
        if allowRolesToAddKeywords and [
            role for role in user.getRolesInContext(context)
                if role in allowRolesToAddKeywords]:
            allowNewItems = True

        args.setdefault('pattern_options', {})
        args['pattern_options']['allowNewItems'] = allowNewItems

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
    KeywordsWidget,
    title='Keywords widget',
    description=('Keywords widget'),
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
        'allow_sorting': True,
    })

    def _base_args(self, context, field, request):
        args = super(RelatedItemsWidget, self)._base_args(context, field,
                                                          request)

        value = request.get(field.getName(), None)
        if value is None:
            value = field.getAccessor(context)()
            if field.multiValued:
                value = [IUUID(o) for o in value if o]
            else:
                value = '' if value is None else IUUID(value)
        else:
            value = [v.split('/')[0]
                     for v in value.strip().split(self.separator)]

        vocabulary_factory = getattr(field, 'vocabulary_factory', None)
        if not self.vocabulary:
            self.vocabulary = vocabulary_factory

        args['name'] = field.getName()
        if field.multiValued:
            args['value'] = self.separator.join(value)
        else:
            args['value'] = value

        args.setdefault('pattern_options', {})
        args['pattern_options']['maximumSelectionSize'] = \
            -1 if field.multiValued else 1
        args['pattern_options']['orderable'] = self.allow_sorting
        args['pattern_options'] = dict_merge(
            get_relateditems_options(context, args['value'], self.separator,
                                     self.vocabulary, self.vocabulary_view,
                                     field.getName(), widget=self),
            args['pattern_options'])

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
            get_querystring_options(context, self.querystring_view),
            args['pattern_options'])

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
                                     field.getRaw(context))
                         ).decode(charset)

        args.setdefault('pattern_options', {})
        merged = dict_merge(get_tinymce_options(context, field, request),
                            args['pattern_options'])
        args['pattern_options'] = merged

        return args

    def edit(self, context, field, request):
        """Render widget on edit.

        :returns: Widget's HTML.
        :rtype: string
        """
        from Products.Archetypes.mimetype_utils import getAllowedContentTypes
        from Products.Archetypes.mimetype_utils import getDefaultContentType
        from lxml import etree

        rendered = ''
        allowed_mime_types = getAllowedContentTypes(context)
        if not allowed_mime_types or len(allowed_mime_types) <= 1:
            # Display textarea with default widget
            rendered = self._base(
                **self._base_args(context, field, request)).render()
        else:
            # Let pat-textarea-mimetype-selector choose the widget

            # Initialize the widget without a pattern
            base_args = self._base_args(context, field, request)
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
            value_mime_type = field.getContentType(context)\
                or getDefaultContentType(context)
            mt_select = etree.Element('select')
            mt_select.attrib['id'] = '{}_text_format'.format(field.getName())
            mt_select.attrib['name'] = '{}_text_format'.format(field.getName())
            mt_select.attrib['class'] = mt_pattern_name
            mt_select.attrib['{}{}'.format('data-', mt_pattern_name)] =\
                json.dumps({
                    'textareaName': field.getName(),
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

    def validate(self, field_name, vocabulary_name=None):
        field = self.context.getField(field_name)
        if field is not None:
            # If a vocabulary name was specified and it doesn't match
            # the value for the field or the widget, fail.
            if vocabulary_name and (
               vocabulary_name != getattr(field.widget, 'vocabulary', None) and
               vocabulary_name != getattr(field, 'vocabulary_factory', None)):
                return False
            return field.checkPermission('w', self.context)
        raise AttributeError('No such field: {}'.format(field_name))
