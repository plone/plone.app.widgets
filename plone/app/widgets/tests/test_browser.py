# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

from zope.globalrequest import setRequest
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from plone.app.widgets.testing import TestRequest
from plone.app.widgets.browser import WidgetsView
import json


class BrowserTest(unittest.TestCase):

    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        setRequest(self.request)
        self.portal = self.layer['portal']

    def testVocabularyNoResults(self):
        """Tests that the widgets displays correctly
        """
        view = WidgetsView(self.portal, self.request)
        query = {
            'criteria': [
                {
                    'i': 'path',
                    'o': 'plone.app.querystring.operation.string.path',
                    'v': '/foo'
                }
            ]
        }
        self.request.form.update({
            'name': 'plone.app.vocabularies.catalog',
            'query': json.dumps(query)
        })
        data = json.loads(view.getVocabulary())
        self.assertEquals(len(data['results']), 0)

    def testVocabularyCatalogResults(self):
        self.portal.invokeFactory('Document', id="page", title="page")
        self.portal.page.reindexObject()
        view = WidgetsView(self.portal, self.request)
        query = {
            'criteria': [
                {
                    'i': 'path',
                    'o': 'plone.app.querystring.operation.string.path',
                    'v': '/plone'
                }
            ],
            'attributes': ['UID', 'id', 'title', 'path']
        }
        self.request.form.update({
            'name': 'plone.app.vocabularies.catalog',
            'query': json.dumps(query)
        })
        data = json.loads(view.getVocabulary())
        self.assertEquals(len(data['results']), 1)

