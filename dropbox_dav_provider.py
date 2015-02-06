from collections import OrderedDict
from io import BytesIO
from os.path import basename

import arrow
from dropbox.client import DropboxClient, ErrorResponse
# from dropbox.session import DropboxSession
from wsgidav.dav_error import DAVError, HTTP_NOT_FOUND, HTTP_INTERNAL_ERROR
from wsgidav.dav_provider import DAVProvider, _DAVResource
from wsgidav.util import joinUri


class DropboxProvider(DAVProvider):
    def __init__(self, access_token):
        super(DropboxProvider, self).__init__()
        self.client = DropboxClient(access_token)

    def getResourceInst(self, path, environ):
        self._count_getResourceInst += 1
        try:
            metadata = self.client.metadata(path)
        except ErrorResponse as err:
            if err.status == 404:
                return
            raise
        if metadata.get('is_deleted', False):
            return None
        return DropboxResource(path, metadata, environ)


class DropboxResource(_DAVResource):
    date_format = 'ddd, DD MMM YYYY HH:mm:ss Z'

    def __init__(self, path, metadata, environ):
        super(DropboxResource, self).__init__(path, metadata['is_dir'],
                                              environ)
        self.metadata = metadata
        self.client = self.provider.client

    def supportRanges(self):
        return False

    @property
    def members(self):
        try:
            contents = self.metadata['contents']
        except KeyError:
            self.metadata = self.client.metadata(self.path)
            contents = self.metadata['contents']
        return OrderedDict((basename(content['path']), content)
                           for content in contents)

    def getMemberNames(self):
        return [key.encode('utf-8') for key in self.members.keys()]

    def getMember(self, name):
        try:
            member = self.members[name.decode('utf-8')]
        except KeyError:
            raise DAVError(HTTP_NOT_FOUND)
        return DropboxResource(joinUri(self.path, name), member, self.environ)

    def getLastModified(self):
        try:
            modified = self.metadata['modified']
        except KeyError:
            return None
        return arrow.get(modified, self.date_format).timestamp

    def getContent(self):
        return self.client.get_file(self.path)

    def getContentLength(self):
        if self.isCollection:
            return None
        return self.metadata['bytes']

    def getContentType(self):
        if self.isCollection:
            return None
        return self.metadata['mime_type'].encode('utf-8')

    def createCollection(self, name):
        self.client.file_create_folder(joinUri(self.path, name))

    def createEmptyResource(self, name):
        assert '/' not in name
        path = joinUri(self.path, name)
        self.client.put_file(path, '')
        return self.provider.getResourceInst(path, self.environ)

    def beginWrite(self, contentType=None):
        return PutStream(self.client, self.path, overwrite=True)

    def supportRecursiveDelete(self):
        return True

    def delete(self):
        try:
            self.client.file_delete(self.path)
        except ErrorResponse:
            raise DAVError(HTTP_INTERNAL_ERROR)

    def copyMoveSingle(self, destPath, isMove):
        try:
            self.client.file_copy(self.path, destPath)
        except ErrorResponse:
            raise DAVError(HTTP_INTERNAL_ERROR)

    def supportRecursiveMove(self, destPath):
        return True

    def moveRecursive(self, destPath):
        try:
            self.client.file_move(self.path, destPath)
        except ErrorResponse:
            raise DAVError(HTTP_INTERNAL_ERROR)


class PutStream(BytesIO):
    def __init__(self, client, full_path, overwrite=False, parent_rev=None):
        self.client = client
        self.full_path = full_path
        self.overwrite = overwrite
        self.parent_rev = parent_rev

    def close(self):
        self.client.put_file(self.full_path, self, self.overwrite,
                             self.parent_rev)
        super(PutStream, self).close()
