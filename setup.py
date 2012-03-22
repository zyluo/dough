#import os
import sys
from setuptools import setup, find_packages


requirements = ['pyzmq']#, 'python-novaclient', 'python-keystoneclient']

if sys.version_info < (2, 6):
    requirements.append('simplejson')
if sys.version_info < (2, 7):
    requirements.append('argparse')

setup(
    name = "dough",
    version = "0.1",
    description = "OpenStack Billing System",
    long_description = "OpenStack Billing System",
    url = 'https://github.com/lzyeval/dough',
    license = 'Apache',
    author = 'Sina Corp.',
    author_email = 'lzyeval@gmail.com',
    packages = find_packages(exclude=['tests', 'tests.*']),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = requirements
)
"""
tests_require = ["nose", "mock", "mox"],
test_suite = "nose.collector",

entry_points = {
    'console_scripts': ['keystone = keystoneclient.shell:main']
}
"""
