# -*- coding: utf-8 -*-
import os
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.widgets.browser import vocabulary
from plone.app.widgets.browser.file import FileUploadView
from plone.app.widgets.browser.query import QueryStringIndexOptions
from plone.app.widgets.browser.vocabulary import VocabularyView
from plone.app.widgets.interfaces import IFieldPermissionChecker
from plone.app.widgets.testing import ExampleFunctionVocabulary
from plone.app.widgets.testing import ExampleVocabulary
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from plone.app.widgets.testing import TestRequest
from zope.component import provideAdapter
from zope.component import provideUtility
from zope.component.globalregistry import base
from zope.globalrequest import setRequest
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

from zope.component import getAdapter

_dir = os.path.dirname(__file__)

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover


class BrowserTest(unittest.TestCase):

    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        setRequest(self.request)
        self.portal = self.layer['portal']
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        provideUtility(ExampleVocabulary(), name=u'vocab_class')
        provideUtility(ExampleFunctionVocabulary, name=u'vocab_function')
        vocabulary._permissions.update({
            'vocab_class': 'Modify portal content',
            'vocab_function': 'Modify portal content',
        })

    def testAdapter(self):
        """Test querying a class based vocabulary with a search string.
        """
        richtexteditor = getAdapter(self.portal, name='richtexteditor')
        self.assertEquals(richtexteditor.is_selected('TinyMCE'), True)
