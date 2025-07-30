"""
Setup module for the signedGen package.

This module uses setuptools to package the signedGen project, specifying its
metadata, dependencies, and entry points.
"""

from setuptools import setup, find_packages

setup(
    name='signed-gen',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
        ],
    },
    author='EveryCRED',
    author_email='admin@everycred.com',
    description='A package for blockchain signed transactions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
