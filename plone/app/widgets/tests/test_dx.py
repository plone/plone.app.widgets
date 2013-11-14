# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime
from mock import Mock
from plone.app.widgets.testing import ExampleVocabulary
from plone.app.widgets.testing import TestRequest
from plone.testing.zca import UNIT_TESTING
from zope.component import provideUtility
from zope.schema import Date
from zope.schema import Datetime
from zope.schema import List
from zope.schema import Choice
from zope.schema import TextLine
from zope.schema import Tuple

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover


class BaseWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.field = TextLine(__name__='textlinefield')

    def test_widget_pattern_notimplemented(self):
        from plone.app.widgets.dx import BaseWidget
        from plone.app.widgets.utils import NotImplemented

        widget = BaseWidget(self.request)
        widget.field = self.field

        self.assertRaises(
            NotImplemented,
            widget._base_args)

        widget.pattern = 'example'

        self.assertEqual(
            {
                'pattern': 'example',
                'pattern_options': {}
            },
            widget._base_args())

    def test_widget_base_notimplemented(self):
        from plone.app.widgets.dx import BaseWidget
        from plone.app.widgets.base import InputWidget
        from plone.app.widgets.utils import NotImplemented

        widget = BaseWidget(self.request)
        widget.field = self.field
        widget.pattern = 'example'

        self.assertRaises(
            NotImplemented,
            widget.render)

        widget._base = InputWidget

        self.assertEqual(
            '<input class="pat-example" type="text"/>',
            widget.render())


