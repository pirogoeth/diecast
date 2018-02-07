# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import os
import sys

sys.path.insert(0, os.path.abspath('src'))

setup(
    name='diecast',
    version='0.1.0',
    description='Dependency Injector framework for Python 3',

    url='https://glow.dev.maio.me/sjohnson/diecast',
    author='Sean Johnson',
    author_email='sean.johnson@maio.me',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: MIT',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages('src'),
    package_dir={
        '': 'src'
    },
    install_requires=[
    ],
    include_package_data=True,
    exclude_package_data={
        '': ['README.md'],
    },
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'coverage',
    ],
    zip_safe=True,
)
