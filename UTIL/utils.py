import sys
import time

# execute os command
def osCommand(cmd):
    pyVersion = str(sys.version_info)
    if 'major=2' in pyVersion:
        import commands
        return commands.getoutput(cmd)
    else:
        import subprocess
        return subprocess.getoutput(cmd)

def log(msg):
    print(time.strftime("%H:%M:%S") + ": " + msg)
    return

def logv2(msg, type):
    if (msg != ""):
        str = '{0:-<60}'.format(msg)
        print(str + type)
