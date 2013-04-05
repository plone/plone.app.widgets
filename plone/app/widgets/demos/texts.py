"""

    Demo form for z3c.form fields and widgets

"""

from zope.interface import Interface
import zope.schema

from plone.supermodel import model

from plone.app.widgets.demos.demo import WidgetDemoForm
from plone.app.widgets.demos.demo import IN_CORE_DESCRIPTION
from plone.app.widgets.demos.demo import get_doc


class ITextExamples(model.Schema):
    """ Single choice and multiple choice examples """

    textLine = zope.schema.TextLine(
        title=u"zope.schema.TextLine",
        description=get_doc(zope.schema.TextLine))

    asciiLine = zope.schema.ASCIILine(
        title=u"zope.schema.ASCIILine",
        description=get_doc(zope.schema.ASCIILine))

    text = zope.schema.Text(
        title=u"zope.schema.Text",
        description=get_doc(zope.schema.Text))


#@widget_demo
class TextExamples(WidgetDemoForm):
    """
    """
    schema = ITextExamples

    label = u"Text examples"

    package = IN_CORE_DESCRIPTION  # Says that shipped with vanilla Plone
    layer = Interface  # Means that eanbled withou taddons (all browserlayers)
