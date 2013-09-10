# -*- coding: utf-8 -*-

import json
from DateTime import DateTime
from datetime import datetime
from zope.component import getUtility
from zope.component import queryMultiAdapter
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from plone.app.widgets import base
from plone.app.querystring.interfaces import IQuerystringRegistryReader
from plone.uuid.interfaces import IUUID


class BaseWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro': "patterns_widget",
        'pattern': None,
    })

    _widget = base.BaseWidget

    def _widget_args(self, context, field, request):
        options = {}
        for name in self._properties.keys():
            if name in ['blurrable', 'condition', 'description', 'helper_css',
                        'helper_js', 'label', 'macro', 'modes', 'populate',
                        'postback', 'show_content_type', 'visible', 'pattern',
                        'ajax_vocabulary']:
                continue
            options[name] = getattr(self, name)
        return {
            'name': field.getName(),
            'pattern': self.pattern,
            'pattern_options': options,
        }

    def view(self, context, field, request):
        return field.getAccessor(context)()

    def edit(self, context, field, request):
        args = self._widget_args(context, field, request)
        return self._widget(**args).render()


class InputWidget(BaseWidget):
    _properties = BaseWidget._properties.copy()
    _widget = base.InputWidget

    def _widget_args(self, context, field, request):
        args = super(InputWidget, self)._widget_args(context, field, request)
        # XXX: we might need to decode the value and encoding shouldn't be
        # hardcoded (value.decode('utf-8'))
        args['value'] = request.get(field.getName(),
                                    field.getAccessor(context)())
        return args


class DateWidget(InputWidget):
    _properties = InputWidget._properties.copy()
    _properties.update({
        'pattern': 'pickadate'
    })
    _widget = base.DateWidget

    def _widget_args(self, context, field, request):
        args = super(InputWidget, self)._widget_args(context, field, request)
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


class DatetimeWidget(DateWidget):
    _properties = DateWidget._properties.copy()
    _widget = base.DatetimeWidget

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
    DateWidget,
    title='Datetime widget',
    description=('Datetime widget'),
    used_for=('Products.Archetypes.Field.DateTimeField',)
)


class SelectWidget(BaseWidget):
    _properties = InputWidget._properties.copy()
    _properties.update({
        'pattern': 'select2',
        'separator': ';',
    })
    _widget = base.SelectWidget

    def _widget_args(self, context, field, request):
        args = super(SelectWidget, self)._widget_args(context, field, request)
        args['options'] = field.Vocabulary(context).items()
        return args


class Select2Widget(InputWidget):
    _properties = InputWidget._properties.copy()
    _properties.update({
        'pattern': 'select2',
        'separator': ';',
        'orderable': False,
        'ajax_vocabulary': None
    })
    _widget = base.Select2Widget

    def getWidgetValue(self, context, field, request):
        return self.separator.join(
            request.get(field.getName(), field.getAccessor(context)()))

    def _widget_args(self, context, field, request):
        args = super(Select2Widget, self)._widget_args(context, field, request)

        vocabulary_name = getattr(field, 'vocabulary_factory', None)
        if self.ajax_vocabulary:
            vocabulary_name = self.ajax_vocabulary
        if vocabulary_name:
            portal_state = queryMultiAdapter((context, request),
                                             name=u'plone_portal_state')
            url = ''
            if portal_state:
                url += portal_state.portal_url()
            url += '/@@getVocabulary?name=' + vocabulary_name
            if 'pattern_options' not in args:
                args['pattern_options'] = {}
            args['pattern_options']['ajaxvocabulary'] = url
        args['value'] = self.getWidgetValue(context, field, request)
        return args

    def process_form(self, instance, field, form, empty_marker=None):
        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker
        value = value.strip().split(self.separator)
        return value, {}


registerWidget(
    Select2Widget,
    title='Select2 widget',
    description=('Select2 widget'),
    used_for=('Products.Archetypes.Field.LinesField',)
)


class RelatedItemsWidget(Select2Widget):
    _properties = Select2Widget._properties.copy()
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
        portal_state = queryMultiAdapter((context, request),
                                         name=u'plone_portal_state')
        url = ''
        vocabulary_view = self.vocabulary_view
        if portal_state:
            url += portal_state.portal_url()
        url += '/' + vocabulary_view + '?name=' + vocabulary_name
        if 'pattern_options' not in args:
            args['pattern_options'] = {}
        args['pattern_options']['ajaxvocabulary'] = url

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


class QueryStringWidget(InputWidget):
    _properties = InputWidget._properties.copy()
    _properties.update({
        'pattern': 'querystring',
    })

    def _widget_args(self, context, field, request):
        args = super(QueryStringWidget, self)._widget_args(
            context, field, request)

        registry = getUtility(IRegistry)
        config = IQuerystringRegistryReader(registry)()

        if 'pattern_options' not in args:
            args['pattern_options'] = {}
        args['pattern_options'].update(config)

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
