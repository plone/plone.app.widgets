from zope.interface import implements
from plone.namedfile.storages import MAXCHUNKSIZE
from plone.namedfile.interfaces import IStorage


class Zope2FileUploadStorable(object):
    implements(IStorage)

    def store(self, data, blob):
        data.seek(0)

        fp = blob.open('w')
        block = data.read(MAXCHUNKSIZE)
        while block:
            fp.write(block)
            block = data.read(MAXCHUNKSIZE)
        fp.close()
