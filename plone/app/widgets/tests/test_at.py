# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

import mock
from DateTime import DateTime
from datetime import datetime
from plone.app.widgets.testing import TestRequest


class DateWidgetTests(unittest.TestCase):

    def createWidget(self, lang='en', **kw):
        from plone.app.widgets.at import DateWidget
        widget = DateWidget(**kw)
        widget.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': lang})
        return widget

    def test_subclass(self):
        from plone.app.widgets.at import DateWidget
        from plone.app.widgets.base import DateWidget as BaseDateWidget
        from Products.Archetypes.Widget import TypesWidget
        self.assertTrue(DateWidget, TypesWidget)
        self.assertTrue(DateWidget._widget, BaseDateWidget)

    def test__properties(self):
        widget = self.createWidget()
        self.assertEqual(
            widget._properties, {
                'blurrable': False,
                'condition': '',
                'description': '',
                'helper_css': (),
                'helper_js': (),
                'label': '',
                'macro': 'patterns_widget',
                'modes': ('view', 'edit'),
                'populate': True,
                'postback': True,
                'show_content_type': False,
                'visible': {'edit': 'visible', 'view': 'visible'},
                'pattern': 'pickadate',
            }
        )

    def test__call_(self):
        widget = self.createWidget()
        mode = mock.Mock()
        ins = mock.MagicMock()
        request = mock.Mock()
        ins.REQUEST = request
        widget(mode, ins)

    def test_process_form_value_is_empty(self):
        widget = self.createWidget()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {}
        self.assertFalse(widget.process_form(ins, field, form))

    def test_process_form_with_invalid_date_returns_emptymarker(self):
        widget = self.createWidget()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field_date': 'something',
        }
        self.assertEqual(
            widget.process_form(ins, field, form), None
        )

    def test_process_form_with_valid_date_without_time(self):
        widget = self.createWidget()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field_date': '2011-11-22',
        }
        self.assertEqual(
            widget.process_form(ins, field, form)[0].asdatetime(),
            datetime(2011, 11, 22, 0, 0)
        )

    def test_process_form_with_oldyear(self):
        widget = self.createWidget()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field_date': '99-11-22',
        }
        R = DateTime(datetime(99, 11, 22))
        self.assertEqual(
            widget.process_form(ins, field, form),
            (R, {})
        )


class DatetimeWidgetTests(unittest.TestCase):

    def createWidget(self, lang='en', **kw):
        from plone.app.widgets.at import DatetimeWidget
        widget = DatetimeWidget(**kw)
        widget.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': lang})
        return widget

    def test__properties(self):
        widget = self.createWidget()
        self.assertEqual(
            widget._properties,
            {
                'blurrable': False,
                'condition': '',
                'description': '',
                'helper_css': (),
                'helper_js': (),
                'label': '',
                'macro': 'patterns_widget',
                'modes': ('view', 'edit'),
                'populate': True,
                'postback': True,
                'show_content_type': False,
                'visible': {'edit': 'visible', 'view': 'visible'},
                'pattern': 'pickadate',
            }
        )

    def test_process_form_with_valid_datetime(self):
        widget = self.createWidget()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field_date': '2011-11-22',
            'field_time': '13:30',
        }
        self.assertEqual(
            widget.process_form(ins, field, form)[0].asdatetime(),
            (datetime(2011, 11, 22, 13, 30))
        )

    def test_process_form_with_oldyear(self):
        widget = self.createWidget()
        ins = mock.Mock()
        field = mock.Mock()
        field.getName.return_value = 'field'
        form = {
            'field_date': '99-11-22',
            'field_time': '12:30',
        }
        self.assertEqual(
            widget.process_form(ins, field, form)[0].asdatetime(),
            (datetime(99, 11, 22, 12, 30))
        )


class Select2WidgetTests(unittest.TestCase):

    def createWidget(self, lang='en', **kw):
        from plone.app.widgets.at import Select2Widget
        widget = Select2Widget(**kw)
        widget.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': lang})
        return widget

    def test__properties(self):
        widget = self.createWidget()
        self.assertEqual(
            widget._properties,
            {
                'ajax_vocabulary': None,
                'blurrable': False,
                'condition': '',
                'description': '',
                'helper_css': (),
                'helper_js': (),
                'label': '',
                'macro': 'patterns_widget',
                'modes': ('view', 'edit'),
                'orderable': False,
                'populate': True,
                'postback': True,
                'separator': ';',
                'show_content_type': False,
                'visible': {'edit': 'visible', 'view': 'visible'},
                'pattern': 'select2',
            }
        )
