#!/usr/bin/env python

from datetime import datetime


def print_verdict(verdict_string):
    """
        print verdict,
        TODO: verdict string formatter
    """
    print('verdict: %s' % verdict_string)


def print_fail(fail_string):
    """
        print fail,
        TODO: fail string formatter
    """
    print('fail: %s' % fail_string)


def get_epoch_time():
    """
        return the epoch of current time
    """
    return int(datetime.now().strftime('%s'))


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
