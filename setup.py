#!/usr/bin/env python
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('hog/__init__.py') as f:
    data = re.search(r'\(\s*(\d*).\s*(\d*).\s*(\d)*\)', f.read())
    version = ".".join([data.group(1), data.group(2), data.group(3)])
assert version

packages = [
    'hog',
]

requirements = [
    'eventlet',
    'requests',
]

classifiers = [
    'Topic :: Terminals',
    'Topic :: Utilities',
    'Environment :: Console',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'License :: OSI Approved :: MIT License',
]

setup(
    name='hog',
    version=version,
    packages=packages,
    zip_safe=False,

    author='Park Hyunwoo',
    author_email='ez.amiryo' '@' 'gmail.com',
    maintainer='Park Hyunwoo',
    maintainer_email='ez.amiryo' '@' 'gmail.com',
    url='http://github.com/lqez/hog',

    description='Sending multiple `HTTP` requests `ON` `GREEN` thread',
    classifiers=classifiers,

    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'hog = hog.hog:main',
        ],
    },
)
