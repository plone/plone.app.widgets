from plone.app.widgets.at.base import PatternsWidget


class CalendarWidget(PatternsWidget):
    _properties = PatternsWidget._properties.copy()
    _properties.update({
        'pattern': 'calendar',
        'pattern_options': {},
        'pattern_extra_options': {
            'pickadate': {}
        },
    })
