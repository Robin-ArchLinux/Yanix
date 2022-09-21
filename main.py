import sys
import subprocess
import common_cmd
import config_system
import install_system
from argos import Argos
from constant import IS_DEBUG


def main(argv: str):
    Argos.configure(IS_DEBUG)
    match argv:
        case '--install':
            install_system.run()
        case '--config':
            config_system.run()


if __name__ == '__main__':
    main(sys.argv[1])
