from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from zope.interface import implementer
from zope.component import adapter
from plone.app.contenttypes.interfaces import ICollection
from plone.app.widgets.dx import QueryStringWidget
from plone.app.widgets.interfaces import IWidgetsLayer


@adapter(getSpecification(ICollection['query']), IWidgetsLayer)
@implementer(IFieldWidget)
def QueryStringFieldWidget(field, request):
    return FieldWidget(field, QueryStringWidget(request))
