#!/usr/bin/env python
# coding:utf-8
import os
import sys
import logging
import traceback
from pprint import pprint

import shlex

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
        pid_of_process = []
        commands = []
        commands.append('ps -ef')
        for text_wanted in texts_wanted:
            commands.append("grep -i '%s'" % text_wanted)
        commands.append("grep -v 'grep'")

        logging.debug('try to get the pid of the process')

        print('getting list of process')
        print_process_command = ' | '.join(commands)
        logging.debug(print_process_command)
        ps_list = os.popen(print_process_command).read().split('\n')

        from pprint import pprint
        print('dump the value of: ps_list')
        pprint(ps_list)

        for ps_printout in ps_list:

            # TODO: consider remove me

            if ps_printout.find(texts_wanted[0]) > -1:

                # from sys import platform
                if platform == "linux" or platform == "linux2":
                    # linux
                    print('the target process found')
                    pid_of_process.append(int(shlex.split(ps_printout)[1]))

                    logging.debug(','.join(pid_of_process))
                elif platform == "darwin":
                    # OS X
                    print('the target process found')
                    print(shlex.split(ps_printout))
                    pid_of_process.append(int(shlex.split(ps_printout)[1]))

                elif platform == "win32":
                    # Windows...
                    pass

        # NOTE: return -1 if not found
        if pid_of_process ==[]:
            pid_of_process == [-1]

        return pid_of_process

    except Exception as e:
        print('error during getting the pid of the process')

        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: process_wanted')
        pprint(texts_wanted)

        print('dump the value of: print_process_command')
        pprint(print_process_command)

        print('dump the value of: ps_list')
        pprint(ps_list)

        print('dump the value of: platform')
        pprint(platform)

        print('dump the value of: ps_printout')
        pprint(ps_printout)

        print('dump the value of: pid_of_process')
        pprint(pid_of_process)

        raise e
    else:
        pass
