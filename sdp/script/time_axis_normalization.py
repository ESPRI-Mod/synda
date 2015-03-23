#!/usr/bin/env python
"""
.. module:: rewrite_time_axis.py
   :platform: Unix
   :synopsis: Rewrite and/or check time axis of CMIP5 files upon local IPSL-ESGF datanode.

.. moduleauthor:: Levavasseur, G. <glipsl@ipsl.jussieu.fr> and Laliberte, F. <frederic.laliberte@utoronto.ca>


"""

# Module imports
import re, os, argparse, logging
from uuid import uuid4
import numpy as np
from netCDF4 import Dataset, date2num, num2date
from multiprocessing.dummy import Pool as ThreadPool
from copy import copy
from netcdftime import datetime as phony_datetime



# Program version
__version__ = '{0} {1}-{2}-{3}'.format('v1.1', '2015', '01', '21')

# Throttle upon number of threads to spawn
_THREAD_POOL_SIZE = 4


class _ProcessingContext(object):
    """Encapsulate processing context information for main process."""
    def __init__(self, args):
        self.root = args.root
        self.check = args.check
        self.write = args.write
        self.force = args.force
        self.verbose = args.verbose
        self.realm = None
        self.version = None
        self.frequency = None
        self.calendar = None
        self.tunits = None
        self.funits = None
        self.filename = None


class _AxisStatus(object):
    """Encapsulate file information."""
    def __init__(self):
        self.directory = None
        self.file = None
        self.start = None
        self.end = None
        self.last = None
        self.steps = None
        self.instant = False
        self.frequency = None
        self.calendar = None
        self.tunits = None
        self.units = None
        self.control = []
        self.bnds = None
        self.checksum = None


def _get_args(args_list):
    """Returns parsed command line arguments."""
    parser=argparse.ArgumentParser(
        description = """Rewrite and/or check CMIP5 file time axis on CICLAD filesystem, considering
                       (i) uncorrupted filename period dates and
                       (ii) properly-defined times units, time calendar and frequency NetCDF attributes.

                       Returns status:
                       000: Unmodified time axis.
                       001: Corrected time axis because wrong timesteps.
                       002: Corrected time axis because of changing time units.
                       003: Ignored time axis because of inconsistency between last date of time axis and end date of filename period (e.g., wrong time axis length).
                       004: Corrected time axis deleting time boundaries for instant time.""",
        epilog="Developped by G. Levavasseur (CNRS/IPSL)")
    parser.add_argument('root',
                        nargs = '?',
                        help = """Dataset root path to browse following CMIP5 DRS
                                (e.g., <PREFIX>/esg/CMIP5/merge/NCAR/CCSM4/amip/day/atmos/cfDay/r7i1p1/latest/)
                                ONLY LATEST IS ACCEPTED!""")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--check',
                        action = 'store_true',
                        default = False,
                        help = 'Check time axis squareness.')
    group.add_argument('-w', '--write',
                        action = 'store_true',
                        default = False,
                        help = """Rewrite time axis depending on checking (including --check).
                                THIS ACTION DEFINITELY MODIFY INPUT FILES!""")
    group.add_argument('-f', '--force',
                        action = 'store_true',
                        default = False,
                        help = """Force time axis writing overpassing checking step.
                                THIS ACTION DEFINITELY MODIFY INPUT FILES!""")
    parser.add_argument('-v', '--verbose',
                        action = 'store_true',
                        default = False,
                        help = 'Verbose mode')
    parser.add_argument('-V', '--version',
                        action = 'version',
                        version = "%(prog)s ({0})".format(__version__),
                        help = 'Program version')
    return parser.parse_args(args_list)


