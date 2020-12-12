"""
Spawner is a non-blocking command runner library
"""
import subprocess as sp
import threading
from select import select
from shlex import split
import time


class Spawner:
    """
    Spawner class
    """
    def __init__(self,
                 command,
                 on_data_callback=None,
                 on_error_callback=None,
                 on_finished_callback=None,
                 shell=False,
                 daemon=False):
        """
        Initialize the class with the command and the callback functions
        :param command:
        :param on_data_callback:
        :param on_error_callback:
        :param on_finished_callback:
        """
        # Assign command
        self.command = command

        # Assign callback functions
        self.on_data_callback = on_data_callback
        self.on_error_callback = on_error_callback
        self.on_finished_callback = on_finished_callback

        # Assign shell value
        self.shell = shell

        # Assign daemon value
        self.daemon = shell

        # Declare null thread objects for output and error listening
        self.thread_listen_output = None
        self.thread_listen_error = None

        # Declare null process object
        self.process = None

    def listen_output(self):
        """
        The function which is used for listening the stdout stream
        :return:
        """
        while True:
            # Read output data from the stdout stream
            output = self.process.stdout.readline()
            # If output is not null or empty then convey it to the callback function
            if output:
                self.on_data_callback(output.decode('utf-8'))
            # Check if process has finished by return code
            if self.process.poll() is not None:
                # If there is return code then convey it to the callback function and break the loop
                self.on_finished_callback(self.process.poll())
                break

    def listen_error(self):
        """
        The function which is used for listening the stderr stream
        :return:
        """
        while True:
            # Check if stderr stream is available, or break the loop
            if self.process.stderr:
                # Read the buffer whether there is data in inside
                buffer, _, _ = select([self.process.stderr], [], [], 0)
                # If buffer is not null then it means there is data to read
                if buffer:
                    # Convey the error data to the callback function
                    self.on_error_callback(self.process.stderr.readline())
                # If there is return code then break the loop
                if self.process.poll():
                    break
            else:
                break
            # Avoid excessive CPU load
            time.sleep(0.05)

    def run(self):
        """
        The function to initialize the core objects
        :return:
        """
        # Creates a process with the given command
        if self.shell:
            self.command = split(self.command)
        self.process = sp.Popen(self.command, stdout=sp.PIPE, stderr=sp.PIPE, shell=self.shell)

        # Initialize the output listening thread and start it
        self.thread_listen_output = threading.Thread(target=self.listen_output)
        self.thread_listen_output.start()

        # Initialize the error listening thread and start it
        self.thread_listen_error = threading.Thread(target=self.listen_error)
        self.thread_listen_error.start()

    def wait(self):
        """
        The function to be used for waiting the command run to be finished
        :return:
        """
        # Joins the output and error listening threads
        self.thread_listen_output.join()
        self.thread_listen_error.join()

    def kill(self):
        """
        The function to kill the process
        :return:
        """
        if not self.process.poll():
            self.process.kill()
