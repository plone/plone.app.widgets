# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

from plone.app.widgets.testing import TestRequest


class BaseWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.base.BaseWidget
    """

    def test_defaults(self):
        from plone.app.widgets.base import BaseWidget

        widget = BaseWidget('example')
        self.assertEqual(
            widget.render(),
            '<input class="pat-example"/>')

        self.assertEqual(widget.name, None)
        self.assertEqual(widget.klass, 'pat-example')

    def test_different_element_tag(self):
        from plone.app.widgets.base import BaseWidget
        self.assertEqual(
            BaseWidget('example', el='select').render(),
            '<select class="pat-example"/>')

    def test_set_name_attribute(self):
        from plone.app.widgets.base import BaseWidget

        widget = BaseWidget('example', name='example')
        self.assertEqual(
            widget.render(),
            '<input class="pat-example" name="example"/>')

        self.assertEqual(widget.name, 'example')

        widget.name = 'example2'
        self.assertEqual(
            widget.render(),
            '<input class="pat-example" name="example2"/>')

        self.assertEqual(widget.name, 'example2')

        del widget.name
        self.assertEqual(
            widget.render(),
            '<input class="pat-example"/>')

        self.assertEqual(widget.name, None)

    def test_setting_patterns_options(self):
        from plone.app.widgets.base import BaseWidget

        widget = BaseWidget('example', pattern_options={
            'option1': 'value1',
            'option2': 'value2',
        })

        self.assertEqual(
            widget.render(),
            '<input class="pat-example" data-pat-example="{'
            '&quot;option2&quot;: &quot;value2&quot;, '
            '&quot;option1&quot;: &quot;value1&quot;}"/>')


class InputWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.base.InputWidget
    """

    def test_defaults(self):
        from plone.app.widgets.base import InputWidget

        widget = InputWidget('example')
        self.assertEqual(
            widget.render(),
            '<input class="pat-example" type="text"/>')

        self.assertEqual(widget.type, 'text')
        self.assertEqual(widget.value, None)

    def test_set_type_and_value(self):
        from plone.app.widgets.base import InputWidget

        widget = InputWidget('example', _type='email', value='example')
        self.assertEqual(
            widget.render(),
            '<input class="pat-example" type="email" value="example"/>')

        self.assertEqual(widget.type, 'email')
        self.assertEqual(widget.value, 'example')

        widget.type = 'text'
        widget.value = 'example2'
        self.assertEqual(
            widget.render(),
            '<input class="pat-example" type="text" value="example2"/>')

        self.assertEqual(widget.type, 'text')
        self.assertEqual(widget.value, 'example2')

        del widget.type
        del widget.value
        self.assertEqual(
            widget.render(),
            '<input class="pat-example"/>')

        self.assertEqual(widget.type, None)
        self.assertEqual(widget.value, None)

    def test_can_not_change_element_tag(self):
        from plone.app.widgets.base import InputWidget
        self.assertRaises(
            TypeError,
            InputWidget, 'example', el='select')


class SelectWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.SelectWidget
    """

    def test_defaults(self):
        from plone.app.widgets.base import SelectWidget

        widget = SelectWidget('example')

        self.assertEqual(
            widget.render(),
            '<select class="pat-example"> </select>')
        self.assertEqual(list(widget.options), [])
        self.assertEqual(widget.selected, [])

    def test_set_options_and_selected(self):
        from plone.app.widgets.base import SelectWidget

        options = [
            ('token1', 'value1'),
            ('token2', 'value2'),
            ('token3', 'value3'),
        ]
        widget = SelectWidget('example', selected='token2', options=options)

        self.assertEqual(
            widget.render(),
            '<select class="pat-example">'
            '<option value="token1">value1</option>'
            '<option value="token2" selected="selected">value2</option>'
            '<option value="token3">value3</option>'
            '</select>')

        self.assertEqual(list(widget.options), options)
        self.assertEqual(widget.selected, ['token2'])

        widget.selected = 'token1'
        self.assertEqual(
            widget.render(),
            '<select class="pat-example">'
            '<option value="token1" selected="selected">value1</option>'
            '<option value="token2">value2</option>'
            '<option value="token3">value3</option>'
            '</select>')

        self.assertEqual(list(widget.options), options)
        self.assertEqual(widget.selected, ['token1'])

        del widget.selected
        self.assertEqual(
            widget.render(),
            '<select class="pat-example">'
            '<option value="token1">value1</option>'
            '<option value="token2">value2</option>'
            '<option value="token3">value3</option>'
            '</select>')

        del widget.options
        self.assertEqual(
            widget.render(),
            '<select class="pat-example"/>')

    def test_can_not_change_element_tag(self):
        from plone.app.widgets.base import SelectWidget
        self.assertRaises(
            TypeError,
            SelectWidget, 'example', el='select')


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