def _time_init(ctx):
    """Returns required reference time properties, especially calendar to initialise CDMS calendar."""
    file = _get_file_list(ctx.root)[0]
    data = Dataset(ctx.root+file, 'r')
    ctx.frequency = ctx.root.split('/')[8]
    ctx.version = os.path.realpath(ctx.root).split('/')[12]
    ctx.tunits = _control_time_units(data.variables['time'].units)
    ctx.funits = _convert_time_units(ctx.tunits, ctx.frequency)
    ctx.realm = ctx.root.split('/')[9]
    ctx.calendar = data.variables['time'].calendar
    if ctx.calendar == 'standard' and ctx.root.split('/')[6] == 'CMCC-CM':
        ctx.calendar = 'proleptic_gregorian'
    data.close()
    logging.info('Version = {0}'.format(ctx.version))
    logging.info('Frequency = {0}'.format(ctx.frequency))
    logging.info('Calendar = {0}'.format(ctx.calendar))
    logging.info('Time units = {0}'.format(ctx.tunits))


def _get_file_list(directory):
    """Returns sorted list of filenames in directory."""
    try:
        files = sorted(os.listdir(directory))
    except:
        logging.error('No such directory: {0}'.format(directory))
        raise Exception('No such directory: {0}'.format(directory))
    pattern = re.compile(r'([\w.-]+)_([\w.-]+)_([\w.-]+)_([\w.-]+)_([\w.-]+)_([\d]+)-([\d]+).nc')
    for file in files:
        if re.match(pattern, file) == None:
            logging.error('Invalid filename: {0}'.format(file))
            raise Exception('Invalid filename: {0}'.format(file))
    return files


def _control_time_units(tunits):
    """Control time units format as at least "days since YYYY-MM-DD"."""
    units = tunits.split()
    units[0] = unicode('days')
    if len(units[2].split('-')) == 1:
        units[2] = units[2] + '-{0}-{1}'.format('01','01')
    elif len(units[2].split('-')) == 2:
        units[2] = units[2] + '-{0}'.format('01')
    return ' '.join(units)


def _convert_time_units(unit, frequency):
    """Converts file default time units depending on frequency."""
    units = {'subhr':'minutes',
             '3hr':'hours',
             '6hr':'hours',
             'day':'days',
             'mon':'months',
             'yr' :'years'}
    return unit.replace('days', units[frequency])


