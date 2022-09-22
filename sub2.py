# sub2.py
from time import sleep


def log(s: str):
    print('[Sub] ' + s)


for i in range(5):
    log('Msg ' + str(i))
    sleep(0.5)