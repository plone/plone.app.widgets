# -*- coding: utf-8 -*-
"""

    Demostrate all widgets.

    Each widget / field registers itself as a

"""

from zope.interface import Interface, implements
from zope.component import getAdapters
from zope.component import getGlobalSiteManager

import zope.schema
import zope.schema.interfaces

from five import grok
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile

import z3c.form
import z3c.form.form
import z3c.form.field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget

from z3c.form.browser.textlines import TextLinesFieldWidget

from Products.CMFCore.interfaces import ISiteRoot

from plone.autoform.form import AutoExtensibleForm
import plone.autoform.directives as form
from plone.supermodel import model

from Products.CMFPlone.utils import safe_unicode

#: This warning should be given when the user might try default=[] or default={}
DEFAULT_MUTABLE_WARNING = """
    .. warn ::

        Don't use default=[] argument, because default mutable arguments will
        break when processing multiple parallel HTTP requests.

    * http://stackoverflow.com/questions/1132941/least-astonishment-in-python-the-mutable-default-argument

"""


IN_CORE_DESCRIPTION = "Provided in Plone core since version 4.1: see zope.schema and z3c.form packages"


class IWidgetDemo(Interface):
    """
    Field / widget adapter registration.

    Demo form dynamically polls all the demo adapter registrations and
    fills the demo fields with these.

    Each widget description field must be filled with description about
    how to use field / widget.

    Package where the widget is defined is automatically filled in.
    """

    def getForm():
        """
        :return: None or zope.schema.Field
        """


grok.templatedir(".")


class Demos(grok.View):
    """ Render all demo forms with their widgets in a nice view.
    """

    grok.context(ISiteRoot)
    grok.name("widgets-demo")
    grok.template("widgets-demo")

    label = u"Plone fields and widgets demo"
    description = u"Demostrate fields widges available for Dexterity and plone.app.z3cform forms"

    def update(self):

        # We query against HTTPRequest and browser layers,
        # as all widgets might not be functional without enabling
        # addon in the control panel first
        self.demos = [klass(self.context, self.request)for name, klass in getAdapters((self.request,), provided=IWidgetDemo)]
        for form in self.demos:
            form.update()

        import ipdb ; ipdb.set_trace()
        form.render()


def widget_demo(klass):
    """ Class decorator to tell this class to contribute to the demo form.

    :param browser_layer_interface:
        zope.interface.Interface marker interface telling which addon provides the widget.
        Give zope.interface.Interface to mark that the widget is always available, regarless of enabled addon.

    """
    layer = klass.layer

    def factory(request):
        return klass

    gsm = getGlobalSiteManager()
    gsm.registerAdapter(factory=factory, required=(layer,),
                        name=klass.__name__, provided=IWidgetDemo)
    return klass


class IChoiceExamples(model.Schema):

    multiChoiceOrderedList = zope.schema.List(
        title=u"List multiple choices",
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
class ChoiceExamples(AutoExtensibleForm, z3c.form.form.EditForm):
    """
    """
    schema = IChoiceExamples
    ignoreContext = True

    package = IN_CORE_DESCRIPTION
    layer = Interface
