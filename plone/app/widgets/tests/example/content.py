from DateTime import DateTime

from Products.Archetypes import atapi
from Products.Archetypes.examples.SimpleType import SimpleType

from plone.app.widgets import at


Schema = atapi.BaseSchema.copy() + atapi.Schema((
    atapi.TextField(
        'inputfield',
        widget=at.InputWidget(
            label='Text field',
            description='',
        ),
    ),
    atapi.TextField(
        'selectfield',
        widget=at.SelectWidget(
            label='Select field',
            description='',
        ),
    ),
    atapi.TextField(
        'select2field',
        widget=at.Select2Widget(
            label='Select2 field',
            description='',
        ),
    ),
    atapi.DateTimeField(
        'datefield',
        default_method=DateTime,
        widget=at.DateWidget(
            label='Date field',
            description='',
        ),
    ),
    atapi.DateTimeField(
        'datetimefield',
        default_method=DateTime,
        widget=at.DatetimeWidget(
            label='Datetime field',
            description='',
            ampm=1,
        ),
    ),
))


class ExampleType(SimpleType):
    """A simple archetype"""

    schema = Schema
    archetype_name = meta_type = "ExampleType"
    portal_type = 'ExampleType'

atapi.registerType(ExampleType, 'plone.app.widgets.tests.example')
