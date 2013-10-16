# -*- coding: utf-8 -*-

from Products.CMFCore.interfaces import ISiteRoot
from datetime import datetime
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component import providedBy
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('plone.app.widgets')
_plone = MessageFactory('plone')


class NotImplemented(Exception):
    """Raised when method/property is not implemented"""


def get_date_options(request):
    calendar = request.locale.dates.calendars['gregorian']
    # TODO: take first weekday into account when you like
    # weekdaysFull, weekdaysShort
    today = datetime.today()
    return {
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
        'placeholder': translate(_plone('Enter date...'), context=request),
        'today': translate(_plone(u"Today"), context=request),
        'clear': translate(_plone(u"Clear"), context=request),
    }


def get_time_options(request):
    return {
        'format': translate(
            _('pickadate_time_format', default='h:i a'),
            context=request),
        'placeholder': translate(_plone('Enter time...'), context=request),
        'today': translate(_plone(u"Today"), context=request),
    }


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
            return root.absolute_url()
    return ''

