from mock import Mock
from mock import patch
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from plone.app.widgets.utils import get_querystring_options
from plone.app.widgets.utils import get_relateditems_options
from plone.app.widgets.utils import get_tinymce_options

import unittest


class MockTool(Mock):
    firstweekday = 6


class UtilsTests(unittest.TestCase):

    def test__first_weekday(self):
        # make sure, plone.app.event is available and mock it.
        mock = Mock()
        modules = {
            'plone': mock,
            'plone.app': mock.module,
            'plone.app.event': mock.module.module,
            'plone.app.event.base': mock.module.module.module,
        }
        with patch('Products.CMFCore.utils.getToolByName', new=MockTool), \
             patch.dict('sys.modules', modules):
            # test for plone.app.event installed
            from plone.app.event import base
            base.first_weekday = lambda: 0
            base.wkday_to_mon1 = lambda x: x
            from plone.app.widgets import utils
            reload(utils)  # reload utils, so that plone.app.event mock import
                           # works, even if it was imported before.,,
            orig_HAS_PAE = utils.HAS_PAE
            utils.HAS_PAE = True
            self.assertEqual(utils.first_weekday(), 0)
            base.first_weekday = lambda: 1
            self.assertEqual(utils.first_weekday(), 1)
            base.first_weekday = lambda: 5
            self.assertEqual(utils.first_weekday(), 1)

            # test without plone.app.event installed
            utils.HAS_PAE = False
            self.assertEqual(utils.first_weekday(), 0)

        # restore original state
        utils.HAS_PAE = orig_HAS_PAE
        reload(utils)


class TestQueryStringOptions(unittest.TestCase):
    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        setRoles(self.layer['portal'], TEST_USER_ID, ['Contributor'])

    def test__query_string_options(self):
        """Test query string options on root:
        All URLs and paths equal root url and path,
        no favorites
        """

        portal = self.layer['portal']
        options = get_querystring_options(
            portal,
            '@@qsOptions'
        )

        # Test base options
        self.assertEqual(
            options['indexOptionsUrl'],
            'http://nohost/plone/@@qsOptions'
        )

        self.assertEqual(
            options['previewCountURL'],
            'http://nohost/plone/@@querybuildernumberofresults'
        )

        self.assertEqual(
            options['previewURL'],
            'http://nohost/plone/@@querybuilder_html_results'
        )

        # Test options of the AJAX select widget
        self.assertEqual(
            options['patternAjaxSelectOptions']['separator'],
            ';'
        )

        # Test options of the date picker
        self.assertEqual(
            options['patternDateOptions']['time'],
            False
        )

        # Test options of the related items widget
        self.assertEqual(
            options['patternRelateditemsOptions']['basePath'],
            '/plone'
        )


