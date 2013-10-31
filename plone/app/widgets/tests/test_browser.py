# -*- coding: utf-8 -*-

from mock import Mock
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.widgets.browser.vocabulary import VocabularyView
from plone.app.widgets.browser.query import QueryStringIndexOptions
from plone.app.widgets.browser.file import FileUploadView
from plone.app.widgets.interfaces import IFieldPermissionChecker
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from plone.app.widgets.testing import TestRequest
from zope.globalrequest import setRequest
from zope.component import provideAdapter
from zope.component.globalregistry import base
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from StringIO import StringIO
import transaction

import json

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover


class PermissionChecker(object):
    def __init__(self, context):
        pass

    def validate(self, field_name):
        if field_name == 'allowed_field':
            return True
        elif field_name == 'disallowed_field':
            return False
        else:
            raise AttributeError('Missing Field')

class ICustomPermissionProvider(Interface):
    pass

def _enable_permission_checker(context):
    provideAdapter(PermissionChecker, adapts=(ICustomPermissionProvider,),
                   provides=IFieldPermissionChecker)
    alsoProvides(context, ICustomPermissionProvider)

def _disable_permission_checker(context):
    noLongerProvides(context, ICustomPermissionProvider)
    base.unregisterAdapter(required=(ICustomPermissionProvider,),
                           provided=IFieldPermissionChecker)


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
        # batch pages are 1-based
        self.request.form.update({
            'name': 'plone.app.vocabularies.Catalog',
            'query': json.dumps(query),
            'attributes': ['UID', 'id', 'title', 'path'],
            'batch': {
                'page': '1',
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
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')

    def testVocabularyMissing(self):
        view = VocabularyView(self.portal, self.request)
        self.request.form.update({
            'name': 'vocabulary.that.does.not.exist',
        })
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')

    def testPermissionCheckerAllowed(self):
        # Setup a custom permission checker on the portal
        _enable_permission_checker(self.portal)
        view = VocabularyView(self.portal, self.request)

        # Allowed field is allowed
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'allowed_field',
        })
        data = json.loads(view())
        self.assertEquals(len(data['results']),
                          len(self.portal.portal_types.objectIds()))
        _disable_permission_checker(self.portal)

    def testPermissionCheckerUnknownVocab(self):
        _enable_permission_checker(self.portal)
        view = VocabularyView(self.portal, self.request)
        # Unknown vocabulary gives error
        self.request.form.update({
            'name': 'vocab.does.not.exist',
            'field': 'allowed_field',
        })
        data = json.loads(view())
        self.assertEquals(data['error'],
                          'No factory with name "{}" exists.'.format(
            'vocab.does.not.exist'))
        _disable_permission_checker(self.portal)

    def testPermissionCheckerDisallowed(self):
        _enable_permission_checker(self.portal)
        view = VocabularyView(self.portal, self.request)
        # Disallowed field is not allowed
        # Allowed field is allowed
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'disallowed_field',
        })
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')
        _disable_permission_checker(self.portal)

    def testPermissionCheckerShortCircuit(self):
        _enable_permission_checker(self.portal)
        view = VocabularyView(self.portal, self.request)
        # Known vocabulary name short-circuits field permission check
        # global permission
        self.request.form['name'] = 'plone.app.vocabularies.Users'
        self.request.form.update({
            'name': 'plone.app.vocabularies.Users',
            'field': 'disallowed_field',
        })
        data = json.loads(view())
        self.assertEquals(data['results'], [])
        _disable_permission_checker(self.portal)

    def testPermissionCheckerUnknownField(self):
        _enable_permission_checker(self.portal)
        view = VocabularyView(self.portal, self.request)
        # Unknown field is raises error
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'missing_field',
        })
        with self.assertRaises(AttributeError):
            view()
        _disable_permission_checker(self.portal)

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

    def testQueryStringConfiguration(self):
        view = QueryStringIndexOptions(self.portal, self.request)
        data = json.loads(view())
        # just test one so we know it's working...
        self.assertEqual(data['indexes']['sortable_title']['sortable'], True)

    def testFileUpload(self):
        view = FileUploadView(self.portal, self.request)
        fdata = StringIO('foobar')
        fdata.filename = 'foobar.txt'
        self.request.form['file'] = fdata
        self.request.REQUEST_METHOD = 'POST'
        data = json.loads(view())
        self.assertEqual(data['url'], 'http://nohost/plone/foobar.txt')
        self.assertTrue(data['UID'] is not None)
        # clean it up...
        self.portal.manage_delObjects(['foobar.txt'])
        transaction.commit()
