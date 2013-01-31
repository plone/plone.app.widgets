# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except:
    import unittest
    assert unittest

from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, setRoles, login


class PloneAppWidgetsClassTest(unittest.TestCase):

    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.types = self.portal.portal_types

    def test_css_registered(self):
        css = getattr(self.portal, 'portal_css')
        css_ids = css.getResourceIds()
        self.assertTrue('++resource++plone.app.widgets.css' in css_ids)

    def test_js_registered(self):
        js = getattr(self.portal, 'portal_javascripts')
        js_ids = js.getResourceIds()
        self.assertTrue('++resource++plone.app.widgets.js' in js_ids)
        import pdb; pdb.set_trace()

    def test_widgets_bundle_in_sunburst_theme(self):
        import pdb; pdb.set_trace()

    def test_skin_path_in_sunburt_theme(self):
        import pdb; pdb.set_trace()

    def test_browser_layer(self):
        import pdb; pdb.set_trace()
