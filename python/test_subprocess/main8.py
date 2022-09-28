import pexpect

x = pexpect.spawn('sudo pacman -Syu --needed code') #Start subprocess.
x.interact()                     #Imbed subprocess in current process.

command = "sudo pacman -Syu --needed code"
process = pexpect.spawn(command)
process.expect(pexpect.EOF)
output = process.before

process.close()
exit_code = process.exitstatus
print(exit_code)