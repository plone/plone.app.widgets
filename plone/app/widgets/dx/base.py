import json
from lxml import etree
from plone.app.widgets.base import BasePatternsWidget


class PatternsWidget(object):

    pattern_el_type = 'input'

    @property
    def pattern_name(self):
        raise NotImplemented

    def render(self):
        widget = BasePatternsWidget(self.pattern_name, self.pattern_el_type)
        widget.el.attrib['name'] = self.name

        value = self.value
        if value is None:
            value = ''

        if hasattr(self, 'customize_widget'):
            self.customize_widget(widget, value)

        return widget.render()