def _time_axis_processing(ctx):
    """Time axis process in three step: rebuild, check and rewrite."""
    # Extract start and end dates from filename
    start_date, end_date = _dates_from_filename(ctx.filename, ctx.calendar)
    start = _date2num(start_date, units = ctx.funits, calendar = ctx.calendar)
    # Set time length, True/False instant axis and incrementation in frequency units
    data = Dataset(ctx.root+ctx.filename, 'r+')
    length = data.variables['time'].shape[0]
    instant = _is_instant_time_axis(ctx.filename, ctx.realm)
    inc = _time_inc(ctx.frequency)
    # Instanciates object to display axis status
    status = _AxisStatus()
    status.directory = ctx.root
    status.file = ctx.filename
    status.start = _date_print(start_date)
    status.end = _date_print(end_date)
    status.steps = length
    status.frequency = ctx.frequency
    status.calendar = ctx.calendar
    status.tunits = ctx.tunits
    status.units = _control_time_units(data.variables['time'].units)
    if instant:
        status.instant = True
    # Rebuild a proper time axis
    axis_hp, last_hp = _rebuild_time_axis(start, length, instant, inc, ctx) # High precision
    axis_lp, last_lp = _rebuild_time_axis(trunc(start, 5), length, instant, inc, ctx) # Low precision avoiding float precision issues
    # Control consistency between last time date and end date from filename
    if not _last_date_checker(_date_print(last_hp), _date_print(end_date)) and not _last_date_checker(_date_print(last_lp), _date_print(end_date)):
        status.control.append('003')
        logging.warning('ERROO3 - Inconsistent last and end dates for {0}'.format(ctx.filename))
    else:
        if _last_date_checker(_date_print(last_hp), _date_print(end_date)):
            status.last = _date_print(last_hp) ; axis = axis_hp
        elif _last_date_checker(_date_print(last_lp), _date_print(end_date)):
            status.last = _date_print(last_lp) ; axis = axis_lp
        # Control consistency between instant time and time boundaries
        if instant and ('time_bnds' in data.variables.keys()):
            status.control.append('004')
            logging.warning('ERROO4 - Inconsistent time_bnds with instant time for {0}'.format(ctx.filename))
            # Delete time bounds and bounds attribute from file
            if ctx.write or ctx.force:
                del data.variables['time'].bounds
                data.close()
                _nc_var_delete(ctx.root, ctx.filename, 'time_bnds')
                # Compute checksum
                status.checksum = _checksum(ctx.root+ctx.filename)
                data = Dataset(ctx.root+ctx.filename, 'r+')
        # Check time axis squareness
        if ctx.check or ctx.write:
            time = data.variables['time'][:]
            if _time_checker(axis, time):
                status.control.append('000')
            else:
                status.control.append('001')
                logging.warning('ERROO1 - Wrong time axis for {0}'.format(ctx.filename))
            # Rebuild, read and check time boundaries squareness if needed
            if 'time_bnds' in data.variables.keys():
                axis_bnds = _rebuild_time_bnds(start, length, inc, ctx)
                time_bnds = data.variables['time_bnds'][:,:]
                if _time_checker(axis_bnds, time_bnds):
                    status.bnds = True
                else:
                    status.bnds = False
        # Rewrite time axis depending on checking
        if (ctx.write and not _time_checker(axis, time)) or ctx.force:
            data.variables['time'][:] = axis
            # Rewrite time units according to CMIP5 requirements (i.e., same units for all files)
            data.variables['time'].units = ctx.tunits
            # Rewrite time boundaries if needed
            if 'time_bnds' in data.variables.keys():
                data.variables['time_bnds'][:,:] = axis_bnds
            # Compute checksum
            status.checksum = _checksum(ctx.root+ctx.filename)
        # Control consistency between time units
        if ctx.tunits != status.units:
            status.control.append('002')
            logging.warning('ERROO2 - Changing time units for {0}'.format(ctx.filename))
    # Close file
    data.close()
    # Return file status
    return status


def _checksum(file):
    """Do MD5 checksum by Shell"""
    try:
        shell = os.popen("md5sum {0} | awk -F ' ' '{{ print $1 }}'".format(file), 'r')
        return shell.readline()[:-1]
    except:
        logging.error('Checksum failed for {0}'.format(file))
        raise Exception('Checksum failed for {0}'.format(file))


def _nc_var_delete(directory, filename, variable):
    """Delete NetCDF variable using NCO operators and overwrite input file."""
    # Generate unique filename to avoid multithreading errors
    tmp = '{0}{1}'.format(str(uuid4()), '.nc')
    try:
        os.popen("ncks -x -O -v {3} {0}{1} {0}{2} ; mv {0}{2} {0}{1}".format(directory, filename, tmp, variable), 'r')
        source = open('{0}{1}'.format(directory, tmp), 'r') # Temporary corrected file by ncks in read mode
        destination = open('{0}{1}'.format(directory, filename), 'w') # Currently input file on process in (over)write mode
        # Dumping source to destination to keep hard link system in pipeline
        destination.write(source.read())
        # Close files
        source.close() ; destination.close()
        os.remove('{0}{1}'.format(directory, tmp))
    except:
        os.remove('{0}{1}'.format(directory, tmp))
        logging.error('Deleting time_bnds failed for {0}'.format(file))
        raise Exception('Deleting time_bnds failed for {0}'.format(file))


