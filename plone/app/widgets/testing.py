# -*- coding: utf-8 -*-

import doctest

from zope.interface import implements
from zope.publisher.browser import TestRequest as BaseTestRequest

from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from plone.app.widgets.interfaces import IWidgetsLayer


class TestRequest(BaseTestRequest):
    implements(IWidgetsLayer)


class DummyContext(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class DummyATField(object):

    def getName(self):
        return 'dummyname'

    def getAccessor(self, context):
        def accessor():
            return 'dummyvalue'
        return accessor


class PloneAppWidgetsLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.widgets
        self.loadZCML(package=plone.app.widgets)
        import plone.app.widgets.tests.example
        self.loadZCML(package=plone.app.widgets.tests.example)

        # Install product and call its initialize() function
        z2.installProduct(app, 'plone.app.widgets.tests.example')

    def tearDownZope(self, app):
        # Uninstall product and call its uninstall() function
        z2.uninstallProduct(app, 'plone.app.widgets.tests.example')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.widgets:default')
        self.applyProfile(portal, 'plone.app.widgets.tests.example:example')


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
