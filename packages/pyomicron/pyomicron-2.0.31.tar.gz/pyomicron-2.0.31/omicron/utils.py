# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2016)
#
# This file is part of PyOmicron.
#
# PyOmicron is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyOmicron is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyOmicron.  If not, see <http://www.gnu.org/licenses/>.

"""Miscellaneous utilities
"""

import os
import subprocess
import sys
import time
from pathlib import Path
from shutil import which
from tempfile import gettempdir

from gwpy.time import from_gps
from packaging.version import Version

from . import const


def get_output_directory(args):
    """Return the output directory as parsed from the command-line args
    """
    return str(get_output_path(args))


def get_output_path(args):
    """Return the output path as parsed from the command-line args
    """
    if args.output_dir is None:
        if args.gps is None:
            dirname = args.group
        else:
            dirname = "{0}-{1[0]}-{1[1]}".format(args.group, args.gps)
        return (const.OMICRON_PROD / dirname).resolve(strict=False)
    return args.output_dir.resolve(strict=False)


def find_omicron():
    """Find the omicron executable in the environment

    Either via `PATH` or relative to the current python interpreter

    Returns
    -------
    path : `pathlib.Path`
        the path of the omicron executable

    Raises
    ------
    RuntimeError
        if omicron cannot be found, or is not executable
    """
    exe = which(
        "omicron",
        path=os.pathsep.join((
            os.getenv("PATH", ""),
            str(Path(sys.executable).parent),
        )),
    )
    if not exe or not os.access(exe, os.X_OK):
        raise RuntimeError(
            "cannot locate omicron in environment or is not executable"
        )
    return Path(exe).resolve()


def get_omicron_version(executable=None):
    """Parse the version number from the Omicron executable path

    Parameters
    ----------
    executable : `str`
        path of Omicron executable

    Returns
    -------
    version : `str`
        the Omicron-format version string, e.g. `vXrY`

    Examples
    --------
    >>> get_omicron_version()
    '2.1.0'
    """  # noqa: E501
    executable = executable or find_omicron()
    try:
        return Version(
            subprocess.check_output(
                [executable, "version"],
                env={"OMICRON_HTML": gettempdir()},
            ).decode("utf-8").rsplit(maxsplit=1)[-1],
        )
    except subprocess.CalledProcessError as ex:
        raise RuntimeError(f"failed to determine omicron version from executable: {str(ex)}")


def astropy_config_path(parent, update_environ=True):
    """Create and return a directory for a temporary astropy config path
    """
    parent = Path(parent)
    astropath = parent / ".config" / "astropy"
    astropath.mkdir(exist_ok=True, parents=True)
    confpath = astropath.parent
    if update_environ:
        os.environ["XDG_CONFIG_HOME"] = str(confpath)
    return confpath


def gps_to_hr(gps):
    """
    Convert a gps time to a human readable string for our log files
    @param LIGOTimeGPS | int | float gps: time to consider
    @return str: hr string eg: "1386527433 (12/13/23 18:30:16)"
    """
    dt = from_gps(int(gps))
    dt_str = dt.strftime('%x %X')
    ret = f'{int(gps)} ({dt_str})'
    return ret


def deltat_to_hr(dt):
    """
    Convert a time in seconds to a human readable string
    @param int dt: delta t
    @return str: <sec> [<day>] HH:MM:SS
    """
    ret = f'{dt}'
    if dt > 0:
        day = f'{int(dt) / 86400}' if dt >= 86400 else ''
        time_str = time.strftime('%H:%M:%S', time.gmtime(int(dt)))
        ret += f' - {day}  {time_str}'

    return ret


def write_segfile(segs, outfile):
    """
    write a segment list to a file with human readable string
    @param SegList segs: segment list
    @param Path|str outfile: path to output file
    @return:  None
    """
    with open(outfile, 'w') as f:
        print('# seg   start   stop    duration', file=f)
        for seg in segs:
            print(f'# {gps_to_hr(seg[0])} {gps_to_hr(seg[1])}  {deltat_to_hr(abs(seg))}', file=f)
            print(f'{seg[0]} {seg[1]}  {abs(seg)}', file=f)
