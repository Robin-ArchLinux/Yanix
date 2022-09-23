import subprocess

cmd = "sudo pacman -Syu --needed code"
res = subprocess.run(cmd, shell=True, text=True, stdin=None, stdout=None, stderr=subprocess.PIPE,
                     encoding="utf8")
