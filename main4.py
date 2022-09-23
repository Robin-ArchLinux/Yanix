#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import select
import termios
import tty
import pty
from subprocess import Popen

path = os.path.dirname(os.path.abspath(__file__)) + "/paru"
# command = "bash"
cmd = 'sudo pacman -Syu --needed code'.split()

# command = 'docker run -it --rm centos /bin/bash'.split()

def run_cmd_with_interactive(command, cwd):
    # save original tty setting then set it to raw mode
    old_tty = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())

    # open pseudo-terminal to interact with subprocess
    master_fd, slave_fd = pty.openpty()

    try:
        # use os.setsid() make it run in a new process group, or bash job control will not be enabled
        p = Popen(command,
                  preexec_fn=os.setsid,
                  stdin=slave_fd,
                  stdout=slave_fd,
                  stderr=slave_fd,
                  universal_newlines=True, cwd=cwd)

        while p.poll() is None:
            r, w, e = select.select([sys.stdin, master_fd], [], [])
            if sys.stdin in r:
                d = os.read(sys.stdin.fileno(), 10240)
                print(f"from sys.stdin, {d}")
                os.write(master_fd, d)
            elif master_fd in r:
                o = os.read(master_fd, 10240)
                if o:
                    print(f"from master_fd, {o}")
                    os.write(sys.stdout.fileno(), o)
    finally:
        # restore tty settings back
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)


run_cmd_with_interactive(cmd, path)