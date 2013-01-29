from zope.component import adapts
from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from Products.ATContentTypes.interface import IATContentType
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

from plone.app.widgets.interfaces import IWidgetsLayer
from plone.app.widgets.at.select2 import Select2Widget
from plone.app.widgets.at.datetime import DateTimeWidget

_plone = MessageFactory('plone')


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
                field.widget = Select2Widget(
                    label=old.label,
                    description=old.description,
                    pattern_options="width:30em;",
                    tags='plone.app.vocabularies.Keywords',
                )

            if field.__name__ in ['language']:

                field.widget = Select2Widget(
                    label=old.label,
                    description=old.description,
                    pattern_options='width:15em;',
                    element_type="select",
                )

            if field.__name__ in ['effectiveDate', 'expirationDate']:
                field.widget = DateTimeWidget(
                    label=old.label,
                    description=old.description
                )

            if field.__name__ in ['contributors']:
                field.widget = Select2Widget(
                    label=old.label,
                    description=_plone(u"The names of people that have "
                                       u"contributed to this item."),
                    multiple=True,
                    ajax_vocabulary="plone.app.vocabularies.Users",
                    pattern_options="width:30em;placeholder:Add "
                                    "contributors...;",
                )

            if field.__name__ in ['creators']:
                field.widget = Select2Widget(
                    label=old.label,
                    description=_plone(u"The names of people that have "
                                       u"contributed to this item."),
                    multiple=True,
                    ajax_vocabulary="plone.app.vocabularies.Users",
                    pattern_options="width:30em;placeholder:Add creators...;"
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
