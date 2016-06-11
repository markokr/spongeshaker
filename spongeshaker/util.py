"""Random helper code.
"""

from __future__ import division, absolute_import, print_function

import sys
from binascii import b2a_hex, a2b_hex

__all__ = []

# Convertsion to/from hex string
if sys.hexversion < 0x3000000:
    def tohex(bstr):
        return b2a_hex(bstr)
    def fromhex(strval):
        return a2b_hex(strval)
else:
    def tohex(bstr):
        if isinstance(bstr, str):
            bstr = bstr.encode('ascii')
        return b2a_hex(bstr).decode('ascii')
    def fromhex(strval):
        if isinstance(strval, str):
            strval = strval.encode('ascii')
        return a2b_hex(strval)


# Simple 10*1 padding for basic Keccak
PAD_KECCAK = fromhex('01')

