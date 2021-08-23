import json
from os import path as path
from typing import Optional

HOME = path.expanduser('~')
DEFAULT_TOKEN_FILE = '.oxApiToken'
DEFAULT_CUSTOMER_FILE = '.oxApiCustomer'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class StringFileCache:
    def __init__(self, parent_dir: str, filename: str):
        self._path = path.abspath(path.join(parent_dir or HOME, filename))
        self._content: Optional[str] = None

    def get(self):
        # from memory first
        if self._content:
            return self._content
        # file is next, if it's there, return it
        if path.exists(self._path) and path.isfile(self._path):
            with open(self._path, 'r') as f:
                self._content = f.read()
        # otherwise it stays None
        return self._content

    def set(self, content):
        if content != self._content:
            # update file only if needed
            with open(self._path, 'w+') as f:
                f.write(content)
        self._content = content
        return self._content


class TokenCache(StringFileCache, metaclass=Singleton):
    def __init__(self, parent_dir: str = HOME):
        super(TokenCache, self).__init__(parent_dir, filename=DEFAULT_TOKEN_FILE)

    def get(self):
        val = super(TokenCache, self).get()
        return json.loads(val) if val else None

    def set(self, val: dict):
        super(TokenCache, self).set(json.dumps(val))


class CustomerCredsCache(StringFileCache, metaclass=Singleton):
    def __init__(self, parent_dir: str = HOME):
        super(CustomerCredsCache, self).__init__(parent_dir, filename=DEFAULT_CUSTOMER_FILE)

    def get(self):
        val = super(CustomerCredsCache, self).get()
        return json.loads(val) if val else None

    def set(self, val: dict):
        super(CustomerCredsCache, self).set(json.dumps(val))
