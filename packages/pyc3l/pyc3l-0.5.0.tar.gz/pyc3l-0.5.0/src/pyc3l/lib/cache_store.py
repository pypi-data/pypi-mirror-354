# -*- coding: utf-8 -*-

import os.path

import sys
import time

from kids.cache import cache
import kids.file as kf


class FileStore(object):
    """A simple file-based key-value store.

    It maps a value to a file thanks to the ``key_to_path`` method.

    It doesn't clear any files. It's up to the user to manage the cache size.
    
    """

    def __init__(self, path, key_to_path=None, encode=(lambda v: v), decode=(lambda c: c)):
        self._path = path
        self._key_to_path = key_to_path
        self._encode = encode
        self._decode = decode

    def is_valid(self, path, key):
        full_path = os.path.join(self._path, path)
        if not os.path.exists(full_path):
            return False
        return True

    def cache_maintenance(self):
        pass

    def __getitem__(self, key):
        path = self._key_to_path(key)
        if not self.is_valid(path, key):
            raise KeyError(key)
        return self.read_file(path)

    def read_file(self, full_path):
        return self._decode(kf.get_contents(full_path))

    def __setitem__(self, key, value):
        import pdb; pdb.set_trace()
        path = self._key_to_path(key)
        self.save_file(path, value)
        self.cache_maintenance()

    def save_file(self, path, value):
        full_path = os.path.join(self._path, path)
        kf.mkdir(kf.dirname(full_path), recursive=True)
        kf.put_contents(full_path, self._encode(value))

    def __delitem__(self, key):
        import pdb; pdb.set_trace()
        path = self._key_to_path(key)
        if not self.is_valid(path, key):
            raise KeyError(key)
        self.remove_file(path)

    def remove_file(self, path):
        full_path = os.path.join(self._path, path)
        os.remove(full_path)
        
    def clear(self):
        import pdb; pdb.set_trace()  # fmt: skip
        kf.rm(self._path, recursive=True)
        
    def __getattr__(self, key):
        if key.startswith("_"):
            raise AttributeError(key)
        return self.__class__(os.path.join(self._path, key))


class TTLFileStoreMixin(FileStore):

    def __init__(self, *args, **kwargs):
        if "ttl" in kwargs:
            self._ttl = kwargs.pop("ttl")
        super().__init__(*args, **kwargs)

    def is_valid(self, path, key):
        if super().is_valid(path, key) is False:
            return False
        if self._ttl is None:
            return True
        if time.time() - os.path.getmtime(path) < self._ttl:
            return True
        self.remove_file(path)
        return False


class MaxSizeFileStoreMixin(FileStore):

    def __init__(self, *args, **kwargs):
        if "max_size" in kwargs:
            self._max_size = kwargs.pop("max_size")
        super().__init__(*args, **kwargs)

    def cache_maintenance(self):
        if self._max_size is None:
            return
        import ipdb; ipdb.set_trace()  # fmt: skip
        total_size = self.total_size()
        for f, s in paths_size:
            os.remove(os.path.join(self._path, paths_by_ts.pop(0)))
            total_size -= s
            if total_size <= self._max_size:
                break

    ## YYYvlab: should cache and maintain
    def get_paths_by_ts(self):
        return sorted(
            os.listdir(self._path),
            key=lambda f: os.path.getmtime(os.path.join(self._path, f))
        )

    ## YYYvlab: should cache and maintain
    def get_paths_size(self):
        return [
            (f, os.path.getsize(os.path.join(self._path, f)))
            for f in self.get_paths_by_ts()
        ]

    ## YYYvlab: should cache and maintain
    def total_size(self):
        return sum(s for _, s in self.get_paths_size())
    

class XDGCacheFileStore(FileStore):

    def __init__(self, store_name, key_to_path, encode=(lambda v: v), decode=(lambda c: c)):
        appname = sys.argv[0].split("/")[-1]
        path = os.path.join((
            os.environ.get('XDG_CACHE_HOME') or
            os.path.join(os.path.expanduser('~'), '.cache')
        ), appname, store_name)
        super().__init__(path, key_to_path, encode=encode, decode=decode)


class FullFileStore(XDGCacheFileStore, TTLFileStoreMixin, MaxSizeFileStoreMixin): pass


class FileStoreFactory(object):

    def __init__(self, name="fscache", store_class=FullFileStore, *args, **kwargs):
        self._name = name
        self._store_class = store_class
        self._args = args
        self._kwargs = kwargs

    def obj_to_name(self, obj):
        return obj.__qualname__
        
    def __call__(self, obj, *args, **kwargs):
        name = self.obj_to_name(obj)
        a = args + self._args
        kw = {**kwargs, **self._kwargs}
        return self._store_class(os.path.join(self._name, name), *a, **kw)