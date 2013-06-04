from Products.Archetypes import atapi
from Products.CMFCore import utils
from Products.CMFCore.permissions import AddPortalContent

PROJECTNAME = 'plone.app.widgets.tests.example'


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    from plone.app.widgets.tests.example.content import ExampleType
    assert ExampleType

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(PROJECTNAME),
        PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit(
            "%s: %s" % (PROJECTNAME, atype.portal_type),
            content_types=(atype,),
            permission=AddPortalContent,
            extra_constructors=(constructor,),
        ).initialize(context)
