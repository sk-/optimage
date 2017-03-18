#!/usr/bin/env python
# Copyright 2015 Sebastian Kreft
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages


setup(
    name='optimage',
    version='0.3.0',
    description='Optimage: Lossless Compressor for PNG and JPEG',
    long_description=open('README.rst').read(),
    author='Sebastian Kreft',
    url='http://github.com/sk-/optimage',
    py_modules = ['optimage', 'test_optimage', 'test_optimage_e2e'],
    package_data={'': ['README.rst', 'LICENSE']},
    zip_safe=True,
    scripts=['scripts/optimage'],
    setup_requires=['pytest-runner'],
    install_requires=['Pillow'],
    tests_require=['pytest', 'pytest-cov', 'pytest-catchlog'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Archiving :: Compression',
    ],
)
