import json
from lxml import html


class BasePatternsWidget(object):

    def __init__(self, name, element_type='input'):
        self.el = html.Element(element_type)
        self.name = name
        self.options = {}

    def render(self):
        self.el.attrib['class'] = 'pat-' + self.name
        if self.options:
            for name, value in self.options.items():
                if type(value) in [dict, list]:
                    value = json.dumps(value)
                self.el.attrib['data-%s-%s' % (self.name, name)] = value
        return html.tostring(self.el)
