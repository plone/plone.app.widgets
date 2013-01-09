import json
from zope.component import getMultiAdapter
from plone.app.widgets.at.base import PatternsWidget


class AutocompleteWidget(PatternsWidget):
    _properties = PatternsWidget._properties.copy()
    _properties.update({
        'input_type': 'textarea',
        'pattern': 'autocomplete',
        'pattern_options': {
            'prompt': 'Add tag...',
            'ajax-url': '!getAjaxUrl',
        },
        'pattern_extra_options': {
            'textext': {}
        },
    })

    def formatAccessor(self, value):
        return '\n'.join(value)

    def getAjaxUrl(self, context, request, field):
        state = getMultiAdapter((context, request), name=u'plone_portal_state')
        return '%s/@@autocomplete?source=%s' % (
            state.portal_url(), 'plone.app.vocabularies.Keywords')

    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker
        if emptyReturnsMarker and value == '':
            return empty_marker
        return '\n'.join(json.loads(value)), {}
