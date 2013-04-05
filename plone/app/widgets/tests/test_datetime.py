# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest
    assert unittest

import datetime
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.schema import Date
from zope.schema import Datetime
from zope.globalrequest import setRequest
from z3c.form.interfaces import IDataConverter
from z3c.form import form
from z3c.form import field
from plone.app.widgets.dx.datetime import IDateWidget
from plone.app.widgets.dx.datetime import DateWidget
from plone.app.widgets.dx.datetime import IDateTimeWidget
from plone.app.widgets.dx.datetime import DateTimeWidget
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from plone.app.widgets.testing import TestRequest
from plone.app.widgets.testing import DummyContext


class DxBaseWidgetTest(unittest.TestCase):
    """Base test case for dexterity widgets
    """

    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        setRequest(self.request)


class IDateWidgetTest(Interface):

    start = Date(title=u"Start", default=datetime.date(2013, 4, 4))
    end = Date(title=u"End")


class DateWidgetTestForm(form.Form):

    fields = field.Fields(IDateWidgetTest)


class DxDateWidgetTest(DxBaseWidgetTest):
    """Tests dexterity date widget
    """

    def testDisplay(self):
        """Tests that the widgets displays correctly
        """
        widget = DateWidget(self.request)
        widget.id = 'id'
        widget.name = 'name'
        self.assertRegexpMatches(
            widget.render(),
            (r'<input name="name" type="text" value="" '
                    r'class="pat-datetime" '
                    r'data-datetime-ampm="false" '
                    r'data-datetime-formatSubmit="yyyy-mm-dd" '
                    r'data-datetime-format="[^"]+"/>')
        )
        widget.value = '2013-04-04'
        self.assertRegexpMatches(
            widget.render(),
            (r'<input name="name" type="text" value="2013-04-04" '
                    r'class="pat-datetime" '
                    r'data-datetime-ampm="false" '
                    r'data-datetime-formatSubmit="yyyy-mm-dd" '
                    r'data-datetime-format="[^"]+"/>')
        )

    def testConverter(self):
        """Tests that the data converter works as expected
        """
        context = DummyContext()
        alsoProvides(context, IDateWidgetTest)
        form_ = DateWidgetTestForm(context, self.request)
        form_.update()
        for field_name in ['start', 'end']:
            converter = getMultiAdapter(
                (form_.widgets[field_name].field, form_.widgets[field_name]),
                IDataConverter
            )
            self.assertEqual(
                converter.toWidgetValue(datetime.date(2013, 4, 4)),
                '2013-04-04'
            )
            self.assertEqual(
                converter.toFieldValue('2013-04-04'),
                datetime.date(2013, 4, 4)
            )

    def testForm(self):
        """Tests that the correct widget is picked up, namely,
        that we are correctly overriding default widgets.
        """
        context = DummyContext()
        alsoProvides(context, IDateWidgetTest)
        form_ = DateWidgetTestForm(context, self.request)
        form_.update()
        self.assertTrue(IDateWidget.providedBy(form_.widgets['start']))
        self.assertTrue(IDateWidget.providedBy(form_.widgets['end']))


class IDateTimeWidgetTest(Interface):

    start = Datetime(
        title=u"Start",
        default=datetime.datetime(2013, 4, 4, 8, 13)
    )
    end = Datetime(title=u"End")


class DateTimeWidgetTestForm(form.Form):

    fields = field.Fields(IDateTimeWidgetTest)


class DxDateTimeWidgetTest(DxBaseWidgetTest):
    """Tests dexterity datetime widget
    """

    def testDisplay(self):
        """Tests that the widgets displays correctly
        """
        widget = DateTimeWidget(self.request)
        widget.id = 'id'
        widget.name = 'name'
        self.assertRegexpMatches(
            widget.render(),
            (r'<input name="name" type="text" value="" '
                    r'class="pat-datetime" '
                    r'data-datetime-ampm="false" '
                    r'data-datetime-formatSubmit="yyyy-mm-dd HH:MM" '
                    r'data-datetime-format="[^"]+"/>')
        )
        widget.value = '2013-04-04 08:13'
        self.assertRegexpMatches(
            widget.render(),
            (r'<input name="name" type="text" value="2013-04-04 08:13" '
                    r'class="pat-datetime" '
                    r'data-datetime-ampm="false" '
                    r'data-datetime-formatSubmit="yyyy-mm-dd HH:MM" '
                    r'data-datetime-format="[^"]+"/>')
        )

    def testConverter(self):
        """Tests that the data converter works as expected
        """
        context = DummyContext()
        alsoProvides(context, IDateTimeWidgetTest)
        form_ = DateTimeWidgetTestForm(context, self.request)
        form_.update()
        for field_name in ['start', 'end']:
            converter = getMultiAdapter(
                (form_.widgets[field_name].field, form_.widgets[field_name]),
                IDataConverter
            )
            self.assertEqual(
                converter.toWidgetValue(datetime.datetime(2013, 4, 4, 8, 13)),
                '2013-04-04 08:13'
            )
            self.assertEqual(
                converter.toFieldValue('2013-04-04 08:13'),
                datetime.datetime(2013, 4, 4, 8, 13)
            )

    def testForm(self):
        """Tests that the correct widget is picked up, namely,
        that we are correctly overriding default widgets.
        """
        context = DummyContext()
        alsoProvides(context, IDateTimeWidgetTest)
        form_ = DateTimeWidgetTestForm(context, self.request)
        form_.update()
        self.assertTrue(IDateTimeWidget.providedBy(form_.widgets['start']))
        self.assertTrue(IDateTimeWidget.providedBy(form_.widgets['end']))
