"""Low-level API for sponge implementations.
"""

from __future__ import division, absolute_import, print_function

__all__ = ['Sponge']

class Sponge(object):
    """Generic sponge API.
    """
    def __init__(self, capacity):
        """Initialze sponge with given capacity (in bits).
        """

    def absorb(self, data):
        """Add data to sponge by XOR-ing it into state.
        """

    def squeeze(self, nbytes):
        """Extract given number of bytes from state.
        """

    def squeeze_xor(self, data):
        """Return data XOR-ed with state.
        """

    def encrypt(self, data):
        """Return data XOR-ed into state.

        The state should already absorbed and permuted before
        encrypting starts.  This means .absorb(key) + .pad()
        should be called.
        """

    def decrypt(self, enc_data):
        """Return enc_data XOR-ed with state.

        This is reverse of .encrypt() - it assumes enc_data
        was created by XOR-ing current state with cleartext.
        This function reverses it.
        """

    def pad(self, suffix):
        """pad(suffix) - Add padding and permute state.

        The suffix is added into state, then also final bit is flipped.
        So to get original simple 10*1 padding given in the Keccak SHA3 proposal,
        the suffix needs to be '01'.

        If padding is suffix is empty, then final bit is not flipped, to support
        case when initial data for encryption is added without padding - which
        is bad style.
        """

    def rewind(self):
        """Move internal position to start of state.

        Useful for PRNG/duplex modes.  In fact, it should not
        be touched at all in other modes.
        """

    def forget(self):
        """Clear internal state, except capacity.
        """

    def copy(self):
        """Return new instance with same state.
        """


