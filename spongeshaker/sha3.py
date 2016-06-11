"""Final SHA3 algorithm selection.

Current values correspond to final FIPS 202 (Aug 2015).

All hash objects follow common `hashlib`_ interface for
hash functions.  shake128 and shake256 will returns
256- and 512- bit result from .digest() by default.
It can be changed by giving alternative bit-length
to init function.

Alternatively, .extract() function can be called
repeatedly to get unlimited stream of result bytes.
"""

from __future__ import division, absolute_import, print_function

from spongeshaker.hashing import SpongeHash
from spongeshaker.keccak import KeccakSponge
from spongeshaker.util import fromhex

__all__ = [
    'sha3_224',
    'sha3_256',
    'sha3_384',
    'sha3_512',
    'shake128',
    'shake256',
]

# Add Sakura padding to basic Keccak padding
# Keccak:   1 0*
# SHA3:     0 1 1 0*
# RAWSHAKE: 1 1 1 0*
# SHAKE:    1 1 1 1 1 0*

PAD_SHA3 = fromhex('06')
PAD_RAWSHAKE = fromhex('07')
PAD_SHAKE = fromhex('1f')

#
# Proposed SHA3 values by NIST - Draft FIPS 202 (Apr 2014)
#

def sha3_224(data = None):
    """Proposed SHA3-224 by NIST (c=448).

    Security level: 112/224 bits.

    Returns :class:`spongeshaker.hashing.SpongeHash` for SHA3-224.
    """
    return SpongeHash(448, 224, data, "SHA3-224", KeccakSponge, PAD_SHA3)

def sha3_256(data = None):
    """Proposed SHA3-256 by NIST (c=512).

    Security level: 128/256 bits.

    Returns :class:`spongeshaker.hashing.SpongeHash` for SHA3-256.
    """
    return SpongeHash(512, 256, data, "SHA3-256", KeccakSponge, PAD_SHA3)

def sha3_384(data = None):
    """Proposed SHA3-384 by NIST (c=768).

    Security level: 192/384 bits.

    Returns :class:`spongeshaker.hashing.SpongeHash` for SHA3-384.
    """
    return SpongeHash(768, 384, data, "SHA3-384", KeccakSponge, PAD_SHA3)

def sha3_512(data = None):
    """Proposed SHA3-512 by NIST (c=1024).

    Security level: 256/512 bits.

    Returns :class:`spongeshaker.hashing.SpongeHash` for SHA3-512.
    """
    return SpongeHash(1024, 512, data, "SHA3-512", KeccakSponge, PAD_SHA3)

#
# Variable-length SHAKE functions.
#

def shake128(data = None, digest_size = 256):
    """Proposed SHAKE128 hash by NIST (c=256).

    Security level: 128 bits.

    Parameters:
        data
            initial data to hash.
        digest_size
            Output size for .digest()/.hexdigest() when used as normal hash.
            Default: 256 bits.

    Returns :class:`spongeshaker.hashing.SpongeHash` for SHAKE128.
    """
    return SpongeHash(256, digest_size, data, "SHAKE128", KeccakSponge, PAD_SHAKE)

def shake256(data = None, digest_size = 512):
    """Proposed SHAKE256 hash by NIST (c=512).

    Security level: 256 bits.

    Parameters:
        data
            initial data to hash.
        digest_size
            Output size for .digest()/.hexdigest() when used as normal hash.
            Default: 512 bits.

    Returns :class:`spongeshaker.hashing.SpongeHash` for SHAKE256.
    """
    return SpongeHash(512, digest_size, data, "SHAKE256", KeccakSponge, PAD_SHAKE)

