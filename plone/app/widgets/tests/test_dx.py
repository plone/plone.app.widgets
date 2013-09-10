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
from plone.app.widgets.testing import TestRequest


class BaseWidgetTests(unittest.TestCase):

    def test_base(self):
        from plone.app.widgets.dx import BaseWidget
        request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        widget = BaseWidget(request)
        widget.name = 'example'
        self.assertEqual(
            widget._widget_args(),
            {
                'name': 'example',
                'pattern': None,
                'pattern_options': {},
            },
        )

    def test_input(self):
        from plone.app.widgets.dx import InputWidget
        request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'},
                              example='example-value')
        widget = InputWidget(request)
        widget.name = 'example'
        self.assertEqual(
            widget._widget_args(),
            {
                'name': 'example',
                'pattern': None,
                'pattern_options': {},
                'value': 'example-value',
            },
        )

    def test_select(self):
        from plone.app.widgets.dx import SelectWidget
        request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'},
                              example='example-value')
        widget = SelectWidget(request)
        widget.id = 'example'
        widget.name = 'example'
        widget.field = TextLine(__name__='selectfield')
        widget.field.vocabulary = SimpleVocabulary.fromValues(
            ['option1', 'option2', 'option3'])
        widget.terms = widget.field.vocabulary
        self.assertEqual(
            widget._widget_args(),
            {
                'name': 'example',
                'pattern': 'select2',
                'pattern_options': {},
                'options': [('--NOVALUE--', u'No value'),
                            ('option1', 'option1'),
                            ('option2', 'option2'),
                            ('option3', 'option3')],
                'selected': (),
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

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})

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
