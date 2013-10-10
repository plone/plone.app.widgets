# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from plone.app.widgets.testing import ExampleVocabulary
from plone.app.widgets.testing import TestRequest
from plone.testing.zca import UNIT_TESTING
from zope.component import provideUtility
from zope.schema import Date
from zope.schema import Datetime
from zope.schema import List
from zope.schema import TextLine
from zope.schema import Tuple

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover


class DatetimeWidgetTests(unittest.TestCase):

    def setUp(self):
        from plone.app.widgets.dx import DatetimeWidget

        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.field = Datetime(__name__='datetimefield')
        self.widget = DatetimeWidget(self.request)

    def test_widget(self):
        self.assertEqual(
            self.widget._base_args(),
            {
                'pattern': 'pickadate',
                'value': u'',
                'name': None,
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
            }
        )

    def test_data_converter(self):
        from plone.app.widgets.dx import DatetimeWidgetConverter
        converter = DatetimeWidgetConverter(self.field, self.widget)

        self.assertEqual(
            converter.toFieldValue(''),
            converter.field.missing_value,
        )

        self.assertEqual(
            converter.toFieldValue('2000-10-30 15:40'),
            datetime(2000, 10, 30, 15, 40),
        )

        self.assertEqual(
            converter.toFieldValue('21-10-30 15:40'),
            datetime(21, 10, 30, 15, 40),
        )

        self.assertEqual(
            converter.toWidgetValue(converter.field.missing_value),
            '',
        )

        self.assertEqual(
            converter.toWidgetValue(datetime(2000, 10, 30, 15, 40)),
            '2000-10-30 15:40',
        )

        self.assertEqual(
            converter.toWidgetValue(datetime(21, 10, 30, 15, 40)),
            '21-10-30 15:40',
        )


class DateWidgetTests(unittest.TestCase):

    def setUp(self):
        from plone.app.widgets.dx import DateWidget

        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.field = Date(__name__='datefield')
        self.widget = DateWidget(self.request)
        self.widget.field = self.field

    def test_widget(self):
        self.assertEqual(
            self.widget._widget_args(),
            {
                'pattern': 'pickadate',
                'value': u' 00:00',
                'name': None,
                'pattern_options': {
                    'placeholderTime': u'Enter time...',
                    'min': [1913, 1, 1],
                    'monthsFull': [u'January', u'February', u'March', u'April',
                                   u'May', u'June', u'July', u'August',
                                   u'September', u'October', u'November',
                                   u'December'],
                    'max': [2033, 1, 1],
                    'clear': u'Clear',
                    'time': False,
                    'weekdaysShort': [u'Sun', u'Mon', u'Tue', u'Wed', u'Thu',
                                      u'Fri', u'Sat'],
                    'weekdaysFull': [u'Sunday', u'Monday', u'Tuesday',
                                     u'Wednesday', u'Thursday', u'Friday',
                                     u'Saturday'],
                    'monthsShort': [u'Jan', u'Feb', u'Mar', u'Apr', u'May',
                                    u'Jun', u'Jul', u'Aug', u'Sep', u'Oct',
                                    u'Nov', u'Dec'],
                    'selectYears': 200,
                    'format_date': 'mmmm d, yyyy',
                    'placeholderDate': u'Enter date...',
                    'today': u'Today',
                }
            }
        )

    def test_data_converter(self):
        from plone.app.widgets.dx import DateWidgetConverter
        converter = DateWidgetConverter(self.field, self.widget)

        self.assertEqual(
            converter.toFieldValue(''),
            converter.field.missing_value,
        )

        self.assertEqual(
            converter.toFieldValue('2000-10-30'),
            date(2000, 10, 30),
        )

        self.assertEqual(
            converter.toFieldValue('21-10-30'),
            date(21, 10, 30),
        )

        self.assertEqual(
            converter.toWidgetValue(converter.field.missing_value),
            '',
        )

        self.assertEqual(
            converter.toWidgetValue(date(2000, 10, 30)),
            '2000-10-30',
        )

        self.assertEqual(
            converter.toWidgetValue(date(21, 10, 30)),
            '21-10-30',
        )


class SelectWidgetTests(unittest.TestCase):

    layer = UNIT_TESTING

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        provideUtility(ExampleVocabulary(), name=u'example')

    def test_widget(self):
        from plone.app.widgets.dx import Select2Widget
        widget = Select2Widget(self.request)
        self.assertEqual(
            widget._widget_args(),
            {
                'name': None,
                'value': None,
                'pattern': 'select2',
                'pattern_options': {'separator': ';'},
            }
        )

        widget.ajax_vocabulary = 'example'
        self.assertEqual(
            widget._widget_args(),
            {
                'name': None,
                'value': None,
                'pattern': 'select2',
                'pattern_options': {
                    'ajaxVocabulary': '/@@getVocabulary?name=example',
                    'separator': ';'
                },
            }
        )

        widget.value = 'three;two'
        self.assertEqual(
            widget._widget_args(),
            {
                'name': None,
                'value': 'three;two',
                'pattern': 'select2',
                'pattern_options': {
                    'ajaxVocabulary': '/@@getVocabulary?name=example',
                    'initvaluemap': {'three': u'Three', 'two': u'Two'},
                    'separator': ';'
                },
            }
        )

    def test_data_converter(self):
        from plone.app.widgets.dx import Select2Widget
        from plone.app.widgets.dx import Select2WidgetConverter

        field1 = List(__name__='listfield', value_type=TextLine())
        widget1 = Select2Widget(self.request)
        widget1.field = field1
        converter1 = Select2WidgetConverter(field1, widget1)

        self.assertEqual(
            converter1.toFieldValue(''),
            field1.missing_value,
        )

        self.assertEqual(
            converter1.toFieldValue('123;456;789'),
            ['123', '456', '789'],
        )

        self.assertEqual(
            converter1.toWidgetValue([]),
            '',
        )

        self.assertEqual(
            converter1.toWidgetValue(['123', '456', '789']),
            '123;456;789',
        )

        field2 = Tuple(__name__='tuplefield', value_type=TextLine())
        widget2 = Select2Widget(self.request)
        widget2.field = field2
        converter2 = Select2WidgetConverter(field2, widget2)

        self.assertEqual(
            converter2.toFieldValue(''),
            field2.missing_value,
        )

        self.assertEqual(
            converter2.toFieldValue('123;456;789'),
            ('123', '456', '789'),
        )

        self.assertEqual(
            converter2.toWidgetValue(tuple()),
            '',
        )

        self.assertEqual(
            converter2.toWidgetValue(('123', '456', '789')),
            '123;456;789',
        )


class AjaxSelectWidgetTests(unittest.TestCase):

    layer = UNIT_TESTING


class QueryStringWidgetTests(unittest.TestCase):

    layer = UNIT_TESTING


class RelatedItemsWidgetTests(unittest.TestCase):

    layer = UNIT_TESTING
