
from zope.interface import implementsOnly
from zope.interface import implementer
from zope.component import adapts
from zope.component import adapter
from zope.schema.interfaces import IDatetime
from z3c.form.converter import BaseDataConverter
from z3c.form.widget import Widget
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IWidget
from z3c.form.interfaces import IFieldWidget
from plone.app.z3cform.widget import IDatetimeField
from plone.app.widgets import datetime
from plone.app.widgets.dx.base import PatternsWidget
from plone.app.widgets.interfaces import IWidgetsLayer


class IDateTimeWidget(IWidget):
    pass


class DateTimeWidget(PatternsWidget, Widget):

    implementsOnly(IDateTimeWidget)

    def __init__(self, *args, **kw):
        super(DateTimeWidget, self).__init__(*args, **kw)
        self._pattern_options = {}
        self._pattern_el_type = 'input'
        self._pattern_name = 'datetime'

    def render_element(self, el):

        el.attrib['type'] = 'text'
        el.attrib['value'] = self.value

        return el


class DateTimeWidgetConverter(BaseDataConverter):
    """Data converter for ITextLinesWidget."""

    adapts(IDatetime, IDateTimeWidget)

    def toWidgetValue(self, value):
        """Convert from text lines to HTML representation."""
        if value is self.field.missing_value:
            return u''
        return value.strftime('%Y-%m-%d %H:%M')

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        return datetime.strptime(value, '%Y-%m-%d %H:%M')


@adapter(IDatetimeField, IWidgetsLayer)
@implementer(IFieldWidget)
def DateTimeFieldWidget(field, request):
    """IFieldWidget factory for DateTimeWidget."""
    return FieldWidget(field, DateTimeWidget(request))
