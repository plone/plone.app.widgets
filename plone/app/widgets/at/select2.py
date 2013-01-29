import json
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.schema.interfaces import IVocabularyFactory
from plone.app.widgets.at.base import PatternsWidget


class Select2Widget(PatternsWidget):
    _properties = PatternsWidget._properties.copy()
    _properties.update({
        'pattern': 'select2',
        'pattern_options': '',
        'tags': '',
        'multiple': False,
        'ajax_vocabulary': '',
        'ajax_url': '/@@widgets/getVocabulary?name=',
    })

    def formatAccessor(self, value, context, field, request):
        if type(value) in [list, tuple]:
            return ','.join(value)
        return value

    def updateOptions(self, value, context, field, request):
        state = getMultiAdapter((context, request), name=u'plone_portal_state')
        if self.ajax_vocabulary and self.element_type is not "select":
            self.pattern_options += 'ajaxUrl:' + \
                state.portal_url() + self.ajax_url + self.ajax_vocabulary + ';'
        if self.tags:
            factory = queryUtility(IVocabularyFactory, self.tags)
            tags = [i.token for i in factory(context)]
            self.pattern_options += 'tags:' + json.dumps(tags) + ';'
        if self.multiple is True:
            self.pattern_options += 'multiple:true;'
        if self.ajax_vocabulary:
            factory = queryUtility(IVocabularyFactory, self.ajax_vocabulary)
            vocabulary = factory(context)
            data = {}
            if type(value) in [list, tuple]:
                for item in value:
                    term = vocabulary.getTerm(item)
                    if term:
                        data[term.token] = term.title
                    else:
                        data[item] = item
            else:
                term = vocabulary.getTerm(value)
                data.append(dict(id=term.token, text=term.title))
            self.pattern_options += 'initSelection:' + json.dumps(data) + ';'

    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker
        if emptyReturnsMarker and value == '':
            return empty_marker

        value = value.strip()
        if self.multiple or self.tags:
            value = value.split(',')
        return value, {}
