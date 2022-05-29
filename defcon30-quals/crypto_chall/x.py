from pwn import *

p = remote('crypto-challenge-lpw5gjiu6sqxi.shellweplayaga.me', 31337)
p.sendline('ticket{} ')

def menu(choice):
    p.recvuntil('>')
    p.sendline(str(choice))

qq = 0x468f42db6a682b136aadcacf3b8be3
pp = 0x20b14a31870069c5ff9a63b311d337
ee = 0x10001
nn = pp * qq
msg = 0x25

keynum = -1

def create_key_mes():
    global keynum

    menu(0)
    menu(0)
    keynum += 1
    return keynum

def create_key_13():
    global keynum

    menu(0)
    menu(1)
    keynum += 1
    return keynum

def create_bytekey():
    global keynum

    menu(0)
    menu(2)
    menu('0xf')
    keynum += 1
    return keynum

def create_key_epq():
    global keynum

    menu(0)
    menu(3)
    menu(hex(ee))
    menu(hex(pp))
    menu(hex(qq))
    keynum += 1
    return keynum

def create_key_edn():
    global keynum

    menu(0)
    menu(3)
    menu(hex(ee))
    menu(hex(dd))
    menu(hex(nn))
    keynum += 1
    return keynum

def decrypt(keynum, yesno=False):
    menu(2)
    menu(keynum)
    menu(1)
    menu(hex(msg))
    if yesno:
        menu('y')
    p.recvuntil('Your decrypted message is:\n\n')
    return p.recvuntil('\n\n', drop=True)

def encrypt(keynum, yesno=False, enc_msg=b"dank memes"):
    menu(1)
    menu(keynum)
    menu(enc_msg)
    p.recvuntil('Your encrypted message is:\n\n')
    return p.recvuntil('\n\n', drop=True)

create_key_epq()
create_key_mes()

def optimize(keynum):
    for _ in range(9):
        decrypt(keynum)
    return decrypt(keynum, True)

leak = optimize(0)
print('leak', leak.hex())
leak = int(leak.hex(), 16)

ee = int(raw_input('E from sage:'))

create_key_mes()
create_key_epq()
create_key_mes()
for _ in range(9):
    decrypt(3)
# decrypt multi msg
menu(2)
menu(3)
menu(1)
msg = '0x' + '0' * 14 + '2' + '0' * (0x60 - 21)
msg = msg.ljust(0x5c)
menu(msg)
menu('y')
flag = encrypt(4, enc_msg='0' * 0x40)
flag = bytearray(bytes.fromhex(flag[2:].decode('utf-8')))
print(flag)
for i in range(len(flag)):
    flag[i] ^= 0x30
print(flag)
# flag{dOnT_pUt_YoUr_lAmBdA_iN_a_LaMdA!!houchik3ohleet1ia7ohnoob7}

p.interactive()
