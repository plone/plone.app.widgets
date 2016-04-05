# -*- coding: utf-8 -*-

from Acquisition import aq_base
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from datetime import datetime
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component import providedBy
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import IVocabularyFactory
from z3c.form.interfaces import IForm
from zope.component import getMultiAdapter
from zope.component import ComponentLookupError
import json
from zope.globalrequest import getRequest

_ = MessageFactory('plone')


try:
    from plone.app.event import base as pae_base
    HAS_PAE = True
except ImportError:
    HAS_PAE = False


def first_weekday():
    if HAS_PAE:
        wkday = pae_base.wkday_to_mon1(pae_base.first_weekday())
        if wkday > 1:
            return 1  # Default to Monday
        return wkday
    else:
        cal = getToolByName(getSite(), 'portal_calendar', None)
        if cal:
            wkday = cal.firstweekday
            if wkday == 6:  # portal_calendar's Sunday is 6
                return 0  # Sunday
        return 1  # other cases: Monday


class NotImplemented(Exception):
    """Raised when method/property is not implemented"""


def get_date_options(request):
    calendar = request.locale.dates.calendars['gregorian']
    today = datetime.today()
    return {
        'time': False,
        'date': {
            'firstDay': calendar.week.get('firstDay') == 1 and 1 or 0,
            'weekdaysFull': [
                calendar.days.get(t, (None, None))[0]
                for t in (7, 1, 2, 3, 4, 5, 6)],
            'weekdaysShort': [
                calendar.days.get(t, (None, None))[1]
                for t in (7, 1, 2, 3, 4, 5, 6)],
            'monthsFull': calendar.getMonthNames(),
            'monthsShort': calendar.getMonthAbbreviations(),
            'selectYears': 200,
            'min': [today.year - 100, 1, 1],
            'max': [today.year + 20, 1, 1],
            'format': translate(
                _('pickadate_date_format', default='mmmm d, yyyy'),
                context=request),
            'placeholder': translate(_('Enter date...'), context=request),
            'today': translate(_(u"Today"), context=request),
            'clear': translate(_(u"Clear"), context=request),
        }
    }


def get_datetime_options(request):
    options = get_date_options(request)
    options['time'] = {
        'format': translate(
            _('pickadate_time_format', default='h:i a'),
            context=request),
        'placeholder': translate(_('Enter time...'), context=request),
        'today': translate(_(u"Today"), context=request),
    }
    return options


def get_ajaxselect_options(context, value, separator, vocabulary_name,
                           vocabulary_view, field_name=None):
    options = {'separator': separator}
    if vocabulary_name:
        options['vocabularyUrl'] = '{}/{}?name={}'.format(
            get_context_url(context), vocabulary_view, vocabulary_name)
        if field_name:
            options['vocabularyUrl'] += '&field={}'.format(field_name)
        if value:
            vocabulary = queryUtility(IVocabularyFactory, vocabulary_name)
            if vocabulary:
                options['initialValues'] = {}
                vocabulary = vocabulary(context)
                # Catalog
                if vocabulary_name == 'plone.app.vocabularies.Catalog':
                    uids = value.split(separator)
                    try:
                        catalog = getToolByName(context, 'portal_catalog')
                    except AttributeError:
                        catalog = getToolByName(getSite(), 'portal_catalog')
                    for item in catalog(UID=uids):
                        options['initialValues'][item.UID] = item.Title
                else:
                    for value in value.split(separator):
                        try:
                            term = vocabulary.getTerm(value)
                            options['initialValues'][term.token] = term.title
                        except LookupError:
                            options['initialValues'][value] = value
    return options


def get_relateditems_options(context, value, separator, vocabulary_name,
                             vocabulary_view, field_name=None):
    portal = get_portal()
    options = get_ajaxselect_options(portal, value, separator,
                                     vocabulary_name, vocabulary_view,
                                     field_name)
    if IForm.providedBy(context):
        context = context.context
    request = getRequest()
    msgstr = translate(_(u'Search'), context=request)
    options.setdefault('searchText', msgstr)
    msgstr = translate(_(u'Entire site'), context=request)
    options.setdefault('searchAllText', msgstr)
    msgstr = translate(_('tabs_home',
                       default=u'Home'),
                       context=request)
    options.setdefault('homeText', msgstr)
    options.setdefault('folderTypes', ['Folder'])
    options.setdefault(
        'treeVocabularyUrl',
        '{}/@@getVocabulary?name=plone.app.vocabularies.Catalog'.format(
            portal is not None and portal.absolute_url() or '')
    )
    options.setdefault('sort_on', 'sortable_title')
    options.setdefault('sort_order', 'ascending')

    nav_root = getNavigationRootObject(context, portal)
    options['basePath'] = (
        '/'.join(nav_root.getPhysicalPath()) if nav_root else '/'
    )
    options['rootPath'] = (
        '/'.join(portal.getPhysicalPath()) if portal else '/'
    )
    return options


def get_querystring_options(context, querystring_view):
    portal_url = get_portal_url(context)
    try:
        base_url = context.absolute_url()
    except AttributeError:
        base_url = portal_url
    return {
        'indexOptionsUrl': '{}/{}'.format(portal_url, querystring_view),
        'previewURL': '%s/@@querybuilder_html_results' % base_url,
        'previewCountURL': '%s/@@querybuildernumberofresults' % base_url
    }


def get_tinymce_options(context, field, request):
    """
    We're just going to be looking up settings from
    plone pattern options
    """
    options = {}
    try:
        pattern_options = getMultiAdapter(
            (context, request, field),
            name="plone_settings").tinymce()['data-pat-tinymce']
        options = json.loads(pattern_options)
    except (ComponentLookupError, AttributeError):
        pass
    return options


def get_portal():
    closest_site = getSite()
    if closest_site is not None:
        for potential_portal in closest_site.aq_chain:
            if ISiteRoot in providedBy(potential_portal):
                return potential_portal


def get_portal_url(context):
    portal = get_portal()
    if portal:
        root = getNavigationRootObject(context, portal)
        if root:
            try:
                return root.absolute_url()
            except AttributeError:
                return portal.absolute_url()
        else:
            return portal.absolute_url()
    return ''


def get_context_url(context):
    if IForm.providedBy(context):
        # Use the request URL if we are looking at an addform
        url = context.request.get('URL')
    elif hasattr(context, 'absolute_url'):
        url = context.absolute_url
        if callable(url):
            url = url()
    else:
        url = get_portal_url(context)
    return url


def get_widget_form(widget):
    form = getattr(widget, 'form', None)
    if getattr(aq_base(form), 'parentForm', None) is not None:
        form = form.parentForm
    return form
