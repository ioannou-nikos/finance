from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import finance

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding','utf-8')
    sep = kwargs.get('sep','\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)
    
long_description = read('README.txt', 'CHANGES.txt')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
        
    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)
        
setup(
    name='finance',
    version=finance.__version__,
    url='http://github.com/ioannou-nikos/finance/',
    licence='Apache Software Licence',
    author='Nikos Ioannou',
    tests_require=['pytest'],
    install_requires=['libs','go','here'],
    cmdclass={'test':PyTest},
    author_email='ioannou.nikos@gmail.com',
    description='Desc goes here',
    long_description=long_description,
    packages=['finance'],
    include_package_data=True,
    platforms='any',
    test_suite='finance.test.test_finance',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: Alpha',
        'Natural Language :: Greek - English',
        'Environment :: Desktop',
        'Intended Audience :: All',
        'Licence :: OSI Approved :: Apache Software Licence',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    extras_require={
        'testing':['pytest'],
    }
)