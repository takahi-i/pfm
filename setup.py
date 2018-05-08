#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import pip
from setuptools import setup, find_packages
from pip.req import parse_requirements

LONG_DESCRIPTION = """
Data scientists launch a Jupyter Notebook servers to tackle each machine learning task. Usually local computers are not
enough to handle multiple machine learning tasks. And therefore data scientists do their experiments in servers launched
in remote hosts such as EC2 instances.

To connect Jupyter Notebook servers in remote hosts, we use ssh port forwarding. Port forwarding is useful since we do
not consume resources in local PC.

Unfortunately, when connecting servers in multiple remote hosts and ports numbers, we easily forget the port number or
assign the local port number which is used in another task. Especially when there are multiple remote hosts and ssh
servers as the following image, understanding the combinations of remote hosts and local ports are difficult.

pfm manages the remote hosts and port numbers used in port forwarding. Users understand which local ports are used and
which ports are not. Once users register the port forwarding information, pfm generates ssh parameters any time
specifying the task name.
"""

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ str(requirement.req) for requirement in parse_requirements('requirements.txt', session = pip.download.PipSession()) ]

setup_requirements = [
    # TODO(takahi-i): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pfm',
    version='0.5.0',
    description="Tiny port forward manager",
    long_description=LONG_DESCRIPTION,
    author="Takahiko Ito",
    author_email='takahiko03@gmail.com',
    url='https://github.com/takahi-i/pfm',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pfm=pf_manager.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pfm',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
