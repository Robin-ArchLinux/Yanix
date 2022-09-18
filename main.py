import sys
import subprocess
import common_cmd
from loguru import logger
from argos import Argos
from constant import IS_DEBUG


def test_cmd(args):
    cmd1 = """
    cd /home
    ls
    cd robin
    ls
    """
    cp = subprocess.run(cmd1, shell=True, stdout=subprocess.PIPE)
    print(cp.stdout.decode("UTF8"))


def install_system():
    Argos.configure(IS_DEBUG)
    common_cmd.set_keyboard_layout("us")
    common_cmd.set_time_zone("Asia/Shanghai")
    home_file_list = common_cmd.list_dir("/home/robin")


def config_system():
    pass


def main(argv: str):
    match argv:
        case 'install':
            install_system()
        case 'config':
            config_system()


if __name__ == '__main__':
    main(sys.argv[1])
