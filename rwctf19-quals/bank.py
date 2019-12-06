from schnorr import *
from pwn import *
import hashlib

# rwctf{P1Ain_SChNorr_n33Ds_m0re_5ecur1ty!}

def prove(prefix):
    for i in xrange(0x10000):
        proof = prefix + '%05x' % i
        test = hashlib.sha1(proof).digest()
        if test[-1] == '\0' and test[-2] == '\0':
            return proof

r = remote('tcp.realworldctf.com', 20014)

prefix = r.recvline().strip().split()[-1]
print prefix
proof = prove(prefix)
print proof
r.send(proof)

r.recvuntil('Please tell us your public key:')
r.sendline(('%d, %d' % G).encode('base64').replace('\n', ''))
r.sendline('3'.encode('base64').replace('\n', ''))
r.recvuntil('one of us: (')
x = int(r.recvuntil('L,', drop=True))
y = int(r.recvuntil('L)', drop=True))
pk = (x, y)
print pk

r.recvuntil('Please tell us your public key:')
r.sendline(('%d, %d' % G).encode('base64').replace('\n', ''))
r.sendline('1'.encode('base64').replace('\n', ''))
sig = schnorr_sign('DEPOSIT', 1)
assert schnorr_verify('DEPOSIT', G, sig)
r.sendline(sig.encode('base64').replace('\n', ''))

r.recvuntil('Please tell us your public key:')
r.sendline(('%d, %d' % G).encode('base64').replace('\n', ''))
r.sendline('1'.encode('base64').replace('\n', ''))
sig = schnorr_sign('DEPOSIT', 1)
assert schnorr_verify('DEPOSIT', G, sig)
r.sendline(sig.encode('base64').replace('\n', ''))

_G = G[0], -G[1]
t = point_add(pk, _G)
t = t[0], -t[1]
assert point_add(pk, t) == G
print on_curve(t)

r.recvuntil('Please tell us your public key:')
r.sendline(('%d, %d' % t).encode('base64').replace('\n', ''))
r.sendline('2'.encode('base64').replace('\n', ''))
sig = schnorr_sign('WITHDRAW', 1)
assert schnorr_verify('WITHDRAW', G, sig)
r.sendline(sig.encode('base64').replace('\n', ''))

r.interactive()
