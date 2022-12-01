# -*- coding: utf-8 -*-
import zope.deferredimport


zope.deferredimport.deprecated(
    "Import from plone.app.z3cform.utils instead (this package will be removed in Plone 7)",
    el_attrib='plone.app.z3cform.utils:el_attrib',
    dict_merge='plone.app.z3cform.utils:dict_merge',
)
zope.deferredimport.deprecated(
    "Import from plone.app.z3cform.widgets.patterns instead (this package will be removed in Plone 7)",
    BaseWidget='plone.app.z3cform.widgets.patterns:BaseWidget',
    InputWidget='plone.app.z3cform.widgets.patterns:InputWidget',
    SelectWidget='plone.app.z3cform.widgets.patterns:SelectWidget',
    TextareaWidget='plone.app.z3cform.widgets.patterns:TextareaWidget',
)
