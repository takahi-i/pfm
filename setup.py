#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import pip
from setuptools import setup, find_packages
from pip.req import parse_requirements

with open('README.rst') as readme_file:
    readme = readme_file.read()

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
    long_description=readme + '\n\n' + history,
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
