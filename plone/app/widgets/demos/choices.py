"""

    Demo form for z3c.form fields and widgets

"""

from zope.interface import Interface
import zope.schema

from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget

from plone.supermodel import model
from plone.autoform import directives as form

from plone.app.widgets.demos.demo import WidgetDemoForm
from plone.app.widgets.demos.demo import IN_CORE_DESCRIPTION
from plone.app.widgets.demos.demo import DEFAULT_MUTABLE_WARNING
from plone.app.widgets.demos.demo import DEMO_VOCABULARY


class IChoiceExamples(model.Schema):
    """ Single choice and multiple choice examples """

    multiChoiceOrderedList = zope.schema.List(
        title=u"zope.schema.List(value_type=zope.schema.Choice)",
        description=u"Multiple choices with list manipular and store "
                    u"values in zope.schema.List (maps to python List)." +
                    DEFAULT_MUTABLE_WARNING,
        value_type=zope.schema.Choice(vocabulary=DEMO_VOCABULARY))

    form.widget(multiChoiceCheckbox=CheckBoxFieldWidget)
    multiChoiceCheckbox = zope.schema.List(
        title=u"zope.schema.List() and checkBoxFieldWidget",
        description=u"Select multiple checkboxes using checkboxes and store "
                    u"values in zope.schema.List (maps to python List)." +
                    DEFAULT_MUTABLE_WARNING,
        required=False,
        value_type=zope.schema.Choice(vocabulary=DEMO_VOCABULARY))

    multiChoiceOne = zope.schema.Choice(
        title=u"zope.schema.Choice",
        description=u"Select one choice using ``<select>`` and store value as "
                    u"vocabulary term string",
        vocabulary=DEMO_VOCABULARY,
        default="Document")

    form.widget(radioButton=RadioFieldWidget)
    radioButton = zope.schema.Choice(
        title=u"zope.schema.Choice and RadioFieldWidget",
        description=u"Select one choice using radio button and store value as "
                    u"vocabulary term string",
        vocabulary=DEMO_VOCABULARY,
        default="Document")


class ChoiceExamples(WidgetDemoForm):
    """
    """
    schema = IChoiceExamples

    label = u"Single and multiple choices"

    package = IN_CORE_DESCRIPTION  # Says that shipped with vanilla Plone
    layer = Interface  # Means that eanbled withou taddons (all browserlayers)
