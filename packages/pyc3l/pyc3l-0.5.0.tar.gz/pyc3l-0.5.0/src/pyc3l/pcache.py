# -*- coding: utf-8 -*-

import pickle
import fcntl
from contextlib import contextmanager


class DirtyDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dirty = False

    def __setitem__(self, key, value):
        self._dirty = True
        super().__setitem__(key, value)

    def __delitem__(self, key):
        self._dirty = True
        super().__delitem__(key)

    def update(self, *args, **kwargs):
        self._dirty = True
        super().update(*args, **kwargs)

    def clear(self):
        self._dirty = True
        super().clear()

    def pop(self, key, default=None):
        self._dirty = True
        return super().pop(key, default)

    def popitem(self):
        self._dirty = True
        return super().popitem()

    def setdefault(self, key, default=None):
        if key not in self:
            self._dirty = True
        return super().setdefault(key, default)

    def is_dirty(self):
        return self._dirty


@contextmanager
def locked_pickle_cache(path):
    # Open the file in read/write mode, create if not exists.
    try:
        f = open(path, 'r+b')
    except FileNotFoundError:
        f = open(path, 'w+b')
    with f:
        # Lock the file exclusively.
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.seek(0)
            data = pickle.load(f)
            if not isinstance(data, dict):
                data = {}
        except (EOFError, pickle.UnpicklingError):
            data = {}
        cache = DirtyDict(data)
        yield cache
        # Save only if modified.
        if cache.is_dirty():
            f.seek(0)
            pickle.dump(dict(cache), f)
            f.truncate()
        fcntl.flock(f, fcntl.LOCK_UN)


class PersistentCache(object):
    """Dict like key/value store that persists to disk.

    Only implements get/set/del methods.

    """

    def __init__(self, path):
        self.path = path

    def __getitem__(self, key):
        with locked_pickle_cache(self.path) as cache:
            return cache[key]

    def __setitem__(self, key, value):
        with locked_pickle_cache(self.path) as cache:
            cache[key] = value
