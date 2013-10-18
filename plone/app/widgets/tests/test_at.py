# -*- coding: utf-8 -*-

from datetime import datetime
from plone.app.widgets.testing import TestRequest

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

import mock


class BaseWidgetTests(unittest.TestCase):

    def test_widget_pattern_notimplemented(self):
        from plone.app.widgets.at import BaseWidget
        from plone.app.widgets.utils import NotImplemented

        widget = BaseWidget()

        with self.assertRaises(NotImplemented):
            widget._base_args(None, None, None)

        widget.pattern = 'example'

        self.assertEqual(
            {
                'pattern': 'example',
                'pattern_options': {}
            },
            widget._base_args(None, None, None))

    def test_widget_base_notimplemented(self):
        from plone.app.widgets.at import BaseWidget
        from plone.app.widgets.base import InputWidget
        from plone.app.widgets.utils import NotImplemented

        widget = BaseWidget(pattern='example')

        with self.assertRaises(NotImplemented):
            widget.edit(None, None, None)

        widget._base = InputWidget

        self.assertEqual(
            '<input class="pat-example" type="text"/>',
            widget.edit(None, None, None))


class DateWidgetTests(unittest.TestCase):

    def setUp(self):
        from plone.app.widgets.at import DateWidget
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.context = mock.Mock()
        self.field = mock.Mock()
        self.field.getAccessor.return_value = lambda: u''
        self.field.getName.return_value = 'fieldname'
        self.widget = DateWidget()

    def test_widget(self):
        self.assertEqual(
            {
                'pattern': 'pickadate',
                'value': u'',
                'name': 'fieldname',
                'pattern_options': {
                    'date': {
                        'min': [1913, 1, 1],
                        'max': [2033, 1, 1],
                        'clear': u'Clear',
                        'format': 'mmmm d, yyyy',
                        'monthsFull': [u'January', u'February', u'March',
                                       u'April', u'May', u'June', u'July',
                                       u'August', u'September', u'October',
                                       u'November', u'December'],
                        'weekdaysShort': [u'Sun', u'Mon', u'Tue', u'Wed',
                                          u'Thu', u'Fri', u'Sat'],
                        'weekdaysFull': [u'Sunday', u'Monday', u'Tuesday',
                                         u'Wednesday', u'Thursday', u'Friday',
                                         u'Saturday'],
                        'today': u'Today',
                        'selectYears': 200,
                        'placeholder': u'Enter date...',
                        'monthsShort': [u'Jan', u'Feb', u'Mar', u'Apr', u'May',
                                        u'Jun', u'Jul', u'Aug', u'Sep', u'Oct',
                                        u'Nov', u'Dec']
                    },
                    'time': False
                }
            },
            self.widget._base_args(self.context, self.field, self.request),
        )

    def test_process_form(self):
        form = {
            'fieldname': '2011-11-22',
        }
        self.assertEqual(
            self.widget.process_form(
                self.context, self.field, form)[0].asdatetime(),
            (datetime(2011, 11, 22))
        )


class DatetimeWidgetTests(unittest.TestCase):

    def setUp(self):
        from plone.app.widgets.at import DatetimeWidget
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.context = mock.Mock()
        self.field = mock.Mock()
        self.field.getAccessor.return_value = lambda: u''
        self.field.getName.return_value = 'fieldname'
        self.widget = DatetimeWidget()

    def test_widget(self):
        self.assertEqual(
            {
                'pattern': 'pickadate',
                'value': u'',
                'name': 'fieldname',
                'pattern_options': {
                    'date': {
                        'min': [1913, 1, 1],
                        'max': [2033, 1, 1],
                        'clear': u'Clear',
                        'format': 'mmmm d, yyyy',
                        'monthsFull': [u'January', u'February', u'March',
                                       u'April', u'May', u'June', u'July',
                                       u'August', u'September', u'October',
                                       u'November', u'December'],
                        'weekdaysShort': [u'Sun', u'Mon', u'Tue', u'Wed',
                                          u'Thu', u'Fri', u'Sat'],
                        'weekdaysFull': [u'Sunday', u'Monday', u'Tuesday',
                                         u'Wednesday', u'Thursday', u'Friday',
                                         u'Saturday'],
                        'today': u'Today',
                        'selectYears': 200,
                        'placeholder': u'Enter date...',
                        'monthsShort': [u'Jan', u'Feb', u'Mar', u'Apr', u'May',
                                        u'Jun', u'Jul', u'Aug', u'Sep', u'Oct',
                                        u'Nov', u'Dec']
                    },
                    'time': {
                        'placeholder': u'Enter time...',
                        'today': u'Today',
                        'format': 'h:i a'
                    }
                }
            },
            self.widget._base_args(self.context, self.field, self.request),
        )

    def test_process_form(self):
        form = {
            'fieldname': '2011-11-22 13:30',
        }
        self.assertEqual(
            self.widget.process_form(
                self.context, self.field, form)[0].asdatetime(),
            (datetime(2011, 11, 22, 13, 30))
        )


class SelectWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.context = mock.Mock()
        self.vocabulary = mock.Mock()
        self.vocabulary.items.return_value = [
            ('one', 'one'),
            ('two', 'two'),
            ('three', 'three'),
        ]
        self.field = mock.Mock()
        self.field.getAccessor.return_value = lambda: ()
        self.field.getName.return_value = 'fieldname'
        self.field.Vocabulary.return_value = self.vocabulary

    def test_widget(self):
        from plone.app.widgets.at import SelectWidget
        widget = SelectWidget()
        self.assertEqual(
            {
                'multiple': False,
                'name': 'fieldname',
                'pattern_options': {'separator': ';'},
                'pattern': 'select2',
                'value': (),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(self.context, self.field, self.request),
        )

        widget.multiple = True
        self.assertEqual(
            {
                'multiple': True,
                'name': 'fieldname',
                'pattern_options': {'separator': ';'},
                'pattern': 'select2',
                'value': (),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(self.context, self.field, self.request),
        )

        self.field.getAccessor.return_value = lambda: u'one'
        self.assertEqual(
            {
                'multiple': True,
                'name': 'fieldname',
                'pattern_options': {'separator': ';'},
                'pattern': 'select2',
                'value': (u'one'),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(self.context, self.field, self.request),
        )


class RelatedItemsWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.context = mock.Mock()
        self.field = mock.Mock()
        self.field.getAccessor.return_value = lambda: 'fieldvalue'
        self.field.getName.return_value = 'fieldname'

    def test_widget(self):
        from plone.app.widgets.at import RelatedItemsWidget
        widget = RelatedItemsWidget()
        self.assertEqual(
            {
                'name': 'fieldname',
                'value': 'fieldvalue',
                'pattern': 'relateditems',
                'pattern_options': {'separator': ';'},
            },
            widget._base_args(self.context, self.field, self.request),
        )


class TinyMCEWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.context = mock.Mock()
        self.field = mock.Mock()
        self.field.getAccessor.return_value = lambda: 'fieldvalue'
        self.field.getName.return_value = 'fieldname'

    def test_widget(self):
        from plone.app.widgets.at import TinyMCEWidget
        widget = TinyMCEWidget()
        self.assertEqual(
            {
                'name': 'fieldname',
                'value': 'fieldvalue',
                'pattern': 'tinymce',
                'pattern_options': {},
            },
            widget._base_args(self.context, self.field, self.request),
        )
