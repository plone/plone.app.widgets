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


class DateWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.base.DateWidget
    """

    def test_defaults(self):
        from plone.app.widgets.base import DateWidget
        widget = DateWidget()
        self.assertEqual(
            widget.render(),
            '<input class="pat-pickadate" type="date" data-pat-pickadate="{&quot;date&quot;: {&quot;formatSubmit&quot;: &quot;yyyy-mm-dd&quot;, &quot;format&quot;: &quot;mmmm d, yyyy&quot;}, &quot;time&quot;: &quot;false&quot;}"/>')  # noqa

    def test_localization(self):
        from plone.app.widgets.base import DateWidget
        request_en = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        widget_en = DateWidget(request=request_en)
        self.assertEqual(
            widget_en.render(),
            '<input class="pat-pickadate" type="date" data-pat-pickadate="{&quot;date&quot;: {&quot;format&quot;: &quot;mmmm d, yyyy&quot;, &quot;max&quot;: [2033, 1, 1], &quot;clear&quot;: &quot;Clear&quot;, &quot;min&quot;: [1913, 1, 1], &quot;monthsFull&quot;: [&quot;January&quot;, &quot;February&quot;, &quot;March&quot;, &quot;April&quot;, &quot;May&quot;, &quot;June&quot;, &quot;July&quot;, &quot;August&quot;, &quot;September&quot;, &quot;October&quot;, &quot;November&quot;, &quot;December&quot;], &quot;weekdaysShort&quot;: [&quot;Sun&quot;, &quot;Mon&quot;, &quot;Tue&quot;, &quot;Wed&quot;, &quot;Thu&quot;, &quot;Fri&quot;, &quot;Sat&quot;], &quot;weekdaysFull&quot;: [&quot;Sunday&quot;, &quot;Monday&quot;, &quot;Tuesday&quot;, &quot;Wednesday&quot;, &quot;Thursday&quot;, &quot;Friday&quot;, &quot;Saturday&quot;], &quot;today&quot;: &quot;Today&quot;, &quot;selectYears&quot;: 200, &quot;formatSubmit&quot;: &quot;yyyy-mm-dd&quot;, &quot;monthsShort&quot;: [&quot;Jan&quot;, &quot;Feb&quot;, &quot;Mar&quot;, &quot;Apr&quot;, &quot;May&quot;, &quot;Jun&quot;, &quot;Jul&quot;, &quot;Aug&quot;, &quot;Sep&quot;, &quot;Oct&quot;, &quot;Nov&quot;, &quot;Dec&quot;]}, &quot;time&quot;: &quot;false&quot;}"/>')  # noqa

        request_de = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'de'})
        widget_de = DateWidget(request=request_de)
        self.assertEqual(
            widget_de.render(),
            '<input class="pat-pickadate" type="date" data-pat-pickadate="{&quot;date&quot;: {&quot;format&quot;: &quot;mmmm d, yyyy&quot;, &quot;max&quot;: [2033, 1, 1], &quot;clear&quot;: &quot;Clear&quot;, &quot;min&quot;: [1913, 1, 1], &quot;monthsFull&quot;: [&quot;Januar&quot;, &quot;Februar&quot;, &quot;M\\u00e4rz&quot;, &quot;April&quot;, &quot;Mai&quot;, &quot;Juni&quot;, &quot;Juli&quot;, &quot;August&quot;, &quot;September&quot;, &quot;Oktober&quot;, &quot;November&quot;, &quot;Dezember&quot;], &quot;weekdaysShort&quot;: [&quot;So&quot;, &quot;Mo&quot;, &quot;Di&quot;, &quot;Mi&quot;, &quot;Do&quot;, &quot;Fr&quot;, &quot;Sa&quot;], &quot;weekdaysFull&quot;: [&quot;Sonntag&quot;, &quot;Montag&quot;, &quot;Dienstag&quot;, &quot;Mittwoch&quot;, &quot;Donnerstag&quot;, &quot;Freitag&quot;, &quot;Samstag&quot;], &quot;today&quot;: &quot;Today&quot;, &quot;selectYears&quot;: 200, &quot;formatSubmit&quot;: &quot;yyyy-mm-dd&quot;, &quot;monthsShort&quot;: [&quot;Jan&quot;, &quot;Feb&quot;, &quot;Mrz&quot;, &quot;Apr&quot;, &quot;Mai&quot;, &quot;Jun&quot;, &quot;Jul&quot;, &quot;Aug&quot;, &quot;Sep&quot;, &quot;Okt&quot;, &quot;Nov&quot;, &quot;Dez&quot;]}, &quot;time&quot;: &quot;false&quot;}"/>')  # noqa


class DatetimeWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.base.DatetimeWidget
    """

    def test_defaults(self):
        from plone.app.widgets.base import DatetimeWidget
        widget = DatetimeWidget()
        self.assertEqual(
            widget.render(),
            '<input class="pat-pickadate" type="datetime-local" data-pat-pickadate="{&quot;date&quot;: {&quot;formatSubmit&quot;: &quot;yyyy-mm-dd&quot;, &quot;format&quot;: &quot;mmmm d, yyyy&quot;}, &quot;time&quot;: {&quot;formatSubmit&quot;: &quot;HH:i&quot;, &quot;format&quot;: &quot;HH:i&quot;}}"/>')  # noqa

    def test_localization(self):
        from plone.app.widgets.base import DatetimeWidget
        request_en = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        widget_en = DatetimeWidget(request=request_en)
        self.assertEqual(
            widget_en.render(),
            '<input class="pat-pickadate" type="datetime-local" data-pat-pickadate="{&quot;date&quot;: {&quot;format&quot;: &quot;mmmm d, yyyy&quot;, &quot;max&quot;: [2033, 1, 1], &quot;clear&quot;: &quot;Clear&quot;, &quot;min&quot;: [1913, 1, 1], &quot;monthsFull&quot;: [&quot;January&quot;, &quot;February&quot;, &quot;March&quot;, &quot;April&quot;, &quot;May&quot;, &quot;June&quot;, &quot;July&quot;, &quot;August&quot;, &quot;September&quot;, &quot;October&quot;, &quot;November&quot;, &quot;December&quot;], &quot;weekdaysShort&quot;: [&quot;Sun&quot;, &quot;Mon&quot;, &quot;Tue&quot;, &quot;Wed&quot;, &quot;Thu&quot;, &quot;Fri&quot;, &quot;Sat&quot;], &quot;weekdaysFull&quot;: [&quot;Sunday&quot;, &quot;Monday&quot;, &quot;Tuesday&quot;, &quot;Wednesday&quot;, &quot;Thursday&quot;, &quot;Friday&quot;, &quot;Saturday&quot;], &quot;today&quot;: &quot;Today&quot;, &quot;selectYears&quot;: 200, &quot;formatSubmit&quot;: &quot;yyyy-mm-dd&quot;, &quot;monthsShort&quot;: [&quot;Jan&quot;, &quot;Feb&quot;, &quot;Mar&quot;, &quot;Apr&quot;, &quot;May&quot;, &quot;Jun&quot;, &quot;Jul&quot;, &quot;Aug&quot;, &quot;Sep&quot;, &quot;Oct&quot;, &quot;Nov&quot;, &quot;Dec&quot;]}, &quot;time&quot;: {&quot;formatSubmit&quot;: &quot;HH:i&quot;, &quot;format&quot;: &quot;HH:i&quot;}}"/>')  # noqa

        request_de = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'de'})
        widget_de = DatetimeWidget(request=request_de)
        self.assertEqual(
            widget_de.render(),
            '<input class="pat-pickadate" type="datetime-local" data-pat-pickadate="{&quot;date&quot;: {&quot;format&quot;: &quot;mmmm d, yyyy&quot;, &quot;max&quot;: [2033, 1, 1], &quot;clear&quot;: &quot;Clear&quot;, &quot;min&quot;: [1913, 1, 1], &quot;monthsFull&quot;: [&quot;Januar&quot;, &quot;Februar&quot;, &quot;M\\u00e4rz&quot;, &quot;April&quot;, &quot;Mai&quot;, &quot;Juni&quot;, &quot;Juli&quot;, &quot;August&quot;, &quot;September&quot;, &quot;Oktober&quot;, &quot;November&quot;, &quot;Dezember&quot;], &quot;weekdaysShort&quot;: [&quot;So&quot;, &quot;Mo&quot;, &quot;Di&quot;, &quot;Mi&quot;, &quot;Do&quot;, &quot;Fr&quot;, &quot;Sa&quot;], &quot;weekdaysFull&quot;: [&quot;Sonntag&quot;, &quot;Montag&quot;, &quot;Dienstag&quot;, &quot;Mittwoch&quot;, &quot;Donnerstag&quot;, &quot;Freitag&quot;, &quot;Samstag&quot;], &quot;today&quot;: &quot;Today&quot;, &quot;selectYears&quot;: 200, &quot;formatSubmit&quot;: &quot;yyyy-mm-dd&quot;, &quot;monthsShort&quot;: [&quot;Jan&quot;, &quot;Feb&quot;, &quot;Mrz&quot;, &quot;Apr&quot;, &quot;Mai&quot;, &quot;Jun&quot;, &quot;Jul&quot;, &quot;Aug&quot;, &quot;Sep&quot;, &quot;Okt&quot;, &quot;Nov&quot;, &quot;Dez&quot;]}, &quot;time&quot;: {&quot;formatSubmit&quot;: &quot;HH:i&quot;, &quot;format&quot;: &quot;HH:i&quot;}}"/>')  # noqa


