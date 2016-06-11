"""High-level APIs to Keccak1600 algorithm.
"""

from __future__ import division, absolute_import, print_function

from spongeshaker.util import tohex

__all__ = ['SpongeHash', 'SpongeHashInvalidState']

class SpongeHashInvalidState(Exception):
    """Extracting has started, cannot .update()/.digest()."""

class SpongeHash(object):
    """Generic :mod:`hashlib` compatible hash function API.
    """
    __slots__ = ('name', 'block_size', 'digest_size', '_padding', '_sponge', '_extracting')

    def __init__(self, capacity_bits, output_bits,
                 data=None, name = None,
                 sponge_class = None,
                 padding = None,
                 _sponge = None,
                 _extracting = False):
        """Initialize sponge instance with specified parameters.

        Parameters:
            capacity_bits
                number of bits for capacity.
            digest_bits
                number of bits for digest output.
            data
                initial data to hash.
            name
                User-visible name for hash+parameters.
            sponge_class
                Sponge implementation class that implements the
                :class:`spongeshaker.sponge.Sponge` interface.
            padding
                Start bytes for padding bytes to use, final bit
                is always added.
        """
        self._sponge = _sponge or sponge_class(capacity_bits)
        self._padding = padding
        self.name = name or _sponge.name
        self.block_size, rem1 = divmod(self._sponge.rate, 8)
        self.digest_size, rem2 = divmod(output_bits, 8)
        self._extracting = _extracting
        if rem1 or rem2:
            raise ValueError("capacity_bits and output_bits must be multiple of 8")
        if data is not None:
            self.update(data)

    def copy(self):
        """Create copy of current state.
        """
        s2 = self._sponge.copy()
        return SpongeHash(s2.capacity, self.digest_size * 8,
                None, self.name, None, self._padding,
                s2, self._extracting)

    def update(self, data):
        """Update state with data.

        Cannot be used after :meth:`extract` is called.
        """
        if self._extracting:
            raise SpongeHashInvalidState()
        self._sponge.absorb(data)

    def digest(self):
        """Return final hash digest.

        This follows the :mod:`hashlib` convention that
        state is not changed so :meth:`update` can be
        called again to add more data to state.
        """
        if self._extracting:
            raise SpongeHashInvalidState()
        tmp = self._sponge.copy()
        tmp.pad(self._padding)
        return tmp.squeeze(self.digest_size)

    def hexdigest(self):
        """Return :meth:`digest` value as hexadecimal string.
        """
        return tohex(self.digest())

    def extract(self, count):
        """Extract data from hash state.

        This function can be continued to be called
        to extract unlimited amount of bytes from state.

        It *does* change the state, so :meth:`update`, :meth:`digest`
        and :meth:`hexdigest` will throw error after :meth:`extract`
        has been called.
        """
        if not self._extracting:
            self._sponge.pad(self._padding)
            self._extracting = True
        return self._sponge.squeeze(count)