def _dates_from_filename(filename,calendar):
    """Returns datetime objetcs for start and end dates in filename."""
    pattern = re.compile(r'([\w.-]+)_([\w.-]+)_([\w.-]+)_([\w.-]+)_([\w.-]+)_([\d]+)-([\d]+).nc')
    dates=[]
    for i in [6, 7]:
        digits = _untroncated_timestamp(pattern.search(filename).group(i))
        # Convert string digits to %Y-%m-%d %H:%M:%S format
        date_as_since = ''.join([''.join(triple) for triple in zip(digits[::2],digits[1::2],['','-','-',' ',':',':',':'])])[:-1]
        # Use num2date to create netCDF4 datetime objects
        dates.append(num2date(0.0, units = 'days since '+ date_as_since, calendar = calendar))
    return dates


def _untroncated_timestamp(timestamp):
    """Returns proper digits for yearly and monthly truncated timestamp."""
    if len(timestamp) == 4:
        # Start year at january 1st
        return (timestamp+'0101').ljust(14,'0')
    elif len(timestamp) == 6:
        # Start month at first day
        return (timestamp+'01').ljust(14,'0')
    else:
        return timestamp.ljust(14,'0')


def _num2date(num_axis, units, calendar):
    """A wrapper from netCDF4.num2date able to handle 'years since' and 'months since' units"""
    # num_axis is the numerical time axis incremented following units (i.e., by years, months, days, etc).
    if not units.split(' ')[0] in ['years','months']:
        # If units are not 'years' or 'months since', call usual netcdftime.num2date:
        return num2date(num_axis, units = units, calendar = calendar)
    else:
        # Return to time refenence with 'days since'
        units_as_days = 'days '+' '.join(units.split(' ')[1:])
        # Convert the time refrence 'units_as_days' as datetime object
        start_date = num2date(0.0, units = units_as_days, calendar = calendar)
        # Control num_axis to always get an Numpy array (even with a scalar)
        num_axis_mod = np.atleast_1d(np.array(num_axis))
        if units.split(' ')[0] == 'years':
            # If units are 'years since'
            # Define the number of maximum and minimum years to build a date axis covering the whole 'num_axis' period
            max_years = np.floor(np.max(num_axis_mod)) + 1
            min_years = np.ceil(np.min(num_axis_mod)) - 1
            # Create a date axis with one year that spans the entire period by year
            years_axis = np.array([_add_year(start_date, years_to_add) for years_to_add in np.arange(min_years, max_years+2)])
            # Convert rebuilt years axis as 'number of days since'
            year_axis_as_days = date2num(years_axis, units = units_as_days, calendar = calendar)
            # Index of each years
            yind = np.vectorize(np.int)(np.floor(num_axis_mod))
            # Rebuilt num_axis as 'days since' addint the number of days since referenced time with an half-increment (num_axis_mod - yind) = 0 or 0.5
            num_axis_mod_days = (year_axis_as_days[yind - int(min_years)] + (num_axis_mod - yind) * np.diff(year_axis_as_days)[yind - int(min_years)])
        elif units.split(' ')[0] == 'months':
            # If units are 'months since'
            # Define the number of maximum and minimum months to build a date axis covering the whole 'num_axis' period
            max_months = np.floor(np.max(num_axis_mod)) + 1
            min_months = np.ceil(np.min(num_axis_mod)) - 1
            # Create a date axis with one month that spans the entire period by month
            months_axis = np.array([_add_month(start_date,months_to_add) for months_to_add in np.arange(min_months,max_months+12)])
            # Convert rebuilt months axis as 'number of days since'
            months_axis_as_days = date2num(months_axis, units = units_as_days, calendar = calendar)
            # Index of each months
            mind = np.vectorize(np.int)(np.floor(num_axis_mod))
            # Rebuilt num_axis as 'days since' addint the number of days since referenced time with an half-increment (num_axis_mod - mind) = 0 or 0.5
            num_axis_mod_days = (months_axis_as_days[mind - int(min_months)] + (num_axis_mod - mind) * np.diff(months_axis_as_days)[mind - int(min_months)])
        # Convert result as date axis
        return num2date(num_axis_mod_days, units = units_as_days, calendar = calendar)


