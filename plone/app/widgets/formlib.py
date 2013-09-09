try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.CMFCore.utils import getToolByName
from plone.app.widgets.base import Select2Widget


class UberRelatedItemWidget(UberSelectionWidget, Select2Widget):

    separator = ';'

    def __init__(self, field, request):
        Select2Widget.__init__(self, 'relateditems')
        UberSelectionWidget.__init__(self, field, request)

        self.site = getSite()
        pprops = getToolByName(self.site, 'portal_properties')
        site_props = pprops.site_properties
        folder_types = site_props.getProperty(
            'typesLinkToFolderContentsInFC', ['Folder', 'Large Plone Folder'])

        base_query = self.source.base_query.copy()
        query = base_query.copy()
        criterias = []
        if 'portal_type' in query:
            criterias.append({
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': query['portal_type']
            })
        if 'is_folderish' in query:
            criterias.append({
                'i': 'is_folderish',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': query['is_folderish']
            })
        self.pattern_options = {
            'separator': self.separator,
            'maximumSelectionSize': 1,
            'folderTypes': folder_types,
            'baseCriteria': criterias
        }

    def _value(self):
        value = None
        if self._renderedValueSet():
            value = self._data
        else:
            token = self.request.form.get(self.name)

            if token is not None:
                uid = token.split('/')[0]
                catalog = getToolByName(self.site, 'portal_catalog')
                brains = catalog(UID=uid)
                if len(brains) > 0:
                    item = brains[0]
                    value = item.getPath()[
                        len('/'.join(self.site.getPhysicalPath())):]
        if value is None:
            value = []
        return value

    def template(self, *args, **kwargs):
        url = getSite().absolute_url()
        url += '/@@getVocabulary?name=plone.app.vocabularies.Catalog'
        self.pattern_options['ajaxvocabulary'] = url
        if self._data and self._data is not self._data_marker:
            catalog = getToolByName(self.site, 'portal_catalog')
            items = catalog(path={
                'query': '/'.join(self.site.getPhysicalPath()) + self._data,
                'depth': 0
            })
            if len(items) > 0:
                item = items[0]
                self.value = item.UID
        return self.render()
