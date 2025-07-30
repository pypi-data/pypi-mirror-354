#!/usr/bin/env python
# Copyright (C) Duncan Macleod (2016)
#
# This file is part of LIGO-Omicron.
#
# LIGO-Omicron is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LIGO-Omicron is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LIGO-Omicron.  If not, see <http://www.gnu.org/licenses/>.

"""Process LIGO data using the Omicron event trigger generator (ETG)

This utility can be used to process one or more channels or LIGO data using
Omicron with minimal manual labour in determining segments, finding data,
and configuring HTCondor.

The input to this should be an INI-format configuration file that lists the
processing parameters and channels that pass to Omicron, something like:

```ini
[GW]
q-range = 3.3166 150
frequency-range = 4.0 8192.0
frametype = H1_HOFT_C00
state-flag = H1:DMT-CALIBRATED:1
sample-frequency = 16384
chunk-duration = 124
segment-duration = 64
overlap-duration = 4
mismatch-max = 0.2
snr-threshold = 5
channels = H1:GDS-CALIB_STRAIN
```

The above 'GW' group name should then be passed to `omicron-process` along
with any customisations available from the command line, e.g.

```
omicron-process GW --config-file ./config.ini
```

By default `omicron-process` will look at the most recent data available
('online' mode), to run in 'offline' mode, pass the `--gps` argument

```
omicron-process GW --config-file ./config.ini --gps <gpsstart> <gpsstop>
```

The output of `omicron-process` is a Directed Acyclic Graph (DAG) that is
*automatically* submitted to condor for processing.

"""
import logging
import time
import traceback

from omicron_utils.conda_fns import get_conda_run
from omicron_utils.omicron_config import OmicronConfig

from omicron.utils import gps_to_hr, deltat_to_hr, write_segfile

prog_start = time.time()

from gwpy.segments import SegmentList, Segment

import argparse
import configparser
import os
import re
import sys
import shutil
import time
from getpass import getuser
from pathlib import Path
from subprocess import check_call
from tempfile import gettempdir
from time import sleep
from glue import pipeline

from gwpy.io.cache import read_cache
from gwpy.time import to_gps, tconvert

from .. import (const, segments, log, data, parameters, utils, condor, __version__)

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'

try:
    OMICRON_PATH = str(utils.find_omicron())
except RuntimeError:
    OMICRON_PATH = None

DAG_TAG = "omicron"

logger = log.Logger('omicron-process')
# the OmicronConfig class cannot  accept a log message so only  critical errors
old_level = logger.getEffectiveLevel()
logger.setLevel(logging.CRITICAL)
omicron_config = OmicronConfig(logger=logger)
config = omicron_config.get_config()
logger.setLevel(old_level)
logger.info(f'Using config: {omicron_config.path.absolute()}')


def clean_exit(exitcode, tempfiles=None):
    if tempfiles:
        clean_tempfiles(tempfiles)
    sys.exit(exitcode)


def gps2str(gps):
    """Creat a string drom gps time for filenames
    :param LIGOTimeGPS gps: input gps time
    :returns str: something like 20220726.193002
    """
    dt = tconvert(gps)
    ret = dt.strftime('%Y%m%d.%H%M%S')
    return ret


def clean_dirs(dir_list):
    """Remove any empty directories we created
    NB: each of those directories may contain subdirectories which we will also delete if empty
    """
    for adir in dir_list:
        pdir = Path(adir)
        flist = list(pdir.glob('*'))
        if len(flist) == 0:
            pdir.rmdir()
        else:
            can_delete = True
            for file in flist:
                if file.is_dir():
                    can_delete &= remove_empty_dir(file)
                else:
                    # we found a file. Do not delete this direcory
                    can_delete = False

            if can_delete:
                pdir.rmdir()


def remove_empty_dir(dir_path):
    """
    Remove a directory if empty or if all it contains is empty directories.
    This is a recursive function, it calls itself if it finds a directory.
    :@param Path dir_path: directory to check
    :@return boolean: True if directory was deleted
    """
    ret = True
    if not dir_path.is_dir():
        ret = False
    else:
        flist = list(dir_path.glob('*'))
        if len(flist) == 0:
            dir_path.rmdir()
        else:
            for file in flist:
                if file.is_dir():
                    ret = remove_empty_dir(file)
                    if not ret:
                        break
            if ret:
                dir_path.rmdir()
    return ret


def clean_tempfiles(tempfiles):
    for f in map(Path, tempfiles):
        if f.is_dir():
            shutil.rmtree(f)
        else:
            f.unlink()
        logger.debug("Deleted path '{}'".format(f))


