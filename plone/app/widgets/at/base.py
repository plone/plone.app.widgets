import json
from lxml import etree
from Products.Archetypes.Widget import TypesWidget


class PatternsWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro': "patterns_widgets",
        'element_type': 'input',
        'pattern': '',
        'pattern_options': {},
    })

    def _process_args(self, **kwargs):
        new_kwargs = {}
        for kwarg in kwargs:
            if kwarg in ['pattern_options']:
                new_kwargs[kwarg] = {}
                new_kwargs[kwarg].update(self._properties[kwarg])
                new_kwargs[kwarg].update(kwargs[kwarg])
            else:
                new_kwargs[kwarg] = kwargs[kwarg]
        super(PatternsWidget, self)._process_args(**new_kwargs)

    def view(self, context, field, request):
        return field.getAccessor(context)()

    def edit(self, context, field, request):
        value = field.getAccessor(context)()
        if value is None:
            value = ''

        if hasattr(self, 'updateOptions'):
            self.updateOptions(value, context, field, request)

        formatted = value
        if hasattr(self, 'formatAccessor'):
            formatted = self.formatAccessor(value, context, field, request)

        el = etree.Element(self.element_type)
        el.attrib['name'] = field.getName()

        if self.element_type == 'input':
            el.attrib['type'] = 'text'
            el.attrib['value'] = formatted
        elif self.element_type == 'textarea':
            el.text = formatted
        elif self.element_type == 'select' and field.vocabulary:
            for token, title in field.Vocabulary(context).items():
                option = etree.Element('option')
                option.attrib['value'] = token
                if token == value:
                    option.attrib['selected'] = 'selected'
                option.text = title
                el.append(option)

        else:
            raise Exception(
                "Wrong 'element_type' selected ('%s')." % (self.element_type))

        if self.pattern:
            el.attrib['class'] = 'pat-' + self.pattern
            if self.pattern_options:
                for name, value in self.pattern_options.items():
                    if type(value) in [dict, list]:
                        value = json.dumps(value)
                    el.attrib['data-' + self.pattern + '-' + name] = value

        return etree.tostring(el)
