import subprocess
import sys
from typing import List
from result import Result, Ok, Err

from argos import Argos


def run_cmd(cmd) -> Result[str, str]:
    Argos.i(cmd)
    # p_open = subprocess.Popen(cmd, text=True,encoding="UTF-8", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # stdout, stderr = p_open.communicate("Y\n")
    # if stdout is None:
    #     return Err(stderr.strip())
    # else:
    #     return Ok(stdout.strip())

    res = subprocess.run(cmd, shell=True, text=True, stdin=None, stdout=None, stderr=subprocess.PIPE, encoding="utf8")
    if res.returncode == 0:
        return Ok("")
    else:
        return Err(res.stderr.strip())


def pac_install(package):
    cmd = f"sudo pacman -Syu --needed {package}"
    result = run_cmd(cmd)
    match result:
        case Ok(_):
            Argos.s(f"package: {package} install success.")
        case Err(e):
            Argos.e(f"install package failed, error:\n{e}")


def list_dir(directory) -> List:
    cmd = f"ls {directory}"
    result = run_cmd(cmd)
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
    is_paru_installed = run_cmd("paru -h")
    match is_paru_installed:
        case Ok(_):
            Argos.s("paru has already installed")
        case Err(_):
            pac_install("base-devel")
            cmd = "git clone https://aur.archlinux.org/paru.git && cd paru && makepkg -si"
            result = run_cmd(cmd)
            match result:
                case Ok(_):
                    Argos.s(f"install paru success")
                case Err(e):
                    Argos.e(f"install paru failed")


def aur_install(package):
    cmd = f"paru -Syu --needed {package}"
    result = run_cmd(cmd)
    match result:
        case Ok(_):
            Argos.s(f"package: {package} install success.")
        case Err(e):
            Argos.e(e)
