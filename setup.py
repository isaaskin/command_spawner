from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'Command Spawner'
LONG_DESCRIPTION = 'Command Spawner is a non-blocking command runner library ' \
                   'for Python'

# Setting up
setup(
    name="command_spawner",
    version=VERSION,
    author="Isa Askin",
    author_email="isa33649@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    keywords=['python', 'command spawner', 'spawn', 'command', 'shell',
              'bash'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)