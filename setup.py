#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # NOQA

requirements = [
    'eventlet',
    'requests',
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
    description='Testing multiple HTTP request on green thread',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'hog = hog:main',
        ],
    },
)
