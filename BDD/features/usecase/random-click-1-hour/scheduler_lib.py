#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='debug.log',
                    filemode='a')

from sys import platform


class processNotFoundException(Exception):
    pass


def normalize_string_to_list(object):
    output = object
    if type(output) == type([]):
        pass
    else:
        output = [str(object)]
    return output


def getPidOfProcess(texts_wanted):
    """to get the pid of the process by its grepable text

    Args:
        texts_wanted: the iconic text of the process

    Returns:
        Return1 : the pid of the process

    Assumption:
        single process per android_serial
    """

    texts_wanted = normalize_string_to_list(texts_wanted)

    try:
        pid_of_process = -1
        commands = []
        commands.append('ps -ef')
        for text_wanted in texts_wanted:
            commands.append("grep -i '%s'" % text_wanted)
        commands.append("grep -v 'grep'")

        logging.debug('try to get the pid of the process')

        print('getting list of process')
        ps_printout = os.popen(' | '.join(commands)).read().strip()

        if ps_printout.find(texts_wanted[0]) > -1:

            # from sys import platform
            if platform == "linux" or platform == "linux2":
                # linux
                print('the target process found')
                print(ps_printout.split(' '))
                pid_of_process = int(ps_printout.split(' ')[1])
            elif platform == "darwin":
                # OS X
                print('the target process found')
                print(ps_printout.split(' '))
                pid_of_process = int(ps_printout.split(' ')[1])
            elif platform == "win32":
                # Windows...
                pass

        return pid_of_process

    except Exception as e:
        print('error during getting the pid of the process')

        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: process_wanted')
        pprint(texts_wanted)

        print('dump the value of: pid_of_process')
        pprint(pid_of_process)

        raise e
    else:
        pass