def _date2num(date_axis, units, calendar):
    """A wrapper from netCDF4.date2num able to handle 'years since' and 'months since' units"""
    # date_axis is the date time axis incremented following units (i.e., by years, months, days, etc).
    if not units.split(' ')[0] in ['years','months']:
        # If units are not 'years' or 'months since', call usual netcdftime.date2num:
        return date2num(date_axis, units = units, calendar = calendar)
    else:
        # Return to time refenence with 'days since'
        units_as_days = 'days '+' '.join(units.split(' ')[1:])
        # Convert date axis as number of days since time reference
        days_axis = date2num(date_axis, units = units_as_days, calendar = calendar)
        # Convert the time refrence 'units_as_days' as datetime object
        start_date = num2date(0.0, units = units_as_days, calendar = calendar)
        # Create years axis from input date axis
        years = np.array([date.year for date in np.atleast_1d(np.array(date_axis))])
        if units.split(' ')[0] == 'years':
            # If units are 'years since'
            # Define the number of maximum and minimum years to build a date axis covering the whole 'num_axis' period
            max_years = np.max(years - start_date.year) + 1
            min_years = np.min(years - start_date.year) - 1
            # Create a date axis with one year that spans the entire period by year
            years_axis = np.array([_add_year(start_date,yid) for yid in np.arange(min_years, max_years+2)])
            # Convert years axis as number of days since time reference
            years_axis_as_days = date2num(years_axis, units = units_as_days, calendar = calendar)
            # Find closest index for years_axis_as_days in days_axis
            closest_index = np.searchsorted(years_axis_as_days, days_axis)
            # ???
            return min_years + closest_index + (days_axis - years_axis_as_days[closest_index]) / np.diff(years_axis_as_days)[closest_index]
        elif units.split(' ')[0] == 'months':
            # If units are 'months since'
            # Define the number of maximum and minimum months to build a date axis covering the whole 'num_axis' period
            max_months = np.max(12 * (years - start_date.year)) + 1
            min_months = np.min(12 * (years - start_date.year)) - 1
            # Create a date axis with one month that spans the entire period by month
            months_axis = np.array([_add_month(start_date,mid) for mid in np.arange(min_months,max_months+12)])
            # Convert months axis as number of days since time reference
            months_axis_as_days = date2num(months_axis, units = units_as_days, calendar = calendar)
            # Find closest index for months_axis_as_days in days_axis
            closest_index = np.searchsorted(months_axis_as_days, days_axis)
            # ???
            return min_months + closest_index + (days_axis - months_axis_as_days[closest_index]) / np.diff(months_axis_as_days)[closest_index]


def _add_month(date, months_to_add):
    """Finds the next month from date. Accepts datetime or phony datetime from netCDF4.num2date"""
    date_next = phony_datetime(year = date.year, month = date.month, day = date.day, hour = date.hour, minute = date.minute, second = date.second)
    years_to_add = int((date.month+months_to_add - np.mod(date.month+months_to_add - 1, 12) - 1) / 12)
    new_month = int(np.mod(date.month+months_to_add - 1, 12)) + 1
    date_next.year += years_to_add
    date_next.month = new_month
    return date_next


def _add_year(date, years_to_add):
    """Finds the next year from date. Accepts datetime or phony datetime from netCDF4.num2date"""
    date_next = phony_datetime(year = date.year, month = date.month, day = date.day, hour = date.hour, minute = date.minute, second = date.second)
    date_next.year += years_to_add
    return date_next


