#!/usr/bin/env python
# coding:utf-8
import os, sys
import logging
import traceback
from pprint import pprint

logging.basicConfig(level=logging.DEBUG,
   format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
   datefmt='%a, %d %b %Y %H:%M:%S',
   filename='debug.log',
   filemode='a')


def normalize_string_to_list(object):
    output = object
    if type(output) == type([]):
        pass
    else:
        output=[str(object)]
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
    class processNotFoundException(Exception):
        pass

    texts_wanted=normalize_string_to_list(texts_wanted)



    try:
        commands=[]
        commands.append('ps -ef')
        for text_wanted in texts_wanted:
            commands.append("grep -i '%s'" % text_wanted)
        commands.append("grep -v 'grep'")

        logging.debug('try to get the pid of the process')

        ps_printout = os.popen(' | '.join(commands)).read().strip()

        if len(ps_printout.split('\r')) > 0 :
            return int(ps_printout.split()[1])
            pass
        else:
            raise processNotFoundException

        pass
    except Exception as e:
        print('error during getting the pid of the process')

        # TODO: consider remove me
        from pprint import pprint
        print('dump the value of: process_wanted')
        pprint(texts_wanted)

        raise e
    else:
        pass
