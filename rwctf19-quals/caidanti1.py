M = (2 ** 64) - 1

def rol(x, n):
    return ((x << n) | (x >> (64 - n))) & M

def add(x, y):
    return (x + y) & M

def sub(x, y):
    return (x - y) & M

def enc(x, y):
    v7 = 0x70697A7A6174716C
    v10 = 0x6C7174617A7A6970
    v9, v8 = x, y
    for i in xrange(32):
        v8 = v7 ^ add(v9, rol(v8, 56))
        v9 = v8 ^ rol(v9, 3)
        v10 = i ^ add(v7, rol(v10, 56))
        v7 = v10 ^ rol(v7, 3)
    return v8, v9

def dec(x, y):
    v7 = 0x70697A7A6174716C
    v10 = 0x6C7174617A7A6970
    k = []
    for i in xrange(32):
        k.append(v7)
        v10 = i ^ add(v7, rol(v10, 56))
        v7 = v10 ^ rol(v7, 3)
    v8, v9 = x, y
    for i in xrange(31, -1, -1):
        v9 = rol(v8 ^ v9, 61)
        v8 = rol(sub(k[i] ^ v8, v9), 8)
    return v9, v8

assert enc(0, 0) == (0x39af29ba501f0b21, 0xf9e6bb25024bd95c)
sol = dec(0xC96AAC2F35C3833F, 0x8F1FA1AD36C66F95)
print map(hex, sol)
print map(hex, enc(*sol))
