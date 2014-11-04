from mock import Mock
from mock import patch

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover


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
            self.assertEquals(utils.first_weekday(), 0)
            base.first_weekday = lambda: 1
            self.assertEquals(utils.first_weekday(), 1)
            base.first_weekday = lambda: 5
            self.assertEquals(utils.first_weekday(), 1)

            # test without plone.app.event installed
            utils.HAS_PAE = False
            self.assertEquals(utils.first_weekday(), 0)

        # restore original state
        utils.HAS_PAE = orig_HAS_PAE
        reload(utils)
