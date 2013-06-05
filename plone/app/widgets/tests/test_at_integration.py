# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView


class BaseWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.at.BaseWidget
    """

    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.example = self.portal[self.portal.invokeFactory(
            'ExampleType', id='example', title='Example')]

        class View(BrowserView):
            template = ViewPageTemplateFile('test_at_integration.pt')

            def render(self, **kw):
                return self.template(**kw)

        self.view = View(self.example, self.request)

    def tearDown(self):
        self.portal.manage_delObjects([self.example.getId()])

    def test_textinput(self):
        from plone.app.widgets.at import InputWidget
        field = self.example.getField('inputfield')
        self.assertIsInstance(field.widget, InputWidget)
        self.assertIn(
            '<input name="inputfield" type="text" value=""/>',
            self.view.render(field=field, mode='edit'))

    def test_date(self):
        from plone.app.widgets.at import DateWidget
        field = self.example.getField('datefield')
        self.assertIsInstance(field.widget, DateWidget)
        self.assertIn(
            '<input class="pat-pickadate" name="datefield" data-pat-pickadate="{&quot;pickadate-clear&quot;: &quot;Clear&quot;, &quot;pickadate-weekdaysFull&quot;: [&quot;2&quot;, &quot;3&quot;, &quot;4&quot;, &quot;5&quot;, &quot;6&quot;, &quot;7&quot;, &quot;1&quot;], &quot;format&quot;: &quot;yyyy-mm-dd @&quot;, &quot;pickadate-today&quot;: &quot;Today&quot;, &quot;pickadate-monthsShort&quot;: [&quot;1&quot;, &quot;2&quot;, &quot;3&quot;, &quot;4&quot;, &quot;5&quot;, &quot;6&quot;, &quot;7&quot;, &quot;8&quot;, &quot;9&quot;, &quot;10&quot;, &quot;11&quot;, &quot;12&quot;], &quot;formatSubmit&quot;: &quot;yyyy-mm-dd&quot;, &quot;pickadate-weekdaysShort&quot;: [&quot;2&quot;, &quot;3&quot;, &quot;4&quot;, &quot;5&quot;, &quot;6&quot;, &quot;7&quot;, &quot;1&quot;], &quot;pickadate-monthsFull&quot;: [&quot;1&quot;, &quot;2&quot;, &quot;3&quot;, &quot;4&quot;, &quot;5&quot;, &quot;6&quot;, &quot;7&quot;, &quot;8&quot;, &quot;9&quot;, &quot;10&quot;, &quot;11&quot;, &quot;12&quot;]}" type="date" value="',  # noqa
            self.view.render(field=field, mode='edit'))

    def test_datetime(self):
        from plone.app.widgets.at import DatetimeWidget
        field = self.example.getField('datetimefield')
        self.assertIsInstance(field.widget, DatetimeWidget)
        self.assertIn(
            '<input class="pat-pickadate" name="datetimefield" data-pat-pickadate="{&quot;pickadate-clear&quot;: &quot;Clear&quot;, &quot;pickadate-weekdaysFull&quot;: [&quot;2&quot;, &quot;3&quot;, &quot;4&quot;, &quot;5&quot;, &quot;6&quot;, &quot;7&quot;, &quot;1&quot;], &quot;format&quot;: &quot;yyyy-mm-dd @ HH:MM&quot;, &quot;pickadate-today&quot;: &quot;Today&quot;, &quot;pickadate-monthsShort&quot;: [&quot;1&quot;, &quot;2&quot;, &quot;3&quot;, &quot;4&quot;, &quot;5&quot;, &quot;6&quot;, &quot;7&quot;, &quot;8&quot;, &quot;9&quot;, &quot;10&quot;, &quot;11&quot;, &quot;12&quot;], &quot;formatSubmit&quot;: &quot;yyyy-mm-dd&quot;, &quot;pickadate-weekdaysShort&quot;: [&quot;2&quot;, &quot;3&quot;, &quot;4&quot;, &quot;5&quot;, &quot;6&quot;, &quot;7&quot;, &quot;1&quot;], &quot;pickadate-monthsFull&quot;: [&quot;1&quot;, &quot;2&quot;, &quot;3&quot;, &quot;4&quot;, &quot;5&quot;, &quot;6&quot;, &quot;7&quot;, &quot;8&quot;, &quot;9&quot;, &quot;10&quot;, &quot;11&quot;, &quot;12&quot;]}" type="datetime-local" value="',  # noqa
            self.view.render(field=field, mode='edit'))

    def test_select(self):
        from plone.app.widgets.at import SelectWidget
        field = self.example.getField('selectfield')
        self.assertIsInstance(field.widget, SelectWidget)
        self.assertIn(
            '<select name="selectfield"> </select>',
            self.view.render(field=field, mode='edit'))

    def test_select2(self):
        from plone.app.widgets.at import Select2Widget
        field = self.example.getField('select2field')
        self.assertIsInstance(field.widget, Select2Widget)
        self.assertIn(
            '<input class="pat-select2" name="select2field" data-pat-select2="{&quot;separator&quot;: &quot;;&quot;}" type="text" value=""/>',  # noqa
            self.view.render(field=field, mode='edit'))
