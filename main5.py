import subprocess
import shlex
from constant import ROOT_DIR

# cmd = "sudo pacman -Syu --needed code"
# cmd = shlex.split(cmd)
# res = subprocess.run(cmd, text=True, stdin=None, stdout=None, stderr=None, cwd=None)

cmd = "makepkg -si"
cmd = shlex.split(cmd)
cwd = f"${ROOT_DIR}/paru"
res = subprocess.run(cmd, text=True, stdin=None, stdout=None, stderr=None, cwd=cwd)
