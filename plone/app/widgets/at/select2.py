from lxml import etree
from zope.component import getMultiAdapter
from plone.app.widgets.at.base import PatternsWidget


class SelectWidget(PatternsWidget):
    _properties = PatternsWidget._properties.copy()
    _properties.update({
        'width': '20em',
    })

    pattern_el_type = 'select'
    pattern_name = 'select2'

    def customize_widget(self, widget, value, context, field, request):

        if self.width:
            widget.options['width'] = self.width

        for token, title in field.Vocabulary(context).items():
            option = etree.Element('option')
            option.attrib['value'] = token
            if token == value:
                option.attrib['selected'] = 'selected'
            option.text = title
            widget.el.append(option)


class TagsWidget(PatternsWidget):
    _properties = PatternsWidget._properties.copy()
    _properties.update({
        'width': '30em',
        'ajax_suggest': '',
        'multiple': True
    })

    pattern_el_type = 'input'
    pattern_name = 'select2'

    def customize_widget(self, widget, value, context, field, request):

        if self.width:
            widget.options['width'] = self.width

        if self.ajax_suggest:
            state = getMultiAdapter(
                (context, request), name=u'plone_portal_state')
            widget.options['ajax_suggest'] = state.portal_url() + \
                '/@@widgets/getVocabulary?name=' + self.ajax_suggest

        if type(value) in [list, tuple]:
            value = ','.join(value)

        widget.el.attrib['value'] = value
        widget.el.attrib['type'] = 'text'

    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker
        if emptyReturnsMarker and value == '':
            return empty_marker

        value = value.strip()
        if self.multiple or self.ajax_suggest:
            value = value.split(',')
        return value, {}
