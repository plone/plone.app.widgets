# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

from datetime import date
from datetime import datetime
from zope.schema import Date
from zope.schema import Datetime
from zope.schema import List
from zope.schema import TextLine
from zope.schema import Tuple
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import provideUtility
from plone.testing.zca import UNIT_TESTING
from plone.app.widgets.testing import ExampleVocabulary
from plone.app.widgets.testing import TestRequest


class InputWidgetTests(unittest.TestCase):

    def test_pattern_must_be_set(self):
        from plone.app.widgets.dx import InputWidget
        from plone.app.widgets.dx import NotImplemented

        request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        widget = InputWidget(request)

        self.assertRaises(
            NotImplemented,
            widget._base_args)

        widget.pattern = 'example1'
        self.assertEqual(
            widget._base_args(),
            {
                'name': None,
                'pattern': 'example1',
                'pattern_options': {},
                'value': None,
            },
        )

    def test_value_from_field(self):
        from plone.app.widgets.dx import InputWidget

        request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        widget = InputWidget(request)
        widget.name = 'example2'
        widget.pattern = 'example1'
        widget.value = 'value2'
        self.assertEqual(
            widget._base_args(),
            {
                'name': 'example2',
                'pattern': 'example1',
                'pattern_options': {},
                'value': 'value2',
            },
        )

    def test_value_from_request(self):
        from plone.app.widgets.dx import InputWidget

        request = TestRequest(
            environ={'HTTP_ACCEPT_LANGUAGE': 'en',
                     'example2': 'value1'
                     })
        widget = InputWidget(request)
        widget.name = 'example2'
        widget.pattern = 'example1'
        widget.value = 'value2'
        self.assertEqual(
            widget._base_args(),
            {
                'name': 'example2',
                'pattern': 'example1',
                'pattern_options': {},
                'value': 'value1',
            },
        )

    def test_pattern_options(self):
        from plone.app.widgets.dx import InputWidget

        request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        widget = InputWidget(request)
        widget.pattern = 'example1'
        widget.pattern_options = {'option1': 'value1',
                                  'option2': 'value2',
                                  }
        self.assertEqual(
            widget._base_args(),
            {
                'name': None,
                'pattern': 'example1',
                'pattern_options': {'option1': 'value1',
                                    'option2': 'value2',
                                    },
                'value': 'value1',
            },
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
                'name': None,
                'pattern': 'pickadate',
                'pattern_options': {'date': {'value': None}, 'time': False},
                'request': self.request
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


class DatetimeWidgetTests(unittest.TestCase):

    def setUp(self):
        from plone.app.widgets.dx import DatetimeWidget

        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.field = Datetime(__name__='datetimefield')
        self.widget = DatetimeWidget(self.request)

    def test_widget(self):
        self.assertEqual(
            self.widget._widget_args(),
            {
                'name': None,
                'pattern': 'pickadate',
                'pattern_options': {
                    'date': {'value': u''}, 'time': {'value': '00:00'}},
                'request': self.request
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


class Select2WidgetTests(unittest.TestCase):

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
                    'ajaxvocabulary': '/@@getVocabulary?name=example',
                    'initvaluemap': {},
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
                    'ajaxvocabulary': '/@@getVocabulary?name=example',
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
