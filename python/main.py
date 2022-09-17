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


def main():
    Argos.configure(IS_DEBUG)
    common_cmd.set_keyboard_layout("us")
    common_cmd.set_time_zone("Asia/Shanghai")
    home_file_list = common_cmd.list_dir("/home/robin")
    pass


main()
