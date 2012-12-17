from zope.interface import Interface


class IQueryResult(Interface):
    """BrowserView to query results for widgets
    """


class IWidgetsLayer(Interface):
    """Browser layer used to indicate that plone.app.widgets is installed
    """
