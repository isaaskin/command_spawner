"""
Command Spawner is a non-blocking command runner library for Python
"""
import os
import subprocess as sp
from shlex import split
from signal import SIGTERM
from sys import platform
from threading import Thread


class CommandSpawner:
    """
    Command Spawner class
    """
    def __init__(self,
                 command,
                 on_output_callback=None,
                 on_error_callback=None,
                 on_finished_callback=None,
                 on_exception_callback=None,
                 shell=False,
                 daemon=False):
        """
        Initialize the class with the command and the callback functions
        :param command: The command to be executed
        :param on_output_callback: The function to be called when new stdout
        data has been received
        :param on_error_callback: The function to be called when new stderr
        data has been received
        :param on_finished_callback: The function to be called when the
        command execution has finished
        :param on_exception_callback: The function to be called
        when exception has been thrown from the process module
        """
        # Assign command
        self.command = command

        # Assign callback functions
        self.callback_functions = {
            'output': on_output_callback,
            'error': on_error_callback,
            'finished': on_finished_callback,
            'exception': on_exception_callback
        }

        # Assign shell value
        self.shell = shell

        # Assign daemon value
        self.daemon = daemon

        # Declare null thread objects for output and error listening
        self.thread_listen_output = None
        self.thread_listen_error = None

        # Declare null process object
        self.process = None

    def handle_callbacks(self, callback_type, data):
        """
        The function to handle the callbacks
        """
        callback_function = self.callback_functions.get(callback_type)
        if callback_function:
            callback_function(data)
            return
        if callback_type == 'exception':
            raise data

    def listen_output(self):
        """
        The function which is used for listening the stdout stream
        :return:
        """
        while True:
            # Read output data from the stdout stream
            output = self.process.stdout.readline()
            # Check if process has finished by return code
            if output:
                self.handle_callbacks('output', output.decode('utf-8'))
            # If output is not null and empty then convey it
            # to the callback function
            if self.process.poll() is not None and output == b'':
                # If there is return code then convey it
                # to the callback function and break the loop
                self.handle_callbacks('finished', self.process.poll())
                break

    def listen_error(self):
        """
        The function which is used for listening the stderr stream
        :return:
        """
        while True:
            # Read error data from the stdout stream
            output = self.process.stderr.readline()
            # If output is not null and empty then convey it
            # to the callback function
            if output:
                self.handle_callbacks('error', output.decode('utf-8'))
            # Check if process has finished by return code
            if self.process.poll() is not None and output == b'':
                break

    def run(self):
        """
        The function to initialize the core objects
        :return:
        """
        # Creates a process with the given command
        if not self.shell:
            self.command = split(self.command)
        try:
            if platform == 'win32':
                self.process = sp.Popen(self.command,
                                        stdout=sp.PIPE,
                                        stderr=sp.PIPE,
                                        shell=self.shell)
            else:
                self.process = sp.Popen(self.command,
                                        stdout=sp.PIPE,
                                        stderr=sp.PIPE,
                                        shell=self.shell,
                                        preexec_fn=os.setsid)
        except Exception as exception:
            self.handle_callbacks('exception', exception)

        # Initialize the output listening thread and start it
        self.thread_listen_output = Thread(target=self.listen_output,
                                           daemon=self.daemon)
        self.thread_listen_output.start()

        # Initialize the error listening thread and start it
        self.thread_listen_error = Thread(target=self.listen_error,
                                          daemon=self.daemon)
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
            if platform == 'win32':
                sp.Popen(f"TASKKILL /F /PID {self.process.pid} /T >NUL",
                         shell=True)
            else:
                os.killpg(os.getpgid(self.process.pid), SIGTERM)
