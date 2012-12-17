try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
import json
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from plone.widgets.query import BaseQuery
from itertools import chain


_user_search_fields = ['login', 'fullname', 'email']


class UserQuery(BaseQuery):

    def __call__(self):
        searchView = getMultiAdapter((aq_inner(self.context), self.request),
                                     name='pas_search')
        query = self.request.get('term', '')
        search = searchView.searchUsers
        results = [search(**{f: query}) for f in _user_search_fields]
        results = searchView.merge(chain(*results), 'userid')
        return json.dumps([(r['userid'], r['description']) for r in results])


class CatalogQuery(BaseQuery):

    @property
    def site_path(self):
        if not hasattr(self, '_site_path'):
            site = getSite()
            self._site_path = '/'.join(site.getPhysicalPath())
        return self._site_path

    def getTitle(self, brain):
        return "%s %s" % (
            brain.Title,
            brain.getPath()[len(self.site_path):]
        )

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = '*%s*' % self.request.get('term', '')
        results = catalog(SearchableText=query)
        return json.dumps([(r.UID, self.getTitle(r)) for r in results])
