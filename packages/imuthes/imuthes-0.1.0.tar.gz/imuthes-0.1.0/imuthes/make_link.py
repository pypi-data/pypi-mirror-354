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

import os
import pathlib
import subprocess
import sys


def make_link(
    target: pathlib.Path,
    link: pathlib.Path,
) -> None:
    """Create a link pointing to target.

    For Windoze, this will be a ``Junction``, for all other OS, a soft link
    :param target: Target path, this will be pointed to.
    :param link: Link path, this will be created.
    """
    if sys.platform != "win32":
        link = link.resolve()
        target = target.resolve()
        link.symlink_to(target)
    else:
        cmd = ["mklink", "/j", os.fsdecode(link), os.fsdecode(target)]
        proc = subprocess.run(cmd, shell=True, capture_output=True)
        if proc.returncode:
            raise OSError(proc.stderr.decode().strip())
