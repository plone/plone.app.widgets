# -*- coding: utf-8 -*-
import zope.deferredimport

# FileFactory only needed by ATContentTypes
zope.deferredimport.initialize()
zope.deferredimport.deprecated(
    'Import IFileFactory from zope.filerepresentation.interfaces instead',
    IFileFactory='zope.filerepresentation.interfaces:IFileFactory',
)

zope.deferredimport.deprecated(
    'Import IFieldPermissionChecker from plone.app.z3cform.interfaces instead',
    IFieldPermissionChecker='plone.app.z3cform.interfaces:IFieldPermissionChecker',  # noqa
)
