#! /usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
import spongeshaker

vers = spongeshaker.__version__
ldesc = open("README.rst").read().strip()
sdesc = ldesc.split('\n')[0].split(' - ')[1].strip()

setup(
    name = "spongeshaker",
    version = vers,
    description = sdesc,
    long_description = ldesc,
    packages = ['spongeshaker'],
    ext_modules = [Extension("spongeshaker.keccak",
                             ["src/keccak.c", "src/pycore.c"])],
    license = "ISC",
    url = "https://github.com/markokr/spongeshaker",
    maintainer = "Marko Kreen",
    maintainer_email = "markokr@gmail.com",
    keywords = ['keccak', 'sponge', 'sha3', 'crypto',
                'hash', 'encryption', 'prng', 'random'],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])

