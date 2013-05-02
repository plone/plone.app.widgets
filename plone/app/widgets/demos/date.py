"""

    Demo form for z3c.form fields and widgets

"""

from zope.interface import Interface
import zope.schema

from plone.supermodel import model

from plone.app.widgets.demos.demo import WidgetDemoForm
from plone.app.widgets.demos.demo import IN_CORE_DESCRIPTION


class IDateExamples(model.Schema):
    """ Single choice and multiple choice examples """

    date = zope.schema.Date(
        title=u"zope.schema.Date",
        description=u"Contains Python datetime.date object")

    dateTime = zope.schema.Datetime(
        title=u"zope.schema.Datetime",
        description=u"Contains Python datetime.datetime object")

    time = zope.schema.Time(
        title=u"zope.schema.Time",
        description=u"???")


class DateExamples(WidgetDemoForm):
    """
    """
    schema = IDateExamples

    label = u"Date and time examples"

    package = IN_CORE_DESCRIPTION  # Says that shipped with vanilla Plone
    layer = Interface  # Means that eanbled withou taddons (all browserlayers)
