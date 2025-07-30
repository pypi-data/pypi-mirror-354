from caselessly.logging import logger
from caselessly.list import caselesslist

logger = logger.getChild(__name__)


class caselessdict(dict):
    """A dictionary subclass that doesn't consider case-sensitivity for string keys."""

    _keymap: dict[str, str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._keymap: dict[str, str] = {}

        for key in self.keys():
            _key = key.casefold() if isinstance(key, str) else key
            self._keymap[_key] = key

    def __contains__(self, key: str) -> bool:
        _key = key.casefold() if isinstance(key, str) else key
        return _key in self._keymap

    def __eq__(self, other: dict) -> bool:
        if not isinstance(other, dict):
            raise TypeError("The 'other' argument must have a dictionary value!")

        if not len(self) == len(other):
            return False

        for key, value in other.items():
            _key = key.casefold() if isinstance(key, str) else key

            if not _key in self._keymap:
                return False
            elif not self[self._keymap[_key]] == value:
                return False

        return True

    def __setitem__(self, key: object, value: object):
        _key = key.casefold() if isinstance(key, str) else key

        self._keymap[_key] = key

        super().__setitem__(self._keymap[_key], value)

    def __getitem__(self, key: object) -> object:
        _key = key.casefold() if isinstance(key, str) else key

        if not _key in self._keymap:
            raise KeyError(f"The dictionary does not contain a '{key}' key!")

        return super().__getitem__(self._keymap[_key])

    def __delitem__(self, key: str):
        _key = key.casefold() if isinstance(key, str) else key

        if _key in self._keymap:
            result = super().__delitem__(self._keymap[_key])
            del self._keymap[_key]
            return result
        else:
            raise KeyError(f"The dictionary does not contain a '{key}' key!")

    def get(self, key: object, default: object = None) -> object | None:
        _key = key.casefold() if isinstance(key, str) else key

        if isinstance(_key, str) and _key in self._keymap:
            return self[self._keymap[_key]]

        return default

    def keys(self) -> caselesslist[str]:
        return caselesslist(super().keys())


# Shorthand alias
cidict = caselessdict