def _is_instant_time_axis(filename, realm) :
   """Returns True if time time axis an instant axis."""
   need_instant_time = [('tas','3hr','atmos'),('uas','3hr','atmos'),('vas','3hr','atmos'),('huss','3hr','atmos'),('mrsos','3hr','land'),('tslsi','3hr','land'),('tso','3hr','ocean'),('ps','3hr','atmos'),('ua','6hrPlev','atmos'),('va','6hrPlev','atmos'),('ta','6hrPlev','atmos'),('psl','6hrPlev','atmos'),('ta','6hrLev','atmos'),('ua','6hrLev','atmos'),('va','6hrLev','atmos'),('hus','6hrLev','atmos'),('ps','6hrLev','atmos'),('clcalipso','cf3hr','atmos'),('clcalipso2','cf3hr','atmos'),('cfadDbze94','cf3hr','atmos'),('cfadLidarsr532','cf3hr','atmos'),('parasolRefl','cf3hr','atmos'),('cltcalipso','cf3hr','atmos'),('cllcalipso','cf3hr','atmos'),('clmcalipso','cf3hr','atmos'),('clhcalipso','cf3hr','atmos'),('cltc','cf3hr','atmos'),('zfull','cf3hr','atmos'),('zhalf','cf3hr','atmos'),('pfull','cf3hr','atmos'),('phalf','cf3hr','atmos'),('ta','cf3hr','atmos'),('h2o','cf3hr','atmos'),('clws','cf3hr','atmos'),('clis','cf3hr','atmos'),('clwc','cf3hr','atmos'),('clic','cf3hr','atmos'),('reffclws','cf3hr','atmos'),('reffclis','cf3hr','atmos'),('reffclwc','cf3hr','atmos'),('reffclic','cf3hr','atmos'),('grpllsprof','cf3hr','atmos'),('prcprof','cf3hr','atmos'),('prlsprof','cf3hr','atmos'),('prsnc','cf3hr','atmos'),('prlsns','cf3hr','atmos'),('reffgrpls','cf3hr','atmos'),('reffrainc','cf3hr','atmos'),('reffrains','cf3hr','atmos'),('reffsnowc','cf3hr','atmos'),('reffsnows','cf3hr','atmos'),('dtaus','cf3hr','atmos'),('dtauc','cf3hr','atmos'),('dems','cf3hr','atmos'),('demc','cf3hr','atmos'),('clc','cf3hr','atmos'),('cls','cf3hr','atmos'),('tas','cf3hr','atmos'),('ts','cf3hr','atmos'),('tasmin','cf3hr','atmos'),('tasmax','cf3hr','atmos'),('psl','cf3hr','atmos'),('ps','cf3hr','atmos'),('uas','cf3hr','atmos'),('vas','cf3hr','atmos'),('sfcWind','cf3hr','atmos'),('hurs','cf3hr','atmos'),('huss','cf3hr','atmos'),('pr','cf3hr','atmos'),('prsn','cf3hr','atmos'),('prc','cf3hr','atmos'),('evspsbl','cf3hr','atmos'),('sbl','cf3hr','atmos'),('tauu','cf3hr','atmos'),('tauv','cf3hr','atmos'),('hfls','cf3hr','atmos'),('hfss','cf3hr','atmos'),('rlds','cf3hr','atmos'),('rlus','cf3hr','atmos'),('rsds','cf3hr','atmos'),('rsus','cf3hr','atmos'),('rsdscs','cf3hr','atmos'),('rsuscs','cf3hr','atmos'),('rldscs','cf3hr','atmos'),('rsdt','cf3hr','atmos'),('rsut','cf3hr','atmos'),('rlut','cf3hr','atmos'),('rlutcs','cf3hr','atmos'),('rsutcs','cf3hr','atmos'),('prw','cf3hr','atmos'),('clt','cf3hr','atmos'),('clwvi','cf3hr','atmos'),('clivi','cf3hr','atmos'),('rtmt','cf3hr','atmos'),('ccb','cf3hr','atmos'),('cct','cf3hr','atmos'),('ci','cf3hr','atmos'),('sci','cf3hr','atmos'),('fco2antt','cf3hr','atmos'),('fco2fos','cf3hr','atmos'),('fco2nat','cf3hr','atmos'),('cl','cfSites','atmos'),('clw','cfSites','atmos'),('cli','cfSites','atmos'),('mc','cfSites','atmos'),('ta','cfSites','atmos'),('ua','cfSites','atmos'),('va','cfSites','atmos'),('hus','cfSites','atmos'),('hur','cfSites','atmos'),('wap','cfSites','atmos'),('zg','cfSites','atmos'),('rlu','cfSites','atmos'),('rsu','cfSites','atmos'),('rld','cfSites','atmos'),('rsd','cfSites','atmos'),('rlucs','cfSites','atmos'),('rsucs','cfSites','atmos'),('rldcs','cfSites','atmos'),('rsdcs','cfSites','atmos'),('tnt','cfSites','atmos'),('tnta','cfSites','atmos'),('tntmp','cfSites','atmos'),('tntscpbl','cfSites','atmos'),('tntr','cfSites','atmos'),('tntc','cfSites','atmos'),('tnhus','cfSites','atmos'),('tnhusa','cfSites','atmos'),('tnhusc','cfSites','atmos'),('tnhusd','cfSites','atmos'),('tnhusscpbl','cfSites','atmos'),('tnhusmp','cfSites','atmos'),('evu','cfSites','atmos'),('edt','cfSites','atmos'),('pfull','cfSites','atmos'),('phalf','cfSites','atmos'),('tas','cfSites','atmos'),('ts','cfSites','atmos'),('psl','cfSites','atmos'),('ps','cfSites','atmos'),('uas','cfSites','atmos'),('vas','cfSites','atmos'),('sfcWind','cfSites','atmos'),('hurs','cfSites','atmos'),('huss','cfSites','atmos'),('pr','cfSites','atmos'),('prsn','cfSites','atmos'),('prc','cfSites','atmos'),('evspsbl','cfSites','atmos'),('sbl','cfSites','atmos'),('tauu','cfSites','atmos'),('tauv','cfSites','atmos'),('hfls','cfSites','atmos'),('hfss','cfSites','atmos'),('rlds','cfSites','atmos'),('rlus','cfSites','atmos'),('rsds','cfSites','atmos'),('rsus','cfSites','atmos'),('rsdscs','cfSites','atmos'),('rsuscs','cfSites','atmos'),('rldscs','cfSites','atmos'),('rsdt','cfSites','atmos'),('rsut','cfSites','atmos'),('rlut','cfSites','atmos'),('rlutcs','cfSites','atmos'),('rsutcs','cfSites','atmos'),('prw','cfSites','atmos'),('clt','cfSites','atmos'),('clwvi','cfSites','atmos'),('clivi','cfSites','atmos'),('rtmt','cfSites','atmos'),('ccb','cfSites','atmos'),('cct','cfSites','atmos'),('ci','cfSites','atmos'),('sci','cfSites','atmos'),('fco2antt','cfSites','atmos'),('fco2fos','cfSites','atmos'),('fco2nat','cfSites','atmos')]
   pattern = re.compile(r'([\w.-]+)_([\w.-]+)_([\w.-]+)_([\w.-]+)_([\w.-]+)_([\d]+)-([\d]+).nc')
   if (pattern.search(filename).group(1), pattern.search(filename).group(2), realm) in need_instant_time:
      return True
   else:
      return False


