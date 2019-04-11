# -*- coding: utf-8 -*-
import zope.deferredimport

# can be removed in Plone 6
zope.deferredimport.initialize()
zope.deferredimport.deprecated(
    'Import Zope2FileUploadStorable from plone.app.z3cform.factories instead',
    Zope2FileUploadStorable='plone.app.z3cform.factories:Zope2FileUploadStorable',
)
