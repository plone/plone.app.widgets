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
from zope.deprecation import deprecate
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import IVocabularyFactory

import json
import zope.deferredimport


_ = MessageFactory('plone')


zope.deferredimport.deprecated(
    'Import first_weekday from plone.app.event.base instead',
    first_weekday='plone.app.event.base:first_weekday',
)


class NotImplemented(Exception):
    """Raised when method/property is not implemented"""


def get_date_options(request):
    calendar = request.locale.dates.calendars['gregorian']
    today = datetime.today()
    return {
        'behavior': 'native',
        'week-numbers': 'show',
        'first-day': calendar.week.get('firstDay') == 1 and 1 or 0,
        'today': translate(_(u"Today"), context=request),
        'clear': translate(_(u"Clear"), context=request),
    }


def get_datetime_options(request):
    options = get_date_options(request)
    return options


@deprecate("features were moved into the AjaxSelectWidget, remove in Plone 6")
def get_ajaxselect_options(context, value, separator, vocabulary_name,
                           vocabulary_view, field_name=None):
    # code now part of the widget, let it in here for BBB and remove in Plone 6
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
                             vocabulary_view, field_name=None,
                             include_recently_added=True):

    if IForm.providedBy(context):
        context = context.context

    request = getRequest()
    site = get_top_site_from_url(context, request)
    options = {
        'separator': separator,
    }
    if not vocabulary_name:
        # we need a vocabulary!
        raise ValueError('RelatedItems needs a vocabulary')
    options['vocabularyUrl'] = '{0}/{1}?name={2}'.format(
        get_context_url(site), vocabulary_view, vocabulary_name,
    )
    if field_name:
        options['vocabularyUrl'] += '&field={0}'.format(field_name)
    if value:
        options['initialValues'] = {}
        catalog = False
        if vocabulary_name == 'plone.app.vocabularies.Catalog':
            catalog = getToolByName(getSite(), 'portal_catalog')
        for value in value.split(separator):
            title = value
            if catalog:
                result = catalog(UID=value)
                title = result[0].Title if result else value
            options['initialValues'][value] = title

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

    if include_recently_added:
        # Options for recently used key
        tool = getToolByName(context, 'portal_membership')
        user = tool.getAuthenticatedMember()
        options['recentlyUsed'] = False  # Keep that off in Plone 5.1
        options['recentlyUsedKey'] = (u'relateditems_recentlyused_%s_%s' % (
            field_name or '',
            user.id
        ))  # use string substitution with %s here for automatic str casting.

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
        'patternAjaxSelectOptions': {'separator': ';'},
        'patternRelateditemsOptions': get_relateditems_options(
            context,
            None,
            ';',
            'plone.app.vocabularies.Catalog',
            '@@getVocabulary',
            'relatedItems',
            include_recently_added=False
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
