qq = 0x468f42db6a682b136aadcacf3b8be3
pp = 0x20b14a31870069c5ff9a63b311d337
ee = 0x10001

def reverse(l):
    dq = discrete_log(Mod(l, qq), Mod(37, qq))
    print(dq)
    dp = discrete_log(Mod(l, pp), Mod(37, pp))
    print(dp)
    d = crt([dq, dp], [qq - 1, pp - 1])
    print(d)
    assert pow(37, d, pp * qq) == l
    
    phi = (pp - 1) * (qq - 1)
    C = (0x4847464544434241 << 64) + 0x25a48
    assert (d * ee - 1) % (qq - 1) == 0
    for i in range(1, 0x10000):
        r = ((phi * i + d) * ee - 1) / (qq - 1)
        if i % 100 == 0:
            print(i, r)
        for dv in divisors(r):
            if int(dv >> 64) == 0x4847464544434241:
                return dv - C + 1

def search(text_base):
    C = (0x4847464544434241 << 64) + 0x25a48
    x = C + text_base
    z = text_base + 0x25a70

    for i in range(0, 0x100000, 2):
        y = int((b'%010x' % i).hex(), 16)
        t = (x - 1) * (y - 1) // gcd(x - 1, y - 1)
        d, e, _ = xgcd(z, t)
        e = e % t
        if d == 1 and gcd(e, phi) == 1 and e < 2 ^ 256:
            print(hex(y), e, hex(z))
            return e

def pwn(l):
    base = reverse(l)
    print(hex(base))
    search(base)
