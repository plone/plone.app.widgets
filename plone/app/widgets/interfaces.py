from plone.app.z3cform.interfaces import IPloneFormLayer
from zope.filerepresentation.interfaces import IFileFactory
from zope.interface import Interface


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


class IFieldPermissionChecker(Interface):
    """Adapter factory for checking whether a user has permission to
    edit a specific field on a content object.
    """

    def validate(field_name, vocabulary_name=None):
        """Returns True if the current user has permission to edit the
        `field_name` field.  Returns False if the user does not have
        permission.  Raises and AttributeError if the field cannot be
        found.
        """
