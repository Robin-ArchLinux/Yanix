import subprocess


def main():
    cmd1 = """
    cd /home
    ls
    cd robin
    ls
    """
    cp = subprocess.run(cmd1, shell=True, stdout=subprocess.PIPE)
    print(cp.stdout.decode("UTF8"))
    pass


main()
