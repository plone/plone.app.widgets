from zope.interface import Interface
from plone.app.z3cform.interfaces import IPloneFormLayer
from zope.filerepresentation.interfaces import IFileFactory


class IWidgetsLayer(IPloneFormLayer):
    """Browser layer used to indicate that plone.app.widgets is installed
    """


class IWidgetsView(Interface):
    """A view that gives access to various widget related functions.
    """

    def getVocabulary():
        """Returns vocabulary
        """

    def bodyDataOptions():
        """Returns the data attributes to be used on the body tag.
        """


class IATCTFileFactory(IFileFactory):
    """ adapter factory for ATCT
    """


class IDXFileFactory(IFileFactory):
    """ adapter factory for DX types
    """
