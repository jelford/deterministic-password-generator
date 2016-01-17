#! /usr/bin/env python3
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README')) as f:
    long_description = f.read()

setup(
    name='deterministic-password-generator',
    version='0.0.1',
    description='Generates passwords according to user-defined rules',
    long_description=long_description,
    url='https://github.com/jelford/deterministic-password-generator',
    author='James Elford',
    author_email='james.p.elford@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),
        install_requires=[
            'cryptography>=1.2.1',
        ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
        'mock',
    ],

        entry_points={
            'console_scripts': [
                'dpg = deterministicpasswordgenerator.__main__:main'
            ]
        }

)