class Select2WidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.base.Select2Widget
    """

    def test_defaults(self):
        from plone.app.widgets.base import Select2Widget

        widget = Select2Widget()
        self.assertEqual(
            widget.render(),
            '<input class="pat-select2" type="text"/>')

        self.assertEqual(widget.type, 'text')
        self.assertEqual(widget.name, None)
        self.assertEqual(widget.value, None)

    def test_set_name_and_value(self):
        from plone.app.widgets.base import Select2Widget

        widget = Select2Widget(name='example1', value='example2')
        self.assertEqual(
            widget.render(),
            '<input class="pat-select2" name="example1" type="text" '
            'value="example2"/>')

        self.assertEqual(widget.name, 'example1')
        self.assertEqual(widget.value, 'example2')

        widget.name = 'example'
        widget.value = 'example'
        self.assertEqual(
            widget.render(),
            '<input class="pat-select2" name="example" type="text" '
            'value="example"/>')

        self.assertEqual(widget.name, 'example')
        self.assertEqual(widget.value, 'example')

        del widget.name
        del widget.value
        self.assertEqual(
            widget.render(),
            '<input class="pat-select2" type="text"/>')

        self.assertEqual(widget.name, None)
        self.assertEqual(widget.value, None)

    def test_can_not_change_element_tag(self):
        from plone.app.widgets.base import Select2Widget
        self.assertRaises(
            TypeError,
            Select2Widget, el='select')
