"""

    Demo form for z3c.form fields and widgets

"""

from zope.interface import Interface
import zope.schema

from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget

from plone.supermodel import model
from plone.autoform import directives as form

from plone.app.widgets.demos.demo import widget_demo
from plone.app.widgets.demos.demo import WidgetDemoForm
from plone.app.widgets.demos.demo import IN_CORE_DESCRIPTION
from plone.app.widgets.demos.demo import DEFAULT_MUTABLE_WARNING


class IChoiceExamples(model.Schema):
    """ Single choice and multiple choice examples """

    multiChoiceOrderedList = zope.schema.List(
        title=u"List multiple choices: zope.schema.List and ",
        description=u"Multiple choices with list manipular and store values in zope.schema.List (maps to python List)." + DEFAULT_MUTABLE_WARNING,
        value_type=zope.schema.Choice(vocabulary="plone.app.vocabularies.PortalTypes"))

    form.widget(multiChoiceCheckbox=CheckBoxFieldWidget)
    multiChoiceCheckbox = zope.schema.List(
        title=u"Checkbox multiple choices",
        description=u"Select multiple checkboxes using checkboxes and store values in zope.schema.List (maps to python List)." + DEFAULT_MUTABLE_WARNING,
        required=False,
        value_type=zope.schema.Choice(vocabulary="plone.app.vocabularies.PortalTypes"))

    form.widget(radioButton=RadioFieldWidget)
    radioButton = zope.schema.Choice(
        title=u"Radio button",
        description=u"Select one choice using radio button and store value as vocabulary term string",
        vocabulary="plone.app.vocabularies.PortalTypes",
        default="Document")


@widget_demo
class ChoiceExamples(WidgetDemoForm):
    """
    """
    schema = IChoiceExamples

    label = u"Single and multiple choices"
    description = IChoiceExamples.__doc__

    package = IN_CORE_DESCRIPTION  # Says that shipped with vanilla Plone
    layer = Interface  # Means that eanbled withou taddons (all browserlayers)
