# ------------------------------------------------------------------------------
#  Imuthes by NetLink Consulting GmbH
#
#  Copyright (c) 2025. Bernhard W. Radermacher
#
#  This program is free software: you can redistribute it and/or modify it under
#  the terms of the GNU Lesser General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
#  details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

import collections.abc
from abc import ABCMeta, abstractmethod
from types import MappingProxyType


# noinspection PyUnresolvedReferences
class Mapping(collections.abc.Mapping, metaclass=ABCMeta):
    """Abstract implementation using ``self._data`` for storage.

    Implement ``__init__`` to populate ``self._data``.
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def __getitem__(self, item):
        return self._data[item]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"{str(self._data)}"


class NamedMapping(Mapping):
    """Mapping providing access via attribute name.

    If attribute name contains '_' and is not found, search is repeated with '_' replaced by '-'.

    If not found search is repeated case-insensitive.

    :param kwargs: The values to use for Mapping
    :type kwargs: dict
    """

    __slots__ = ("_data", "_normalized")

    def __init__(self, **kwargs):
        self._data = MappingProxyType({k: v for k, v in kwargs.items()})
        self._normalized = {}
        for k in self._data:
            self._normalized[k.lower()] = self._data[k]

    def __search(self, item):
        if item not in self._data:
            if "_" in item:
                return self.__search(item.replace("_", "-"))
            elif not item.islower():
                return self.__search(item.lower())
            else:
                raise AttributeError(item)
        return self._data[item]

    def __getattr__(self, item):
        return self.__search(item)

    def __str__(self):
        return f"{str(self._data)}"


class DeepNamedMapping(NamedMapping):
    """Deep Mapping providing access via attribute name.

    If attribute name contains '_' and is not found, search is repeated with '_' replaced by '-'.

    If not found search is repeated case-insensitive.

    :param kwargs: The values to use for Mapping
    :type kwargs: dict
    """

    def __init__(self, **kwargs: collections.abc.Mapping):
        # Need to recurse for directories...
        for k, v in kwargs.items():
            if isinstance(v, collections.abc.Mapping):
                kwargs[k] = DeepNamedMapping(**v)
        super().__init__(**kwargs)
