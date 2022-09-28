import sys
from python import config_system, install_system
from python.argos import Argos
from python.constant import IS_DEBUG


def main(argv: str):
    Argos.configure(IS_DEBUG)
    match argv:
        case '--install':
            install_system.run()
        case '--config':
            config_system.run()


if __name__ == '__main__':
    main(sys.argv[1])
