import json
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.vocabularies.types import BAD_TYPES
from plone.app.layout.viewlets import common


class SearchBoxViewlet(common.SearchBoxViewlet):
    index = ViewPageTemplateFile('searchbox.pt')

    @property
    def pattern_class(self):
        if self.search_input_id == 'nolivesearchGadget':
            return ''
        return 'pat-livesearch'

    @property
    def pattern_options(self):
        types = getToolByName(self.context, 'portal_types')
        site_properties = getToolByName(
            self.context, 'portal_properties').site_properties
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')

        return json.dumps({
            "ajaxvocabulary": "%s/@@getVocabulary?name=%s" % (
                portal_state.portal_url(),
                'plone.app.vocabularies.Catalog'),
            "baseCriteria": [{
                "i": "portal_type",
                "o": "plone.app.querystring.operation.selection.is",
                "v": [
                    item for item in types.listContentTypes()
                    if item not in site_properties.types_not_searched
                    and item not in BAD_TYPES]
            }]
        })
