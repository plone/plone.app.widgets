# -*- coding: utf-8 -*-
import zope.deferredimport


zope.deferredimport.deprecated(
    "Import from plone.app.z3cform.widgets.base instead (this package will be removed in Plone 7)",
    NotImplemented='plone.app.z3cform.widgets.base:PatternNotImplemented',
)
zope.deferredimport.deprecated(
    "Import from plone.app.z3cform.widgets.datetime instead (this package will be removed in Plone 7)",
    get_date_options='plone.app.z3cform.widgets.datetime:get_date_options',
    get_datetime_options='plone.app.z3cform.widgets.datetime:get_date_options',
)
zope.deferredimport.deprecated(
    "Import from plone.app.z3cform.widgets.relateditems instead (this package will be removed in Plone 7)",
    get_relateditems_options='plone.app.z3cform.widgets.relateditems:get_relateditems_options',
)
zope.deferredimport.deprecated(
    "Import from plone.app.z3cform.widgets.querystring instead (this package will be removed in Plone 7)",
    get_querystring_options='plone.app.z3cform.widgets.querystring:get_querystring_options',
)
zope.deferredimport.deprecated(
    "Import from plone.app.z3cform.widgets.richtext instead (this package will be removed in Plone 7)",
    get_tinymce_options='plone.app.z3cform.widgets.richtext:get_tinymce_options',
)
zope.deferredimport.deprecated(
    "Import from plone.app.z3cform.utils instead (this package will be removed in Plone 7)",
    get_portal='plone.app.z3cform.utils:get_portal',
    get_portal_url='plone.app.z3cform.utils:get_portal_url',
    get_context_url='plone.app.z3cform.utils:get_context_url',
    get_Widget_form='plone.app.z3cform.utils:get_Widget_form',
)
