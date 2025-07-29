# === nanosignfs/core.py ===

import os
from fuse import FUSE, Operations
from . import signer
from .config import STORAGE_PATH

class NanoSignFS(Operations):
    def __init__(self):
        self.root = STORAGE_PATH
        os.makedirs(self.root, exist_ok=True)

    def _full_path(self, path):
        return os.path.join(self.root, path.lstrip('/'))

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        if not os.path.exists(full_path):
            raise FileNotFoundError
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in (
            'st_atime', 'st_ctime', 'st_gid', 'st_mode',
            'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)
        return ['.', '..'] + os.listdir(full_path)

    def create(self, path, mode):
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def open(self, path, flags):
        return os.open(self._full_path(path), flags)

    def read(self, path, size, offset, fh):
        with open(self._full_path(path), 'rb') as f:
            f.seek(offset)
            return f.read(size)

    def write(self, path, data, offset, fh):
        full_path = self._full_path(path)
        with open(full_path, 'r+b' if os.path.exists(full_path) else 'wb') as f:
            f.seek(offset)
            f.write(data)
        signer.sign_file(full_path)
        return len(data)

