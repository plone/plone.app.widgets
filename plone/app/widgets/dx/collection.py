import json # XXX: maybe we should use defusedjson
from zope.interface import implementer
from zope.interface import implementsOnly
from zope.component import adapter
from zope.component import adapts
from zope.schema.interfaces import IList
from z3c.form.interfaces import IWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.converter import BaseDataConverter
from z3c.form.widget import Widget
from z3c.form.widget import FieldWidget
from plone.app.contenttypes.interfaces import ICollection
from plone.app.widgets.interfaces import IWidgetsLayer
from plone.app.widgets.dx.base import PatternsWidget


class IQueryStringWidget(IWidget):
    """Marker interface for the p.a.widgets QueryStringWidget
    """


class QueryStringWidget(PatternsWidget, Widget):

    pattern_name = 'querystring'

    implementsOnly(IQueryStringWidget)

    def customize_widget(self, widget, value):
        widget.el.attrib['type'] = 'text'
        widget.el.attrib['value'] = value


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
