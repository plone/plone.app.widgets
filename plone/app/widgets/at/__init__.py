from zope.component import adapts
from zope.interface import implements
from Products.ATContentTypes.interface import IATContentType
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

from plone.app.widgets.interfaces import IWidgetsLayer
from plone.app.widgets.at.autocomplete import AutocompleteWidget
from plone.app.widgets.at.calendar import CalendarWidget


class ATWidgetsExtender(object):
    """
    """

    implements(ISchemaModifier, IBrowserLayerAwareExtender)
    adapts(IATContentType)
    layer = IWidgetsLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        for field in schema.fields():
            old = field.widget

            if field.__name__ in ['subject']:
                field.widget = AutocompleteWidget(
                    label=old.label,
                    description=old.description,
                    vocabulary='plone.app.vocabularies.Keywords',
                    pattern_options={
                        'prompt': 'Add tag...',  # TODO: i18n
                    },
                )

            if field.__name__ in ['effectiveDate', 'expirationDate']:
                field.widget = CalendarWidget(
                    label=old.label,
                    description=old.description
                )

            if field.__name__ in ['contributors', 'creators']:
                field.widget = AutocompleteWidget(
                    label=old.label,
                    description=old.description,
                    vocabulary='plone.app.vocabularies.Users',
                    pattern_options={
                        # TODO: i18n
                        'prompt': 'Add ' + field.__name__ + '...',
                        'ajax-cache-results': 'false',
                    },
                )

        #for fieldname in ['contributors', 'creators']:
        #    if fieldname in schema:
        #        field = schema[fieldname]
        #        widget = field.widget
        #        field.widget = AutocompleteWidget(
        #            label=widget.label,
        #            description=widget.description,
        #        )
        #if 'customViewFields' in schema:
        #    field = schema['customViewFields']
        #    widget = field.widget
        #    field.widget = ChosenWidget(
        #        label=widget.label,
        #        description=widget.description,
        #        js_options={
        #            'allow_sortable': True
        #        }
        #    )

        #if 'relatedItems' in schema:
        #    field = schema['relatedItems']
        #    widget = field.widget
        #    field.widget = ChosenAjaxWidget(
        #        label=widget.label,
        #        description=widget.description,
        #        ajax_rel_url='widget-catalog-query'
        #    )
