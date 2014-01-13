# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five import BrowserView
from Products.ZCTextIndex.ParseTree import ParseError
from logging import getLogger
from plone.app.vocabularies.interfaces import ISlicableVocabulary
from plone.app.widgets.interfaces import IFieldPermissionChecker
from types import FunctionType
from zope.component import queryAdapter
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import inspect
import json

logger = getLogger(__name__)


_permissions = {
    'plone.app.vocabularies.Users': 'Modify portal content',
    'plone.app.vocabularies.Catalog': 'View',
    'plone.app.vocabularies.Keywords': 'Modify portal content',
    'plone.app.vocabularies.SyndicatableFeedItems': 'Modify portal content'
}


def _parseJSON(s):
    if isinstance(s, basestring):
        s = s.strip()
        if (s.startswith('{') and s.endswith('}')) or \
                (s.startswith('[') and s.endswith(']')):  # detect if json
            return json.loads(s)
    return s


_unsafe_metadata = ['Creator', 'listCreators', 'author_name', 'commentors']
_safe_callable_metadata = ['getURL', 'getPath']


class VocabularyView(BrowserView):

    def error(self):
        return json.dumps({
            'results': [],
            'total': 0,
            'error': True
        })

    def __call__(self):
        """
        Accepts GET parameters of:
        name: Name of the vocabulary
        field: Name of the field the vocabulary is being retrieved for
        query: string or json object of criteria and options.
            json value consists of a structure:
                {
                    criteria: object,
                    sort_on: index,
                    sort_order: (asc|reversed)
                }
        attributes: comma seperated, or json object list
        batch: {
            page: 1-based page of results,
            size: size of paged results
        }
        """
        context = self.context
        self.request.response.setHeader("Content-type", "application/json")

        factory_name = self.request.get('name', None)
        field_name = self.request.get('field', None)
        if not factory_name:
            return json.dumps({'error': 'No factory provided.'})
        authorized = None
        sm = getSecurityManager()
        if (factory_name not in _permissions or
                not IPloneSiteRoot.providedBy(context)):
            # Check field specific permission
            if field_name:
                permission_checker = queryAdapter(context,
                                                  IFieldPermissionChecker)
                if permission_checker is not None:
                    authorized = permission_checker.validate(field_name,
                                                             factory_name)
            if not authorized:
                return json.dumps({'error': 'Vocabulary lookup not allowed'})
        # Short circuit if we are on the site root and permission is
        # in global registry
        elif not sm.checkPermission(_permissions[factory_name], context):
            return json.dumps({'error': 'Vocabulary lookup not allowed'})

        factory = queryUtility(IVocabularyFactory, factory_name)
        if not factory:
            return json.dumps({
                'error': 'No factory with name "%s" exists.' % factory_name})

        # check if factory accepts query argument
        query = _parseJSON(self.request.get('query', ''))
        batch = _parseJSON(self.request.get('batch', ''))

        if type(factory) is FunctionType:
            factory_spec = inspect.getargspec(factory)
        else:
            factory_spec = inspect.getargspec(factory.__call__)
        try:
            supports_batch = False
            vocabulary = None
            if query and 'query' in factory_spec.args:
                if 'batch' in factory_spec.args:
                    vocabulary = factory(self.context,
                                         query=query, batch=batch)
                    supports_batch = True
                else:
                    vocabulary = factory(self.context, query=query)
            elif query:
                raise KeyError("The vocabulary factory %s does not support "
                               "query arguments",
                               factory)

            if batch and supports_batch:
                    vocabulary = factory(context, query, batch)
            elif query:
                    vocabulary = factory(context, query)
            else:
                vocabulary = factory(context)

        except (TypeError, ParseError):
            raise
            return self.error()

        try:
            total = len(vocabulary)
        except TypeError:
            total = 0  # do not error if object does not support __len__
                       # we'll check again later if we can figure some size
                       # out
        if batch and ('size' not in batch or 'page' not in batch):
            batch = None  # batching not providing correct options
            logger.error("A vocabulary request contained bad batch "
                         "information. The batch information is ignored.")
        if batch and not supports_batch and \
                ISlicableVocabulary.providedBy(vocabulary):
            # must be slicable for batching support
            page = int(batch['page'])
            # page is being passed in is 1-based
            start = (max(page-1, 0)) * int(batch['size'])
            end = start + int(batch['size'])
            vocabulary = vocabulary[start:end]

        items = []

        attributes = _parseJSON(self.request.get('attributes', ''))
        if isinstance(attributes, basestring) and attributes:
            attributes = attributes.split(',')

        if attributes:
            base_path = '/'.join(context.getPhysicalPath())
            for vocab_item in vocabulary:
                item = {}
                for attr in attributes:
                    key = attr
                    if ':' in attr:
                        key, attr = attr.split(':', 1)
                    if attr in _unsafe_metadata:
                        continue
                    if key == 'path':
                        attr = 'getPath'
                    vocab_value = vocab_item.value
                    val = getattr(vocab_value, attr, None)
                    if callable(val):
                        if attr in _safe_callable_metadata:
                            val = val()
                        else:
                            continue
                    if key == 'path':
                        val = val[len(base_path):]
                    item[key] = val
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
