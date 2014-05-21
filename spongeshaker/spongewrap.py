"""SpongeWrap - AEAD encryption with sponge.

http://sponge.noekeon.org/SpongeDuplex.pdf
"""

from .keccak import KeccakSponge
from .util import fromhex

__all__ = ['SpongeWrap']

# empty byte-string
_EMPTY = fromhex("")

# next block will be key stream
_PAD_KEYSTREAM = fromhex("03")

# next block will not be key stream
_PAD_PLAINSTREAM = fromhex("02")

class SpongeWrap(object):
    """Authenticated encryption with sponge.

    Each block is padded, padding includes "frame bit"
    before the standard 10*1 padding.

    Frame bit = 0: next block will not be keystream.
    Frame bit = 1: next block will be keystream.
    """
    __slots__ = ('_sponge', '_cur_pad')

    def __init__(self, capacity = 512, sponge_class = KeccakSponge):
        self._sponge = sponge_class(capacity)
        self._cur_pad = _PAD_PLAINSTREAM

    def _add(self, data, this_pad, sfunc):
        if not self._cur_pad:
            raise Exception("SpongeWrap: cannot add data after digest is called")
        if this_pad != self._cur_pad:
            # pad immediately if data type changed
            self._sponge.pad(this_pad)
            self._cur_pad = this_pad

        # add data block-by-block
        dpos = 0
        maxbytes = self._sponge.rbytes - 1
        res = []
        while dpos < len(data):
            bpos = self._sponge.pos
            avail = maxbytes - bpos
            if avail == 0:
                self._sponge.pad(this_pad)
                continue
            dlen = len(data) - dpos
            if dlen > avail:
                dlen = avail
            r = sfunc(data[dpos : dpos + dlen])
            res.append(r)
            dpos += dlen
        return res

    def add_header(self, data):
        self._add(data, _PAD_PLAINSTREAM, self._sponge.absorb)

    def encrypt_body(self, data):
        res = self._add(data, _PAD_KEYSTREAM, self._sponge.encrypt)
        return _EMPTY.join(res)

    def decrypt_body(self, data):
        res = self._add(data, _PAD_KEYSTREAM, self._sponge.decrypt)
        return _EMPTY.join(res)

    def digest(self, n):
        if self._cur_pad:
            self._sponge.pad(_PAD_PLAINSTREAM)
            self._cur_pad = None
        return self._sponge.squeeze(n)

