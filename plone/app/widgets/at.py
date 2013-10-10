# -*- coding: utf-8 -*-

import json
from DateTime import DateTime
from datetime import datetime
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
from Products.CMFCore.utils import getToolByName
from plone.app.widgets import base
from plone.uuid.interfaces import IUUID


class BaseWidget(TypesWidget):
    """

        Example usage

            TextField(
                id='text',
                required=True,
                searchable=True,
                widget=BaseWidget(
                    label='Insert text',
                    pattern='example',
                    pattern_options={
                        'option1': 'value1',
                        'option2': 'value2',
                    },
                ),
            )

        above widget would produce

            <input
                value=""
                class="pat-example'
                data-pat-example='{"option1": 'value1', "options2": "value2" }'
                />

    """

    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro': 'patterns_widget',
        'pattern': '',
        'pattern_options': {},
    })

    _base = base.InputWidget,

    def _widget_args(self, context, field, request):
        pattern_options = {}
        for name in self._properties.keys():
            if name.startswith('pattern_'):
                pattern_options[name[len('pattern_'):]] = getattr(self, name)
        return {
            'name': field.getName(),
            'pattern': self.pattern,
            'pattern_options': pattern_options,
            'value': request.get(field.getName(),
                                 field.getAccessor(context)()),
        }

    def view(self, context, field, request):
        return field.getAccessor(context)()

    def edit(self, context, field, request):
        args = self._widget_args(context, field, request)
        return self._widget(**args).render()


class DatetimeWidget(BaseWidget):
    _properties = BaseWidget._properties.copy()

    def _widget_args(self, context, field, request):
        args = super(DatetimeWidget, self)._widget_args(context, field,
                                                        request)
        value = request.get(field.getName(), field.getAccessor(context)())
        if value:
            if isinstance(value, DateTime):
                value = '%02d:%02d' % (value.hour(), value.minute())
            else:
                value = '%02d:%02d' % (value.hour, value.minute)
        else:
            value = ''
        args['pattern_options']['time'] = {'value': value}

        return args


registerWidget(
    DatetimeWidget,
    title='Datetime widget',
    description=('Datetime widget'),
    used_for=('Products.Archetypes.Field.DateTimeField',)
)























class SelectWidget(BaseWidget):
    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'select2',
        'separator': ';',
    })
    _widget = base.SelectWidget

    def _widget_args(self, context, field, request):
        args = super(SelectWidget, self)._widget_args(context, field, request)
        args['items'] = field.Vocabulary(context).items()
        return args


class TinyMCEWidget(BaseWidget):
    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'tinymce',
    })
    _widget = base.TextareaWidget

    def _widget_args(self, context, field, request):
        args = super(TinyMCEWidget, self)._widget_args(context, field, request)
        return args


registerWidget(
    TinyMCEWidget,
    title='TinyMCE widget',
    description=('TinyMCE widget'),
    used_for=('Products.Archetypes.Field.TextField',)
)

class DateWidget(BaseWidget):
    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'pickadate'
    })
    _widget = base.InputWidget

    def _widget_args(self, context, field, request):
        args = super(BaseWidget, self)._widget_args(context, field, request)
        args['request'] = request
        value = request.get(field.getName(), field.getAccessor(context)())
        if value:
            if isinstance(value, DateTime):
                value = '%d-%02d-%02d' % (
                    value.year(), value.month(), value.day())
            else:
                value = '%d-%02d-%02d' % (value.year, value.month, value.day)
        else:
            value = ''
        args['pattern_options']['date'] = {'value': value}

        return args

    security = ClassSecurityInfo()
    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None):
        """Basic impl for form processing in a widget"""

        date_value = form.get(field.getName() + '_date', empty_marker)
        time_value = form.get(field.getName() + '_time', '00:00')
        if date_value is empty_marker or date_value == '':
            return empty_marker

        parts = date_value.split('-') + time_value.split(':')

        # TODO: timezone is not handled

        try:
            value = DateTime(datetime(*map(int, parts)))
        except:
            return empty_marker

        return value, {}


