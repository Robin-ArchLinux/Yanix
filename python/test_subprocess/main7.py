import subprocess
import shlex

cmd = "sudo pacman -Syu --needed gimp"
ssh = subprocess.Popen(shlex.split(cmd),
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       )

# Send ssh commands to stdin
# ssh.stdin.write("uname -a\n")
# ssh.stdin.write("uptime\n")
# ssh.stdin.close()

# Fetch output
for line in ssh.stdout:
    print(line.strip())
