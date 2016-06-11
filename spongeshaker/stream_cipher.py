"""Stream cipher with Keccak.

Stream cipher is basically PRNG, seeded with key,
that generarates bytes that are XORed with data.

That means each message/stream *must* have unique stream,
either by having unique key or IV.  Otherwise the data
can be trivially recovered.
"""

from __future__ import division, absolute_import, print_function

from .keccak import KeccakSponge
from .util import PAD_KECCAK

__all__ = ['SpongeStreamCipher']

class SpongeStreamCipher(object):
    """Keccak Stream Cipher.

    Example encryption::

        state = KeccakStream(576)
        state.add_initial_data(key)
        ciphertext = state.encrypt(cleartext)
        mac = state.final_digest(16)

    Example decryption::

        state = KeccakStream(576)
        state.add_initial_data(key)
        cleartext = state.decrypt(cleartext)
        mac = state.final_digest(16)

    """
    __slots__ = ('_sponge', '_state', '_initial_data_pad', '_data_pad')

    _NODATA = 0
    _INITIAL = 1
    _ENCRYPT = 2
    _DECRYPT = 3

    def __init__(self, sponge, initial_data_pad = PAD_KECCAK, data_pad = PAD_KECCAK):
        """Set up Keccak stream with given capacity (in bits) and padding.
        """
        self._sponge = sponge
        self._state = self._NODATA
        self._initial_data_pad = initial_data_pad
        self._data_pad = data_pad

    def add_initial_data(self, data):
        """Add initial data - key, iv, extra plaintext.
        """
        if self._state not in (self._NODATA, self._INITIAL):
            raise Exception("add_initial_data: wrong moment")
        self._state = self._INITIAL
        self._sponge.absorb(data)

    def encrypt(self, plaintext):
        """Encrypt data.

        Return plaintext XOR-ed with keystream.
        """
        if self._state not in (self._INITIAL, self._ENCRYPT):
            raise Exception("encrypt: wrong moment")
        if self._state == self._INITIAL:
            self._sponge.pad(self._initial_data_pad)
        self._state = self._ENCRYPT
        return self._sponge.squeeze_xor(plaintext)

    def decrypt(self, ciphertext):
        """Decrypt data.

        Return ciphertext XOR-ed with keystream.
        """
        if self._state not in (self._INITIAL, self._DECRYPT):
            raise Exception("decrypt: wrong moment")
        if self._state == self._INITIAL:
            self._sponge.pad(self._initial_data_pad)
        self._state = self._DECRYPT
        return self._sponge.squeeze_xor(ciphertext)

class KeccakStreamCipher(SpongeStreamCipher):
    def __init__(self, capacity = 512, initial_data_pad = PAD_KECCAK, data_pad = PAD_KECCAK):
        super(KeccakStreamCipher, self).__init__(KeccakSponge(capacity), initial_data_pad, data_pad)

