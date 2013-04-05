from zope.interface import Interface


class IWidgetDemo(Interface):
    """ A marker interface marking form for widgets demo.

    Demo form dynamically polls all the demo adapter registrations and
    fills the demo fields with these.
    """
