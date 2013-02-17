from plone.app.widgets.at.base import PatternsWidget


class DateTimeWidget(PatternsWidget):

    pattern_name = 'datetime'
    pattern_el_type = 'input'

    def customize_widget(self, widget, value, context, field, request):
        if value:
            value = value.strftime('%Y-%m-%d %H:%M')
        widget.el.attrib['value'] = value
