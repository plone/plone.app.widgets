"""

    Demo form for z3c.form fields and widgets

"""

from zope.interface import Interface
import zope.schema

from plone.supermodel import model

from plone.app.widgets.demos.demo import WidgetDemoForm
from plone.app.widgets.demos.demo import IN_CORE_DESCRIPTION
from plone.app.widgets.demos.demo import get_doc


NUMBER_HELP = """
All number fields in ``zope.schema`` take following useful arguments

* ``min``

* ``max``

Example::

    class LocalizationOfStenosisForm(form.Schema):

        degreeOfStenosis = schema.Float(
            title=u"Degree of stenosis %",
            required=False,
            min=0.0,
            max=100.0
            )

For more information please see

* http://developer.plone.org/forms/z3c.form.html#validators

"""


class INumberExamples(model.Schema):
    """ Single choice and multiple choice examples """

    intField = zope.schema.Int(
        title=u"zope.schema.Int",
        description=get_doc(zope.schema.Int))

    floatField = zope.schema.Float(
        title=u"zope.schema.Float",
        description=get_doc(zope.schema.Float))


class NumberExamples(WidgetDemoForm):
    """
    """
    schema = INumberExamples

    label = u"Number examples"
    help = NUMBER_HELP

    package = IN_CORE_DESCRIPTION  # Says that shipped with vanilla Plone
    layer = Interface  # Means that eanbled withou taddons (all browserlayers)
