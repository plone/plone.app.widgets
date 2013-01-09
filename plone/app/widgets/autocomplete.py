import json
import inspect
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.Five import BrowserView


class AutocompleteView(BrowserView):
    """
    """

    def __call__(self):
        self.request.response.setHeader("Content-type", "application/json")

        factory_name = self.request.get('source', None)
        if not factory_name:
            return json.dumps({'error': 'No source provided'})

        factory = queryUtility(IVocabularyFactory, factory_name)
        if not factory:
            return json.dumps({
                'error': 'No source with name "%s".' % factory_name})

        # check if factory excepts query argument
        query = self.request.get('query', '')
        factory_spec = inspect.getargspec(factory.__call__)
        if query and len(factory_spec.args) >= 3 and \
                factory_spec.args[2] == 'query':
            vocabulary = factory(self.context, query)
        else:
            vocabulary = factory(self.context)

        items = []
        for item in vocabulary:
            items.append(item.token)

        # TODO: add option for limiting number of results
        # TODO: add option for batching
        # TODO: add option for sorting

        return json.dumps(items)
