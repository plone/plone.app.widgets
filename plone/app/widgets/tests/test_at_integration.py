# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

from datetime import date
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class BaseWidgetTests(unittest.TestCase):
    """Tests for plone.app.widgets.at.BaseWidget
    """

    maxDiff = None
    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        languages = getToolByName(self.portal, 'portal_languages')
        languages.manage_setLanguageSettings(
            'de', ['de'], setUseCombinedLanguageCodes=False)
        languages.setLanguageBindings()

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

    def _widget_pattern_options(self, field):
        args = field.widget._widget_args(self.example, field, self.request)
        return field.widget._widget(**args).pattern_options

    def test_date(self):
        from plone.app.widgets.at import DateWidget
        field = self.example.getField('datefield')
        self.assertIsInstance(field.widget, DateWidget)

        options = self._widget_pattern_options(field)
        del options['date']['value']
        year = date.today().year
        self.assertEqual(options, {
            'date': {
                'clear': u'Clear',
                'format': 'mmmm d, yyyy',
                'formatSubmit': 'yyyy-mm-dd',
                'max': [year + 20, 1, 1],
                'min': [year - 100, 1, 1],
                'monthsFull': [
                    u'Januar', u'Februar', u'M\xe4rz', u'April', u'Mai',
                    u'Juni', u'Juli', u'August', u'September', u'Oktober',
                    u'November', u'Dezember'],
                'monthsShort': [
                    u'Jan', u'Feb', u'Mrz', u'Apr', u'Mai', u'Jun', u'Jul',
                    u'Aug', u'Sep', u'Okt', u'Nov', u'Dez'],
                'selectYears': 200,
                'today': u'Today',
                'weekdaysFull': [
                    u'Sonntag', u'Montag', u'Dienstag', u'Mittwoch',
                    u'Donnerstag', u'Freitag', u'Samstag'],
                'weekdaysShort': [
                    u'So', u'Mo', u'Di', u'Mi', u'Do', u'Fr', u'Sa']
                },
            'time': 'false',
            })

        html = self.view.render(field=field, mode='edit')
        self.assertIn(
            '<input class="pat-pickadate" name="datefield" type="date" ',  # noqa
            html)

    def test_datetime(self):
        from plone.app.widgets.at import DatetimeWidget
        field = self.example.getField('datetimefield')
        self.assertIsInstance(field.widget, DatetimeWidget)

        options = self._widget_pattern_options(field)
        del options['date']['value']
        del options['time']['value']
        year = date.today().year
        self.assertEqual(options, {
            'date': {
                'clear': u'Clear',
                'format': 'mmmm d, yyyy',
                'formatSubmit': 'yyyy-mm-dd',
                'max': [year + 20, 1, 1],
                'min': [year - 100, 1, 1],
                'monthsFull': [
                    u'Januar', u'Februar', u'M\xe4rz', u'April', u'Mai',
                    u'Juni', u'Juli', u'August', u'September', u'Oktober',
                    u'November', u'Dezember'],
                'monthsShort': [
                    u'Jan', u'Feb', u'Mrz', u'Apr', u'Mai', u'Jun', u'Jul',
                    u'Aug', u'Sep', u'Okt', u'Nov', u'Dez'],
                'selectYears': 200,
                'today': u'Today',
                'weekdaysFull': [
                    u'Sonntag', u'Montag', u'Dienstag', u'Mittwoch',
                    u'Donnerstag', u'Freitag', u'Samstag'],
                'weekdaysShort': [
                    u'So', u'Mo', u'Di', u'Mi', u'Do', u'Fr', u'Sa'],
                },
            'time': {
                'format': 'HH:i',
                'formatSubmit': 'HH:i',
                },
            })

        html = self.view.render(field=field, mode='edit')
        self.assertIn(
            '<input class="pat-pickadate" name="datetimefield" type="datetime-local" ',  # noqa
            html)

    def test_select(self):
        from plone.app.widgets.at import SelectWidget
        field = self.example.getField('selectfield')
        self.assertIsInstance(field.widget, SelectWidget)
        self.assertIn(
            '<select class="pat-select2" name="selectfield" data-pat-select2="{&quot;separator&quot;: &quot;;&quot;}"> </select>',  # noqa
            self.view.render(field=field, mode='edit'))

    def test_select2(self):
        from plone.app.widgets.at import Select2Widget
        field = self.example.getField('select2field')
        self.assertIsInstance(field.widget, Select2Widget)
        self.assertIn(
            '<input class="pat-select2" name="select2field" type="text" value="" data-pat-select2="{&quot;orderable&quot;: false, &quot;separator&quot;: &quot;;&quot;}"/>',  # noqa
            self.view.render(field=field, mode='edit'))
