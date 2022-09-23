import os
import subprocess
import sys
import select
import termios
import tty
import pty
from typing import List
from result import Result, Ok, Err
from constant import ROOT_DIR

from argos import Argos


def run_cmd(cmd, pipe=False, cwd=None) -> Result[str, str]:
    Argos.d(f"➜  {cmd}")
    # p_open = subprocess.Popen(cmd, text=True,encoding="UTF-8", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # stdout, stderr = p_open.communicate("Y\n")
    # if stdout is None:
    #     return Err(stderr.strip())
    # else:
    #     return Ok(stdout.strip())

    if pipe:
        res = subprocess.run(cmd, shell=True, text=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             encoding="utf8", cwd=cwd)
        if res.returncode == 0:
            return Ok(res.stdout.strip())
        else:
            return Err(res.stderr.strip())
    else:
        res = subprocess.run(cmd, shell=True, text=True, stdin=None, stdout=None, stderr=None, cwd=cwd)
        Argos.e(f"return code: {res.returncode}")
        if res.returncode == 0:
            return Ok()
        else:
            return Err(res.stderr.strip())


def run_cmd_with_interactive(command, cwd=None):
    # save original tty setting then set it to raw mode
    old_tty = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())

    # open pseudo-terminal to interact with subprocess
    master_fd, slave_fd = pty.openpty()

    try:
        # use os.setsid() make it run in a new process group, or bash job control will not be enabled
        p = subprocess.Popen(command,
                             preexec_fn=os.setsid,
                             stdin=slave_fd,
                             stdout=slave_fd,
                             stderr=slave_fd,
                             universal_newlines=True, cwd=cwd)

        while p.poll() is None:
            r, w, e = select.select([sys.stdin, master_fd], [], [])
            if sys.stdin in r:
                d = os.read(sys.stdin.fileno(), 10240)
                os.write(master_fd, d)
            elif master_fd in r:
                o = os.read(master_fd, 10240)
                if o:
                    os.write(sys.stdout.fileno(), o)
    finally:
        # restore tty settings back
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)


def pac_install(package):
    cmd = f"sudo pacman -Syu --needed {package}"
    run_cmd_with_interactive(cmd)
    # result = run_cmd(cmd)
    # match result:
    #     case Ok(_):
    #         Argos.s(f"package: {package} install success.")
    #     case Err(e):
    #         Argos.e(f"install package failed, error:\n{e}")


def list_dir(directory) -> List:
    cmd = f"ls {directory}"
    result = run_cmd(cmd, True)
    match result:
        case Ok(value):
            file_list = value.split("\n")
            Argos.s(file_list)
            return file_list
        case Err(e):
            Argos.e(e)


def set_keyboard_layout(layout):
    cmd = f"loadkeys {layout}"
    result = run_cmd(cmd)
    match result:
        case Ok(_):
            Argos.s(f"set keyboard layout to `{layout}`")
        case Err(e):
            Argos.e(f"set keyboard layout failed: {e}")


def set_time_zone(zone):
    cmd = f"timedatectl set-timezone {zone}"
    result = run_cmd(cmd)
    match result:
        case Ok(_):
            Argos.s(f"set time zone to `{zone}`")
        case Err(e):
            Argos.e(f"set time zone failed: {e}")


def install_paru():
    is_paru_installed = run_cmd("paru -h", pipe=True)
    match is_paru_installed:
        case Ok(_):
            Argos.s("paru has already installed")
        case Err(_):
            pac_install("base-devel")
            run_cmd("git clone https://aur.archlinux.org/paru.git")
            pac_install("rust")
            cmd = "makepkg -si"
            result = run_cmd(cmd, cwd=f"{ROOT_DIR}/paru")
            match result:
                case Ok(_):
                    Argos.s(f"install paru success")
                case Err(e):
                    Argos.e(f"install paru failed, err: {e}")


def aur_install(package):
    cmd = f"paru -Syu --needed {package}"
    result = run_cmd(cmd)
    match result:
        case Ok(_):
            Argos.s(f"package: {package} install success.")
        case Err(e):
            Argos.e(e)
