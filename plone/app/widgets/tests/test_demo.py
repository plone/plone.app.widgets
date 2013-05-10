# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

from plone.app.widgets.testing import PLONEAPPWIDGETS_FUNCTIONAL_TESTING

from plone.testing.z2 import Browser


class WidgetsDemoTest(unittest.TestCase):
    """ See that the widget demo page opens without exceptions """

    layer = PLONEAPPWIDGETS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_open_demo_page(self):
        """ Open the widgets demo page
        """
        browser = Browser(self.portal)
        browser.open(self.portal.absolute_url() + "/@@widgets-demo")
