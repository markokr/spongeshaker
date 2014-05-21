"""Random helper code.
"""

import sys
from binascii import b2a_hex, a2b_hex

__all__ = []

# Convertsion to/from hex string
if sys.hexversion < 0x3000000:
    def tohex(s):
        return b2a_hex(s)
    def fromhex(s):
        return a2b_hex(s)
else:
    def tohex(s):
        if isinstance(s, str):
            s = s.encode('ascii')
        return b2a_hex(s).decode('ascii')
    def fromhex(s):
        if isinstance(s, str):
            s = s.encode('ascii')
        return a2b_hex(s)


# Simple 10*1 padding for basic Keccak
PAD_KECCAK = fromhex('01')

