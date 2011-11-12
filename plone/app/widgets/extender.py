from plone.widgets.archetypes import ChosenWidget
from archetypes.schemaextender.interfaces import ISchemaModifier
from zope.component import adapts
from zope.interface import implements
from Products.ATContentTypes.interface import IATContentType


class WidgetsModifier(object):
    """
    change any content...
    """
    adapts(IATContentType)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        if 'subject' in schema:
            subject = schema['subject']
            subject_widget = subject.widget
            subject.widget = ChosenWidget(
                label=subject_widget.label,
                description=subject_widget.description)
            subject.vocabulary_factory = 'plone.app.vocabularies.Keywords'
