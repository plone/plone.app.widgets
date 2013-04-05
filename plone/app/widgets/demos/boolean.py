"""

    Demo form for z3c.form fields and widgets

"""

from zope.interface import Interface
import zope.schema

from plone.supermodel import model

from plone.app.widgets.demos.demo import WidgetDemoForm
from plone.app.widgets.demos.demo import IN_CORE_DESCRIPTION
from plone.app.widgets.demos.demo import get_doc


class IBooleanExamples(model.Schema):
    """ Single choice and multiple choice examples """

    boolField = zope.schema.Bool(
        title=u"zope.schema.Bool",
        description=get_doc(zope.schema.Bool))

    boolField = zope.schema.Float(
        title=u"zope.schema.Bool with z3c.form.",
        )


class BoolExamples(WidgetDemoForm):
    """
    """
    schema = IBooleanExamples

    label = u"Boolean examples"

    package = IN_CORE_DESCRIPTION  # Says that shipped with vanilla Plone
    layer = Interface  # Means that eanbled withou taddons (all browserlayers)
