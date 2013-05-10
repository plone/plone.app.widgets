# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

from zope.globalrequest import setRequest

from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from plone.app.widgets.testing import DummyContext
from plone.app.widgets.testing import DummyATField
from plone.app.widgets.testing import TestRequest


class BaseWidgetTest(unittest.TestCase):
    """Tests base widget
    """

    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        self.context = DummyContext()
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        setRequest(self.request)

    def testNotImplemneted(self):
        """ Using base pattern widget should raise NotImplemented exception.
        """

        from plone.app.widgets.at.base import PatternsWidget as ATWidget
        from plone.app.widgets.dx.base import PatternsWidget as DXWidget

        widget = DXWidget(self.request)
        self.assertRaises(NotImplementedError, widget.render)

        widget = ATWidget()
        self.assertRaises(NotImplementedError, widget.edit,
                          self.context, None, self.request)

    def testDefaultBehavior(self):
        """ Base pattern widget default behavior.
        """
        from plone.app.widgets.at.base import PatternsWidget as BaseATWidget
        from plone.app.widgets.dx.base import PatternsWidget as BaseDXWidget

        class DXWidget(BaseDXWidget):
            pattern_name = 'example'

        widget = DXWidget(self.request)
        widget.name = 'dummyname'
        self.assertEqual(widget.render(),
                         '<input name="dummyname" class="pat-example"/>')

        class ATWidget(BaseATWidget):
            pattern_name = 'example'

        widget = ATWidget()
        field = DummyATField()
        self.assertEqual(widget.edit(self.context, field, self.request),
                         '<input name="dummyname" class="pat-example"/>')
