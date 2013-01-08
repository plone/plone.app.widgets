from plone.app.widgets.at.base import PatternsWidget


class CalendarWidget(PatternsWidget):
    _properties = PatternsWidget._properties.copy()
    _properties.update({
        'pattern': 'calendar',
        'pattern_options': {
            'formatSubmit': 'yyyy-m-d H:M',
        },
        'pattern_extra_options': {
            'pickadate': {}
        },
    })

    def formatAccessor(self, value):
        if value:
            return value.strftime('%Y-%m-%d %H:%M')
        return value
