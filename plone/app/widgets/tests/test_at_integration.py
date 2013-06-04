# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING


class BaseWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.at.base.BaseWidget
    """

    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def test_something(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        # TODO: Unauthorized: Cannot create ExampleType
        #portal.invokeFactory('ExampleType', id='example', title='Example')
