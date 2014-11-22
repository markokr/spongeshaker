r"""Tests module.

#
# Values from KeccakCodePackage/TestVectors
#

>>> EMPTY = fromhex("") # 0 bits
>>> SHORT = fromhex("52A608AB21CCDD8A4457A57EDE782176") # 128 bits
>>> LONG = fromhex("3A3A819C48EFDE2AD914FBF00E18AB6BC4F14513AB27D0C178A188B61431E7F5623CB66B23346775D386B50E982C493ADBBFC54B9A3CD383382336A1A0B2150A15358F336D03AE18F666C7573D55C4FD181C29E6CCFDE63EA35F0ADF5885CFC0A3D84A2B2E4DD24496DB789E663170CEF74798AA1BBCD4574EA0BBA40489D764B2F83AADC66B148B4A0CD95246C127D5871C4F11418690A5DDF01246A0C80A43C70088B6183639DCFDA4125BD113A8F49EE23ED306FAAC576C3FB0C1E256671D817FC2534A52F5B439F72E424DE376F4C565CCA82307DD9EF76DA5B7C4EB7E085172E328807C02D011FFBF33785378D79DC266F6A5BE6BB0E4A92ECEEBAEB1") # 2040 bits

>>> sha3_224(EMPTY).hexdigest()
'6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7'
>>> sha3_224(SHORT).hexdigest()
'b1571bed52e54eef377d99df7be4bc6682c43387f2bf9acc92df608f'
>>> sha3_224(LONG).hexdigest()
'94689ea9f347dda8dd798a858605868743c6bd03a6a65c6085d52bed'

>>> sha3_256(EMPTY).hexdigest()
'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a'
>>> sha3_256(SHORT).hexdigest()
'2c7e7cb356fdc68ec8927e499d2a6bae2b781817919c829ebbe8225baed46967'
>>> sha3_256(LONG).hexdigest()
'c11f3522a8fb7b3532d80b6d40023a92b489addad93bf5d64b23f35e9663521c'

>>> sha3_384(EMPTY).hexdigest()
'0c63a75b845e4f7d01107d852e4c2485c51a50aaaa94fc61995e71bbee983a2ac3713831264adb47fb6bd1e058d5f004'
>>> sha3_384(SHORT).hexdigest()
'feee2ef332515284e0ba247c62f264199044d03877c58e54b51a62e39e91c27aaae384837eb9d479b4c0308cfc6b779b'
>>> sha3_384(LONG).hexdigest()
'128dc611762be9b135b3739484cfaadca7481d68514f3dfd6f5d78bb1863ae68130835cdc7061a7ed964b32f1db75ee1'

>>> sha3_512(EMPTY).hexdigest()
'a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a615b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26'
>>> sha3_512(SHORT).hexdigest()
'001618372e75147af90c0cf16c3bbdaa069ddbc62483b392d028ded49f75084a5dfcc53aecd9f57ddbb73daa041fd71089d8fb5edf6cfaf6f1e4e25ad3de266c'
>>> sha3_512(LONG).hexdigest()
'6e8b8bd195bdd560689af2348bdc74ab7cd05ed8b9a57711e9be71e9726fda4591fee12205edacaf82ffbbaf16dff9e702a708862080166c2ff6ba379bc7ffc2'

>>> shake128(EMPTY).hexdigest()
'7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef26'
>>> shake128(SHORT).hexdigest()
'3a0faca70c9d2b81d1064d429ea3b05ad27366f64985379ddd75bc73d6a83810'
>>> shake128(LONG).hexdigest()
'14236e75b9784df4f57935f945356cbe383fe513ed30286f91060759bcb0ef4b'

>>> shake256(EMPTY).hexdigest()
'46b9dd2b0ba88d13233b3feb743eeb243fcd52ea62b81b82b50c27646ed5762fd75dc4ddd8c0f200cb05019d67b592f6fc821c49479ab48640292eacb3b7c4be'
>>> shake256(SHORT).hexdigest()
'57119c4507f975ad0e9ea4f1166e5f9b590bf2671aaeb41d130d2c570bafc579b0b9ec485cc736a0a848bbc886cbaa79ffcd067ce64b3b410741ab011c544225'
>>> shake256(LONG).hexdigest()
'8a5199b4a7e133e264a86202720655894d48cff344a928cf8347f48379cef347dfc5bcffab99b27b1f89aa2735e23d30088ffa03b9edb02b9635470ab9f10389'

State copy.

>>> x = sha3_256(bs("The quick brown fox jumps over the lazy dog"))
>>> y = x.copy()
>>> z = x.copy()
>>> x.hexdigest() == y.hexdigest()
True
>>> x.update(bs("."))
>>> z.update(bs("."))
>>> x.hexdigest() == z.hexdigest()
True
>>> x.hexdigest()
'a80f839cd4f83f6c3dafc87feae470045e4eb0d366397d5c6ce34ba1739f734d'

KeccakPRNG

>>> x = KeccakPRNG(1024)
>>> x.add_entropy(bs("The quick brown fox jumps over the lazy dog."))
>>> tohex(x.get_random_bytes(32))
'ab7192d2b11f51c7dd744e7b3441febf397ca07bf812cceae122ca4ded638788'
>>> tohex(x.get_random_bytes(32))
'9064f8db9230f173f6d1ab6e24b6e50f065b039f799f5592360a6558eb52d760'
>>> tohex(x.get_random_bytes(32))
'7ca34f68abb61bbd1821c0a499599426031a56c495b3cf91b84cacafb9be816b'
>>> tohex(x.get_random_bytes(32))
'e7afb50b3a1c80f654ba212be0ad8a4be8f6a476bfcc66b9401fe65924bd547d'
>>> x.add_entropy(bs("More entropy."))
>>> tohex(x.get_random_bytes(32))
'ec9f73358469f4b7fea10dfb7dfaa768f573089b8e00507ec3a1fdfb2e60b35d'

#
# Test values from original Keccak submission - c=576 is the proposed stream mode.
#

>>> padtest(576, "CC", '''56b97029b479ff5dd15f17d12983e3b835bb0531d9b8d49b103b025ca53f991741298e961d1fad00fc365c7761b
... fb278ae473980d612c1629e075a3fdbae7f82b0f0af54df187f358852e19ea4347cf5ceea676a1dce3a47447e237fd74204f9a4b7f7c9cc7c
... c8b865b1d554e2f5f4a8ee17dbdde7267894558a20972c9eb6cf5f62ce9151437718ed4aff08fa76d803806e6ce47d229aae839369e31888b
... 26429e27bc3756021cb51498bcf2527d4bb04838bc1ceed9985a2a66ff8cb8c2d58b7099304e7f9622c583b093024a5fcde2be781474c159d
... f24d77d328c298f5766a8a0dbf7ae790a509ccf59e0cacd0abf21492e0095a87ecdb55990093917aaa96d7f68b7b859b8094aec0ddb6fb352
... a6cc1f007fa988ed764f5d6f21f9d8ade9ce7aca4de6570da39d9acceb46d2582fa4c4231de0b736fb341041d24cfae6c0761f43a2cf7383f
... 38742579218afcab53d2e6816640de05644d877558e965b1a28406999f31ccc43ac0b02bc5448b66ad3b6f8de04c0e25845c8671b6f059490
... 9a057f17fd06031707c8b4599889c994a35c193dbf84a7a0919cd054f67ceb7965f420d02da3477efc8b55413c241adcf71cb10fe7e3e720b
... 8c1736837b06e4b27461b71c6cac892437530bbfe05cf426272f80f11709b9db964f5dedab9e757c2f7a972b6a4c2443b03ad787ab1e24366
... 0bced739157a434800696841acea4''')
True
>>> padtest(576, '''3A3A819C48EFDE2AD914FBF00E18AB6BC4F14513AB27D0C178A188B61431E7F5623CB66B23346775D386B50E982C493ADBBFC5
... 4B9A3CD383382336A1A0B2150A15358F336D03AE18F666C7573D55C4FD181C29E6CCFDE63EA35F0ADF5885CFC0A3D84A2B2E4DD24496DB789E6631
... 70CEF74798AA1BBCD4574EA0BBA40489D764B2F83AADC66B148B4A0CD95246C127D5871C4F11418690A5DDF01246A0C80A43C70088B6183639DCFD
... A4125BD113A8F49EE23ED306FAAC576C3FB0C1E256671D817FC2534A52F5B439F72E424DE376F4C565CCA82307DD9EF76DA5B7C4EB7E085172E328
... 807C02D011FFBF33785378D79DC266F6A5BE6BB0E4A92ECEEBAEB1''',
... '''9435fc671dfcfcdac149277e2caaa80ed3d4a2359300db892b8093dffa9442bb5c08f242f2fc2cb5f8388032299f1df47a57489a4fc0d66d88e
... 483092320a471897fb6ade67897e5138c45f19174a4b1ae0e510fa390825d17568989c3659fc57b9345d7d93ee588cb2629c5770808195257bbf42
... b069576d94011989dc6ebc43cfc7cd27b6f9853904f3eb3842bbb37d2bd807f05468f5057f78373b6f34462095a1205c1fca0d15fbcf890ee78ab6
... f94cb778b5d6f3620e6e6d6ee688eecc619e22e25e0bb5e143a53472e4f1d1f91a8e625087b0f608770c4b9909749ab50ddcdac59bb3c975aba4dc
... eb2b3a2c436ed103ed6d9c62cd63a69a0bdd2baabfbfd63eef34507637f5e8a16a4fcb33d66141781e10bc6262833ec6e2953cedd5f652b76fa042
... ec0d34ba20f5657e28c08b6b61dfa8da78cf997127e17a35d75ab35542fe6bb9ce5bd06119da6b497ac1ae12947b0c214de28ed5dda7815fb6d5de
... f81025934c877cb91e923191581b508bbabdfe4bb2dd5af6af414bfa28830e4380355bdf2483cabd01b046956b85d5a34f46849ba1cc869f5babd1
... b41ec775fcb4b5fbad79661daf47dbe7bc6380bc5034bfe626526f3305abe270bbbf29280e58b71db269cf7962d9dc1731bd10d5633b1b10e76791
... c0fcfddf1c8263f17f8b68b1a0589fe5c9403d272fa133442980588bc1f385c3af240d8f195ab1a3400''')
True

Keccak Encryption

>>> ctx = SpongeWrap(1536)
>>> ctx.add_header(bs("password"))
>>> tohex(ctx.encrypt_body(bs("Secret message")))
'9c48ef7549911055381d6980f33d'
>>> tohex(ctx.digest(16))
'84bb60d0463b86769b5a0a3bd474b125'

>>> ctx = SpongeWrap(1536)
>>> ctx.add_header(bs("password"))
>>> stdstr(ctx.decrypt_body(fromhex('9c48ef7549911055381d6980f33d')))
'Secret message'
>>> tohex(ctx.digest(16))
'84bb60d0463b86769b5a0a3bd474b125'

Validate Encryption

>>> s = KeccakSponge(1536)
>>> s.absorb(b"passwor\x82d")
>>> s.pad(b"\x03")
>>> s.absorb(b"Secret \x83")
>>> s.absorb(b"message\x82")
>>> tohex(s.squeeze(16))
'84bb60d0463b86769b5a0a3bd474b125'


"""

