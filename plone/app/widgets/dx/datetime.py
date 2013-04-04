
from zope.interface import implementsOnly
from zope.interface import implementer
from zope.component import adapts
from zope.component import adapter
from zope.schema.interfaces import IDate
from zope.schema.interfaces import IDatetime
from zope.i18n import translate
from z3c.form.converter import BaseDataConverter
from z3c.form.widget import Widget
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IWidget
from z3c.form.interfaces import IFieldWidget
from plone.app.z3cform.widget import IDatetimeField
from plone.app.z3cform.widget import IDateField
from plone.app.widgets import datetime  # We can't 'import datetime'
from plone.app.widgets.dx.base import PatternsWidget
from plone.app.widgets.interfaces import IWidgetsLayer


class BaseWidgetConverter(BaseDataConverter):
    """Data converter for date/datetime stuff."""

    format = None

    def toWidgetValue(self, value):
        """Convert from text lines to HTML representation."""
        if value is self.field.missing_value:
            return u''
        return value.strftime(self.format)

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        return datetime.datetime.strptime(value, self.format)


class BaseWidget(PatternsWidget, Widget):

    pattern_name = 'datetime'

    pickadateFormat = None

    formatSubmit = None

    def customize_widget(self, widget, value):
        widget.el.attrib['type'] = 'text'
        widget.el.attrib['value'] = value
        widget.options['format'] = translate(
            'pickadate_%s_format' % self.type,
            domain='plone.app.widgets',
            context=self.request,
            default=self.pickadateFormat
        )
        widget.options['formatSubmit'] = self.formatSubmit
        # TODO: we should get AM/PM from locales,
        # better if done in Javascript where H is 12 hours (with AMPM)
        # and HH 24 hours (no AMPM)
        widget.options['ampm'] = 'false'


class IDateTimeWidget(IWidget):
    pass


class DateTimeWidget(BaseWidget):

    implementsOnly(IDateTimeWidget)

    type = 'datetime'

    pickadateFormat = 'yyyy-mm-dd @ HH:MM'

    formatSubmit = 'yyyy-mm-dd HH:MM'


class DateTimeWidgetConverter(BaseWidgetConverter):
    """Data converter for datetime."""

    adapts(IDatetime, IDateTimeWidget)

    format = '%Y-%m-%d %H:%M'


@adapter(IDatetimeField, IWidgetsLayer)
@implementer(IFieldWidget)
def DateTimeFieldWidget(field, request):
    """IFieldWidget factory for DateTimeWidget."""
    return FieldWidget(field, DateTimeWidget(request))


class IDateWidget(IWidget):
    pass


class DateWidget(BaseWidget):

    implementsOnly(IDateWidget)

    type = 'date'

    pickadateFormat = 'yyyy-mm-dd @'

    formatSubmit = 'yyyy-mm-dd'


class DateWidgetConverter(BaseWidgetConverter):
    """Data converter for date."""

    adapts(IDate, IDateWidget)

    format = '%Y-%m-%d'

    def toFieldValue(self, value):
        if not value:
            return self.field.missing_value
        return datetime.date.strptime(value, self.format)


@adapter(IDateField, IWidgetsLayer)
@implementer(IFieldWidget)
def DateFieldWidget(field, request):
    """IFieldWidget factory for DateWidget."""
    return FieldWidget(field, DateWidget(request))
