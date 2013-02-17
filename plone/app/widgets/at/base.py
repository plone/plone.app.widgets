from Products.Archetypes.Widget import TypesWidget
from plone.app.widgets.base import BasePatternsWidget


class PatternsWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro': "patterns_widgets",
    })

    pattern_el_type = 'input'

    @property
    def pattern_name(self):
        raise NotImplemented

    def view(self, context, field, request):
        return field.getAccessor(context)()

    def edit(self, context, field, request):
        widget = BasePatternsWidget(self.pattern_name, self.pattern_el_type)
        widget.el.attrib['name'] = field.getName()

        value = field.getAccessor(context)()
        if value is None:
            value = ''

        if hasattr(self, 'customize_widget'):
            self.customize_widget(widget, value, context, field, request)

        return widget.render()
