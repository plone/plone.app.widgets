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

from Products.CMFCore.interfaces import ISiteRoot

from plone.autoform.form import AutoExtensibleForm

#: This warning should be given when the user might try default=[] or default={}
DEFAULT_MUTABLE_WARNING = """
    .. warn ::

        Don't use default=[] argument, because default mutable arguments will
        break when processing multiple parallel HTTP requests.

    * http://stackoverflow.com/questions/1132941/least-astonishment-in-python-the-mutable-default-argument

"""


IN_CORE_DESCRIPTION = "Provided in Plone core since version 4.1: see zope.schema and z3c.form packages"


class IWidgetDemo(Interface):
    """ A marker interface marking form for widgets demo.

    Demo form dynamically polls all the demo adapter registrations and
    fills the demo fields with these.
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

        form.render()


class WidgetDemoForm(AutoExtensibleForm, z3c.form.form.EditForm):
    """ Base class for all widget demo forms.
    """

    ignoreContext = True


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


