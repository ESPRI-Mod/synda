#!/usr/bin/env python
"""
.. module:: overlaps.py
   :platform: Unix
   :synopsis: Highlight chunked files producing overlpas in a time series.

.. moduleauthor:: Denvil, S. <sdipsl@ipsl.jussieu.fr> and Levavasseur, G. <glipsl@ipsl.jussieu.fr>


"""

# Module imports
import re, os, argparse, logging
import numpy as np
import networkx as nx
from netCDF4 import Dataset, date2num, num2date
from netcdftime import datetime as phony_datetime



class _ProcessingContext(object):
    """Encapsulate processing context information for main process."""
    def __init__(self, args):
        self.always = args.always
        self.verbose = args.verbose
        self.exclude = args.exclude
        self.remove = args.remove
        self.directory = args.directory


def _get_args(args_list):
    """Returns parsed command line arguments."""
    parser = argparse.ArgumentParser(
        description = """Highlight chunked files producing overlpas in a time series.""",
        epilog="Developped by G. Levavasseur (CNRS/IPSL)")
    parser.add_argument('directory',
        nargs = '?',
        help = """Dataset root path to browse following CMIP5 DRS""")
    parser.add_argument('-v', '--verbose',
        action = 'store_true',
        default = False,
        help = """Verbose mode""")
    parser.add_argument('-a', '--always',
        action = 'store_true',
        default = False,
        help = """List the most consecutive files if no complete shortest path exists""")
    parser.add_argument('-x', '--exclude',
        action = 'store_true',
        default = False,
        help = """List the files causing the overlap, default is to list non overlapping files""")
    parser.add_argument('-r', '--remove',
        action = 'store_true',
        default = False,
       help = """Remove overlapping files. THIS ACTION DEFINITELY MODIFY INPUT DIRECTORY!""")
    return parser.parse_args(args_list)


def _find_key(dic, val):
    """Return the key of dictionary given the value."""
    return [k for k, v in dic.iteritems() if v == val][0]


def _dates_from_filename(filename,calendar,frequency):
    """Returns datetime objetcs for start and end dates in filename."""
    pattern = re.compile(r'([\w.-]+)_([\w.-]+)_([\w.-]+)_([\w.-]+)_([\w.-]+)_([\d]+)-([\d]+).nc')
    dates=[]
    for i in [6, 7]: 
        digits = _untroncated_timestamp(pattern.search(filename).group(i))
        # Convert string digits to %Y-%m-%d %H:%M:%S format
        date_as_since = ''.join([''.join(triple) for triple in zip(digits[::2],digits[1::2],['','-','-',' ',':',':',':'])])[:-1]
        # Use num2date to create netCDF4 datetime objects
        dates.append(num2date(0.0, units = 'days since '+ date_as_since, calendar = calendar))
    if _time_inc(frequency)[1] in ['years','months']:
        dates.append(_num2date(_time_inc(frequency)[0], units = _time_inc(frequency)[1] +' since '+ date_as_since, calendar = calendar)[0])
    else:
        dates.append(_num2date(_time_inc(frequency)[0], units = _time_inc(frequency)[1] +' since '+ date_as_since, calendar = calendar))
    return dates


def _time_inc(frequency):
    """Return tuple used for time incrementation depending on frequency: (raising value, time unit)."""
    inc = {'subhr': [30, 'minutes'],
           '3hr'  : [3, 'hours'],
           '6hr'  : [6, 'hours'],
           'day'  : [1, 'days'],
           'mon'  : [1, 'months'],
           'yr'   : [1, 'years']}
    return inc[frequency]


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


def _datetime_to_string(datetimes):
    """Converts a list of datetime object into list of strings with appropriate digits."""
    dates = []
    for datetime in datetimes:
        dates.append(str(datetime.year).zfill(4) + str(datetime.month).zfill(2) + str(datetime.day).zfill(2) + str(datetime.hour).zfill(2) + str(datetime.minute).zfill(2))
    return dates