class DateWidgetTests(unittest.TestCase):

    def setUp(self):
        from plone.app.widgets.dx import DateWidget
        self.maxDiff = None

        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.field = Date(__name__='datefield')
        self.widget = DateWidget(self.request)
        self.widget.field = self.field
        self.widget.pattern_options = {'date': {'firstDay': 0}}

    def test_widget(self):
        self.assertEqual(
            {
                'pattern': 'pickadate',
                'value': u'',
                'name': None,
                'pattern_options': {
                    'date': {
                        'firstDay': 0,
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
            self.widget._base_args(),
        )

    def test_data_converter(self):
        from plone.app.widgets.dx import DateWidgetConverter
        converter = DateWidgetConverter(self.field, self.widget)

        self.assertEqual(
            converter.field.missing_value,
            converter.toFieldValue(''),
        )

        self.assertEqual(
            date(2000, 10, 30),
            converter.toFieldValue('2000-10-30'),
        )

        self.assertEqual(
            date(21, 10, 30),
            converter.toFieldValue('21-10-30'),
        )

        self.assertEqual(
            '',
            converter.toWidgetValue(converter.field.missing_value),
        )

        self.assertEqual(
            '2000-10-30',
            converter.toWidgetValue(date(2000, 10, 30)),
        )

        self.assertEqual(
            '21-10-30',
            converter.toWidgetValue(date(21, 10, 30)),
        )


class DatetimeWidgetTests(unittest.TestCase):

    def setUp(self):
        from plone.app.widgets.dx import DatetimeWidget
        self.maxDiff = None

        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.field = Datetime(__name__='datetimefield')
        self.widget = DatetimeWidget(self.request)
        self.widget.pattern_options = {'date': {'firstDay': 0}}

    def test_widget(self):
        self.assertEqual(
            {
                'pattern': 'pickadate',
                'value': u'',
                'name': None,
                'pattern_options': {
                    'date': {
                        'firstDay': 0,
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
            self.widget._base_args(),
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

    def test_data_converter_timezone(self):
        from plone.app.widgets.dx import DatetimeWidgetConverter
        context = Mock()

        # Test for previously set datetime, without tzinfo and no timezone on
        # context.
        # Should not apply a timezone to the field value.
        dt = datetime(2013, 11, 13, 10, 20)
        setattr(context, self.field.getName(), dt)
        self.widget.context = context
        converter = DatetimeWidgetConverter(self.field, self.widget)
        self.assertEqual(
            converter.toFieldValue('2013-11-13 10:20'),
            datetime(2013, 11, 13, 10, 20),
        )

        # Test for previously set datetime, with tzinfo but no timezone on
        # context.
        # Should apply UTZ zone to field value, to be able to be compared with
        # the timezone aware datetime from the context.
        import pytz
        nl = pytz.timezone('Europe/Amsterdam')
        dt = nl.localize(datetime(2013, 11, 13, 10, 20))
        setattr(context, self.field.getName(), dt)
        context.timezone = None
        self.widget.context = context
        converter = DatetimeWidgetConverter(self.field, self.widget)
        self.assertEqual(
            converter.toFieldValue('2013-11-13 10:20'),
            pytz.utc.localize(datetime(2013, 11, 13, 10, 20)),
        )

        # Test for previously set datetime, with tzinfo and timezone one
        # context.
        # Should apply the zone based on "timezone" value to field value, to be
        # able to be CORRECTLY compared with the timezone aware datetime from
        # the context.
        nl = pytz.timezone('Europe/Amsterdam')
        dt = nl.localize(datetime(2013, 11, 13, 10, 20))
        setattr(context, self.field.getName(), dt)
        context.timezone = "Europe/Amsterdam"
        self.widget.context = context
        converter = DatetimeWidgetConverter(self.field, self.widget)
        self.assertEqual(
            converter.toFieldValue('2013-11-13 10:20'),
            nl.localize(datetime(2013, 11, 13, 10, 20)),
        )

        # cleanup
        self.widget.context = None


class SelectWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})

    def test_widget(self):
        from plone.app.widgets.dx import SelectWidget
        widget = SelectWidget(self.request)
        widget.field = Choice(
            __name__='selectfield',
            values=['one', 'two', 'three']
        )
        widget.terms = widget.field.vocabulary
        self.assertEqual(
            {
                'multiple': False,
                'name': None,
                'pattern_options': {},
                'pattern': 'select2',
                'value': (),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(),
        )

        widget.multiple = True
        self.assertEqual(
            {
                'multiple': True,
                'name': None,
                'pattern_options': {},
                'pattern': 'select2',
                'value': (),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(),
        )

        widget.value = 'one'
        self.assertEqual(
            {
                'multiple': True,
                'name': None,
                'pattern_options': {},
                'pattern': 'select2',
                'value': ('one'),
                'items': [
                    ('one', 'one'),
                    ('two', 'two'),
                    ('three', 'three')
                ]
            },
            widget._base_args(),
        )


class AjaxSelectWidgetTests(unittest.TestCase):

    layer = UNIT_TESTING

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        provideUtility(ExampleVocabulary(), name=u'example')

    def test_widget(self):
        from plone.app.widgets.dx import AjaxSelectWidget
        widget = AjaxSelectWidget(self.request)
        self.assertEqual(
            {
                'name': None,
                'value': None,
                'pattern': 'select2',
                'pattern_options': {'separator': ';'},
            },
            widget._base_args()
        )

        widget.vocabulary = 'example'
        self.assertEqual(
            widget._base_args(),
            {
                'name': None,
                'value': None,
                'pattern': 'select2',
                'pattern_options': {
                    'vocabularyUrl': '/@@getVocabulary?name=example',
                    'separator': ';'
                },
            }
        )

        widget.value = 'three;two'
        self.assertEqual(
            widget._base_args(),
            {
                'name': None,
                'value': 'three;two',
                'pattern': 'select2',
                'pattern_options': {
                    'vocabularyUrl': '/@@getVocabulary?name=example',
                    'initialValues': {'three': u'Three', 'two': u'Two'},
                    'separator': ';'
                },
            }
        )

    def test_data_converter_list(self):
        from plone.app.widgets.dx import AjaxSelectWidget
        from plone.app.widgets.dx import AjaxSelectWidgetConverter

        field = List(__name__='listfield', value_type=TextLine())
        widget = AjaxSelectWidget(self.request)
        widget.field = field
        converter = AjaxSelectWidgetConverter(field, widget)

        self.assertEqual(
            converter.toFieldValue(''),
            field.missing_value,
        )

        self.assertEqual(
            converter.toFieldValue('123;456;789'),
            ['123', '456', '789'],
        )

        self.assertEqual(
            converter.toWidgetValue([]),
            None,
        )

        self.assertEqual(
            converter.toWidgetValue(['123', '456', '789']),
            '123;456;789',
        )

    def test_data_converter_tuple(self):
        from plone.app.widgets.dx import AjaxSelectWidget
        from plone.app.widgets.dx import AjaxSelectWidgetConverter

        field = Tuple(__name__='tuplefield', value_type=TextLine())
        widget = AjaxSelectWidget(self.request)
        widget.field = field
        converter = AjaxSelectWidgetConverter(field, widget)

        self.assertEqual(
            converter.toFieldValue(''),
            field.missing_value,
        )

        self.assertEqual(
            converter.toFieldValue('123;456;789'),
            ('123', '456', '789'),
        )

        self.assertEqual(
            converter.toWidgetValue(tuple()),
            None,
        )

        self.assertEqual(
            converter.toWidgetValue(('123', '456', '789')),
            '123;456;789',
        )


class QueryStringWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})

    def test_widget(self):
        from plone.app.widgets.dx import QueryStringWidget
        widget = QueryStringWidget(self.request)
        self.assertEqual(
            {
                'name': None,
                'value': None,
                'pattern': 'querystring',
                'pattern_options': {
                    'indexOptionsUrl': '/@@qsOptions',
                    'previewCountURL': '/@@querybuildernumberofresults',
                    'previewURL': '/@@querybuilder_html_results',
                },
            },
            widget._base_args()
        )


class RelatedItemsWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})

    def test_widget(self):
        from plone.app.widgets.dx import RelatedItemsWidget
        context = Mock()
        context.portal_properties.site_properties\
            .getProperty.return_value = ['SomeType']
        widget = RelatedItemsWidget(self.request)
        widget.context = context
        self.assertEqual(
            {
                'name': None,
                'value': None,
                'pattern': 'relateditems',
                'pattern_options': {
                    'folderTypes': ['SomeType'],
                    'separator': ';',
                    'vocabularyUrl': '/@@getVocabulary?name='
                                     'plone.app.vocabularies.Catalog',
                },
            },
            widget._base_args()
        )
