# -*- coding: utf-8 -*-

from datetime import datetime
from mock import Mock
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.widgets.browser.vocabulary import VocabularyView
from plone.app.widgets.testing import PLONEAPPWIDGETS_INTEGRATION_TESTING
from plone.app.widgets.testing import TestRequest
from plone.testing.zca import ZCML_DIRECTIVES
from Products.Archetypes.atapi import BaseContent
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import Schema
from zope.configuration import xmlconfig
from zope.globalrequest import setRequest

import json

try:
    import unittest2 as unittest
except ImportError:  # pragma: nocover
    import unittest  # pragma: nocover
    assert unittest  # pragma: nocover

import plone.uuid


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
        self.context = Mock()
        self.field = Mock()
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
        self.context = Mock()
        self.field = Mock()
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
        self.context = Mock()
        self.vocabulary = Mock()
        self.vocabulary.items.return_value = [
            ('one', 'one'),
            ('two', 'two'),
            ('three', 'three'),
        ]
        self.field = Mock()
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

    def test_widget_orderable(self):
        from plone.app.widgets.at import SelectWidget
        widget = SelectWidget()
        widget.multiple = True
        widget.orderable = True
        self.assertEqual(
            {
                'multiple': True,
                'name': 'fieldname',
                'pattern_options': {'orderable': True, 'separator': ';'},
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


# TODO
#class AjaxSelectWidgetTests(unittest.TestCase):

class RelatedItemsWidgetTests(unittest.TestCase):

    layer = ZCML_DIRECTIVES

    def setUp(self):

        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.context = Mock(absolute_url=lambda: '')
        self.field = Mock()

        xmlconfig.file('configure.zcml', plone.uuid,
                       context=self.layer['configurationContext'])

    def test_widget(self):
        from zope.event import notify
        from zope.interface import implements
        from zope.lifecycleevent import ObjectCreatedEvent
        from plone.uuid.interfaces import IUUID
        from plone.uuid.interfaces import IAttributeUUID
        from plone.app.widgets.at import RelatedItemsWidget

        class ExampleContent(object):
            implements(IAttributeUUID)

        obj1 = ExampleContent()
        obj2 = ExampleContent()
        notify(ObjectCreatedEvent(obj1))
        notify(ObjectCreatedEvent(obj2))

        self.field.getName.return_value = 'fieldname'
        self.field.getAccessor.return_value = lambda: [obj1, obj2]
        self.context.portal_properties.site_properties\
            .getProperty.return_value = ['SomeType']

        widget = RelatedItemsWidget()

        self.assertEqual(
            {
                'name': 'fieldname',
                'value': '{};{}'.format(IUUID(obj1), IUUID(obj2)),
                'pattern': 'relateditems',
                'pattern_options': {
                    'folderTypes': ['SomeType'],
                    'separator': ';',
                    'vocabularyUrl': '/@@getVocabulary?name='
                                     'plone.app.vocabularies.Catalog'
                                     '&field=fieldname',
                },
            },
            widget._base_args(self.context, self.field, self.request),
        )


class QueryStringWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.context = Mock()
        self.field = Mock()

    def test_widget(self):
        from plone.app.widgets.at import QueryStringWidget

        self.field.getName.return_value = 'fieldname'
        self.field.getRaw.return_value = [
            {'query': 'string1'},
            {'query': 'string2'},
        ]

        widget = QueryStringWidget()

        self.assertEqual(
            {
                'name': 'fieldname',
                'value': '[{"query": "string1"}, {"query": "string2"}]',
                'pattern': 'querystring',
                'pattern_options': {'indexOptionsUrl': '/@@qsOptions'},
            },
            widget._base_args(self.context, self.field, self.request),
        )


class TinyMCEWidgetTests(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        self.context = Mock()
        self.field = Mock()
        self.field.getAccessor.return_value = lambda: 'fieldvalue'
        self.field.getName.return_value = 'fieldname'

    def test_widget(self):
        from plone.app.widgets.at import TinyMCEWidget
        widget = TinyMCEWidget()
        self.context.portal_properties.site_properties\
            .getProperty.return_value = 'utf-8'
        self.assertEqual(
            {
                'name': 'fieldname',
                'value': 'fieldvalue',
                'pattern': 'tinymce',
                'pattern_options': {},
            },
            widget._base_args(self.context, self.field, self.request),
        )


class ArchetypesVocabularyPermissionTests(unittest.TestCase):

    layer = PLONEAPPWIDGETS_INTEGRATION_TESTING

    def setUp(self):
        self.request = TestRequest(environ={'HTTP_ACCEPT_LANGUAGE': 'en'})
        setRequest(self.request)
        self.portal = self.layer['portal']

        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        class TestAT(BaseContent):

            schema = BaseContent.schema.copy() + Schema((
                StringField('allowed_field',
                            write_permission='View'),
                StringField('disallowed_field',
                            write_permission='View management screens'),
                StringField('default_field'),
                ))

        self.portal._setObject('test_at', TestAT('test_at'),
                               suppress_events=True)

        self.portal.test_at.manage_permission('View',
                                              ('Anonymous',),
                                              acquire=False)
        self.portal.test_at.manage_permission('View management screens',
                                              (),
                                              acquire=False)
        self.portal.test_at.manage_permission('Modify portal content',
                                              ('Editor', 'Manager',
                                               'Site Adiminstrator'),
                                              acquire=False)

    def testVocabularyFieldAllowed(self):
        view = VocabularyView(self.portal.test_at, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'allowed_field',
        })
        data = json.loads(view())
        self.assertEquals(len(data['results']),
                          len(self.portal.portal_types.objectIds()))

    def testVocabularyFieldDisallowed(self):
        view = VocabularyView(self.portal.test_at, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'disallowed_field',
        })
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')

    def testVocabularyFieldDefaultPermission(self):
        view = VocabularyView(self.portal.test_at, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'default_field',
        })
        # If the field is does not have a security declaration, the
        # default edit permission is tested (Modify portal content)
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        data = json.loads(view())
        self.assertEquals(data['error'], 'Vocabulary lookup not allowed')

        setRoles(self.portal, TEST_USER_ID, ['Editor'])
        # Now access should be allowed, but the vocabulary does not exist
        data = json.loads(view())
        self.assertEquals(len(data['results']),
                          len(self.portal.portal_types.objectIds()))

    def testVocabularyMissingField(self):
        view = VocabularyView(self.portal.test_at, self.request)
        self.request.form.update({
            'name': 'plone.app.vocabularies.PortalTypes',
            'field': 'missing_field',
        })
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        with self.assertRaises(AttributeError):
            view()