class TestRelatedItemsOptions(unittest.TestCase):
    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        setRoles(self.layer['portal'], TEST_USER_ID, ['Contributor'])

    def test__base_relateditems_options(self):
        """Test related items options on root:
        All URLs and paths equal root url and path,
        no favorites
        """

        portal = self.layer['portal']
        options = get_relateditems_options(
            portal,
            None,
            '#!@',
            'test_vocab',
            '@@vocab',
            'testfield'
        )

        # vocab is correctly set
        self.assertTrue(
            '@@vocab?name=test_vocab&field=testfield'
            in options['vocabularyUrl']
        )

        # rootUrl contains something
        self.assertTrue(
            bool(options['rootUrl'])
        )

        root_path = context_path = '/'.join(portal.getPhysicalPath())
        root_url = context_url = portal.absolute_url()

        # context_path contains something, otherwise this test is meaningless
        self.assertTrue(bool(context_path))
        # context_url contains something, otherwise this test is meaningless
        self.assertTrue(bool(context_url))

        self.assertEqual(
            options['rootUrl'],
            root_url
        )

        self.assertEqual(
            options['rootPath'],
            root_path
        )

        self.assertEqual(
            options['vocabularyUrl'],
            root_url + '/@@vocab?name=test_vocab&field=testfield'
        )

        self.assertEqual(
            options['basePath'],
            context_path
        )

        self.assertEqual(
            options['contextPath'],
            context_path
        )

        self.assertEqual(
            options['separator'],
            '#!@'
        )

        self.assertTrue(
            'favorites' not in options
        )

    def test__subfolder_relateditems_options(self):
        """Test related items options on subfolder:
        Vocab called on root, start path is folder, have favorites.
        """

        portal = self.layer['portal']
        portal.invokeFactory('Folder', 'sub')
        sub = portal.sub
        options = get_relateditems_options(
            sub,
            None,
            '#!@',
            'test_vocab',
            '@@vocab',
            'testfield'
        )

        # vocab is correctly set
        self.assertTrue(
            '@@vocab?name=test_vocab&field=testfield'
            in options['vocabularyUrl']
        )

        # rootUrl contains something
        self.assertTrue(
            bool(options['rootUrl'])
        )

        root_path = '/'.join(portal.getPhysicalPath())
        root_url = portal.absolute_url()
        context_path = '/'.join(sub.getPhysicalPath())
        context_url = sub.absolute_url()

        # context_path contains something, otherwise this test is meaningless
        self.assertTrue(bool(context_path))
        # context_url contains something, otherwise this test is meaningless
        self.assertTrue(bool(context_url))

        self.assertEqual(
            options['rootUrl'],
            root_url
        )

        self.assertEqual(
            options['rootPath'],
            root_path
        )

        self.assertEqual(
            options['vocabularyUrl'],
            root_url + '/@@vocab?name=test_vocab&field=testfield'
        )

        self.assertEqual(
            options['basePath'],
            context_path
        )

        self.assertEqual(
            options['contextPath'],
            context_path
        )

        self.assertEqual(
            options['separator'],
            '#!@'
        )

        self.assertEqual(
            len(options['favorites']),
            2
        )

        self.assertEqual(
            sorted(options['favorites'][0].keys()),
            ['path', 'title']
        )

    def test__subdocument_relateditems_options(self):
        """Test related items options on subdoc:
        Vocab called on root, start path is root as document is not folderish,
        no favorites.
        """

        portal = self.layer['portal']
        portal.invokeFactory('Document', 'sub')
        sub = portal.sub
        options = get_relateditems_options(
            sub,
            None,
            '#!@',
            'test_vocab',
            '@@vocab',
            'testfield'
        )

        # vocab is correctly set
        self.assertTrue(
            '@@vocab?name=test_vocab&field=testfield'
            in options['vocabularyUrl']
        )

        # rootUrl contains something
        self.assertTrue(
            bool(options['rootUrl'])
        )

        root_path = '/'.join(portal.getPhysicalPath())
        root_url = portal.absolute_url()
        context_path = '/'.join(sub.getPhysicalPath())
        context_url = sub.absolute_url()

        # context_path contains something, otherwise this test is meaningless
        self.assertTrue(bool(context_path))
        # context_url contains something, otherwise this test is meaningless
        self.assertTrue(bool(context_url))

        self.assertEqual(
            options['rootUrl'],
            root_url
        )

        self.assertEqual(
            options['rootPath'],
            root_path
        )

        self.assertEqual(
            options['vocabularyUrl'],
            root_url + '/@@vocab?name=test_vocab&field=testfield'
        )

        self.assertEqual(
            options['basePath'],
            root_path
        )

        self.assertEqual(
            options['contextPath'],
            context_path
        )

        self.assertEqual(
            options['separator'],
            '#!@'
        )

        self.assertTrue(
            'favorites' not in options
        )


class TestTinyMCEOptions(unittest.TestCase):
    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        setRoles(self.layer['portal'], TEST_USER_ID, ['Contributor'])

    def test__tinymce_options_different_contexts(self):
        """Test if ``get_tinymce_options`` can be called with different
        contexts, including invalid and form contexts.
        """
        request = self.layer['request']
        portal = self.layer['portal']
        portal.invokeFactory('Folder', 'sub')
        sub = portal.sub

        # TinyMCE on portal context
        options = get_tinymce_options(portal, None, request)
        self.assertEqual(options['relatedItems']['basePath'], '/plone')

        # TinyMCE on sub folder context
        options = get_tinymce_options(sub, None, request)
        self.assertEqual(options['relatedItems']['basePath'], '/plone/sub')
