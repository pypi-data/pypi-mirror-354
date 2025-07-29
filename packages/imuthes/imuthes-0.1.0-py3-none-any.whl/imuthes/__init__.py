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

from .classproperty import ClassProperty
from .configuration import get_configuration
from .display_table import DisplayColumn, DisplayTable
from .make_link import make_link
from .mapping import Mapping, NamedMapping, DeepNamedMapping
from .singleton import Singleton

__all__ = [
    "ClassProperty",
    "DisplayColumn",
    "DisplayTable",
    "Mapping",
    "NamedMapping",
    "DeepNamedMapping",
    "Singleton",
    "get_configuration",
    "make_link",
]


__import__("pkg_resources").declare_namespace(__name__)  # pragma: no cover
