from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from zope.interface import implementer
from zope.component import adapter
from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.app.dexterity.behaviors.metadata import IOwnership
from plone.app.widgets.dx.select2 import TagsWidget
from plone.app.widgets.interfaces import IWidgetsLayer


@adapter(getSpecification(ICategorization['subjects']), IWidgetsLayer)
@implementer(IFieldWidget)
def SubjectsFieldWidget(field, request):
    widget = FieldWidget(field, TagsWidget(request))
    widget.ajaxtags = 'plone.app.vocabularies.Keywords'
    return widget


@adapter(getSpecification(IOwnership['contributors']), IWidgetsLayer)
@implementer(IFieldWidget)
def ContributorsFieldWidget(field, request):
    widget = FieldWidget(field, TagsWidget(request))
    widget.ajaxtags = 'plone.app.vocabularies.Users'
    return widget


@adapter(getSpecification(IOwnership['creators']), IWidgetsLayer)
@implementer(IFieldWidget)
def CreatorsFieldWidget(field, request):
    widget = FieldWidget(field, TagsWidget(request))
    widget.ajaxtags = 'plone.app.vocabularies.Users'
    return widget
