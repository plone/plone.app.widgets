from z3c.form.widget import Widget
from plone.app.widgets.base import BasePatternsWidget


class PatternsWidget(Widget):

    pattern_el_type = 'input'

    @property
    def pattern_name(self):
        raise NotImplementedError('pattern_name not implemented!')

    def render(self):
        # Use standard rendering in display mode
        if self.mode == 'display':
            return super(PatternsWidget, self).render()

        widget = BasePatternsWidget(self.pattern_name, self.pattern_el_type)
        widget.el.attrib['name'] = self.name

        value = self.request.get(self.name, self.value)
        if value is None:
            value = ''

        if hasattr(self, 'customize_widget'):
            self.customize_widget(widget, value)

        return widget.render()
