from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from zope.interface import implementer
from zope.component import adapter
from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.app.dexterity.behaviors.metadata import IOwnership
from plone.app.dexterity.behaviors.metadata import IPublication
try:
    from plone.app.relationfield.behavior import IRelatedItems
    HAS_RF = True
except ImportError:
    HAS_RF = False
from plone.app.widgets.dx import DatetimeWidget
from plone.app.widgets.dx import SelectWidget
from plone.app.widgets.dx import Select2Widget
from plone.app.widgets.dx import RelatedItemsWidget
from plone.app.widgets.interfaces import IWidgetsLayer


@adapter(getSpecification(ICategorization['subjects']), IWidgetsLayer)
@implementer(IFieldWidget)
def SubjectsFieldWidget(field, request):
    widget = FieldWidget(field, Select2Widget(request))
    widget.ajax_vocabulary = 'plone.app.vocabularies.Keywords'
    return widget


@adapter(getSpecification(ICategorization['language']), IWidgetsLayer)
@implementer(IFieldWidget)
def LanguageFieldWidget(field, request):
    widget = FieldWidget(field, SelectWidget(request))
    return widget


@adapter(getSpecification(IPublication['effective']), IWidgetsLayer)
@implementer(IFieldWidget)
def EffectiveDateFieldWidget(field, request):
    widget = FieldWidget(field, DatetimeWidget(request))
    return widget


@adapter(getSpecification(IPublication['expires']), IWidgetsLayer)
@implementer(IFieldWidget)
def ExpirationDateFieldWidget(field, request):
    widget = FieldWidget(field, DatetimeWidget(request))
    return widget


@adapter(getSpecification(IOwnership['contributors']), IWidgetsLayer)
@implementer(IFieldWidget)
def ContributorsFieldWidget(field, request):
    widget = FieldWidget(field, Select2Widget(request))
    widget.ajax_vocabulary = 'plone.app.vocabularies.Users'
    return widget


@adapter(getSpecification(IOwnership['creators']), IWidgetsLayer)
@implementer(IFieldWidget)
def CreatorsFieldWidget(field, request):
    widget = FieldWidget(field, Select2Widget(request))
    widget.ajax_vocabulary = 'plone.app.vocabularies.Users'
    return widget


if HAS_RF:
    @adapter(getSpecification(IRelatedItems['relatedItems']), IWidgetsLayer)
    @implementer(IFieldWidget)
    def RelatedItemsFieldWidget(field, request):
        widget = FieldWidget(field, RelatedItemsWidget(request))
        widget.ajax_vocabulary = 'plone.app.vocabularies.Catalog'
        return widget
