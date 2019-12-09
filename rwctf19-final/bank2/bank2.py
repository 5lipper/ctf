from schnorr import *
from pwn import *
import hashlib

# rwctf{2r0unD_Schn0Rr_1s_N07_5AfE._cHEck_tH3_0ak1aNDl9_p4p3r}

def prove(prefix):
    for i in xrange(0x10000):
        proof = prefix + '%05x' % i
        test = hashlib.sha1(proof).digest()
        # return proof
        if test[-1] == '\0' and test[-2] == '\0':
            return proof

# r = remote('127.0.0.1', 20014)
r = remote('172.16.24.100', 20014)

prefix = r.recvline().strip().split()[-1]
print prefix
proof = prove(prefix)
print proof
r.send(proof)

print r.recvuntil('priority!')
r.sendline('1'.encode('base64').replace('\n', ''))
print r.recvuntil('Protocol..')
print r.recvline()
(Gr, pk) = eval(r.recvline())
print(Gr)
T = to_bytes(G[0], 32) + to_bytes(G[1], 32)
PK = to_bytes(pk[0], 32) + to_bytes(pk[1], 32)
commitment = T + PK
assert len(commitment) == 128
r.sendline(commitment.encode('base64').replace('\n', ''))
c = sha256(bytes_point(G) + 'DEPOSIT')
print('c', c)
s = r.recvline()
print('s', s)
sk = int(s.strip('L\n')) // c
sk -= 1
print('sk', sk)
assert point_mul(G, sk) == pk
r.sendline(('\x01' * 64).encode('base64').replace('\n', ''))
print r.recvuntil('priority!')

c = sha256('aaaa')
m = point_add(point_mul(G, (c + 1) * sk % n), point_mul(pk, n - c))
c = sha256(bytes_point(m) + 'WITHDRAW')
assert m == point_add(point_mul(G, (c + 1) * sk % n), point_mul(pk, n - c))
s = (c + 1) * sk % n
c = sha256(bytes_point(point_add(point_mul(G, s), point_mul(pk, n-c))) + 'WITHDRAW')
assert s == (c + 1) * sk % n

r.sendline('0'.encode('base64').replace('\n', ''))
r.recvuntil('signature')
xxx = to_bytes(c, 32) + to_bytes(s, 32)
r.sendline(xxx.encode('base64').replace('\n', ''))

r.interactive()
