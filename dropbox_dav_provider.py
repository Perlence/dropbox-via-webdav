from collections import OrderedDict
from os.path import basename
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO as StringIO

import arrow
from dropbox.client import DropboxClient
# from dropbox.session import DropboxSession
from wsgidav.dav_error import DAVError, HTTP_NOT_FOUND
from wsgidav.dav_provider import DAVProvider, DAVCollection, DAVNonCollection
from wsgidav import util
from wsgidav.util import joinUri


class DropboxProvider(DAVProvider):
    def __init__(self, access_token):
        super(DropboxProvider, self).__init__()
        self.client = DropboxClient(access_token)
        # util.log('DropboxProvider connected to %s' % self.conn)

    def getResourceInst(self, path, environ):
        self._count_getResourceInst += 1
        root = FolderCollection('/', environ)
        return root.resolve('/', path)


class MetadataInfo(object):
    date_format = 'ddd, DD MMM YYYY HH:mm:ss Z'

    def getLastModified(self):
        try:
            modified = self.metadata['modified']
        except KeyError:
            return None
        return arrow.get(modified, self.date_format).timestamp


class FolderCollection(MetadataInfo, DAVCollection):
    def __init__(self, path, environ):
        super(FolderCollection, self).__init__(path, environ)
        self.client = self.provider.client
        self.metadata = self.client.metadata(path)
        # self.metadata = METADATA
        self.members = OrderedDict((basename(content['path']), content)
                                   for content in self.metadata['contents'])

    def getMemberNames(self):
        return [key.encode('utf-8') for key in self.members.keys()]

    def getMember(self, name):
        try:
            member = self.members[name.decode('utf-8')]
        except KeyError:
            raise DAVError(HTTP_NOT_FOUND)
        if member['is_dir']:
            return FolderCollection(joinUri(self.path, name), self.environ)
        else:
            return FileResource(joinUri(self.path, name), self.environ,
                                member)


class FileResource(MetadataInfo, DAVNonCollection):
    def __init__(self, path, environ, metadata):
        super(FileResource, self).__init__(path, environ)
        self.client = self.provider.client
        self.metadata = metadata

    def getContent(self):
        return self.client.get_file(self.metadata['path'])

    def getContentLength(self):
        return self.metadata['bytes']

    def getContentType(self):
        return self.metadata['mime_type'].encode('utf-8')

    def getDisplayName(self):
        return basename(self.metadata['path'])
