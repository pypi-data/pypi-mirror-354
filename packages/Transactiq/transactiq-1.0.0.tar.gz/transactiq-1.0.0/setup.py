"""
Setup module for the Transactify package.

This module uses setuptools to package the Transactify project, specifying its
metadata, dependencies, and entry points.
"""

from setuptools import setup, find_packages

setup(
    name='Transactiq',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'web3==5.25.0',
        'cryptography==3.4.7',
        'smart_open==5.1.0',
        'everycred==1.0.0',
    ],
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
        ],
    },
    author='Manil Jayswal',
    author_email='manil.jayswal@viitor.cloud',
    description='A package for blockchain transactions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/Transactify',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
