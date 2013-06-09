from AccessControl import getSecurityManager
from AccessControl import Unauthorized
import json
import inspect
from zope.interface import implements
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.schema.interfaces import IVocabularyFactory
from Products.Five import BrowserView
from plone.app.widgets.interfaces import IWidgetsView
from plone.app.vocabularies.interfaces import ISlicableVocabulary


_permissions = {
    'plone.app.vocabularies.Users': 'Modify portal content',
    'plone.app.vocabularies.Catalog': 'View'
}

def _parseJSON(s):
    if isinstance(s, basestring):
        s = s.strip()
        if s.startswith('{') and s.endswith('}'): # detect if json
            return json.loads(s)
    return s


class WidgetsView(BrowserView):
    """A view that gives access to various widget related functions.
    """

    implements(IWidgetsView)

    def getVocabulary(self):
        """
        Accepts GET parameters of:
        name: Name of the vocabulary
        query: string or json object of criteria and options.
            json value consists of a structure:
                {
                    criteria: object,
                    sort_on: index,
                    sort_order: (asc|reversed)
                }
        attributes: comma seperated, or json object list
        batch: {
            page: 0-based page of results,
            size: size of paged results
        }
        """
        self.request.response.setHeader("Content-type", "application/json")

        factory_name = self.request.get('name', None)
        if not factory_name:
            return json.dumps({'error': 'No factory provided.'})
        if factory_name not in _permissions:
            return json.dumps({'error': 'Vocabulary lookup not allowed'})
        sm = getSecurityManager()
        if not sm.checkPermission(_permissions[factory_name], self.context):
            raise Unauthorized('You do not have permission to use this vocabulary')
        factory = queryUtility(IVocabularyFactory, factory_name)
        if not factory:
            return json.dumps({
                'error': 'No factory with name "%s" exists.' % factory_name})

        # check if factory excepts query argument
        query = _parseJSON(self.request.get('query', ''))
        attributes = _parseJSON(self.request.get('attributes', ''))
        if isinstance(attributes, basestring) and attributes:
            attributes = attributes.split(',')
        batch = _parseJSON(self.request.get('batch', ''))
        factory_spec = inspect.getargspec(factory.__call__)
        if query and len(factory_spec.args) >= 3 and \
                factory_spec.args[2] == 'query':
            if len(factory_spec.args) >= 4 and \
                    factory_spec.args[3] == 'batch':
                vocabulary = factory(self.context, query, batch)
            else:
                vocabulary = factory(self.context, query)
        else:
            vocabulary = factory(self.context)

        try:
            total = len(vocabulary)
        except AttributeError:
            total = 0 # do not error if object does not support __len__
                      # we'll check again later if we can figure some size out
        if 'size' not in batch or 'page' not in batch:
            batch = None # batching not providing correct options
        if batch and ISlicableVocabulary.providedBy(vocabulary):
            # must be slicable for batching support
            start = batch['page'] * batch['size']
            end = start + batch['size']
            vocabulary = vocabulary[start:end]

        items = []
        if attributes:
            item = {}
            for vocab_item in vocabulary:
                for attr in attributes:
                    vocab_value = vocab_item.value
                    item[attr] = getattr(vocab_value, attr, None)
                items.append(item)
        else:
            for item in vocabulary:
                items.append({'id': item.token, 'text': item.title})

        if total == 0:
            total = len(items)

        return json.dumps({
            'results': items,
            'total': total
        })

    def bodyDataOptions(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        return {
            'data-portal-navigation-url': portal_state.navigation_root_url(),
            'data-portal-url': portal_state.portal_url(),
            'data-context-url': self.context.absolute_url(),
            'data-pattern': 'plone-tabs',
        }