def _get_file_list(directory):
    """Returns file list of a directory."""
    try:   
        files = sorted(os.listdir(directory))
    except:
        raise Exception('No such directory: {0}'.format(directory)) 
    pattern = re.compile(r'([\w.-]+)_([\w.-]+)_([\w.-]+)_([\w.-]+)_([\w.-]+)_([\d]+)-([\d]+).nc')
    for file in files:
        if re.match(pattern, file) == None:
            raise Exception('Invalid filename: {0}'.format(file))
    return files


def run(job):
    """Main entry point."""
    # Instanciate processing context
    ctx = _ProcessingContext(_get_args(['-x', '-v', '-r', job['full_path_variable']]))
    if ctx.directory.split('/')[4] != 'process':
        raise Exception('Product in full_path_variable is "{0}" instead of "process"'.format(ctx.directory.split('/')[4]))
    if ctx.directory.split('/')[8] == 'fx':
        logging.info('"{0}" frequency has no overlap'.format(ctx.directory.split('/')[8]))
    else:
        logging.info('overlap.py started (variable_path = {0})'.format(ctx.directory))     
        # DiGraph creation
        G = nx.DiGraph() ; G.clear()
        starts = [] ; ends = [] ; nexts=[]
        filenames = _get_file_list(ctx.directory)
        data = Dataset(ctx.directory+filenames[0])
        calendar = data.variables['time'].calendar
        data.close()
        frequency = ctx.directory.split('/')[8]
        if ctx.verbose:
            logging.info('{0} | {1} | {2} | {3}'.format('File'.center(70), 'Start'.center(14), 'End'.center(14), 'Next'.center(14)))
        for filename in filenames:
            start, end, next = _datetime_to_string(_dates_from_filename(filename, calendar, frequency))
            if ctx.verbose:
                logging.info('{0} | {1} | {2} | {3}'.format(filename.center(70),start.center(14),end.center(14),next.center(14)))
            starts.append(int(start))
            ends.append(int(end))
            nexts.append(int(next))
            # Add nodes and edges
            G.add_edge(int(start), int(next))
        oldest = min(starts) ; latest = max(nexts) ; match = [] ; overlaps = filenames
        try:
            shortest = nx.shortest_path(G, source = oldest, target = latest)
            logging.info('Shortest path found')
            for i in range(len(shortest)-1):
                for j in range(len(starts)):
                    if (starts[j] == shortest[i] and nexts[j] == shortest[i+1]):
                        match.append(filenames[j])
            for filename in match:
                overlaps.remove(filename)
            if ctx.verbose: 
                if ctx.exclude:
                    logging.info('List of overlapping files:')
                    for filename in overlaps:
                        logging.info(filename)
                else:
                    logging.info('List of matching files:')
                    for filename in match:
                        logging.info(filename)
            if ctx.remove:
                for filename in overlaps:
                    os.remove(ctx.directory+filename)
                if not overlaps:
                    logging.info('No overlapping files')
                else:
                    logging.info('{0} overlapping files removed'.format(len(overlaps)))
        except nx.NetworkXNoPath, e:
            if ctx.always:
                logging.info('Use the longest subtree instead: {0}'.format(str(e)))
                pred, dist = nx.bellman_ford(G, oldest)
                alter_latest = _find_key(dist, max(dist.values()))
                alter_shortest = nx.shortest_path(G, source = oldest, target = alter_latest)
                for i in range(len(alter_shortest)-1):
                    for j in range(len(starts)):
                        if (starts[j] == alter_shortest[i] and nexts[j] == alter_shortest[i+1]):
                            match.append(filenames[j])
                for filename in match:
                    overlaps.remove(filename )
                if ctx.verbose: 
                    if ctx.exclude:
                        logging.info('List of overlapping files:')
                        for filename in overlaps:
                            logging.info(filename)
                    else:
                        logging.info('List of matching files:')
                        for filename in match:
                            logging.info(filename)
                if ctx.remove:
                    for filename in overlaps:
                        os.remove(ctx.directory+filename)
                    if not overlaps:
                        logging.info('No overlapping files')
                    else:
                        logging.info('{0} overlapping files removed'.format(len(overlaps)))
            else:
                logging.info('No shortest path found: {0}'.format(str(e)))
        logging.info('overlap.py complete')


# Main entry point
#if __name__ == "__main__":
#    main()
