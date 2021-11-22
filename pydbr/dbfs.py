import base64
from typing import List
from .common import Api, DatabricksLinkException, ERR_RESOURCE_DOES_NOT_EXIST
from .databricks_data_classes import *

class DBFS(Api):
    def __init__(self, link):
        super().__init__(link, path='dbfs')

    def list(self, path=None) -> List[DatabricksFileInfo]:
        "List DBFS items at given path. Alias for ls"
        get_result = self.link.get(
            self.path('list'),
            params=dict(path=(path or '/')))
        files = get_result.get('files', [])
        result = [DatabricksFileInfo(**f) for f in files]
        return result

    def info(self, path=None) -> DatabricksFileInfo:
        """Get information for DBFS item."""
        response = self.link.get(
            self.path('get-status'),
            params=dict(path=(path or '/')))
        result = DatabricksFileInfo(**response)
        return result

    def ls(self, path=None) -> List[DatabricksFileInfo]:
        """List DBFS items at given path."""
        return self.list(path)

    def exists(self, path) -> bool:
        """Check if given DBFS item exists."""
        try:
            self.list(path)
            result = True
        except DatabricksLinkException as exc:
            if exc.error_code == ERR_RESOURCE_DOES_NOT_EXIST:
                result = False
        return result


    def read_raw(self, path, offset=None, length=None):
        """Read a chunk from a DBFS file and return the API response."""
        offset = offset or 0
        length = length or 1048576

        response = self.link.get(
            self.path('read'),
            params=dict(path=path,offset=offset,length=length),)
        return response

    def read(self, path, offset=None, length=None) -> bytes:
        """Read a chunk from a DBFS file and return the bytes."""
        response = self.read_raw(path, offset, length)
        return base64.b64decode(response['data'])


    def read_all(self, path, chunk_size=None) -> bytes:
        """Read entire file from DBFS and return they bytes."""
        chunk_size = chunk_size or 1048576
        content = b''
        offset = 0
        while (True):
            this_read = self.read_raw(
                    path, 
                    offset=offset,
                    length=chunk_size)
            if not this_read['bytes_read']:
                break
            offset += this_read['bytes_read']
            content += base64.b64decode(this_read['data'])
        return content

    def mkdirs(self, path):
        """Create missing DBFS directories recursively."""
        response = self.link.post(
            self.path('mkdirs'),
            json=dict(path=path))
        return response

    def delete(self, path, recursive=False):
        """Remove DBFS item. Alias for rm"""
        response = self.link.post(
            self.path('delete'),
            json=dict(path=path,
                      recursive=str(recursive).lower()))
        return response

    def rm(self, path, recursive=False):
        """Remove DBFS items."""
        return self.delete(path, recursive)
