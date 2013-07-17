# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

from AccessControl import Unauthorized
from zope.globalrequest import setRequest
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from plone.app.widgets.testing import TestRequest
from plone.app.widgets.browser import VocabularyView
import json
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class BrowserTest(unittest.TestCase):

    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        setRequest(self.request)
        self.portal = self.layer['portal']
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def testVocabularyNoResults(self):
        """Tests that the widgets displays correctly
        """
        view = VocabularyView(self.portal, self.request)
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
            'name': 'plone.app.vocabularies.Catalog',
            'query': json.dumps(query)
        })
        data = json.loads(view())
        self.assertEquals(len(data['results']), 0)

    def testVocabularyCatalogResults(self):
        self.portal.invokeFactory('Document', id="page", title="page")
        self.portal.page.reindexObject()
        view = VocabularyView(self.portal, self.request)
        query = {
            'criteria': [
                {
                    'i': 'path',
                    'o': 'plone.app.querystring.operation.string.path',
                    'v': '/plone'
                }
            ]
        }
        self.request.form.update({
            'name': 'plone.app.vocabularies.Catalog',
            'query': json.dumps(query),
            'attributes': ['UID', 'id', 'title', 'path']
        })
        data = json.loads(view())
        self.assertEquals(len(data['results']), 1)
        self.portal.manage_delObjects(['page'])

    def testVocabularyBatching(self):
        amount = 30
        for i in xrange(amount):
            self.portal.invokeFactory('Document', id="page" + str(i),
                                      title="Page" + str(i))
            self.portal['page' + str(i)].reindexObject()
        view = VocabularyView(self.portal, self.request)
        query = {
            'criteria': [
                {
                    'i': 'path',
                    'o': 'plone.app.querystring.operation.string.path',
                    'v': '/plone'
                }
            ]
        }
        self.request.form.update({
            'name': 'plone.app.vocabularies.Catalog',
            'query': json.dumps(query),
            'attributes': ['UID', 'id', 'title', 'path'],
            'batch': {
                'page': '0',
                'size': '10'
            }
        })
        data = json.loads(view())
        self.assertEquals(len(data['results']), 10)
        self.assertEquals(data['total'], amount)

    def testVocabularyUnauthorized(self):
        setRoles(self.portal, TEST_USER_ID, [])
        view = VocabularyView(self.portal, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.Users',
            'query': TEST_USER_NAME
        })
        self.assertRaises(Unauthorized, view)

    def testVocabularyUsers(self):
        acl_users = self.portal.acl_users
        membership = self.portal.portal_membership
        amount = 10
        for i in range(amount):
            id = 'user' + str(i)
            acl_users.userFolderAddUser(id, 'secret', ['Member'], [])
            member = membership.getMemberById(id)
            member.setMemberProperties(mapping={"fullname": id})
        view = VocabularyView(self.portal, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.Users',
            'query': 'user'
        })
        data = json.loads(view())
        self.assertEqual(len(data['results']), amount)
