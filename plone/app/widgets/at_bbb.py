from zope.component import adapts
from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from Products.ATContentTypes.interface import IATContentType
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender

from plone.app.widgets.interfaces import IWidgetsLayer
from plone.app.widgets import at

_plone = MessageFactory('plone')


class MetadataExtender(object):
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
                field.widget = at.Select2Widget(
                    label=old.label,
                    description=old.description,
                    ajax_vocabulary='plone.app.vocabularies.Keywords',
                )

            if field.__name__ in ['language']:
                field.widget = at.SelectWidget(
                    label=old.label,
                    description=old.description,
                )

            if field.__name__ in ['effectiveDate', 'expirationDate']:
                field.widget = at.DatetimeWidget(
                    label=old.label,
                    description=old.description
                )

            if field.__name__ in ['contributors']:
                field.widget = at.Select2Widget(
                    label=old.label,
                    description=_plone(u"The names of people that have "
                                       u"contributed to this item."),
                    ajax_vocabulary="plone.app.vocabularies.Users",
                )

            if field.__name__ in ['creators']:
                field.widget = at.Select2Widget(
                    label=old.label,
                    description=_plone(u"The names of people that are "
                                       u"creators to this item."),
                    ajax_vocabulary="plone.app.vocabularies.Users",
                )

            if field.__name__ == 'relatedItems':
                field.widget = at.RelatedItemsWidget(
                    label=old.label,
                    description=old.description
                )

            if field.__name__ == 'query':
                field.widget = at.QueryStringWidget(
                    label=old.label,
                    description=old.description
                )

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
