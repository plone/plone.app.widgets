from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from zope.interface import implementer
from zope.component import adapter
from plone.app.contenttypes.behaviors.collection import ICollection
from plone.app.event.dx.behaviors import IEventBasic
from plone.app.widgets.dx import QueryStringWidget
from plone.app.widgets.dx import DatetimeWidget
from plone.app.widgets.interfaces import IWidgetsLayer


@adapter(getSpecification(ICollection['query']), IWidgetsLayer)
@implementer(IFieldWidget)
def QueryStringFieldWidget(field, request):
    return FieldWidget(field, QueryStringWidget(request))


@adapter(getSpecification(IEventBasic['start']), IWidgetsLayer)
@implementer(IFieldWidget)
def StartDateFieldWidget(field, request):
    widget = FieldWidget(field, DatetimeWidget(request))
    return widget


@adapter(getSpecification(IEventBasic['end']), IWidgetsLayer)
@implementer(IFieldWidget)
def EndDateFieldWidget(field, request):
    widget = FieldWidget(field, DatetimeWidget(request))
    return widget
