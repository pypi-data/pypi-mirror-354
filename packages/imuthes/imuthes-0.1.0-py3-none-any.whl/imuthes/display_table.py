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

import datetime
from typing import Iterable


from typing import Callable


def attr_getter_factory(name: str) -> Callable:
    if "." in name:
        remainder, inner_name = name.rsplit(".", 1)

        def f(obj):
            return getattr(attr_getter_factory(remainder)(obj), inner_name)

    else:

        def f(obj):
            return getattr(obj, name, "")

    return f


class DisplayColumn:
    """Utility to specify column characteristics for :class:`imuthes.DisplayTable`.

    While the column name can be sufficient, this allows to define alignment and heading of a column.

    .. list-table:: Possible values for ``format``

       * - ``<``
         - left aligned (default)
       * - ``>``
         - right aligned
       * - ``^``
         - centered


    :param name: Column name. If **class-instances** will be added to a table, this can use *dotted* format to specify deeper structure.
    :param format: For now, just the alignment.
    :param header: Header in table column.
    :param is_key: Mark as KEY column.
    :param show_none: Show None (or NULL) explicitly.
    """

    def __init__(
        self,
        name: str,
        format: str = "",
        header: str = None,
        is_key: bool = False,
        show_none: bool = False,
    ):
        self.name = name
        self.format = format
        self.header = name.title() if header is None else header
        self.is_key = is_key
        self.show_none = show_none


class DisplayTable:
    """Table to be displayed in console or browser or as Markdown.

    Values are converted to ``str`` when they are added. If you want to support your own type, make sure to add a ``__str__`` method to the class.

    ============  =================
    Type          Format
    ============  =================
    ``date``      YY-MM-DD
    ``time``      HH:MM:SS
    ``datetime``  YY-MM-DD HH:MM:SS
    ============  =================

    :param args: The columns to display. Either the name of the column, or :class:`imuthes.DisplayColumn`.
    """

    def __init__(self, *args: str | DisplayColumn | Iterable) -> None:
        self._rows = []
        self._columns = []
        for arg in args:
            if not isinstance(arg, DisplayColumn):
                arg = DisplayColumn(arg)
            self._columns.append(arg)

    @property
    def columns(self) -> Iterable[DisplayColumn]:
        return self._columns[:]

    def append(self, value):
        """Append row to table.

        The value can either be a dictionary with the column names, or an object that exposes
        the column names as attributes."""
        if hasattr(value, "__getitem__"):
            f = lambda x: value.get(x.name, "")  # noqa: E731
        else:  # expecting to get an object, but here the name might be nested...
            f = lambda x: attr_getter_factory(x.name)(value)  # noqa: E731
        # row = [f(i) if f(i) is not None else "_None_" for i in self._columns]
        row = [f(i) for i in self._columns]
        for n, i in enumerate(row):
            # if isinstance(i, str) and "\n" in i:
            #     row[n] = i.replace("\n", "<br/>")
            if i is None or isinstance(i, bool):
                continue
            elif isinstance(i, datetime.datetime):
                row[n] = i.strftime("%y-%m-%d %H:%M:%S")
            elif isinstance(i, datetime.date):
                row[n] = i.strftime("%y-%m-%d")
            elif isinstance(i, datetime.time):
                row[n] = i.strftime("%H:%M:%S")
            else:
                row[n] = str(i)
        self._rows.append(row)

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, index):
        return self._rows[index]

    def ascii(self) -> str:
        """Render using ASCII Box

        :return: Multiline String
        """
        # determine length and guess type if not format provided
        columns = {
            i.name: [
                i.format,
                len(i.header) + 2 if i.is_key else len(i.header),
                i.show_none,
            ]
            for i in self._columns
        }
        rows = []
        for row in self._rows:
            row = row[:]
            for n, c in enumerate(columns.keys()):
                if isinstance(row[n], bool):
                    if not columns[c][0]:
                        columns[c][0] = "^"
                    columns[c][1] = max(columns[c][1], 5)
                    row[n] = "*True*" if row[n] else "*False*"
                elif isinstance(row[n], (int, float)):
                    if not columns[c][0]:
                        columns[c][0] = ">"
                    columns[c][1] = max(columns[c][1], len(str(row[n])))
                elif row[n] is None:
                    row[n] = "*None*" if columns[c][2] else ""
                    columns[c][1] = max(columns[c][1], len(row[n]))
                else:
                    columns[c][1] = max(columns[c][1], len(row[n]))
            rows.append(row)

        formatter = (
            "║ {:"
            + "} │ {:".join(
                [f'{columns[i][0] or "<"}{str(columns[i][1])}' for i in columns]
            )
            + "} ║"
        )

        result = [
            "╔═" + "═╤═".join(["═" * columns[i][1] for i in columns.keys()]) + "═╗",
            formatter.format(
                *[f"*{i.header}*" if i.is_key else i.header for i in self._columns]
            ),
            "╟─" + "─┼─".join(["─" * columns[i][1] for i in columns.keys()]) + "─╢",
        ]
        result.extend([formatter.format(*i) for i in rows])
        result.append(
            "╚═" + "═╧═".join(["═" * columns[i][1] for i in columns.keys()]) + "═╝"
        )

        return "\n".join(result)

    def markdown(self) -> str:
        """Render the provided data as a Markdown string.

        :return: Markdown string
        """
        # determine length and guess type if not format provided
        columns = {
            i.name: [
                i.format,
                len(i.header) + 4 if i.is_key else len(i.header),
                ":" if i.format in "<^" else "-",
                ":" if i.format and i.format in "^>" else "-",
                i.show_none,
            ]
            for i in self._columns
        }
        rows = []
        for row in self._rows:
            row = row[:]
            for n, c in enumerate(columns.keys()):
                if isinstance(row[n], bool):
                    if not columns[c][0]:
                        columns[c][0] = "^"
                        columns[c][2] = columns[c][3] = ":"
                    columns[c][1] = max(columns[c][1], 7)
                    row[n] = (
                        "&check;" if row[n] else ""
                    )  # convert to display_table chan
                elif isinstance(row[n], (int, float)):
                    if not columns[c][0]:
                        columns[c][0] = ">"
                        columns[c][3] = ":"
                    columns[c][1] = max(columns[c][1], len(str(row[n])))
                elif row[n] is None:
                    row[n] = "_None_" if columns[c][4] else ""
                    columns[c][1] = max(columns[c][1], len(row[n]))
                else:
                    columns[c][1] = max(columns[c][1], len(row[n]))
            rows.append(row)

        formatter = (
            "| {:"
            + "} | {:".join(
                [f'{columns[i][0] or "<"}{str(columns[i][1])}' for i in columns]
            )
            + "} |"
        )

        result = [
            formatter.format(
                *[f"**{i.header}**" if i.is_key else i.header for i in self._columns]
            ),
            "|"
            + "|".join(
                [
                    columns[i][2] + "-" * columns[i][1] + columns[i][3]
                    for i in columns.keys()
                ]
            )
            + "|",
        ]
        result.extend([formatter.format(*i) for i in rows])

        return "\n".join(result)