import sys
import re

from binascii import b2a_hex, a2b_hex

from spongeshaker.prng import *
from spongeshaker.hashing import *
from spongeshaker.spongewrap import *
from spongeshaker.stream_cipher import *
from spongeshaker.sha3 import *
from spongeshaker.keccak import KeccakSponge
from spongeshaker.util import PAD_KECCAK, fromhex, tohex

if sys.hexversion < 0x3000000:
    def bytes(s, enc):
        return str(s)
    def stdstr(s):
        return s
else:
    def stdstr(s):
        return s.decode('ascii')

def bs(s):
    return bytes(s, 'utf8')


def padtest(capacity, data, exp):
    data = fromhex(re.sub(r'\s+', '', data))
    exp = fromhex(re.sub(r'\s+', '', exp))

    # partial adds
    for s in (1, 3, 5, 7, 11, 17):
        xmd = KeccakPRNG(capacity)
        got = 0
        while got < len(data):
            if got + s > len(data):
                part = data[got : ]
            else:
                part = data[got : got + s]
            xmd.add_entropy(part)
            got += len(part)
        res = xmd.get_random_bytes(len(exp))
        if res != exp:
            raise ValueError("partial add failure")

    # partial extract
    for s in (1, 3, 7, 11, 17, 256, 512):
        res = []
        got = 0
        xmd = KeccakPRNG(capacity)
        xmd.add_entropy(data)
        while got < len(exp):
            if got + s > len(exp):
                part = xmd.get_random_bytes(len(exp) - got)
            else:
                part = xmd.get_random_bytes(s)
            res.append(part)
            got += len(part)
        xres = bytes("", 'ascii').join(res)
        if xres != exp:
            raise ValueError("Data does not match: s=%d\nexp=%s\ngot=%s\n" % (
                s, exp.encode('hex'), xres.encode('hex')))
    return True

if __name__ == '__main__':
    import doctest
    doctest.testmod()

