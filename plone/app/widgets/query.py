import json
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.batching import Batch
from Products.Five import BrowserView


class SourcesView(BrowserView):
    """
    """

    def __call__(self):
        self.request.response.setHeader("Content-type", "application/json")

        name = self.request.get('name')
        source = queryUtility(IVocabularyFactory, name)
        if not source:
            return json.dumps({'error': 'No source with name "%s".' % name})
        source = source(self.context)

        pagenumber = self.request.get('pagenumber', 1)
        pagesize = self.request.get('pagesize', 3)
        batch = Batch.fromPagenumber(
            [item.title for item in source],
            pagesize=pagesize, pagenumber=pagenumber)

        result = {'items': [item for item in batch]}
        if batch.multiple_pages:
            result['batch'] = {
                'pagesize': pagesize,
                'pagenumber': pagenumber,
            }

        return json.dumps(result)
