#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
	long_description = f.read()

setup(
	name='pygrapho',
	version='1.0.0',
	description='Visualize Extremely Large Graphs in Python and ElGrapho',
	long_description_content_type='text/markdown',
	long_description=long_description,
	author='David Pinney',
	author_email='david@pinney.org',
	url='https://github.com/dpinney/pygrapho/',
	packages = ['pygrapho'],
	include_package_data=True,
)