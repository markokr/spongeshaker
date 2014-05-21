"""Pseudo-random number generator API.
"""

from .keccak import KeccakSponge
from .util import PAD_KECCAK

__all__ = ['KeccakPRNG']

class KeccakPRNG(object):
    """Keccak as PRNG.
    """
    __slots__ = ('_sponge', '_initialized', '_extracting')

    def __init__(self, capacity):
        """Initialize PRNG state with specified Keccak variant.
        """
        self._sponge = KeccakSponge(capacity)
        self._initialized = 0
        self._extracting = 0

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
            self._sponge.pad(PAD_KECCAK)
            self._extracting = 1
        return self._sponge.squeeze(nbytes)

