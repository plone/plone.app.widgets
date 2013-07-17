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
            "ajaxvocabulary": "%s/@@getVocabulary?name="
                              "plone.app.vocabularies.Catalog" % (
                              portal_state.portal_url()),
            "baseCriteria": [{
                "i": "portal_type",
                "o": "plone.app.querystring.operation.selection.is",
                "v": [
                    item for item in types.listContentTypes()
                    if item not in site_properties.types_not_searched
                    and item not in BAD_TYPES]
            }]
        })

      #// Livesearch

      #$match = $root.find('.LSBox');
      #var url = $match.parents('form').attr('action').replace('@@search',
      #    '@@getVocabulary?name=plone.app.vocabularies.Catalog');
      #var attrs = {
      #  'ajaxvocabulary': url
      #};
      #$match.attr({
      #  'class': 'pat-livesearch',
      #  'data-pat-livesearch': JSON.stringify(attrs)
      #});
      #$match.find('.searchSection').remove();
      #$match.find('.LSResult').attr({
      #  'class': 'pat-livesearch-container pull-right',
      #  'id': ''
      #});
      #$match.find('.LSShadow').attr('class', 'pat-livesearch-results');
      #$match.find('#searchGadget').addClass('pat-livesearch-input')
      #  .attr('autocomplete', 'off');
      #$match.find('.searchButton').hide();

