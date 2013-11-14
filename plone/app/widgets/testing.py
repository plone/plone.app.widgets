# -*- coding: utf-8 -*-

from doctest import ELLIPSIS
from doctest import NORMALIZE_WHITESPACE
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from plone.app.widgets.interfaces import IWidgetsLayer
from plone.testing import z2
from zope.configuration import xmlconfig
from zope.interface import directlyProvides
from zope.interface import implements
from zope.publisher.browser import TestRequest as BaseTestRequest
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ExampleVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context, query=None):
        items = [u'One', u'Two', u'Three']
        tmp = SimpleVocabulary([
            SimpleTerm(it.lower(), it.lower(), it)
            for it in items
            if query is None
            or query.lower() in it.lower()
        ])
        tmp.test = 1
        return tmp


def ExampleFunctionVocabulary(context, query=None):
    items = [u'First', u'Second', u'Third']
    tmp = SimpleVocabulary([
        SimpleTerm(it.lower(), it.lower(), it)
        for it in items
        if query is None
        or query.lower() in it.lower()
    ])
    return tmp
directlyProvides(ExampleFunctionVocabulary, IVocabularyFactory)


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

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.widgets:default')


PLONEAPPWIDGETS_FIXTURE = PloneAppWidgetsLayer()


class PloneAppWidgetsDXLayer(PloneAppWidgetsLayer):

    def setUpZope(self, app, configurationContext):
        import plone.app.contenttypes
        xmlconfig.file('configure.zcml',
                       plone.app.contenttypes,
                       context=configurationContext)

        try:
            import mockup
            self.loadZCML(package=mockup)
        except:
            pass

        z2.installProduct(app, 'Products.DateRecurringIndex')

        super(PloneAppWidgetsDXLayer, self).setUpZope(app,
                                                      configurationContext)

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        # we need contenttypes before installing widgets
        self.applyProfile(portal, 'plone.app.contenttypes:default')
        super(PloneAppWidgetsDXLayer, self).setUpPloneSite(portal)


PLONEAPPWIDGETS_FIXTURE_DX = PloneAppWidgetsDXLayer()

PLONEAPPWIDGETS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEAPPWIDGETS_FIXTURE,),
    name="PloneAppWidgetsLayer:Integration")
PLONEAPPWIDGETS_DX_ROBOT_TESTING = FunctionalTesting(
    bases=(PLONEAPPWIDGETS_FIXTURE_DX,
           AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="PloneAppWidgetsLayerDX:Robot")

optionflags = (ELLIPSIS | NORMALIZE_WHITESPACE)
