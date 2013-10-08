

def get_calendar_options(request):
    calendar = request.locale.dates.calendars['gregorian']
    # TODO: take first weekday into account when you like
    # weekdaysFull, weekdaysShort
    return {
        'weekdaysFull': [
            calendar.days.get(t, (None, None))[0]
            for t in (7, 1, 2, 3, 4, 5, 6)],
        'weekdaysShort': [
            calendar.days.get(t, (None, None))[1]
            for t in (7, 1, 2, 3, 4, 5, 6)],
        'monthsFull': calendar.getMonthNames(),
        'monthsShort': calendar.getMonthAbbreviations(),
    }

#from zope.component import queryMultiAdapter
#from zope.i18nmessageid import MessageFactory
#_ = MessageFactory('plone.app.widgets')
#P_ = MessageFactory('plone')
#
#def base_url(context, request):
#    portal_state = queryMultiAdapter((context, request),
#                                     name=u'plone_portal_state')
#    url = ''
#    if portal_state:
#        url = portal_state.portal_url()
#    return url
#
#class PickadatePatternWidget(InputWidget):
#    """
#    """
#
#    def __init__(self, name, pattern_options={}, type='date', value=None):
#        super(PickadatePatternWidget, self).__init__(
#            'pickadate', name, pattern_options, type, value)
#
# Date
#        _pattern_options = {'date': {'format': format_date or 'mmmm d, yyyy'},
#                            'time': 'false'}
#        if request is not None:
#            if format_date is None:
#                format_date = translate(
#                    _('pickadate_date_format', default='mmmm d, yyyy'),
#                    context=request)
#            calendar = request.locale.dates.calendars[calendar]
#            year = date.today().year
#            weekdaysFull = [
#                calendar.days.get(t, (None, None))[0]
#                for t in (7, 1, 2, 3, 4, 5, 6)]
#            weekdaysShort = [
#                calendar.days.get(t, (None, None))[1]
#                for t in (7, 1, 2, 3, 4, 5, 6)]
#            _pattern_options = dict_merge(_pattern_options, {
#                'date': {
#                    'selectYears': 200,
#                    'min': [year - 100, 1, 1],
#                    'max': [year + 20, 1, 1],
#                    'monthsFull': calendar.getMonthNames(),
#                    'monthsShort': calendar.getMonthAbbreviations(),
#                    'weekdaysFull': weekdaysFull,
#                    'weekdaysShort': weekdaysShort,
#                    'today': translate(P_(u"Today"), context=request),
#                    'clear': translate(P_(u"Clear"), context=request),
#                    'format': format_date,
#                },
#            })
#
# Datetime
#        timeOptions = pattern_options.get('time', {})
#        if isinstance(timeOptions, dict):
#            timeOptions['format'] = format_time or 'HH:i'
#            if request is not None:
#                if format_time is None:
#                    format_time = translate(
#                        _('pickadate_time_format', default='HH:i'),
#                        context=request)
#                timeOptions['format'] = format_time
#            timeOptions['formatSubmit'] = 'HH:i'
#        self.pattern_options['time'] = timeOptions
