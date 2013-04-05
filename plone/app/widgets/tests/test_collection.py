# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest
    assert unittest

import datetime
import cgi # We need this to escape HTML
from zope.interface import alsoProvides
from zope.component import getMultiAdapter
from zope.globalrequest import setRequest
from z3c.form.interfaces import IDataConverter
from z3c.form import form
from z3c.form import field
from plone.app.contenttypes.interfaces import ICollection
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from plone.app.widgets.dx.collection import IQueryStringWidget
from plone.app.widgets.dx.collection import QueryStringWidget
from plone.app.widgets.testing import TestRequest
from plone.app.widgets.testing import DummyContext


class CollectionWidgetTestForm(form.Form):

    fields = field.Fields(ICollection)


class DxDateWidgetTest(unittest.TestCase):
    """Tests dexterity date widget
    """

    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        setRequest(self.request)

    def testDisplay(self):
        """Tests that the widgets displays correctly
        """
        widget = QueryStringWidget(self.request)
        widget.id = 'id'
        widget.name = 'name'
        self.assertEqual(
            widget.render(),
            ('<input name="name" type="text" value="" '
                    'class="pat-querystring"/>')
        )
        widget.value = ('[{"i":"SearchableText",'
                        '"o":"plone.app.querystring.operation.string.contains",'
                        '"v":"Autoren"}]')
        self.assertEqual(
            widget.render(),
            ('<input name="name" type="text" value="%s" '
                    'class="pat-querystring"/>') % cgi.escape(widget.value, True)
        )

    def testConverter(self):
        """Tests that the data converter works as expected
        """
        context = DummyContext()
        alsoProvides(context, ICollection)
        form_ = CollectionWidgetTestForm(context, self.request)
        form_.update()
        # XXX: Here it's pickin' up the wrong converter
        converter = getMultiAdapter(
            (form_.widgets['query'].field, form_.widgets['query']),
            IDataConverter
        )
        self.assertEqual(
            converter.toWidgetValue([
                { "i":"SearchableText",
                  "o":"plone.app.querystring.operation.string.contains",
                  "v":"Autoren" }
            ]),
            ('[{"i":"SearchableText",'
             '"o":"plone.app.querystring.operation.string.contains",'
             '"v":"Autoren"}]')
        )
        self.assertEqual(
            converter.toFieldValue(
                '[{"i":"SearchableText",'
                '"o":"plone.app.querystring.operation.string.contains",'
                '"v":"Autoren"}]'
            ),
            [
                { "i":"SearchableText",
                  "o":"plone.app.querystring.operation.string.contains",
                  "v":"Autoren" }
            ]
        )

    def testForm(self):
        """Tests that the correct widget is picked up, namely,
        that we are correctly overriding default widgets.
        """
        context = DummyContext()
        alsoProvides(context, ICollection)
        form_ = CollectionWidgetTestForm(context, self.request)
        form_.update()
        self.assertTrue(IQueryStringWidget.providedBy(form_.widgets['query']))

