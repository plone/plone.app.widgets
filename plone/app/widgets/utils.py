# -*- coding: utf-8 -*-

from Acquisition import aq_base
from Acquisition import aq_parent
from datetime import datetime
from OFS.interfaces import IFolder
from OFS.interfaces import ISimpleItem
from plone.app.layout.navigation.root import getNavigationRootObject
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import get_top_site_from_url
from z3c.form.interfaces import IForm
from zope.component import ComponentLookupError
from zope.component import getMultiAdapter
from zope.component import providedBy
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import IVocabularyFactory

import json


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
        },
        'today': translate(_(u"Today"), context=request),
        'clear': translate(_(u"Clear"), context=request),
    }


def get_datetime_options(request):
    options = get_date_options(request)
    options['time'] = {
        'format': translate(
            _('pickadate_time_format', default='h:i a'),
            context=request),
        'placeholder': translate(_('Enter time...'), context=request),
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

    if IForm.providedBy(context):
        context = context.context

    request = getRequest()
    site = get_top_site_from_url(context, request)
    options = get_ajaxselect_options(
        site,
        value,
        separator,
        vocabulary_name,
        vocabulary_view,
        field_name
    )

    nav_root = getNavigationRootObject(context, site)

    if not ISimpleItem.providedBy(context):
        context = nav_root

    # basePath - start to search/browse in here.
    base_path_context = context
    if not IFolder.providedBy(base_path_context):
        base_path_context = aq_parent(base_path_context)
    if not base_path_context:
        base_path_context = nav_root
    options['basePath'] = '/'.join(base_path_context.getPhysicalPath())

    # rootPath - Only display breadcrumb elements deeper than this path.
    options['rootPath'] = '/'.join(site.getPhysicalPath()) if site else '/'

    # rootUrl: Visible URL up to the rootPath. This is prepended to the
    # currentPath to generate submission URLs.
    options['rootUrl'] = site.absolute_url() if site else ''

    # contextPath - current edited object. Will not be available to select.
    options['contextPath'] = '/'.join(context.getPhysicalPath())

    if base_path_context != nav_root:
        options['favorites'] = [
            {
                'title': _(u'Current Content'),
                'path': '/'.join(base_path_context.getPhysicalPath())
            }, {
                'title': _(u'Start Page'),
                'path': '/'.join(nav_root.getPhysicalPath())
            }
        ]

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
        'previewCountURL': '%s/@@querybuildernumberofresults' % base_url,
        'patternDateOptions': get_date_options(getRequest()),
        'patternAjaxSelectOptions': get_ajaxselect_options(
            context,
            None,
            ';',
            None,
            None,
            None
        ),
        'patternRelateditemsOptions': get_relateditems_options(
            context,
            None,
            ';',
            'plone.app.vocabularies.Catalog',
            '@@getVocabulary',
            'relatedItems'
        )
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
