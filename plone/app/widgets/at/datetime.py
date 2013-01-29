from plone.app.widgets.at.base import PatternsWidget


class DateTimeWidget(PatternsWidget):
    _properties = PatternsWidget._properties.copy()
    _properties.update({
        'pattern': 'datetime',
        'pattern_options': 'formatSubmit:yyyy-m-d H:M;',
    })

    def formatAccessor(self, value, context, field, request):
        if value:
            return value.strftime('%Y-%m-%d %H:%M')
        return value
