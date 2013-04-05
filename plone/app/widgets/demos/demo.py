# -*- coding: utf-8 -*-
"""

    Demostrate all widgets.

    Each widget / field registers itself as a

"""

from zope.interface import Interface
from zope.component import getAdapters
from zope.component import getGlobalSiteManager

from five import grok

import z3c.form
import z3c.form.form
import z3c.form.field

from Products.CMFCore.interfaces import ISiteRoot

from plone.autoform.form import AutoExtensibleForm

from .rst import restructured_to_html
from .source import get_class_source

grok.templatedir(".")

#: This warning should be given when the user might try default=[] or default={}
DEFAULT_MUTABLE_WARNING = u"""
    .. warning ::

        Don't use default=[] argument, because default mutable arguments will
        break when processing multiple parallel HTTP requests.

    For more information see
    `default mutable discussion <http://stackoverflow.com/questions/1132941/least-astonishment-in-python-the-mutable-default-argument>`_
    on stackoverflow.com.

"""


IN_CORE_DESCRIPTION = u"Provided in Plone core since version 4.1: see zope.schema and z3c.form packages"


class IWidgetDemo(Interface):
    """ A marker interface marking form for widgets demo.

    Demo form dynamically polls all the demo adapter registrations and
    fills the demo fields with these.
    """


class Demos(grok.View):
    """ Render all demo forms with their widgets in a nice view.

    Read forms which implements IWidgetDemo marke via @widget_demo
    class decocator. Build a nice and useful description string
    for each field in those forms.

    """

    grok.context(ISiteRoot)
    grok.name("widgets-demo")
    grok.template("widgets-demo")

    label = u"Plone fields and widgets demo"
    description = u"Demostrate fields widges available for Dexterity and plone.app.z3cform forms"

    def buildCustomDescriptions(self, form):
        """ For each field, make the description contain extra information how to use it.

        """

        # Get inline source code viewer Python code
        form.source = get_class_source(form.schema)

        for widget in form.widgets.values():

            # Points to orignal zope.schema field which only has one
            # instance in the process. Thus, don't convert this twice.
            field = widget.field

            if not hasattr(field, "_demo_widget_rst"):
                desc = field.description
                string_data = restructured_to_html(desc)
                field.description = string_data.decode("utf-8-")  # z3c.form is strict about unicode
                field._demo_widget_rst = True

    def update(self):

        # We query against HTTPRequest and browser layers,
        # as all widgets might not be functional without enabling
        # addon in the control panel first
        self.demos = [klass(self.context, self.request)for name, klass in getAdapters((self.request,), provided=IWidgetDemo)]
        for form in self.demos:
            form.update()
            self.buildCustomDescriptions(form)

        form.render()


class WidgetDemoForm(AutoExtensibleForm, z3c.form.form.Form):
    """ Base class for all widget demo forms.
    """

    ignoreContext = True


def widget_demo(klass):
    """ Class decorator to tell this form to contributes to the widget demo page.

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