def _time_inc(frequency):
    """Return tuple used for time incrementation depending on frequency: (raising value, time unit)."""
    inc = {'subhr': 30,
           '3hr'  : 3,
           '6hr'  : 6,
           'day'  : 1,
           'mon'  : 1,
           'yr'   : 1}
    return inc[frequency]


def _date_print(date):
    """Print date in format: %Y%m%d %H:%M:%s. Accepts datetime or phony datetime from netCDF4.num2date"""
    return '{0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(date.year, date.month, date.day, date.hour, date.minute, date.second)


def _rebuild_time_axis(start, length, instant, inc, ctx):
    """Rebuild time axis from date axis, depending on frequency and calendar."""
    date_axis, last = _rebuild_date_axis(start, length, instant, inc, ctx)
    axis = _date2num(date_axis, units = ctx.tunits, calendar = ctx.calendar)
    return axis, last


def _rebuild_date_axis(start, length, instant, inc, ctx):
    """Rebuild date axis from start date, depending on frequency and calendar."""
    num_axis = np.arange(start = start, stop = start + length * inc, step = inc)
    if ctx.funits.split(' ')[0] in ['years','months']:
        last = _num2date(num_axis[-1], units = ctx.funits, calendar = ctx.calendar)[0]
    else:
        last = _num2date(num_axis[-1], units = ctx.funits, calendar = ctx.calendar)
    if not instant:
        num_axis += 0.5 * inc
    date_axis = _num2date(num_axis, units = ctx.funits, calendar = ctx.calendar)
    return date_axis, last


