# -*- coding: utf-8 -*-
import doctest

from zope.configuration import xmlconfig

from plone.testing import z2

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting


class PloneAppWidgetsLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import plone.app.widgets
        xmlconfig.file(
            'configure.zcml',
            plone.app.widgets,
            context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.widgets:default')
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        setRoles(portal, TEST_USER_ID, ['Manager'])


PLONEAPPWIDGETS_FIXTURE = PloneAppWidgetsLayer()

PLONEAPPWIDGETS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEAPPWIDGETS_FIXTURE,),
    name="PloneAppWidgetsLayer:Integration")
PLONEAPPWIDGETS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONEAPPWIDGETS_FIXTURE,),
    name="PloneAppWidgetsLayer:Functional")
PLONEAPPWIDGETS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(PLONEAPPWIDGETS_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PloneAppWidgetsLayer:Acceptance")

optionflags = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
