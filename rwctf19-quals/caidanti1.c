#include <stdint.h>

// rwctf{Turns_out_this_is_harder_than_expected}

typedef uint64_t size_t;

typedef struct string {
    const char *ptr;
    uint64_t length;
    uint64_t flags;
} string;

void *memset(void *b, int c, size_t len);

const char *c_str(const string *str);

void _start() {
    uintptr_t text_base = (uintptr_t)__builtin_return_address(0) - 0x7205;
    int (*printf)(const char *, ...);
    int (*exit)(int);
    *(uintptr_t *)&printf = text_base + 0x10C40;
    *(uintptr_t *)&exit = text_base + 0x10C00;
    void *ctx = *(void **)(text_base + 0x12140);
    printf("hello world %#llx\n", text_base);

    uint64_t sol[2] = {0x416564614d756f59, 0x6c6c61434c444946L};

    string magic = {
        .ptr = (char *)&sol,
        .length = 0x10,
        .flags = 0x8000000000000000 | 0x20,
    };

    int (*SecretStorageGetFlag1)(void *, const string *, void *);
    *(uintptr_t *)&SecretStorageGetFlag1 = text_base + 0x7F00;

    string resp;
    memset(&resp, 0, sizeof(resp));

    printf("secret: %s\n", c_str(&magic));

    int ret = SecretStorageGetFlag1(ctx, &magic, &resp);

    printf("request result = %d\n", ret);
    printf("flag: %s\n", c_str(&resp));

    exit(0);
}

void *memset(void *b, int c, size_t len) {
    for (int i = 0; i < len; i++) {
        ((uint8_t *)b)[i] = c;
    }
    return b;
}

const char *c_str(const string *str) {
    if (str->flags & 0x8000000000000000) {
        return str->ptr;
    } else {
        return (const char *)str;
    }
}