registerWidget(
    DateWidget,
    title='Date widget',
    description=('Date widget'),
    used_for=('Products.Archetypes.Field.DateTimeField',)
)


class AjaxSelectWidget(BaseWidget):
    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'select2',
        'separator': ';',
        'orderable': False,
        'ajax_vocabulary': None
    })
    _widget = base.InputWidget

    def getWidgetValue(self, context, field, request):
        return self.separator.join(
            request.get(field.getName(), field.getAccessor(context)()))

    def _widget_args(self, context, field, request):
        args = super(AjaxSelectWidget, self)._widget_args(context, field, request)

        vocabulary_name = getattr(field, 'vocabulary_factory', None)
        if self.ajax_vocabulary:
            vocabulary_name = self.ajax_vocabulary
        if vocabulary_name:
            url = base.base_url(context, request)
            url += '/@@getVocabulary?name=' + vocabulary_name
            if 'pattern_options' not in args:
                args['pattern_options'] = {}
            args['pattern_options']['ajaxVocabulary'] = url
        args['value'] = self.getWidgetValue(context, field, request)
        return args

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
    used_for=('Products.Archetypes.Field.LinesField',)
)


class RelatedItemsWidget(AjaxSelectWidget):
    _properties = AjaxSelectWidget._properties.copy()
    _properties.update({
        'pattern': 'relateditems',
        'separator': ','
    })
    vocabulary_view = "@@getVocabulary"

    def getWidgetValue(self, context, field, request):
        reqvalues = request.get(field.getName(), None)
        if not reqvalues:
            values = request.get(field.getName(), field.getAccessor(context)())
            values = [IUUID(o) for o in values if o]
        else:
            values = [v.split('/')[0]
                      for v in reqvalues.strip().split(self.separator)]
        return self.separator.join(values)

    def _widget_args(self, context, field, request):
        args = super(RelatedItemsWidget, self)._widget_args(
            context, field, request)

        vocabulary_name = getattr(field, 'vocabulary_factory',
                                  self.ajax_vocabulary)
        if not vocabulary_name:
            vocabulary_name = 'plone.app.vocabularies.Catalog'
        url = base.base_url(context, request)
        vocabulary_view = self.vocabulary_view
        url += '/' + vocabulary_view + '?name=' + vocabulary_name
        if 'pattern_options' not in args:
            args['pattern_options'] = {}
        args['pattern_options']['ajaxVocabulary'] = url

        pprops = getToolByName(context, 'portal_properties', None)
        folder_types = ['Folder']
        if pprops:
            site_props = pprops.site_properties
            folder_types = site_props.getProperty(
                'typesLinkToFolderContentsInFC',
                ['Folder'])
        args['pattern_options']['folderTypes'] = folder_types
        return args

    def process_form(self, instance, field, form, empty_marker=None):
        # select2 will add unique identifier information to results
        # so we're stripping it out here.
        value, other = super(RelatedItemsWidget, self).process_form(
            instance, field, form, empty_marker)
        value = [v.split('/')[0] for v in value]
        return value, other


registerWidget(
    RelatedItemsWidget,
    title='Related items widget',
    description=('Related items widget'),
    used_for='Products.Archetypes.Field.ReferenceField')


class QueryStringWidget(BaseWidget):
    _properties = BaseWidget._properties.copy()
    _properties.update({
        'pattern': 'querystring',
    })

    def _widget_args(self, context, field, request):
        args = super(QueryStringWidget, self)._widget_args(
            context, field, request)

        if 'pattern_options' not in args:
            args['pattern_options'] = {}

        args['pattern_options']['indexOptionsUrl'] = '%s/@@qsOptions' % (
            base.base_url(context, request))

        criterias = [dict(c) for c in field.getRaw(context)]
        args['value'] = request.get(field.getName(),
                                    json.dumps(criterias))
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
