# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


PROFILE_ID = 'profile-plone.app.widgets:default'


def upgrade_2_to_3(context):
    """Remove JS and CSS resources from portal_css and portal_js registry.
    Import resource registry configuration.
    """
    setup = getToolByName(context, "portal_setup")
    setup.runImportStepFromProfile(PROFILE_ID, 'jsregistry')
    tool = getToolByName(context, 'portal_javascripts')
    tool.cookResources()
