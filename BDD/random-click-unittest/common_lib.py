#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint

from time import sleep
import datetime


def requirefile(filepath):
    try:
        if os.path.exists(filepath):
            logging.info('checking of %s ok' % filepath)
            pass
        else:
            raise e
        pass
    except Exception as e:
        logging.error('checking of required file fail: %s' % filepath)
        raise e
    else:
        pass


def getTodayString(offset=0):
    """get the day string using the format "yymmdd-hhmmss" with the given offset(default=0, +ve number for the day in the past)

    Args:
        offset : offset by days, 1 for yesterday, 2 for day before yesterday and so on...

    Returns:
        Return1 : the 1st arguments
    """
    t = datetime.datetime.now()
    return (t - datetime.timedelta(days=offset)).strftime('%d%m%Y-%H%M%S')


def setup_logging(logging_directory):
    logging_filename = os.path.sep.join([
        logging_directory,
        os.path.basename(__file__).replace('.py', '') +
        getTodayString() + '-debug.log'
    ])

    LOGGING_FORMATTER = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    logging.basicConfig(
        level=logging.DEBUG,
        format=LOGGING_FORMATTER,
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename=logging_filename,
        filemode='a')

    formatter = logging.Formatter(LOGGING_FORMATTER)

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use

    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    logging.info('initialize done')
    logging.info('log file write to : %s ' % logging_filename)


def get_epoch_time():
    """
        return the epoch of current time
    """
    return int(datetime.datetime.now().strftime('%s'))


def get_time_difference_to(given_time):
    """
    calculate the different (in seconds) between now and the given time

    Args:
        given_time: the int(in epoch format) want to check

    Returns:
        the time different between now and the given_time

    """
    return get_epoch_time() - given_time


def get_end_time(time_to_start, time_to_run):
    """
    return the target end time by a given start time, adding the time to keep run


    Args:
        time_to_start: epoch format of start time
        time_to_run: length of the time to keep (seconds)

    Returns:
        the time to end in epoch format
    """
    return time_to_start + time_to_run


def normalize_string_to_list(object):
    output = object
    if type(output) == type([]):
        pass
    else:
        output = [str(object)]
    return output
