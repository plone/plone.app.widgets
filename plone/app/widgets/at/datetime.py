from plone.app.widgets.at.base import PatternsWidget
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('plone')


class DateTimeWidget(PatternsWidget):

    pattern_name = 'datetime'
    pattern_el_type = 'input'
    calendar_type = 'gregorian'

    def customize_widget(self, widget, value, context, field, request):

        calendar = request.locale.dates.calendars[self.calendar_type]

        widget.options['pickadate-months.full'] = calendar.getMonthNames()
        widget.options['pickadate-months.short'] = \
            calendar.getMonthAbbreviations()
        widget.options['pickadate-weekdays.full'] = calendar.getDayNames()
        widget.options['pickadate-weekdays.short'] = \
            calendar.getDayAbbreviations()
        widget.options['pickadate-today'] = \
            translate(_(u"Today"), context=request)
        widget.options['pickadate-clear'] = \
            translate(_(u"Clear"), context=request)

        if value:
            value = value.strftime('%Y-%m-%d %H:%M')
        widget.el.attrib['value'] = value
