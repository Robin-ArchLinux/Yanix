import subprocess
import pty
import os
import sys
import select
import shlex

cmd = "sudo pacman -Syu --needed code"

m_fd, s_fd = pty.openpty()

# use os.setsid() make it run in a new process group, or bash job control will not be enabled
p = subprocess.Popen(cmd.split(),
                     preexec_fn=os.setsid,
                     stdin=s_fd,
                     stdout=s_fd,
                     stderr=s_fd,
                     universal_newlines=True)

while p.poll() is None:
    r, w, e = select.select([sys.stdin, m_fd], [], [])
    if sys.stdin in r:
        d = os.read(sys.stdin.fileno(), 10240)
        os.write(m_fd, d)
    elif m_fd in r:
        o = os.read(m_fd, 10240)
        if o:
            os.write(sys.stdout.fileno(), o)
