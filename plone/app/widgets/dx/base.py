
import json
from lxml import etree


class PatternsWidget(object):

    _pattern_el_type = 'input'
    _pattern_options = {}

    def render(self):
        value = self.value
        if value is None:
            value = ''

        el = etree.Element(self._pattern_el_type)
        el.attrib['name'] = self.name

        el = self.render_element(el)

        if self._pattern_name:
            el.attrib['class'] = 'pat-' + self._pattern_name
            if self._pattern_options:
                for name, value in self._pattern_options.items():
                    if type(value) in [dict, list]:
                        value = json.dumps(value)
                    el.attrib['data-%s-%s' % (
                        self._pattern_name, name)] = value

        return etree.tostring(el)
