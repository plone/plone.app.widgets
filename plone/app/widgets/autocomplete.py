import json
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.Five import BrowserView


class AutocompleteView(BrowserView):
    """
    """

    def __call__(self):
        self.request.response.setHeader("Content-type", "application/json")

        source_name = self.request.get('source', None)
        if not source_name:
            return json.dumps({'error': 'No source provided'})

        source = queryUtility(IVocabularyFactory, source_name)
        if not source:
            return json.dumps({
                'error': 'No source with name "%s".' % source_name})

        source = source(self.context)

        items = []
        for item in source:
            items.append(item.token)

        # TODO: add option for querying
        # TODO: add option for limiting number of results
        # TODO: add option for batching
        # TODO: add option for sorting

        return json.dumps(items)
