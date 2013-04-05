"""

    Demo form for z3c.form fields and widgets

"""

from zope.interface import Interface
import zope.schema

from plone.supermodel import model

from plone.app.widgets.demos.demo import WidgetDemoForm
from plone.app.widgets.demos.demo import IN_CORE_DESCRIPTION


class ITextExamples(model.Schema):
    """ Single choice and multiple choice examples """

    textLine = zope.schema.TextLine(
        title=u"zope.schema.TextLine",
        description=u"Unicode string")

    asciiLine = zope.schema.TextLine(
        title=u"zope.schema.ASCIILine",
        description=u"7-bit text string (bytes)")


#@widget_demo
class TextExamples(WidgetDemoForm):
    """
    """
    schema = ITextExamples

    label = u"Text examples"

    package = IN_CORE_DESCRIPTION  # Says that shipped with vanilla Plone
    layer = Interface  # Means that eanbled withou taddons (all browserlayers)
