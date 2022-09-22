import pty
import re
import select
import threading
from datetime import datetime, timedelta
import os
import logging
import subprocess
import time
from queue import Queue, Empty

lib_logger = logging.getLogger("lib")

DEVICE_TIMEOUT = 5


# Handler function to be run as a thread for pulling pty channels from an interactive shell
def _pty_handler(pty_master, logger, queue, stop):
    poller = select.poll()
    poller.register(pty_master, select.POLLIN)
    while True:
        # Stop handler if flagged
        if stop():
            logger.debug("Disabling pty handler for interactive shell")
            break

        fd_event = poller.poll(100)
        for descriptor, event in fd_event:
            # Read data from pipe and send to queue if there is data to read
            if event == select.POLLIN:
                data = os.read(descriptor, 1).decode("utf-8")
                if not data:
                    break
                # logger.debug("Reading in to handler queue: " + data)
                queue.put(data)
            # Exit handler if stdout is closing
            elif event == select.POLLHUP:
                logger.debug("Disabling pty handler for interactive shell")
                break


# Function for reading outputs from the given queue by draining it and returning the output
def _get_queue_output(queue: Queue) -> str:
    value = ""
    try:
        while True:
            value += queue.get_nowait()
    except Empty:
        return value


# Helper function to create the needed list for popen and print the command run to the logger
def popen_command(command, logger, *args):
    popen_list = list()
    popen_list.append(command)
    command_output = command
    for arg in args:
        popen_list.append(arg)
        command_output += " " + arg
    lib_logger.debug("Making Popen call using: " + str(popen_list))
    logger.debug("")
    logger.debug(command_output)
    logger.debug("")

    return popen_list


# Class for create an interactive shell and sending commands to it along with logging output to loggers
class InteractiveShell(object):
    def __init__(self, command, logger, *args):
        self.logger = logger
        self.command = command
        self.process = None
        self.popen_list = popen_command(command, logger, *args)
        self.master_stdout = None
        self.slave_stdout = None
        self.master_stderr = None
        self.slave_stderr = None
        self.stdout_handler = None
        self.stderr_handler = None
        self.stdout_queue = None
        self.stderr_queue = None
        self.stop_handlers = False

    # Open interactive shell and setup all threaded IO handlers
    def open(self, shell_prompt, timeout=DEVICE_TIMEOUT):
        # Create PTYs
        self.master_stdout, self.slave_stdout = pty.openpty()
        self.master_stderr, self.slave_stderr = pty.openpty()

        # Create shell subprocess
        self.process = subprocess.Popen(self.popen_list, stdin=self.slave_stdout, stdout=self.slave_stdout,
                                        stderr=self.slave_stderr, bufsize=0, start_new_session=True)

        lib_logger.debug("")
        lib_logger.debug("Started interactive shell for command " + self.command)
        lib_logger.debug("")

        # Create thread and queues for handling pty output and start them
        self.stdout_queue = Queue()
        self.stderr_queue = Queue()
        self.stdout_handler = threading.Thread(target=_pty_handler, args=(self.master_stdout,
                                                                          lib_logger,
                                                                          self.stdout_queue,
                                                                          lambda: self.stop_handlers))
        self.stderr_handler = threading.Thread(target=_pty_handler, args=(self.master_stderr,
                                                                          lib_logger,
                                                                          self.stderr_queue,
                                                                          lambda: self.stop_handlers))
        self.stdout_handler.daemon = True
        self.stderr_handler.daemon = True
        lib_logger.debug("Enabling stderr handler for interactive shell " + self.command)
        self.stderr_handler.start()
        lib_logger.debug("Enabling stdout handler for interactive shell " + self.command)
        self.stdout_handler.start()

        # Wait for shell prompt
        lib_logger.debug("Waiting for shell prompt: " + shell_prompt)
        return self.wait_for(shell_prompt, timeout)

    # Close interactive shell which should also kill all threaded IO handlers
    def close(self):
        # Wait 5 seconds before closing to let shell handle all input and outputs
        time.sleep(5)

        # Stop IO handler threads and terminate the process then wait another 5 seconds for cleanup to happen
        self.stop_handlers = True
        self.process.terminate()
        time.sleep(5)

        # Check for any additional output from the stdout handler
        output = ""
        while True:
            data = _get_queue_output(self.stdout_queue)
            if data != "":
                output += data
            else:
                break
        for line in iter(output.splitlines()):
            self.logger.debug(line)

        # Check for any additional output from the stderr handler
        output = ""
        while True:
            data = _get_queue_output(self.stderr_queue)
            if data != "":
                output += data
            else:
                break
        for line in iter(output.splitlines()):
            self.logger.error(line)

        # Cleanup PTYs
        os.close(self.master_stdout)
        os.close(self.master_stderr)
        os.close(self.slave_stdout)
        os.close(self.slave_stderr)

        lib_logger.debug("Interactive shell command " + self.command + " terminated")

    # Run series of commands given as a list of a list of commands and wait_for strings. If no wait_for is needed then
    # only provide the command. Return if all the commands completed successfully or not.
    # Ex:
    # [
    #     ["ssh jsas@" + vnf_ip, r"jsas@.*:"],
    #     ["juniper123", r"jsas@.*\$"],
    #     ["sudo su", r".*jsas:"],
    #     ["juniper123", r"root@.*#"],
    #     ["usermod -p 'blah' jsas"]
    # ]
    def run_commands(self, commands_list):
        shell_status = True
        for command in commands_list:
            shell_status = self.run(command[0])
            if shell_status and len(command) == 2:
                shell_status = self.wait_for(command[1])

            # Break out of running commands if a command failed
            if not shell_status:
                break

        return shell_status

    # Run given command and return False if error occurs otherwise return True
    def run(self, command, sleep=0):
        # Check process to make sure it is still running and if not grab the stderr output
        if self.process.poll():
            self.logger.error("Interactive shell command " + self.command + " closed with return code: " +
                              self.process.returncode)
            data = _get_queue_output(self.stderr_queue)
            if data != "":
                self.logger.error("Interactive shell error messages:")
                for line in iter(data.splitlines()):
                    self.logger.error(line)
            return False

        # Write command to process and check to make sure a newline is in command otherwise add it
        if "\n" not in command:
            command += "\n"
        os.write(self.master_stdout, command.encode("utf-8"))
        if sleep:
            time.sleep(sleep)

        return True

    # Wait for specific regex expression in output before continuing return False if wait time expires otherwise return
    # True
    def wait_for(self, this, timeout=DEVICE_TIMEOUT):
        timeout = datetime.now() + timedelta(seconds=timeout)
        output = ""

        # Keep searching for output until timeout occurs
        while timeout > datetime.now():
            data = _get_queue_output(self.stdout_queue)
            if data != "":
                # Add to output line and check for match to regex given and if match then break and send output to
                # logger
                output += data
                lib_logger.debug("Checking for " + this + " in data: ")
                for line in iter(output.splitlines()):
                    lib_logger.debug(line)
                if re.search(r"{}\s?$".format(this), output):
                    break
            time.sleep(1)

        # Send output to logger
        for line in iter(output.splitlines()):
            self.logger.debug(line)

        # If wait time expired print error message and return False
        if timeout < datetime.now():
            self.logger.error("Wait time expired when waiting for " + this)
            return False

        return True


if __name__ == '__main__':
