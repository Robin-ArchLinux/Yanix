# main3.py
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from queue import Queue, Empty
from threading import Thread


def func(proc: Popen, que: Queue):
    while True:
        msg = proc.stdout.readline()
        que.put(msg)


proc = Popen('python ./sub2.py', shell=True, encoding='utf-8', bufsize=1,
             stdin=PIPE, stdout=PIPE, stderr=STDOUT)

msg_que = Queue()
th1 = Thread(target=func, args=(proc, msg_que), daemon=True)
th1.start()

while proc.poll() is None:
    sleep(0.2)

    try:
        print(msg_que.get(block=False), end='')
    except Empty:
        print('[Main] Noting get.')