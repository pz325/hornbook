#!/usr/bin/env python

from setuptools import setup

setup(
    # GETTING-STARTED: set your app name:
    name='hornbook',
    # GETTING-STARTED: set your app version:
    version='1.0',
    # GETTING-STARTED: set your app description:
    description='Chinese flash card application',
    # GETTING-STARTED: set author name (your name):
    author='Ping.ZOU',
    # GETTING-STARTED: set author email (your email):
    author_email='sg71.cherub@gmail.com',
    # GETTING-STARTED: set author url (your url):
    url='http://menrfa.wordpress.com',
    # GETTING-STARTED: define required django version:
    install_requires=[
        'Django==1.8.4'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