def trunc(f, n):
    '''Truncates a float f to n decimal places without rounding'''
    slen = len('%.*f' % (n, f))
    return float(str(f)[:slen])


def _time_checker(right_axis, test_axis) :
   """Returns True if right axis is right."""
   if np.array_equal(right_axis, test_axis) :
      return True
   else :
      return False


def _rebuild_time_bnds(start, length, inc, ctx):
    """Rebuild time boundaries from start date, depending on frequency and calendar."""
    num_axis_bnds = np.column_stack(((np.arange(start = start, stop  = start + length * inc, step  = inc)),
                                     (np.arange(start = start, stop  = start + (length+1) * inc, step  = inc)[1:])))
    date_axis_bnds = _num2date(num_axis_bnds, units = ctx.funits, calendar = ctx.calendar)
    axis_bnds = _date2num(date_axis_bnds, units = ctx.tunits, calendar = ctx.calendar)
    return axis_bnds


def _last_date_checker(last, end):
    """Returns True if last and end date are the same."""
    if last != end:
        return False
    else:
        return True


def run(job):
    """Main entry point."""
    # Instanciate on processing context per file (for pool workers)
    ctx = _ProcessingContext(_get_args([job['full_path_variable'],'-w','-v']))
    if ctx.root.split('/')[4] != 'process':
        raise Exception('Product in full_path_variable is "{0}" instead of "process"'.format(ctx.root.split('/')[4]))
    if ctx.root.split('/')[8] == 'fx':
        logging.info('"{0}" frequency has no time axis'.format(ctx.root.split('/')[8]))     
    else:
        logging.info('time_axis_normalization.py started (variable_path={0})'.format(ctx.root))
        # Set driving time properties (calendar, frequency and time units) from first file in directory
        _time_init(ctx)
        # Process
        ctxs = []
        for filename in _get_file_list(ctx.root):
            # Instanciate one processing context per file (for pool workers)
            ctx = copy(ctx)
            ctx.filename = filename
            ctxs.append(ctx)
        logging.info('Files to process = {0}'.format(str(len(ctxs))))
        pool = ThreadPool(_THREAD_POOL_SIZE)
        status = pool.map(_time_axis_processing, ctxs)
        # Close thread pool
        pool.close()
        pool.join()
        # Save filenames (+ checksum) with modified time axis
        logging.info('Save diagnostic')
        job['files'] = {}
        for i in range(len(status)):
            job['files'][status[i].file] = {}
            job['files'][status[i].file]['version'] = ctx.version
            job['files'][status[i].file]['calendar'] = status[i].calendar
            job['files'][status[i].file]['start'] = status[i].start
            job['files'][status[i].file]['end'] = status[i].end
            job['files'][status[i].file]['last'] = status[i].last
            job['files'][status[i].file]['length'] = status[i].steps
            job['files'][status[i].file]['instant'] = status[i].instant
            job['files'][status[i].file]['bnds'] = status[i].bnds
            job['files'][status[i].file]['status'] = ','.join(status[i].control)
            job['files'][status[i].file]['new_checksum'] = status[i].checksum
        logging.info('time_axis_normalization.py complete')
        return job


# Main entry point
#if __name__ == "__main__":
#    main()
