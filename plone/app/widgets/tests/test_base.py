# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover


class BaseWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.base.BaseWidget."""

    def test_defaults(self):
        from plone.app.widgets.base import BaseWidget

        widget = BaseWidget('input', 'example1')
        self.assertEqual(
            widget.render(),
            '<input class="pat-example1"/>')

        self.assertEqual(widget.klass, 'pat-example1')

    def test_different_element_tag(self):
        from plone.app.widgets.base import BaseWidget

        widget = BaseWidget('select', 'example1')
        self.assertEqual(
            widget.render(),
            '<select class="pat-example1"/>')

        self.assertEqual(widget.klass, 'pat-example1')

    def test_setting_patterns_options(self):
        from plone.app.widgets.base import BaseWidget

        widget = BaseWidget(
            'input',
            'example1',
            pattern_options={
                'option1': 'value1',
                'option2': 'value2',
            })

        self.assertEqual(
            widget.render(),
            '<input class="pat-example1" data-pat-example1="{'
            '&quot;option2&quot;: &quot;value2&quot;, '
            '&quot;option1&quot;: &quot;value1&quot;}"/>')


class InputWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.base.InputWidget."""

    def test_defaults(self):
        from plone.app.widgets.base import InputWidget

        widget = InputWidget('example1', name='example2')

        self.assertEqual(
            widget.render(),
            '<input class="pat-example1" type="text" name="example2"/>')

        self.assertEqual(widget.type, 'text')
        self.assertEqual(widget.value, None)

    def test_set_type_and_value(self):
        from plone.app.widgets.base import InputWidget

        widget = InputWidget(
            'example1',
            name='example2',
            type='email',
            value='example3'
        )

        self.assertEqual(
            widget.render(),
            '<input class="pat-example1" type="email" '
            'name="example2" value="example3"/>')

        self.assertEqual(widget.type, 'email')
        self.assertEqual(widget.value, 'example3')

        widget.type = 'text'
        widget.value = 'example4'
        self.assertEqual(
            widget.render(),
            '<input class="pat-example1" type="text" '
            'name="example2" value="example4"/>')

        self.assertEqual(widget.type, 'text')
        self.assertEqual(widget.value, 'example4')

        del widget.type
        del widget.value
        self.assertEqual(
            widget.render(),
            '<input class="pat-example1" name="example2"/>')

        self.assertEqual(widget.type, None)
        self.assertEqual(widget.value, None)


class SelectWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.base.SelectWidget."""

    def test_defaults(self):
        from plone.app.widgets.base import SelectWidget

        widget = SelectWidget('example1', name='example2')

        self.assertEqual(
            widget.render(),
            '<select class="pat-example1" name="example2"></select>')
        self.assertEqual(list(widget.items), [])
        self.assertEqual(widget.value, [])

    def test_set_items_and_value(self):
        from plone.app.widgets.base import SelectWidget

        items = [
            ('token1', 'value1'),
            ('token2', 'value2'),
            ('token3', 'value3'),
        ]
        widget = SelectWidget(
            'example1',
            name='example2',
            value='token2',
            items=items
        )

        self.assertEqual(
            widget.render(),
            '<select class="pat-example1" name="example2">'
            '<option value="token1">value1</option>'
            '<option value="token2" selected="selected">value2</option>'
            '<option value="token3">value3</option>'
            '</select>')

        self.assertEqual(list(widget.items), items)
        self.assertEqual(widget.value, ['token2'])

        widget.value = 'token1'
        self.assertEqual(
            widget.render(),
            '<select class="pat-example1" name="example2">'
            '<option value="token1" selected="selected">value1</option>'
            '<option value="token2">value2</option>'
            '<option value="token3">value3</option>'
            '</select>')

        self.assertEqual(list(widget.items), items)
        self.assertEqual(widget.value, ['token1'])

        del widget.value
        self.assertEqual(
            widget.render(),
            '<select class="pat-example1" name="example2">'
            '<option value="token1">value1</option>'
            '<option value="token2">value2</option>'
            '<option value="token3">value3</option>'
            '</select>')

        del widget.items
        self.assertEqual(
            widget.render(),
            '<select class="pat-example1" name="example2"></select>')

    def test_multiple(self):
        from plone.app.widgets.base import SelectWidget

        items = [
            ('token1', 'value1'),
            ('token2', 'value2'),
            ('token3', 'value3'),
        ]
        widget = SelectWidget(
            'example1',
            name='example2',
            value=['token2'],
            items=items,
            multiple=True,
        )

        self.assertEqual(
            widget.render(),
            '<select class="pat-example1" multiple="multiple" name="example2">'
            '<option value="token1">value1</option>'
            '<option value="token2" selected="selected">value2</option>'
            '<option value="token3">value3</option>'
            '</select>')

        self.assertEqual(list(widget.items), items)
        self.assertEqual(widget.value, ['token2'])

        widget.value = ['token1', 'token2']
        self.assertEqual(
            widget.render(),
            '<select class="pat-example1" multiple="multiple" name="example2">'
            '<option value="token1" selected="selected">value1</option>'
            '<option value="token2" selected="selected">value2</option>'
            '<option value="token3">value3</option>'
            '</select>')

        self.assertEqual(list(widget.items), items)
        self.assertEqual(widget.value, ['token1', 'token2'])

        del widget.value
        self.assertEqual(
            widget.render(),
            '<select class="pat-example1" multiple="multiple" name="example2">'
            '<option value="token1">value1</option>'
            '<option value="token2">value2</option>'
            '<option value="token3">value3</option>'
            '</select>')

        del widget.items
        self.assertEqual(
            widget.render(),
            '<select class="pat-example1" multiple="multiple" '
            'name="example2"></select>')


class TextareaWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.base.TextareaWidget."""

    def test_defaults(self):
        from plone.app.widgets.base import TextareaWidget

        widget = TextareaWidget('example1', name="example2")
        self.assertEqual(
            widget.render(),
            '<textarea class="pat-example1" name="example2"></textarea>')

        self.assertEqual(widget.name, 'example2')
        self.assertEqual(widget.klass, 'pat-example1')
        self.assertEqual(widget.value, '')

    def test_setting_patterns_options(self):
        from plone.app.widgets.base import TextareaWidget

        widget = TextareaWidget(
            'example1',
            name='expample2',
            pattern_options={
                'option1': 'value1',
                'option2': 'value2',
            })

        self.assertEqual(
            widget.render(),
            '<textarea class="pat-example1" name="expample2" '
            'data-pat-example1="{'
            '&quot;option2&quot;: &quot;value2&quot;, '
            '&quot;option1&quot;: &quot;value1&quot;}">'
            '</textarea>')

    def test_set_value(self):
        from plone.app.widgets.base import TextareaWidget

        widget = TextareaWidget('example1', name="example2", value='example3')
        self.assertEqual(
            widget.render(),
            '<textarea class="pat-example1" name="example2">'
            'example3'
            '</textarea>')

        self.assertEqual(widget.value, 'example3')

        widget.value = 'example4'
        self.assertEqual(
            widget.render(),
            '<textarea class="pat-example1" name="example2">'
            'example4'
            '</textarea>')

        del widget.value
        self.assertEqual(
            widget.render(),
            '<textarea class="pat-example1" name="example2"></textarea>')

    def test_can_not_change_element_tag(self):
        from plone.app.widgets.base import TextareaWidget
        self.assertRaises(
            TypeError,
            TextareaWidget, 'example1', el='input', name='example2')


class DivWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.base.DivWidget."""

    def test_defaults(self):
        from plone.app.widgets.base import DivWidget

        widget = DivWidget('upload')
        self.assertEqual(
            widget.render(),
            '<div class="pat-upload"/>')

        self.assertEqual(widget.klass, 'pat-upload')

    def test_setting_patterns_options(self):
        from plone.app.widgets.base import DivWidget

        widget = DivWidget(
            'upload',
            pattern_options={
                'option1': 'value1',
                'option2': 'value2',
            })

        self.assertEqual(
            widget.render(),
            '<div class="pat-upload" '
            'data-pat-upload="{'
            '&quot;option2&quot;: &quot;value2&quot;, '
            '&quot;option1&quot;: &quot;value1&quot;}"/>')
