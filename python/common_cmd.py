import shlex
import logging
import subprocess
from typing import List
from result import Result, Ok, Err

from argos import Argos


def run_cmd(cmd) -> Result[str, str]:
    Argos.i(cmd)
    res = subprocess.run(cmd, shell=True, capture_output=True)
    if (res.returncode == 0):
        return Ok(res.stdout.decode("UTF-8").strip())
    else:
        return Err(res.stderr.decode("UTF-8").strip())


def list_dir(dir) -> List:
    cmd = f"ls {dir}"
    result = run_cmd(cmd)
    match result:
        case Ok(value):
            list = value.split("\n")
            Argos.s(list)
            return list
        case Err(e):
            Argos.e(e)


def set_keyboard_layout(layout):
    cmd = f"loadkeys {layout}"
    result = run_cmd(cmd)
    match result:
        case Ok(value):
            Argos.s(f"set keyboard layout to `{layout}`")
        case Err(e):
            Argos.e(f"set keyboard layout failed: {e}")


def set_time_zone(zone):
    cmd = f"timedatectl set-timezone {zone}"
    result = run_cmd(cmd)
    match result:
        case Ok(value):
            Argos.s(f"set time zone to `{zone}`")
        case Err(e):
            Argos.e(f"set time zone failed: {e}")

