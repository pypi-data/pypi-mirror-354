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
import click


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.pass_context
def main(ctx, **kwargs):
    """Imuthes Utilities"""
    ctx.ensure_object(dict)


@main.command()
@click.option(
    "-t",
    "--target",
    type=click.Path(exists=True, path_type=pathlib.Path),
    required=True,
    help="Target",
)
@click.option(
    "-l",
    "--link",
    type=click.Path(path_type=pathlib.Path),
    required=True,
    help="will be created",
)
@click.pass_context
def make_link(ctx, target, link):
    """Create symbolic link (or junction)"""

    make_link(target=target, link=link)
