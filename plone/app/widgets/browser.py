from AccessControl import getSecurityManager
from AccessControl import Unauthorized
from logging import getLogger
from plone.app.vocabularies.interfaces import ISlicableVocabulary
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.ZCTextIndex.ParseTree import ParseError
from types import FunctionType
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
import inspect
import json
import mimetypes

import pkg_resources

try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    from plone.dexterity.interfaces import IDexterityFTI
    HAS_DEXTERITY = True
from plone.app.widgets.interfaces import IATCTFileFactory, IDXFileFactory
from plone.uuid.interfaces import IUUID

logger = getLogger(__name__)


_permissions = {
    'plone.app.vocabularies.Users': 'Modify portal content',
    'plone.app.vocabularies.Catalog': 'View',
    'plone.app.vocabularies.Keywords': 'Modify portal content'
}


def _parseJSON(s):
    if isinstance(s, basestring):
        s = s.strip()
        if (s.startswith('{') and s.endswith('}')) or \
                (s.startswith('[') and s.endswith(']')):  # detect if json
            return json.loads(s)
    return s


_unsafe_metadata = ['Creator', 'listCreators']
_safe_callable_metadata = ['getURL', 'getPath']


class FileUploadView(BrowserView):

    def __call__(self):
        req = self.request
        if req.REQUEST_METHOD != 'POST':
            return
        filedata = self.request.form.get("file", None)
        if filedata is None:
            return
        filename = filedata.filename
        content_type = mimetypes.guess_type(filename)[0] or ""

        if not filedata:
            return

        # Determine if the default file/image types are DX or AT based
        ctr = getToolByName(self.context, 'content_type_registry')
        type_ = ctr.findTypeName(filename.lower(), '', '') or 'File'

        DX_BASED = False
        if HAS_DEXTERITY:
            pt = getToolByName(self.context, 'portal_types')
            if IDexterityFTI.providedBy(getattr(pt, type_)):
                factory = IDXFileFactory(self.context)
                DX_BASED = True
            else:
                factory = IATCTFileFactory(self.context)
        else:
            factory = IATCTFileFactory(self.context)

        obj = factory(filename, content_type, filedata)

        if DX_BASED:
            if 'File' in obj.portal_type:
                size = obj.file.getSize()
                content_type = obj.file.contentType
            elif 'Image' in obj.portal_type:
                size = obj.image.getSize()
                content_type = obj.image.contentType

            result = {
                "type": content_type,
                "size": size
            }
        else:
            try:
                size = obj.getSize()
            except AttributeError:
                size = obj.getObjSize()

            result = {
                "type": obj.getContentType(),
                "size": size
            }

        result.update({
            'url': obj.absolute_url(),
            'name': obj.getId(),
            'uid': IUUID(obj),
            'filename': filename
        })
        return json.dumps(result)


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
        self.request.response.setHeader("Content-type", "application/json")

        factory_name = self.request.get('name', None)
        if not factory_name:
            return json.dumps({'error': 'No factory provided.'})
        if factory_name not in _permissions:
            return json.dumps({'error': 'Vocabulary lookup not allowed'})
        sm = getSecurityManager()
        if not sm.checkPermission(_permissions[factory_name], self.context):
            raise Unauthorized('You do not have permission to use this '
                               'vocabulary')
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
            supports_query = False
            supports_batch = False
            if query and len(factory_spec.args) >= 3 and \
                    factory_spec.args[2] == 'query':
                supports_query = True
                if len(factory_spec.args) >= 4 and \
                        factory_spec.args[3] == 'batch':
                    supports_batch = True
            if (not supports_query and query):
                raise KeyError("The vocabulary factory %s does not support query arguments", factory)
            if batch and supports_batch:
                    vocabulary = factory(self.context, query, batch)
            elif query:
                    vocabulary = factory(self.context, query)
            else:
                vocabulary = factory(self.context)
        except (TypeError, ParseError):
            raise
            return self.error()

        try:
            total = len(vocabulary)
        except TypeError:
            total = 0  # do not error if object does not support __len__
                       # we'll check again later if we can figure some size out
        if batch and ('size' not in batch or 'page' not in batch):
            batch = None  # batching not providing correct options
            logger.error("A vocabulary request contained bad batch information."
                      "The batch information is ignored.")
        if batch and not supports_batch and ISlicableVocabulary.providedBy(vocabulary):
            # must be slicable for batching support
            page = int(batch['page'])
            start = (max(page, 0)) * int(batch['size'])
            end = start + int(batch['size'])
            vocabulary = vocabulary[start:end]

        items = []

        attributes = _parseJSON(self.request.get('attributes', ''))
        if isinstance(attributes, basestring) and attributes:
            attributes = attributes.split(',')

        if attributes:
            base_path = '/'.join(self.context.getPhysicalPath())
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
