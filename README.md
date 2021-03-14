[![Python package](https://github.com/isaaskin/command_spawner/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/isaaskin/command_spawner/actions/workflows/python-package.yml)
 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# Command Spawner  
Command Spawner is a non-blocking command runner library for Python.  
  
Command Spawner runs commands at background and provides live output, error and finish data through the provided callback functions.

# Installing
Install and update using pip:
```bash
$ pip install command-spawner
```

# Example usage
```python
# Triggered when received new stdout
def on_output(data):
    print(f"Received data: {data}")


# Triggered when received new stderr
def on_error(data):
    print(f"Received error: {data}")


# Triggered when the command execution has finished
def on_finished(data):
    print(f"Finished with return code: {data}")


# Triggered when an exception has been thrown from the process module
def on_exception(exception):
    print(f"Received exception: {exception}")
    # or
    raise exception


command_spawner = CommandSpawner(command="ping google.com",
                                 on_output_callback=on_output,  # Suppress output when it is not provided
                                 on_error_callback=on_error,  # Suppress error when it is not provided
                                 on_finished_callback=on_finished,  # Suppress return code when it is not provided
                                 on_exception_callback=on_exception,  # Raise exception on runtime when it is not provided
                                 shell=False,  # If True, the command will be executed through the shell (not recommended)
                                 daemon=False  # If True, current runtime will not wait for commands to be executed 
                                 )

# The method to run the process
command_spawner.run()

# The method to kill the current process
command_spawner.kill()

# The method to wait for the process to be finished
command_spawner.wait()
```

Enjoy!