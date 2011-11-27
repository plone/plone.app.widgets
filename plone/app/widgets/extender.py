from plone.widgets.archetypes import ChosenWidget
from plone.widgets.archetypes import AjaxChosenWidget
from archetypes.schemaextender.interfaces import ISchemaModifier
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from zope.component import adapts
from zope.interface import implements
from Products.ATContentTypes.interface import IATContentType
from plone.app.widgets.interfaces import ILayer


class WidgetsModifier(object):
    """
    change any content...
    """
    implements(ISchemaModifier, IBrowserLayerAwareExtender)
    adapts(IATContentType)
    layer = ILayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        if 'subject' in schema:
            subject = schema['subject']
            subject_widget = subject.widget
            subject.widget = ChosenWidget(
                label=subject_widget.label,
                description=subject_widget.description,
                js_options={
                    'allow_add_new': True,
                    'no_results_text': 'No results. Press enter to add',
                    'allow_sortable': True
                })
            subject.vocabulary_factory = 'plone.app.vocabularies.Keywords'

        for fieldname in ['contributors', 'creators']:
            if fieldname in schema:
                field = schema[fieldname]
                widget = field.widget
                field.widget = AjaxChosenWidget(
                    label=widget.label,
                    description=widget.description,
                    queryView='widget-user-query'
                )
        if 'customViewFields' in schema:
            field = schema['customViewFields']
            widget = field.widget
            field.widget = ChosenWidget(
                label=widget.label,
                description=widget.description,
                js_options={
                    'allow_sortable': True
                }
            )

        if 'relatedItems' in schema:
            field = schema['relatedItems']
            widget = field.widget
            field.widget = AjaxChosenWidget(
                label=widget.label,
                description=widget.description,
                queryView='widget-catalog-query'
            )
