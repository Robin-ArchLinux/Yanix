# -*- coding: utf-8 -*-
import os
import subprocess
import signal


class MockLogger(object):
    def __init__(self):
        self.info = self.error = self.critical = self.debug

    def debug(self, msg):
        print("LOGGER:" + msg)


class Shell(object):
    def __init__(self, cmd):
        self.cmd = cmd  # cmd包括命令和参数
        self.ret_code = None
        self.ret_info = None
        self.err_info = None
        self._process = None
        # 使用时可替换为具体的logger
        self.logger = MockLogger()

    def run_background(self):
        self.logger.debug("run %s" % self.cmd)
        self._process = subprocess.Popen(self.cmd, shell=True,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)  # 非阻塞

    def run(self):
        self.run_background()
        self.wait()

    def run_cmd(self, cmd):
        self.cmd = cmd
        self.run()

    def wait(self):
        self.logger.debug("waiting %s" % self.cmd)
        self.ret_info, self.err_info = self._process.communicate()  # 阻塞
        self.ret_code = self._process.returncode
        self.logger.debug("waiting %s done. return code is %d" % (self.cmd,
                                                                  self.ret_code))

    def get_status(self):
        ret_code = self._process.poll()
        if ret_code is None:
            status = "RUNNING"
        else:
            status = "FINISHED"
        self.logger.debug("%s status is %s" % (self.cmd, status))
        return status

    def send_signal(self, sig):
        self.logger.debug("send signal %s to %s" % (sig, self.cmd))
        os.kill(self._process.pid, sig)

    def terminate(self):
        self.send_signal(signal.SIGTERM)

    def kill(self):
        self.send_signal(signal.SIGKILL)

    def print_result(self):
        print("return code:", self.ret_code)
        print("return info:", self.ret_info.decode("utf-8"))
        print("error info:", self.err_info.decode("utf-8"))
        print("\n")


class SuShell(Shell):
    '''切换用户执行命令（su方式）。
    XXX 只适合使用root切换至其它用户。
      因为其它切换用户后需要输入密码，这样程序会挂住。
    XXX 含特殊字符的命令可能导致调用失效，如双引号，美元号$
    NOTE 若cmd含有双引号，可使用SuShell2
    '''

    def __init__(self, cmd, user):
        if os.getuid() != 0:  # 非root用户直接报错
            raise Exception('SuShell must be called by root user!')
        cmd = 'su - %s -c "%s"' % (user, cmd)
        Shell.__init__(self, cmd)


if __name__ == "__main__":
    # 1. test normal
    sa = Shell('who')
    sa.run()
    sa.print_result()

    # 2. test stderr
    sb = Shell('ls /export/dir_should_not_exists')
    sb.run()
    sb.print_result()

    # 3. test background
    sc = Shell('sleep 1')
    sc.run_background()

    print('hello from parent process')
    print("return code:", sc.ret_code)
    print("status:", sc.get_status())

    sc.wait()
    sc.print_result()

    # 4. test kill
    import time

    sd = Shell('sleep 2')
    sd.run_background()
    time.sleep(1)
    sd.kill()
    sd.wait()  # NOTE, still need to wait
    sd.print_result()

    # 5. test multiple command and uncompleted command output
    se = Shell('pwd;sleep 1;pwd;pwd')
    se.run_background()
    time.sleep(1)
    se.kill()
    se.wait()  # NOTE, still need to wait
    se.print_result()

    # 6. test wrong command
    sf = Shell('aaaaa')
    sf.run()
    sf.print_result()

    # wrong user
    # si = SuShell('pwd', 'ossuser123')
    # si.run()
    # si.print_result()

    # user need password
    # si = SuShell('pwd', 'root')
    # si.run()
    # si.print_result()
    sf = Shell('sudo pacman -S gimp')
    sf.run()
    sf.print_result()
