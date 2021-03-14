from setuptools import setup, find_packages
import pathlib

VERSION = '1.1.3'
DESCRIPTION = 'Command Spawner'

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Setting up
setup(
    name="command_spawner",
    version=VERSION,
    author="Isa Askin",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/isaaskin/command_spawner",
    install_requires=[],  # add any additional packages that
    keywords=['python', 'command spawner', 'spawn', 'command', 'shell',
              'bash', 'command spawn'],
    lassifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
)
