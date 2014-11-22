
spongeshaker - High-level API to SHA-3 and other sponge modes with Keccak
=========================================================================

This module implements Keccak-f1600 sponge permutation and high-level
APIs for various modes of it, including SHA-3 hashes.

SHA-3 standard is not finalized, so actual output values are not stable yet.
This implementation is up-to-date with 28-May-2014 draft of `FIPS-202`_.
(Although it's unlikely that final SHA-3 changes hash parameters or
padding again, instead they might add more modes.)

Features:

- Hashing (SHA3), PRNG, Stream cipher, AEAD cipher (`SpongeWrap`_).
- Optimized-C implementation from Keccak reference code,
  with separate paths for 64- and 32-bit CPUs.
- Works with both Python 2.x and 3.x.

Todo:

- Sync with final SHA-3.
- Optimized ASM implementations.
- Other Keccak permutation sizes.
- Other sponge algorithms.
- Other sponge modes.

Links:

- `Documentation`_
- `Downloads`_
- `Git`_ repo

.. _Keccak:     https://en.wikipedia.org/wiki/Keccak
.. _Sponge:     https://en.wikipedia.org/wiki/Sponge_function
.. _ISC:        https://en.wikipedia.org/wiki/ISC_license
.. _FIPS-202:   http://csrc.nist.gov/groups/ST/hash/sha-3/sha-3_standard_fips202.html
.. _Git: https://github.com/markokr/spongeshaker
.. _Downloads: https://pypi.python.org/pypi/spongeshaker
.. _Documentation: https://spongeshaker.readthedocs.org/
.. _SpongeWrap: http://sponge.noekeon.org/SpongeDuplex.pdf