def create_parser(config):
    """Create a command-line parser for this entry point
    @param configparser.ConfigParser config: config for our pipelines not Omicron itself

    """

    epilog = """
This source code for this project is available here:

https://github.com/gwpy/pyomicron/

All issues regarding this software should be raised using the GitHub web
interface, bug reports and feature requests are encouraged.

Documentation is available here:

https://pyomicron.readthedocs.io/en/latest/
"""

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    parser._positionals.title = 'Positional arguments'
    parser._optionals.title = 'Optional arguments'

    # basic command-line options
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=__version__,
    )
    ifo = const.IFO
    if ifo:
        grp_file = Path.home() / 'omicron' / 'online' / f'{ifo.lower()}-groups.txt'
        with grp_file.open('r') as grp_fp:
            all_groups = re.sub('\n(?<!$)', ', ', grp_fp.read())
        all_groups = f'({all_groups})'
    else:
        all_groups = ''

    parser.add_argument(
        'group',
        help=f'name of configuration group to process {all_groups} default=all groups',
    )
    parser.add_argument(
        '-t',
        '--gps',
        nargs=2,
        type=to_gps,
        metavar='GPSTIME',
        help='GPS times or date/time for offline processing')
    parser.add_argument(
        '-f',
        '--config-file',
        default=const.OMICRON_CHANNELS_FILE,
        help='path to configuration file (default: %(default)s)',
    )
    parser.add_argument(
        '-i',
        '--ifo',
        default=const.IFO,
        help='IFO prefix to process (default: %(default)s)',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=2,
        help='print verbose output, give more times for more '
        'verbose output',
    )

    parser.add_argument('--warn',
                        action='store_true',
                        help='Convert errors to warnings to help debug'
                        )
    # options for file writing
    outg = parser.add_argument_group('Output options')

    outg.add_argument(
        '-o',
        '--output-dir',
        default=Path.home() / 'omicron' / 'output',
        type=Path,
        help='path to output directory (default: %(default)s)',
    )
    outg.add_argument(
        '-a',
        '--archive',
        action='store_true',
        default=False,
        help='archive created files under %s (default: %%(default)s)'
             % const.OMICRON_ARCHIVE,
    )
    outg.add_argument(
        '-g',
        '--file-tag',
        default='',
        help='additional file tag to be appended to final '
        'file descriptions',
    )
    outg.add_argument('-l', '--log-file', type=Path,
                      help="save a copy of all logger messages to this file, "
                           "default: omicron-process.log in output directory ")

    # data processing/chunking options
    procg = parser.add_argument_group('Processing options')

    if config.has_option('process', 'max_chunks_per_job'):
        default_max_chunks_per_job = int(config['process']['max_chunks_per_job'])
    else:
        default_max_chunks_per_job = 4
    procg.add_argument(
        '-C',
        '--max-chunks-per-job',
        type=int,
        default=default_max_chunks_per_job,
        help='maximum number of chunks to process in a single '
        'condor job (default: %(default)s)',
    )
    if config.has_option('process', 'max_channels_per_job'):
        default_max_channels_per_job = int(config['process']['max_channels_per_job'])
    else:
        default_max_channels_per_job = 30 * 60
    procg.add_argument(
        '-N',
        '--max-channels-per-job',
        type=int,
        default=default_max_channels_per_job,
        help='maximum number of channels to process in a single '
        'condor job (default: %(default)s)',
    )
    if config.has_option('process', 'max_lookback'):
        default_max_lookback = int(config['process']['max_lookback'])
    else:
        default_max_lookback = 30 * 60
    procg.add_argument('--max-online-lookback', type=int, default=default_max_lookback,
                       help='With no immediately previous run, or one that was long ago this is the max time of an '
                            'online job. Default: %(default)d')
    procg.add_argument(
        '-x',
        '--exclude-channel',
        action='append',
        default=[],
        help='exclude channel from the analysis (can be given '
             'multiple times)',
    )

    # condor batch-processing options
    condorg = parser.add_argument_group('Condor options')
    mode = condorg.add_mutually_exclusive_group()
    mode.add_argument(
        '--reattach',
        action='store_true',
        default=False,
        help='if DAG already running, try and reattach to it '
             'and follow it\'s progress, this is only designed '
             'for online running',
    )
    mode.add_argument(
        '--rescue',
        action='store_true',
        default=False,
        help='rescue a failed DAG instead of creating a new one '
             '(default: %(default)s)',
    )
    mode.add_argument(
        '--no-submit',
        action='store_true',
        default=False,
        help='do not submit the DAG to condor (default: %(default)s)',
    )
    if config.has_option('condor', 'universe'):
        def_universe = config.get('condor', 'universe')
    else:
        def_universe = 'vanilla'

    condorg.add_argument(
        '--universe',
        default=def_universe,
        choices=['vanilla', 'local'],
        help='condor universe (default: %(default)s)',
    )
    condorg.add_argument(
        '--executable',
        default=OMICRON_PATH,
        help='path to omicron executable (default: %(default)s)',
    )
    if config.has_option('conda', 'environment'):
        conda_env = config['conda']['environment']
    else:
        conda_env = os.getenv('CONDA_PREFIX')
    condorg.add_argument('--conda-env', default=conda_env,
                         help='conda environment (name or path) for all programs in DAG [%(default)s]')

    if config.has_option('condor', 'condor_retry'):
        default_condor_retry = config['condor']['condor_retry']
    else:
        default_condor_retry = 2
    condorg.add_argument(
        '--condor-retry',
        type=int,
        default=default_condor_retry,
        help='number of times to retry each job if failed '
             '(default: %(default)s)',
    )
    if config.has_option('condor', 'max_concurrent'):
        default_max_concurrent = config['condor']['max_concurrent']
    else:
        default_max_concurrent = 64
    condorg.add_argument('--max-concurrent', default=default_max_concurrent, type=int,
                         help='Max omicron jobs run at one time [%(default)s]')

    condorg.add_argument(
        '--condor-accounting-group',
        default='ligo.prod.o4.detchar.transient.omicron',
        help='accounting_group for condor submission on the LIGO '
        'Data Grid (default: %(default)s)',
    )
    default_user = os.environ.get('_CONDOR_ACCOUNTING_USER')
    default_user = getuser() if not default_user else default_user
    condorg.add_argument(
        '--condor-accounting-group-user',
        default=default_user,
        help='accounting_group_user for condor submission on the '
        'LIGO Data Grid (default: %(default)s)',
    )

    if config.has_option('process', 'condor_request_disk'):
        default_condor_request_disk = config['process']['condor_request_disk']
    else:
        default_condor_request_disk = '20G'
    condorg.add_argument(
        '--condor-request-disk',
        default=default_condor_request_disk,
        help='Required LIGO argument: local disk use (default: %(default)s)',
    )
    condorg.add_argument(
        '--submit-rescue-dag',
        type=int,
        default=0,
        help='number of times to automatically submit the rescue DAG (default: %(default)s)',
    )
    condorg.add_argument(
        '-c',
        '--condor-command',
        action='append',
        type=str,
        default=[],
        metavar="\"key=value\"",
        help="Extra commands to add to the HTCondor submit files, can be given multiple times",
    )
    condorg.add_argument(
        '-d',
        '--dagman-option',
        action='append',
        type=str,
        default=['force', 'import_env'],
        metavar="\"opt | opt=value\"",
        help="Extra options to pass to condor_submit_dag as "
             "\"-{opt} [{value}]\". "
             "Can be given multiple times (default: %(default)s)",
    )
    condorg.add_argument(
        '--auth-type',
        choices=[ 'igwn', 'scitoken'],
        default='scitoken',
        help='How to authenticate to dqsegdb, datafind, and cvmfs'
    )

    # input data options
    datag = parser.add_argument_group('Data options')
    dataexc = datag.add_mutually_exclusive_group()
    dataexc.add_argument(
        '--cache-file',
        type=Path,
        metavar='FILE',
        help='use frame locations from FILE',
    )
    dataexc.add_argument(
        '--use-dev-shm',
        action='store_true',
        default=False,
        help='use low-latency frame buffer in /dev/shm '
             '(default: %(default)s)',
    )
    datag.add_argument(
        '--no-segdb',
        action='store_true',
        default=False,
        help='don\'t use the segment database for state '
             'determination (default: %(default)s)',
    )

    # workflow-generation options
    pipeg = parser.add_argument_group('Pipeline options')
    pipeg.add_argument(
        '--skip-omicron',
        action='store_true',
        default=False,
        help='skip running omicron (default: %(default)s)',
    )
    pipeg.add_argument(
        '--skip-root-merge',
        action='store_true',
        default=False,
        help='skip running omicron-root-merge (default: %(default)s)',
    )
    pipeg.add_argument(
        '--skip-hdf5-merge',
        action='store_true',
        default=False,
        help='skip running omicron-hdf5-merge (default: %(default)s)',
    )
    pipeg.add_argument(
        '--skip-ligolw_add',
        action='store_true',
        default=False,
        help='skip running ligolw_add (default: %(default)s)',
    )
    pipeg.add_argument(
        '--skip-gzip',
        action='store_true',
        default=False,
        help='skip running gzip (default: %(default)s)',
    )
    pipeg.add_argument(
        '--skip-postprocessing',
        action='store_true',
        default=False,
        help='skip all post-processing, equivalent to '
             '--skip-root-merge --skip-hdf5-merge '
             '--skip-ligolw_add --skip-gzip '
             '(default: %(default)s)',
    )
    pipeg.add_argument(
        '--skip-rm',
        action='store_true',
        default=False,
        help='Do not remove all the trigger files created by the job.'
             'Useful for debugging'
             '(default: %(default)s)'
    )

    return parser


