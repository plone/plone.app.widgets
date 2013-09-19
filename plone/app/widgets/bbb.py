import json
#from z3c.form.widget import FieldWidget
#from z3c.form.interfaces import IFieldWidget
#from z3c.form.util import getSpecification
#from zope.interface import implementer
#from zope.component import adapter
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone.interfaces.syndication import ISiteSyndicationSettings
from plone.app.vocabularies.types import BAD_TYPES
from plone.app.layout.viewlets import common
#from plone.app.widgets.dx import Select2Widget
#from plone.app.widgets.interfaces import IWidgetsLayer


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


#@adapter(getSpecification(ISiteSyndicationSettings['site_rss_items']),
#         IWidgetsLayer)
#@implementer(IFieldWidget)
#def SiteRSSItemsFieldWidget(field, request):
#    widget = FieldWidget(field, Select2Widget(request))
#    widget.ajax_vocabulary = 'plone.app.vocabularies.SyndicatableFeedItems'
#    return widget
