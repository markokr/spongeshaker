"""Pseudo-random number generator API.
"""

from __future__ import division, absolute_import, print_function

from .keccak import KeccakSponge
from .util import PAD_KECCAK

__all__ = ['SpongePRNG', 'KeccakPRNG']

class SpongePRNG(object):
    """Sponge as PRNG.
    """
    __slots__ = ('_sponge', '_initialized', '_extracting', '_padding')

    def __init__(self, sponge, padding = PAD_KECCAK):
        """Initialize PRNG state with specified Keccak variant.
        """
        self._sponge = sponge
        self._initialized = 0
        self._extracting = 0
        self._padding = padding

    def add_entropy(self, data):
        """Import new random data into state.
        """
        if data:
            if self._extracting:
                self._sponge.rewind()
                self._extracting = 0
            self._sponge.absorb(data)
            self._initialized = 1

    def get_random_bytes(self, nbytes):
        """Return random bytes from state.
        """
        if not self._initialized:
            raise Exception("PRNG has no entropy.")
        if not self._extracting:
            # add_entropy was called, need to pad+permute
            self._sponge.pad(self._padding)
            self._extracting = 1
        return self._sponge.squeeze(nbytes)

class KeccakPRNG(SpongePRNG):
    """Keccak as PRNG.
    """
    def __init__(self, capacity = 512, padding = PAD_KECCAK):
        super(KeccakPRNG, self).__init__(KeccakSponge(capacity), padding)

