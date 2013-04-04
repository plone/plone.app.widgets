# -*- coding: utf-8 -*-
"""

    Demostrate all widgets.

    Each widget / field registers itself as a

"""

from zope.interface import Interface, implements
from zope.component import queryAdapter
from zope.component import getGlobalSiteManager

import zope.schema

from five import grok
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile

import z3c.form.field

from Products.CMFCore.interfaces import ISiteRoot

from plone.directives.form import Form

#: This warning should be given when the user might try default=[] or default={}
DEFAULT_MUTABLE_WARNING = """
    .. warn ::

        Don't use default=[] argument, because default mutable arguments will
        break when processing multiple parallel HTTP requests.

    * http://stackoverflow.com/questions/1132941/least-astonishment-in-python-the-mutable-default-argument

"""


class IWidgetDemo(Interface):
    """
    Field / widget adapter registration.

    Demo form dynamically polls all the demo adapter registrations and
    fills the demo fields with these.

    Each widget description field must be filled with description about
    how to use field / widget.

    Package where the widget is defined is automatically filled in.
    """

    def getDemoFields():
        """
        :return: None or zope.schema.Field
        """

    def update(form):
        """  Form.update() callback.

        Allows poke the fields for the demo form.
        """

    def updateWidgets(Form):
        """ updateWidgets() callback.

        Allows poke the widget for the demo form.
        """


class DemoForm(Form):
    """ A demo form of edit mode for all widgets who decide to contribute themselves on this form.
    """

    grok.context(ISiteRoot)
    grok.name("widgets-demo")
    label = u"Plone fields and widgets demo"
    description = u"Demostrate fields widges available for Dexterity and plone.app.z3cform forms"

    index = FiveViewPageTemplateFile("demo.pt")

    def update(self):
        super(DemoForm, self).update()
        self.demos = queryAdapter(self.request, IWidgetDemo)
        for demo in self.demos:
            demo.update(self)

    def updateWidgets(self):
        super(DemoForm, self).updateWidgets()
        for demo in self.demos:
            demo.updateWidgets(self)


def demo_field(klass, browser_layer_interface):
    """ Class decorator to tell this field appear on the demo form.

    :param browser_layer_interface:
        zope.interface.Interface marker interface telling which addon provides the widget.
        Give zope.interface.Interface to mark that the widget is always available, regarless of enabled addon.

    """

    gsm = getGlobalSiteManager()
    gsm.registerAdapter(factory=klass, required=(browser_layer_interface,),
                        name=klass.__name__, provided=IWidgetDemo)
    return klass


class BaseDemo(object):
    """ Abstract base class for one field/widget demo.
    """
    implements(IWidgetDemo)

    def update(self, form):
        fields = z3c.form.field.Fields([self.field])
        form.fields += fields

    def updateWidgets(self, form):
        pass


@demo_field(Interface)
class TextLine(BaseDemo):
    field = zope.schema.ITextField(title=u"Text Line")


@demo_field(Interface)
class ASCIILine(BaseDemo):
    field = zope.schema.IASCIILine(title=u"ASCII Line")


@demo_field(Interface)
class MultiChoiceCheckbox(BaseDemo):
    """ Select multiple checkboxes and store values in zope.schema.List (maps to python List).

    """ + DEFAULT_MUTABLE_WARNING

    field = zope.schema.List(title=u"Checkbox multiple choices",
                             required=False,
                             value_type=zope.schema.Choice(vocabulary="plone.app.vocabularies.PortalTypes"),
                             )


@demo_field(Interface)
class Radio(BaseDemo):
    """ Select one item with many using radio button

    """ + DEFAULT_MUTABLE_WARNING

    field = zope.schema.Choice(vocabulary="plone.app.vocabularies.PortalTypes",
                               title=u"Radio button",
                               default="Document"
                               )
