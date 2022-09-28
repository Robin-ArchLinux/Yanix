#!/usr/bin/python
# I have this in a script named  logbatch
import pty, sys, os

if len(sys.argv) < 2:
    print("Need a command to run")
    sys.exit(-1)

logfilename = '%s.log' % os.path.basename(sys.argv[1])  # executable name + '.log'
if os.path.exists(logfilename):
    print(f"\nRefusing to overwrite existing log {logfilename}\n\nRename or remove it and try again\n")
    sys.exit(-1)

logfile = open(logfilename, 'wb')


def read(fd):
    data = os.read(fd, 1024)
    logfile.write(data)
    logfile.flush()  # probably
    return data


sys.stdout.write('Writing log to %r\n' % logfilename)
sys.stdout.flush()
pty.spawn(sys.argv[1:], read)

sys.stdout.write(f"Done with logging \n" )
