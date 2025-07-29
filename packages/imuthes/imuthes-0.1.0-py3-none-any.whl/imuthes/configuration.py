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

import pathlib
from collections import namedtuple
from typing import Iterable


def container_to_tuple(container):
    if not hasattr(container, "__contains__"):
        raise TypeError
    values = []
    if not hasattr(container, "get"):
        contents = list(container)
        return_func = lambda x: tuple(x)  # noqa: E731
    else:
        keys = list(container.keys())
        Node = namedtuple("Node", keys)
        contents = [container[k] for k in keys]
        return_func = lambda x: Node(*x)  # noqa: E731
    for item in contents:
        if not hasattr(item, "__contains__") or hasattr(
            item, "capitalize"
        ):  # not a container or a string
            values.append(item)
        else:
            values.append(container_to_tuple(item))
    return return_func(values)


def parse_configuration(lines: Iterable[str]):
    result = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", maxsplit=1)
        k, v = k.strip(), v.strip()
        keys = k.split(".")
        r = result
        for i in range(len(keys) - 1):
            if keys[i] not in r:
                r[keys[i]] = {}
            r = r[keys[i]]
        r[keys[-1]] = v

    return container_to_tuple(result)


def get_configuration(path: pathlib.Path):
    """Read PATH and make contents available as (nested) NamedTuple.

    :param path: File with configuration
    """
    with path.open("r") as f:
        return parse_configuration(f.readlines())
