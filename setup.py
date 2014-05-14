#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # NOQA

requirements = [
    'eventlet',
    'requests',
]

classifiers = [
    'Topic :: Terminals',
    'Topic :: Utilities',
    'Environment :: Console',
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'License :: OSI Approved :: MIT License',
]

setup(
    name='hog',
    version='0.0.1',
    py_modules=['hog'],
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
            'hog = hog:main',
        ],
    },
)