def main(args=None):
    default_env = config['conda']['environment'] if config.has_option('conda', 'environment') else None
    conda_env = os.getenv('CONDA_PREFIX', default_env)
    if conda_env is None:
        logger.critical('Cannot determine conda environment')
        exit(10)
    else:
        logger.debug(f'Running in {conda_env}')

    parser = create_parser(config)
    args = parser.parse_args(args=args)

    # apply verbosity to logger
    args.verbose = max(5 - args.verbose, 0)
    logger.setLevel(args.verbose * 10)
    if args.log_file:
        log_file = Path(args.log_file)
    else:
        # if not specified default to the output directory
        log_file = Path(args.output_dir) / 'omicron-process.log'
    log_file.parent.mkdir(mode=0o755, exist_ok=True, parents=True)
    logger.add_file_handler(log_file)

    logger.debug(f'Running: {Path(__file__)} version {__version__}')
    logger.debug("Command line args:")
    for arg in vars(args):
        logger.debug(f'    {arg} = {str(getattr(args, arg))}')

    # validate command line arguments
    if args.ifo is None:
        parser.error("Cannot determine IFO prefix from sytem, "
                     "please pass --ifo on the command line")
    if args.executable is None:
        parser.error("Cannot find omicron on path, please pass "
                     "--executable on the command line")

    # validate processing options
    if all((args.skip_root_merge, args.skip_hdf5_merge, args.skip_ligolw_add,
            args.skip_gzip, not args.archive)):
        args.skip_postprocessing = True
    if args.archive:
        argsd = vars(args)
        for arg in ['skip-root-merge', 'skip-hdf5-merge',
                    'skip-ligolw-add', 'skip-gzip']:
            if argsd[arg.replace('-', '_')]:
                parser.error(f"Cannot use --{arg} with --archive")

    # check conflicts
    if args.gps is None and args.cache_file is not None:
        parser.error("Cannot use --cache-file in 'online' mode, "
                     "please use --cache-file with --gps")

    # extract key variables
    ifo = args.ifo
    group = args.group
    online = args.gps is None
    if online:
        logger.info('Online process. gps start, end determined automatically')

    # format file-tag as underscore-delimited upper-case string
    # filetag = args.file_tag
    # if filetag:
    #     filetag = re.sub(r'[:_\s-]', '_', filetag).rstrip('_').strip('_')
    #     if const.OMICRON_FILETAG.lower() in filetag.lower():
    #         afiletag = filetag
    #     else:
    #         afiletag = f'{filetag}_{const.OMICRON_FILETAG.upper()}'
    #     filetag = f'_{filetag}'
    # else:
    #     filetag = ''

    logger.info("--- Welcome to the Omicron processor ---")

    # set up containers to keep track of files that we create here
    tempfiles = []
    keepfiles = []

    # check rescue against --dagman-option force
    if args.rescue and args.dagman_option.count('force') > 1:
        parser.error('--rescue is incompatible with --dagman-option force')
    elif args.rescue:
        args.dagman_option.pop(0)
        logger.info(
            "Running in RESCUE mode - the workflow will be "
            "re-generated in memory without any files being written",
        )

    # set omicron version for future use
    omicronv = utils.get_omicron_version(args.executable)
    const.OMICRON_VERSION = str(omicronv)
    os.environ.setdefault('OMICRON_VERSION', str(omicronv))
    logger.debug('Omicron version: %s' % omicronv)

    # -- parse configuration file and get parameters --------------------------
    config_path = Path(args.config_file)
    if not config_path.is_file():
        raise FileExistsError(f'Configuration file : {str(config_path.absolute())} does not exsit')

    cp = configparser.ConfigParser()
    cp.read(args.config_file)

    # validate
    if not cp.has_section(group):
        raise configparser.NoSectionError(group)

    # get params
    channels = cp.get(group, 'channels').strip('\n').rstrip('\n').split('\n')
    try:  # allow two-column 'channel samplerate' format
        channels, crates = zip(*[c.split(' ', 1) for c in channels])
    except ValueError:
        crates = []
    else:
        crates = set(crates)
    logger.debug("%d channels read" % len(channels))
    for i in range(len(channels) - 1, -1, -1):  # remove excluded channels
        c = channels[i]
        if c in args.exclude_channel:
            channels.pop(i)
            logger.debug("    removed %r" % c)
    logger.debug("%d channels to process" % len(channels))
    cp.set(group, 'channels', '\n'.join(channels))
    frametype = cp.get(group, 'frametype')
    logger.debug("frametype = %s" % frametype)
    chunkdur = cp.getint(group, 'chunk-duration')
    logger.debug("chunkdur = %s" % chunkdur)
    segdur = cp.getint(group, 'segment-duration')
    logger.debug("segdur = %s" % segdur)
    overlap = cp.getint(group, 'overlap-duration')
    logger.debug("overlap = %s" % overlap)
    padding = int(overlap / 2)
    logger.debug("padding = %s" % padding)
    try:
        frange = tuple(map(float, cp.get(group, 'frequency-range').split()))
    except configparser.NoOptionError as e:
        try:
            flow = cp.getfloat(group, 'flow')
            fhigh = cp.getfloat(group, 'flow')
        except configparser.NoOptionError:
            raise e
        frange = (flow, fhigh)
    logger.debug('frequencyrange = [%s, %s)' % tuple(frange))
    try:
        sampling = cp.getfloat(group, 'sample-frequency')
    except configparser.NoOptionError:
        if len(crates) == 1:
            sampling = float(crates[0])
        elif len(crates) > 1:
            raise ValueError(
                "No sample-frequency parameter given, and multiple "
                "sample frequencies parsed from channels list, "
                "cannot continue",
            )
        else:
            sampling = None
    if sampling:
        logger.debug('samplingfrequency = %s' % sampling)

    # get state channel
    try:
        statechannel = cp.get(group, 'state-channel')
    except configparser.NoOptionError:
        statechannel = None
    else:
        try:
            statebits = list(map(
                float,
                cp.get(group, 'state-bits').split(','),
            ))
        except configparser.NoOptionError:
            statebits = [0]
        try:
            stateft = cp.get(group, 'state-frametype')
        except configparser.NoOptionError as e:
            e.args = ('%s, this must be specified if state-channel is given'
                      % str(e),)
            raise

    # get state flag (if given)
    try:
        stateflag = cp.get(group, 'state-flag')
    except configparser.NoOptionError:
        stateflag = None
    else:
        logger.debug("State flag = %s" % stateflag)
        if not statechannel:  # map state flag to state channel
            try:
                statechannel, statebits, stateft = (
                    segments.STATE_CHANNEL[stateflag]
                )
            except KeyError as e:
                if online or args.no_segdb:  # only raise if channel required
                    e.args = (
                        'Cannot map state flag %r to channel' % stateflag,
                    )
                    raise
                else:
                    pass

    if statechannel:
        logger.debug(f"State channel {statechannel}")
        if statebits == 'guardian':
            logger.debug(f"State bits {statebits}")
        else:
            logger.debug("State bits = %s" % ', '.join(map(str, statebits)))
        logger.debug(f"State frametype {stateft}")

    # parse padding for state segments
    statepad = (4, 4)
    if statechannel or stateflag:
        try:
            statepad = cp.get(group, 'state-padding')
        except configparser.NoOptionError:
            statepad = (0, 0)
        else:
            try:
                p = int(statepad)
            except ValueError:
                statepad = tuple(map(float, statepad.split(',', 1)))
            else:
                statepad = (p, p)
        logger.debug("State padding: %s" % str(statepad))

    rundir = utils.get_output_path(args)

    # convert to omicron parameters format
    oconfig = parameters.OmicronParameters.from_channel_list_config(
        cp, group, version=omicronv)
    # and validate things
    oconfig.validate()

    # -- set directories ------------------------------------------------------

    rundir.mkdir(exist_ok=True, parents=True)
    logger.info(f"Using run directory: {rundir}")

    cachedir = rundir / "cache"
    condir = rundir / "condor"
    logdir = rundir / "logs"
    pardir = rundir / "parameters"
    trigdir = rundir / "triggers"
    mergedir = rundir / "merge"
    run_dir_list = [cachedir, condir, logdir, pardir, trigdir, mergedir]
    for d in run_dir_list:
        d.mkdir(exist_ok=True)

    oconfig.set('OUTPUT', 'DIRECTORY', str(trigdir))

    # -- check for an existing process ----------------------------------------

    dagpath = condir / f"{DAG_TAG}-{group}.dag"

    # check dagman lock file
    running = condor.dag_is_running(dagpath)
    if running:
        msg = "Detected {} already running in {}".format(
            dagpath,
            rundir,
        )
        if not args.reattach:
            raise RuntimeError(msg)
        logger.info("{}, will reattach".format(msg))
    else:
        args.reattach = False

    # check dagman rescue files
    nrescue = len(list(condir.glob(f"{dagpath.name}.rescue[0-9][0-9][0-9]")))
    if args.rescue and not nrescue:
        raise RuntimeError(f"--rescue given but no rescue DAG files found for {dagpath}")
    if nrescue and not args.rescue and "force" not in args.dagman_option:
        raise RuntimeError(
            "rescue DAGs found for {} but `--rescue` not given and "
            "`--dagman-option force` not given, cannot continue".format(
                dagpath,
            ),
        )

    newdag = not args.rescue and not args.reattach

    # -- find run segment -----------------------------------------------------

    segfile = str(rundir / "segments.txt")
    keepfiles.append(segfile)
    max_lookback = args.max_online_lookback
    now = tconvert()

    if newdag and online:
        # get limit of available data (allowing for padding)
        end = data.get_latest_data_gps(ifo, frametype) - padding
        frame_age = deltat_to_hr(int(now - end))
        logger.info(f'Last available frame data: {gps_to_hr(end)} age: {frame_age}')

        lookback = max(int(chunkdur * 2.5), max_lookback)
        earliest_online = end - lookback
        try:  # start from where we got to last time
            last_run_segment = segments.get_last_run_segment(segfile)
            start = last_run_segment[1]
            if start < earliest_online:
                logger.warning(f'Segments.txt produced a start time for this run before max-lookback {max_lookback}\n'
                               f'  Found {gps_to_hr(start)} earliest is {gps_to_hr(earliest_online)}')
                start = earliest_online
                if end < start:
                    # this happens when the available frames end before the max lookbak period
                    logger.warning(f'Available data ends {gps_to_hr(end)} before lookback limit'
                                   f' {gps_to_hr(earliest_online)}')
                    exit(0)
            else:
                logger.debug(f"Online segment record recovered: {gps_to_hr(last_run_segment[0])} - "
                             f"{gps_to_hr(last_run_segment[1])}")

        except IOError:  # otherwise start with a sensible amount of data
            if args.use_dev_shm:  # process one chunk
                logger.debug("No online segment record, starting with "
                             "%s seconds" % chunkdur)
                start = end - chunkdur + padding
            else:  # process the last requested seconds (arbitrarily)
                logger.debug(f"No online segment record, starting with {max_lookback} seconds ago, "
                             f"{gps_to_hr(earliest_online)}")
                start = earliest_online

    elif online:
        start, end = segments.get_last_run_segment(segfile)
        if end - start > max_lookback:
            start = end - max_lookback
        else:
            logger.debug(f"Online segment record recovered: {gps_to_hr(start)} - {gps_to_hr(end)}")

    else:
        start, end = args.gps
        start = int(start)
        end = int(end)

    duration = end - start
    datastart = start - padding
    dataend = end + padding
    dataduration = dataend - datastart

    logger.info(f'Processing segment determined as: {gps_to_hr(datastart)} - {gps_to_hr(dataend)}')
    dur_str = deltat_to_hr(dataduration)
    logger.info(f"Duration = {dur_str}")

    # -- find segments and frame files ----------------------------------------

    # minimum allowed duration is one full chunk
    minduration = 1 * chunkdur

    # validate span is long enough
    if dataduration < minduration and online:
        if dataduration < 0:
            logger.info(f'Frame data is not available for interval {gps_to_hr(start)} to {gps_to_hr(end)}')
        else:
            logger.info(f"Segment is too short ({duration} < {minduration}), please try again later")
        clean_dirs(run_dir_list)
        clean_exit(0, tempfiles)
    elif dataduration < minduration:
        ermsg = f'Segment [{start}, {end}) is too short ({duration} < {minduration}), ' \
                f'please; extend the segment, or shorten the timing parameters.'
        logger.critical(ermsg)
        raise ValueError(ermsg)

    # -- find run segments
    # decide how determine segments to process
    # No stateflag (dq segment name) process all data in interval
    # online, short duration, near current time use guardian  channel in raw frame
    # use dqsgdb
    max_guardian = int(config['process']['max_guardian']) if config.has_option('process', 'max_guardian') else 600
    if stateflag is None:
        seg_method = 'frames'
    elif (statechannel is not None) and dataduration < max_guardian:
        seg_method = 'guardian'
    elif stateflag is not None:
        seg_method = 'dqsegdb'
    else:
        seg_method = 'frames'

    # get segments from state vector
    if seg_method == 'guardian':
        logger.info(f'Finding segments for relevant state...  from:{datastart} length: {dataduration}s')
        logger.debug(f'For segment finding: online: {online}, statechannel: {statechannel}, '
                     f'stateflag: {stateflag} args.no_segdb: {args.no_segdb}')
        seg_qry_strt = time.time()
        if statebits == "guardian":  # use guardian
            logger.debug(f'Using guardian for {statechannel}: {gps_to_hr(datastart)}-{gps_to_hr(dataend)}:'
                         f' {(dataend - datastart)} seconds')
            segs = segments.get_guardian_segments(
                statechannel,
                stateft,
                datastart,
                dataend,
                pad=statepad,
            )
        else:
            logger.debug(f'Using statevector for {statechannel}: {datastart}-{dataend}')
            segs = segments.get_state_segments(
                statechannel,
                stateft,
                datastart,
                dataend,
                bits=statebits,
                pad=statepad,
            )
        logger.info(f'State query took {time.time() - seg_qry_strt:.2f}s')

    # get segments from segment database
    elif seg_method == 'dqsegdb':
        logger.info(f'Querying segment database for relevant state: {stateflag} from:{datastart} length:'
                    f' {dataduration}s {deltat_to_hr(dataduration)}')
        seg_qry_strt = time.time()
        segs = segments.query_state_segments(stateflag, datastart, dataend,
                                             pad=statepad)
        logger.info(f'Segment query took {time.time() - seg_qry_strt:.2f}s')

    elif seg_method == 'frames':
        # Get segments from frame cache
        if args.cache_file:
            logger.info('Get segments from cache')
            cache = read_cache(str(args.cache_file))
            cache_segs = segments.cache_segments(cache)
            srch_span = SegmentList([Segment(datastart, dataend)])
            segs = cache_segs & srch_span

        # get segments from frame availability
        else:
            logger.info('Get segments from frame availability')
            fa_qry_strt = time.time()
            segs = segments.get_frame_segments(ifo, frametype, datastart, dataend)
            logger.info(f'Frame availability query took {(time.time() - fa_qry_strt):.2f}s')

    # print frame segments recovered
    if len(segs):
        logger.info("State/frame segments recovered as")
        for seg in segs:
            logger.info(f"    {gps_to_hr(seg[0])} {gps_to_hr(seg[1])} [{abs(seg)}]")
        logger.info(f"Duration = {gps_to_hr(abs(segs))}")

    # if running online, we want to avoid processing up to the extent of
    # available data, so that the next run doesn't get left with a segment that
    # is too short to process
    # There are a few reasons this might be
    #   - the interferometer loses lock a short time after the end of this run
    #   - a restart/other problem means that a frame is missing a short time
    #     after the end of this run

    # so, work out whether we need to truncate:
    try:
        lastseg = segs[-1]
    except IndexError:
        truncate = False
    else:
        truncate = online and newdag and lastseg[1] == dataend

    # if final segment is shorter than two chunks, remove it entirely
    # so that it gets processed next time (when it will either a closed
    # segment, or long enough to process safely)
    if truncate and abs(lastseg) < chunkdur * 2:
        logger.info(
            "The final segment is too short, " f'Minimum length is {int(chunkdur * 2)} '
            "but ends at the limit of "
            "available data, presumably this is an active segment. It "
            "will be removed so that it can be processed properly later",
        )
        segs = type(segs)(segs[:-1])
        dataend = lastseg[0]
    # otherwise, we remove the final chunk (so that the next run has at
    # least that on which to operate), then truncate to an integer number
    # of chunks (so that # PSD estimation operates on a consistent amount
    # of data)
    elif truncate:
        logger.info("The final segment touches the limit of available data, "
                    "the end chunk will be removed to guarantee that the next "
                    "online run has enough data over which to operate")
        t, e = lastseg
        e -= chunkdur + padding  # remove one chunk
        # now truncate to an integer number of chunks
        step = chunkdur
        while t + chunkdur <= e:
            t += step
            step = chunkdur - overlap
        segs[-1] = type(segs[-1])(lastseg[0], t)
        dataend = segs[-1][1]
        logger.info(f"This analysis will now run to  {gps_to_hr(dataend)}")

    # recalculate the processing segment
    dataspan = type(segs)([segments.Segment(datastart, dataend)])

    # -- find the frames
    fr_start = time.time()
    # find frames under /dev/shm (which creates a cache of temporary files)
    if args.cache_file:
        cache = read_cache(str(args.cache_file))
    # only cache if we have state segments
    elif args.use_dev_shm and len(segs):
        cache = data.find_frames(ifo, frametype, datastart, dataend,
                                 on_gaps='warn', tmpdir=cachedir)
        # remove cached files at end of process
        tempfiles.extend(filter(lambda p: str(cachedir) in p, cache))
    # find frames using datafind
    else:
        cache = data.find_frames(ifo, frametype, datastart, dataend,
                                 on_gaps='warn')
    fr_get_time = time.time() - fr_start
    logger.info(f"Frame retrieval returned {len(cache)} files and took {fr_get_time:.2f}s")

    # if not frames for an online run, panic
    if not online and len(cache) == 0:
        raise RuntimeError("No frames found for %s-%s" % (ifo[0], frametype))

    # work out the segments of data available
    try:
        cachesegs = (segments.cache_segments(cache) & dataspan).coalesce()
    except TypeError:  # empty cache
        cachesegs = type(dataspan)()
        alldata = False
    else:
        try:
            alldata = cachesegs[-1][1] >= dataspan[-1][1]
        except IndexError:  # no data overlapping span
            alldata = False

    # write cache of frames (only if creating a new DAG)
    cachefile = cachedir / "frames.lcf"
    keepfiles.append(cachefile)
    if newdag or not cachefile.exists():
        data.write_cache(cache, cachefile)
        logger.info("Cache of %d frames written to\n%s" % (len(cache), cachefile))
    else:
        logger.info("Cache of %d frames NOT written because this is not a new DAG to\n%s" % (len(cache), cachefile))
    oconfig.set('DATA', 'FFL', str(cachefile))

    # restrict analysis to available data (and warn about missing data)
    if segs - cachesegs:
        logger.warning("Not all state times are available in frames")
    segs = (cachesegs & segs).coalesce()

    # Deal with segments that cross a metric day (100,000 boundary)
    seg_tmp = SegmentList()
    for seg in segs:
        sday = int(seg[0] / 1e5)
        eday = int(seg[1] / 1e5)
        if sday == eday:
            seg_tmp.append(seg)
        else:
            seg1 = Segment(seg[0], eday)
            seg2 = Segment(eday, seg[1])
            seg_tmp.append(seg1)
            seg_tmp.append(seg2)
    # apply minimum duration requirement
    segs = type(segs)(s for s in segs if abs(s) >= segdur)

    # if all of the data are available, but no analysable segments were found
    # (i.e. IFO not in right state for all times), record segments.txt
    if newdag and len(segs) == 0 and online and alldata:
        logger.info(
            "No analysable segments found, but up-to-date data are "
            "available. "
        )
        clean_dirs(run_dir_list)
        clean_exit(0, tempfiles)

    # otherwise not all data are available, so
    elif len(segs) == 0 and online:
        logger.info("No analysable segments found, please try again later")
        clean_dirs(run_dir_list)
        clean_exit(0, tempfiles)
    elif len(segs) == 0:
        raise RuntimeError("No analysable segments found")

    # and calculate trigger output segments
    trigsegs = type(segs)(type(s)(*s) for s in segs).contract(padding)

    # display segments
    if len(segs) == 0:
        logger.info('No analyzable segments found. Exiting.')
        exit(0)
    else:
        logger.info("Final data segments selected as")
        for seg in segs:
            logger.info(f"    {gps_to_hr(seg[0])} {gps_to_hr(seg[1])} {abs(seg)}")
        logger.info(f"Duration = {abs(segs)} seconds")

    span = type(trigsegs)([trigsegs.extent()])

    logger.info("This will output triggers for")
    for seg in trigsegs:
        logger.info(f"    {gps_to_hr(seg[0])} {gps_to_hr(seg[1])} {abs(seg)}")
    logger.info(f"Duration = {abs(trigsegs)} seconds")

    # -- config omicron config directory --------------------------------------

    tempfiles.append(utils.astropy_config_path(rundir))

    # -- make parameters files then generate the DAG --------------------------

    fileformats = oconfig.output_formats()

    # generate a 'master' parameters.txt file for archival purposes
    if not newdag:  # if not writing new dag, dump parameters.txt files to /tmp
        pardir = gettempdir()
    parfile, jobfiles = oconfig.write_distributed(
        pardir, nchannels=args.max_channels_per_job)
    logger.debug(f"Created master parameters file\n{parfile} and {len(jobfiles)} job files")

    if newdag:
        keepfiles.append(parfile)

    # create dag
    dag = pipeline.CondorDAG(str(logdir / f"{DAG_TAG}.log"))
    dag.set_dag_file(str(dagpath.with_suffix("")))

    # set up condor commands for all jobs
    base_condorcmds = {
        "accounting_group": args.condor_accounting_group,
        "accounting_group_user": args.condor_accounting_group_user,
        "request_disk": args.condor_request_disk,
    }
    condor_igwn_auth = {
        # scitokens needed for dqsegdb
        'use_oauth_services': 'igwn',
        'igwn_oauth_options_dqsegdb': "--role $ENV('TOKEN_ROLE') --credkey $ENV('TOKEN_CREDKEY')",
        'igwn_oauth_resource_dqsegdb': 'https: // segments.ligo.org',
        'igwn_oauth_permissions_dqsegdb': 'dqsegdb.read',
        'environment': '"BEARER_TOKEN_FILE=$$(_CONDOR_SCRATCH_DIR)/.condor_creds/igwn_dqsegdb.use"'
    }
    condor_apissuer_auth = {
        'use_oauth_services': 'scitokens',
    }
    condor_x509_auth = {
        'getenv': 'X509_USER_PROXY, KRB5CNAME'
    }
    if args.auth_type == 'x509':
        condorcmds = dict(base_condorcmds | condor_x509_auth)
    elif args.auth_type == 'igwn':
        condorcmds = dict(base_condorcmds | condor_igwn_auth)
    elif args.auth_type == 'scitoken':
        condorcmds = dict(base_condorcmds | condor_apissuer_auth)
    else:
        condorcmds = base_condorcmds.copy()
        logger.warning(f'We do not know how to authenticate to dqsegdb or cvmfs. auth-type: {args.auth_type}')

    condorcmds: dict[str, str]

    for cmd_ in args.condor_command:
        key, value = cmd_.split('=', 1)
        condorcmds[key.rstrip().lower()] = value.strip()

    conda_exe, conda_args = get_conda_run(config, args.conda_env, logger)
    conda_arg_list = conda_args.split()
    conda_run_prefix = conda_exe + ' ' + conda_args
    # create omicron job
    ojob_req_mem = config['omicron']['initial_memory'] if config.has_option('omicron', 'initial_memory') else 4096
    ojob = condor.OmicronProcessJob(args.universe, conda_exe, tag='omicron', subdir=condir,
                                    logdir=logdir, **condorcmds)
    for job_arg in conda_arg_list:
        ojob.add_arg(job_arg)

    ojob.add_arg('omicron')

    # This allows us to start with a memory request that works maybe 80%, but bumps it if we go over
    # we also limit individual jobs to a max runtime to cause them to be vacates to deal with NFS hanging
    reqmem = condorcmds.pop('request_memory', ojob_req_mem)
    ojob.add_condor_cmd('my.InitialRequestMemory', f'{reqmem}')
    ojob.add_condor_cmd('request_memory', f'ifthenelse(isUndefined(MemoryUsage), {reqmem}, int(3*MemoryUsage))')
    ojob.add_condor_cmd('periodic_release', '(HoldReasonCode =?= 26 || HoldReasonCode =?= 34) '
                                            ' && (JobStatus == 5) && (time() - EnteredCurrentStatus > 10)')

    ojob.add_condor_cmd('allowed_job_duration', 3 * 3600)
    ojob.add_condor_cmd('periodic_remove', '(JobStatus == 1 && MemoryUsage >= 7000 || (HoldReasonCode =?= 46 ))')
    ojob.add_condor_cmd('allowed_job_duration', 3 * 3600)

    ojob.add_condor_cmd('my.OmicronProcess', f'"{group}"')

    # create post-processing jobs
    ppmem = config['post_process']['initial_memory'] if config.has_option('post_process', 'initial_memory') else 2048
    ppjob = condor.OmicronProcessJob(args.universe, conda_exe,
                                     subdir=condir, logdir=logdir,
                                     tag='post-processing', **condorcmds)
    for job_arg in conda_arg_list:
        ppjob.add_arg(job_arg)

    ppjob.add_arg(shutil.which('bash'))
    ppjob.add_arg('-e')
    ppjob.add_condor_cmd('my.OmicronPostProcess', f'"{group}"')
    ppjob.add_condor_cmd('my.InitialRequestMemory', f'{ppmem}')
    ppjob.add_condor_cmd('request_memory',
                         f'ifthenelse(isUndefined(MemoryUsage), {ppmem}, int(1.5*MemoryUsage))')
    ppjob.add_condor_cmd('periodic_release', '(HoldReasonCode =?= 26 || HoldReasonCode =?= 34) '
                         '&& (JobStatus == 5) && (time() - EnteredCurrentStatus > 10)')

    ppjob.add_condor_cmd('periodic_remove', '((JobStatus == 1) && MemoryUsage >= 7000) || (HoldReasonCode =?= 46)')

    ppjob.add_condor_cmd('environment', '"HDF5_USE_FILE_LOCKING=FALSE"')
    ppnodes = []
    prog_path = dict()
    prog_path['omicron-merge'] = shutil.which('omicron-merge-with-gaps')
    prog_path['rootmerge'] = shutil.which('omicron-root-merge')
    prog_path['hdf5merge'] = shutil.which('omicron-hdf5-merge')
    prog_path['ligolw_add'] = shutil.which('ligolw_add')
    prog_path['gzip'] = shutil.which('gzip')
    prog_path['omicron_archive'] = shutil.which('omicron-archive')
    prog_path['clean_logs'] = shutil.which('omicron-clean-logs')

    goterr = list()
    for exe in prog_path.keys():
        if not prog_path[exe]:
            logger.critical(f'required program: {exe} not found')
            goterr.append(exe)
    if goterr:
        if args.warn:
            logger.warning(goterr)
        else:
            raise ValueError(f'Required programs not found in current environment: {", ".join(goterr)}')

    # create node to remove files
    rmfiles = []
    if not args.skip_rm:
        rm_mem = config['clean']['initial_memory'] if config.has_option('clean', 'initial_memory') else 2048
        rmjob = condor.OmicronProcessJob(
            args.universe, conda_exe,
            subdir=condir, logdir=logdir, tag='post-processing-rm', **condorcmds)
        rm = shutil.which('rm')

        for job_arg in conda_arg_list:
            rmjob.add_arg(job_arg)
        rmscript = condir / "post-process-rm.sh"
        rmjob.add_arg(str(rmscript))

        rmjob.add_condor_cmd('request_memory', f'{rm_mem}M')
        rmjob.add_condor_cmd('+OmicronPostProcess', '"%s"' % group)

    if args.archive:
        archive_mem = config['archive']['initial_memory'] if config.has_option('archive', 'initial_memory') else 2048
        archivejob = condor.OmicronProcessJob(
            args.universe, conda_exe,
            subdir=condir, logdir=logdir, tag='archive', **condorcmds)
        for job_arg in conda_arg_list:
            archivejob.add_arg(job_arg)

        archive_script = condir / "archive.sh"
        archivejob.add_arg(str(archive_script))

        archivejob.add_condor_cmd('request_memory', f'{archive_mem}M')
        archivejob.add_condor_cmd('my.OmicronPostProcess_archive', f'{group}')
    else:
        archivejob = None

    omicron_nodes = list()

    # loop over data segments
    for s, e in segs:
        # distribute segment across multiple nodes
        nodesegs = oconfig.distribute_segment(
            s, e, nperjob=args.max_chunks_per_job)

        omicronfiles = dict()
        # build node for each parameter file
        for i, pf in enumerate(jobfiles):
            chanlist = jobfiles[pf]
            nodes = []
            # loop over distributed segments
            for j, subseg in enumerate(nodesegs):
                if not args.skip_omicron:
                    # work out files for this job
                    nodefiles = oconfig.output_files(*subseg)
                    # build node
                    node = pipeline.CondorDAGNode(ojob)
                    node.set_category('omicron')
                    node.set_name(f'Omicron_{len(omicron_nodes):03d}')
                    node.set_retry(args.condor_retry)
                    node.add_var_arg(str(subseg[0]))
                    node.add_var_arg(str(subseg[1]))
                    node.add_file_arg(pf)
                    # we need to ignore errors in individual omicron jobs after retrying
                    node.set_post_script(shutil.which('omicron-post-script'))
                    # -vvv --return $RETURN --retry $RETRY --max-retry $MAX_RETRIES --log pscript.log
                    node.add_post_script_arg('-vvv')
                    node.add_post_script_arg('--return')
                    node.add_post_script_arg('$RETURN')
                    node.add_post_script_arg('--retry')
                    node.add_post_script_arg('$RETRY')
                    node.add_post_script_arg('--max-retry')
                    node.add_post_script_arg('$MAX_RETRIES')
                    node.add_post_script_arg('--job')
                    node.add_post_script_arg('$JOB')
                    node.add_post_script_arg('--log')
                    post_script_log_file = condir / 'post_script.log'
                    node.add_post_script_arg(str(post_script_log_file.absolute()))

                    for chan in chanlist:
                        for form, flist in nodefiles[chan].items():
                            # record file as output for this channel
                            try:
                                omicronfiles[chan][form].extend(flist)
                            except KeyError:
                                try:
                                    omicronfiles[chan][form] = flist
                                except KeyError:
                                    omicronfiles[chan] = {form: flist}
                    dag.add_node(node)
                    nodes.append(node)              # for this segment
                    omicron_nodes.append(node)      # all nodes

            # post-process (one post-processing job per channel
            #               per data segment)
            if not args.skip_postprocessing:
                script = condir / f"post-process-{i}-{s}-{e}.sh"
                ppnode = pipeline.CondorDAGNode(ppjob)
                ppnode.add_var_arg(str(script))
                operations = []

                # build post-processing nodes for each channel
                for c in chanlist:
                    operations.append('\n# %s' % c)

                    # work out filenames for coalesced files
                    # archpath = Path(io.get_archive_filename(c, ts, td, filetag=afiletag, ext='root',))
                    mergepath = str(mergedir / c)

                    # add ROOT operations
                    if 'root' in fileformats:
                        rootfiles = ' '.join(omicronfiles[c]['root'])
                        no_merge = '--no-merge' if args.skip_root_merge else ''

                        operations.append(f'  {conda_run_prefix} {prog_path["omicron-merge"]} {no_merge}  '
                                          f'--out-dir {mergepath} {rootfiles} ')
                        rmfiles.append(rootfiles)

                    # add HDF5 operations
                    if 'hdf5' in fileformats:
                        hdf5files = ' '.join(omicronfiles[c]['hdf5'])
                        no_merge = '--no-merge' if args.skip_hdf5_merge else ''

                        operations.append(
                            f'  {conda_run_prefix} {prog_path["omicron-merge"]} {no_merge}  '
                            f' --out-dir {mergepath} {hdf5files} ')
                        rmfiles.append(hdf5files)

                    # add LIGO_LW operations
                    if 'xml' in fileformats:
                        xmlfiles = ' '.join(omicronfiles[c]['xml'])

                        no_merge = '--no-merge' if args.skip_ligolw_add else ''
                        no_gzip = '--no-gzip' if args.skip_gzip else ''
                        operations.append(
                            f'  {conda_run_prefix} {prog_path["omicron-merge"]} {no_merge} {no_gzip} --uint-bug '
                            f' --out-dir {mergepath} {xmlfiles} ')

                        rmfiles.append(xmlfiles)

                ppnode.set_category('postprocessing')
                ppnode.set_retry(str(args.condor_retry))
                if not args.skip_omicron:
                    for node in nodes:
                        ppnode.add_parent(node)
                ppnode.set_name(f'post_process_merge_{len(ppnodes):02d}')
                dag.add_node(ppnode)
                ppnodes.append(ppnode)
                tempfiles.append(script)

                # write post-processing file
                if not args.rescue:
                    with script.open("w") as f:
                        # add header
                        print('#!/bin/bash -e\n#', file=f)
                        print("# omicron-process post-processing", file=f)
                        print(f'#\n# File created by\n# {sys.argv[0]}  version: {__version__}\n#', file=f)
                        print("# Group: %s" % group, file=f)
                        print("# Segment: [%d, %d)" % (s, e), file=f)
                        print("# Channels:\n#", file=f)
                        for c in chanlist:
                            print('# %s' % c, file=f)
                        # add post-processing operations
                        print('\n'.join(operations), file=f)
                    if newdag:
                        script.chmod(0o755)

    dag.add_maxjobs_category('omicron', args.max_concurrent)

    # set 'strict' option for Omicron
    # this is done after the nodes are written so that 'strict' is last in
    # the call
    ojob.add_arg('strict')

    # do all archiving last, once all post-processing has completed
    if args.archive:
        archivenode = pipeline.CondorDAGNode(archivejob)
        acache = {fmt: list() for fmt in fileformats}
        if newdag:
            # write shell script to seed archive
            with archive_script.open('w') as f:
                print('#!/bin/bash -e\n', file=f)
                print('# Archive all trigger files saved in the merge directory ', file=f)
                print(f'#\n# File created by this command:\n# {" ".join(sys.argv)}\n#', file=f)
                print(f'# Running: {sys.argv[0]} version {__version__}\n', file=f)

                print(f'{conda_exe} {conda_args} ', end=' ', file=f)
                print(f'{prog_path["omicron_archive"]} --indir {str(mergedir.absolute())} -vvv', file=f)

            archive_script.chmod(0o755)
            # write caches to disk
            for fmt, fcache in acache.items():
                cachefile = cachedir / "omicron-{0}.lcf".format(fmt)
                data.write_cache(fcache, cachefile)
                logger.debug("{0} cache written to {1}".format(fmt, cachefile))
        # add node to DAG
        for node in ppnodes:
            archivenode.add_parent(node)
        archivenode.set_retry(args.condor_retry)
        archivenode.set_category('archive')
        archivenode.set_name('archive ')
        dag.add_node(archivenode)
        tempfiles.append(archive_script)

    # add rm job right at the end
    rmnode = None
    if not args.skip_rm:
        rmnode = pipeline.CondorDAGNode(rmjob)
        with open(rmscript, 'w') as f:
            print('#!/bin/bash -e\n#', file=f)
            print("# omicron-process post-processing-rm", file=f)
            print(f'#\n# File created by\n# {" ".join(sys.argv)}\n#', file=f)
            print("# Group: %s" % group, file=f)
            print("# Segment: [%d, %d)" % (s, e), file=f)
            print("# Channels:\n#", file=f)
            for c in channels:
                print('# %s' % c, file=f)
            print('', file=f)
            for rmset in rmfiles:
                print('%s -f %s' % (rm, rmset), file=f)
        if newdag:
            rmscript.chmod(0o755)
        tempfiles.append(rmscript)
        rmnode.set_category('postprocessing')
    if rmnode:
        rmnode.set_name('rm_files ')
        # set parents for removing files
        if args.archive:  # run this after archiving
            rmnode.add_parent(archivenode)
        else:  # or just after post-processing if not archiving
            for node in ppnodes:
                rmnode.add_parent(node)
        dag.add_node(rmnode)

    # print DAG to file
    dagfile = Path(dag.get_dag_file()).resolve(strict=False)
    if args.rescue:
        logger.info(
            "In --rescue mode, this DAG has been reproduced in memory "
            "for safety, but will not be written to disk, the file is:",
        )
    elif newdag:
        dag.write_sub_files()
        dag.write_dag()
        dag.write_script()
        with open(dagfile, 'a') as f:
            print("DOT", dagfile.with_suffix(".dot"), file=f)
        logger.info("Dag with %d nodes written to" % len(dag.get_nodes()))
        print(dagfile)

    if args.no_submit:
        if newdag:
            write_segfile(span, segfile)
            logger.info("Segments written to\n%s" % segfile)
        logger.info(f"Elapsed: {time.time() - prog_start:.1f} seconds ")
        sys.exit(0)

    # -- submit the DAG and babysit -------------------------------------------

    # submit DAG
    if args.rescue:
        logger.info("--- Submitting rescue DAG to condor ----")
    elif args.reattach:
        logger.info("--- Reattaching to existing DAG --------")
    else:
        logger.info("--- Submitting DAG to condor -----------")

    batch_name = None
    for i in range(args.submit_rescue_dag + 1):
        if args.reattach:  # find ID of existing DAG
            dagid = int(condor.find_job(Owner=getuser(),
                                        OmicronDAGMan=group)['ClusterId'])
            logger.info("Found existing condor ID = %d" % dagid)
        else:  # or submit DAG
            got_batch_name = False
            dagmanargs = set()
            if online:
                dagmanopts = {'-append': '+OmicronDAGMan=\"%s\"' % group}
            else:
                dagmanopts = {}
            for x in args.dagman_option:
                x = '-%s' % x
                try:
                    key, val = x.split('=', 1)
                    if key == '-batch-name':
                        got_batch_name = True
                        if "clusterid" not in val.lower():
                            val += '$(ClusterID)'
                        batch_name = val
                except ValueError:
                    dagmanargs.add(x)
                else:
                    dagmanopts[key] = val
            if not got_batch_name:
                key = '-batch-name'
                onl = 'online' if online else 'offline'
                val = f'omicron-{onl}-{group} $(ClusterID)'
                dagmanopts[key] = val
                batch_name = val

            # confirm submit command
            submit_dag_cmd = f'condor-submit {dagfile.absolute()} ' + ' '.join(dagmanargs)
            for key, val in dagmanopts.items():
                submit_dag_cmd += f' --{key} "{val}"'
            logger.info(f'dag submit\n{submit_dag_cmd}\n')

            dagid = condor.submit_dag(
                str(dagfile),
                *list(dagmanargs),
                **dagmanopts,
            )
            logger.info("Condor ID = %d" % dagid)
            # write segments now -- this means that online processing will
            # _always_ move on even if the workflow fails
            if i == 0:
                segments.write_segments(span, segfile)
                logger.info(f"Segments written to\n{segfile}")
            if 'force' in args.dagman_option:
                args.dagman_option.pop(args.dagman_option.index('force'))

        # monitor the dag
        logger.debug("----------------------------------------")
        logger.info(f"Monitoring DAG: {dagid} {dagfile}")
        cwq = shutil.which('condor_watch_q')
        if cwq:
            sleep(20)       # give condor time to set up the jobs

            if batch_name is None:
                logger.error("Batch name not set")
            else:
                batch_name = batch_name.replace('$(ClusterID)', str(dagid))
            cwq_args = [
                cwq,
                "-exit", "all,done,0",
                "-exit", "any,held,1",
                "-batches", batch_name,
            ]
            logger.info(f"Running condor_watch_q command:\n{' '.join(cwq_args)}")
            check_call(cwq_args)
            print()
        else:
            logger.error('We cannot monitor condor job because condor_watch_q not in our path')

        logger.debug("----------------------------------------")
        sleep(5)
        try:
            stat = condor.get_dag_status(dagid)
        except OSError as exc:  # query failed
            logger.warning(str(exc))
            stat = {}

        # log exitcode
        if "exitcode" not in stat:
            logger.warning("DAG has exited, status unknown")
            break
        if not stat["exitcode"]:
            logger.info("DAG has exited with status {}".format(
                stat.get("exitcode", "unknown"),
            ))
            break
        logger.critical(
            "DAG has exited with status {}".format(stat['exitcode']),
        )

        # handle failure
        if i == args.submit_rescue_dag:
            raise RuntimeError("DAG has failed to complete %d times"
                               % (args.submit_rescue_dag + 1))
        else:
            rescue = condor.find_rescue_dag(str(dagfile))
            logger.warning("Rescue DAG %s was generated" % rescue)

    # mark output and error files of condor nodes that passed to be deleted
    try:
        for node, files in condor.get_out_err_files(dagid, exitcode=0).items():
            tempfiles.extend(files)
    except RuntimeError:
        pass

    # archive files
    stub = '%d-%d' % (start, end)
    for f in map(Path, ["{}.dagman.out".format(dagfile)] + keepfiles):
        archive = logdir / "{0[0]}.{1}.{0[1]}".format(
            f.name.split(".", 1),
            stub,
        )
        if str(f) == str(segfile):
            shutil.copyfile(f, archive)
        else:
            f.rename(archive)
        logger.debug("Archived path\n{} --> {}".format(f, archive))

    # clean up temporary files
    tempfiles.extend(trigdir.glob("ffconvert.*.ffl"))
    if tempfiles is not None:
        logger.debug('Temporary files that cn be deleted')
        for f in tempfiles:
            isd = 'dir:' if Path(f).is_dir() else 'fil:'
            logger.debug(f'Delete {isd} {f}')

    # clean_tempfiles(tempfiles)

    # and exit
    logger.info(f"--- Processing complete. Elapsed: {(time.time() - prog_start):1f} seconds ----------------")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, OSError, NameError, ArithmeticError, RuntimeError) as ex:
        print(ex, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
