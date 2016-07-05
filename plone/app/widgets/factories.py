from zope.interface import implementer
from plone.namedfile.storages import MAXCHUNKSIZE
from plone.namedfile.interfaces import IStorage


@implementer(IStorage)
class Zope2FileUploadStorable(object):

    def store(self, data, blob):
        data.seek(0)

        fp = blob.open('w')
        block = data.read(MAXCHUNKSIZE)
        while block:
            fp.write(block)
            block = data.read(MAXCHUNKSIZE)
        fp.close()
