import json
from zope.interface import implementer
from zope.interface import implementsOnly
from zope.component import adapter
from zope.component import adapts
from zope.schema.interfaces import IList
from z3c.form.interfaces import IWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.converter import BaseDataConverter
from z3c.form.widget import FieldWidget
from plone.app.contenttypes.interfaces import ICollection
from plone.app.widgets.interfaces import IWidgetsLayer
from plone.app.widgets.dx.base import InputWidget


class IQueryStringWidget(IWidget):
    """Marker interface for the QueryStringWidget
    """


class QueryStringWidget(InputWidget):

    pattern = 'querystring'

    implementsOnly(IQueryStringWidget)


class QueryStringDataConverter(BaseDataConverter):

    adapts(IList, IQueryStringWidget)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return value
        return json.dumps(value)

    def toFieldValue(self, value):
        if value is self.field.missing_value:
            return value
        return json.loads(value)


@adapter(getSpecification(ICollection['query']), IWidgetsLayer)
@implementer(IFieldWidget)
def QueryStringFieldWidget(field, request):
    return FieldWidget(field, QueryStringWidget(request))
