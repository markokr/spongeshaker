
spongeshaker - High-level API to SHA-3 and other sponge modes with Keccak
=========================================================================

This module implements Keccak-f1600 sponge permutation and high-level
APIs for various modes of it, including SHA-3 hashes.

This implementation is up-to-date with final version of `FIPS-202`_ (5-Aug-2015).

Features:

- Hashing (SHA3), PRNG, Stream cipher, AEAD cipher (`SpongeWrap`_).
- Optimized-C implementation from Keccak reference code,
  with separate paths for 64- and 32-bit CPUs.
- Works with both Python 2.x and 3.x.

Todo:

- Optimized ASM implementations.
- Other Keccak permutation sizes.
- Other sponge algorithms.
- Other sponge modes.

Example::

  from spongheshaker.sha3 import sha3_256, shake128

  # fixed-length output
  md = sha3_256('Hello ')
  md.update('world!')
  hash = md.digest()

  # variable-length output
  md = shake128('Hello ')
  md.update('world!')
  res1 = md.extract(64)
  res2 = md.extract(64)

Links:

- `Documentation`_
- `Downloads`_
- `Git`_ repo

.. _Keccak:     https://en.wikipedia.org/wiki/Keccak
.. _Sponge:     https://en.wikipedia.org/wiki/Sponge_function
.. _ISC:        https://en.wikipedia.org/wiki/ISC_license
.. _FIPS-202:   http://dx.doi.org/10.6028/NIST.FIPS.202
.. _Git: https://github.com/markokr/spongeshaker
.. _Downloads: https://pypi.python.org/pypi/spongeshaker
.. _Documentation: https://spongeshaker.readthedocs.org/
.. _SpongeWrap: http://sponge.noekeon.org/SpongeDuplex.pdf

