# -*- coding: utf-8 -*-
from zope.interface import Interface

import zope.deferredimport

zope.deferredimport.initialize()
zope.deferredimport.deprecated(
    'Import from new.baz.baaz instead',
    IFileFactory='zope.filerepresentation:interfaces.IFileFactory',
)


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
