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

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = '*%s*' % self.request.get('term', '')
        results = catalog(SearchableText=query)
        return json.dumps([(r.UID, r.Title) for r in results])
