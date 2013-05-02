# -*- coding: utf-8 -*-
"""

    Demostrate all widgets.

    Each widget / field registers itself as a

"""

from zope.component import getAdapters
from zope.interface import Interface
from zope.interface import alsoProvides

from Products.Five.browser import BrowserView

import z3c.form
import z3c.form.form
import z3c.form.field

from plone.autoform.form import AutoExtensibleForm

from Products.CMFPlone.utils import safe_unicode

from .rst import restructured_to_html
from .source import get_class_source
from .interfaces import IWidgetDemo


# This warning should be given when the user might try default=[] or default={}
DEFAULT_MUTABLE_WARNING = u"""

    *Default mutable arguments warning*: Don't use default=[] argument, because
    default mutable arguments will break when processing multiple HTTP
    requests.

"""


IN_CORE_DESCRIPTION = u"Plone core. No addons needed."


#: 4-5 items vocabulary used in the demo to fill in choice examples
DEMO_VOCABULARY = "plone.app.vocabularies.Roles"


def get_doc(klass):
    """ Get class documentation.

    Get docstring, convert unicode and do other smart tricks
    to make it appear on the demo page.
    """
    return safe_unicode(getattr(klass, "__doc__", ""))


class IDemoWidget(Interface):
    pass


class Demos(BrowserView):
    """ Render all demo forms with their widgets in a nice view.

    Read forms which implements IWidgetDemo marke via @widget_demo
    class decocator. Build a nice and useful description string
    for each field in those forms.

    """

    label = u"Plone fields and widgets demo"
    description = u"Demostrate fields widges available for Dexterity and " +\
                  u"plone.app.z3cform forms"

    def buildCustomDescriptions(self, form):
        """ For each field, make the description contain extra information
            how to use it.
        """

        # Get inline source code viewer Python code
        form.source = get_class_source(form.schema)
        form.help = restructured_to_html(getattr(form, "help", None))

        for widget in form.widgets.values():

            alsoProvides(widget, IDemoWidget)

            # Points to orignal zope.schema field which only has one
            # instance in the process. Thus, don't convert this twice.
            field = widget.field

            if not hasattr(field, "_demo_widget_rst"):
                desc = field.description
                string_data = restructured_to_html(desc)
                # z3c.form is strict about unicode
                field.description = string_data.decode("utf-8")
                field._demo_widget_rst = True

    def update(self):
        """
        Fetch all demo forms registered in the system for the template
        consumption.
        """

        # We query against HTTPRequest and browser layers,
        # as all widgets might not be functional without enabling
        # addon in the control panel first
        self.demos = [form for name, form in getAdapters(
            (self.context, self.request,), provided=IWidgetDemo)]
        for form in self.demos:
            form.update()
            self.buildCustomDescriptions(form)

    def __call__(self):
        self.update()
        return self.index()


class WidgetDemoForm(AutoExtensibleForm, z3c.form.form.Form):
    """ Base class for all widget demo forms.
    """

    ignoreContext = True
