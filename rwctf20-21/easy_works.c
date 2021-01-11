#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/types.h>

const char *executable = "./easy_works.elf";

int main(int argc, char *argv[])
{
    if (argc < 2) {
        return -1;
    }

    int exe = open(executable, O_RDONLY);
    if (exe == -1) {
        perror("open");
        return -1;
    }

    if (mmap((void *)0x00408000, 0x100000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANON | MAP_PRIVATE | MAP_FIXED, -1, 0) == MAP_FAILED) {
        perror("mmap");
        return -1;
    }

    if (lseek(exe, 0x80, SEEK_SET) == -1 || read(exe, (void *)0x00408000, 0xdf330) != 0xdf330) {
        perror("read");
        return -1;
    }
    void *ctx = (void *)0x504A00;

    void (*init_ctx)(void *, void *);
    *(uintptr_t *)&init_ctx = 0x40CFC5;

    void (*stream_dec)(void *, void *, int);
    void (*stream_enc)(void *, void *, int);
    *(uintptr_t *)&stream_dec = 0x40DF63;
    *(uintptr_t *)&stream_enc = 0x40DEED;
    void (*block_dec)(void *, void *);
    void (*block_enc)(void *, void *);
    *(uintptr_t *)&block_dec = 0x40DE0F;
    *(uintptr_t *)&block_enc = 0x40DD84;
    void (*set_iv)(void *, void *);
    *(uintptr_t *)&set_iv = 0x40D019;

    uint32_t (*crc32)(uint32_t, void *, uint32_t);
    *(uintptr_t *)&crc32 = 0x40E93B;

    uint8_t A[0x4000] = {0}, B[0x4000] = {0};
    int n = read(0, &A, 0x4000);
    if (!strcmp(argv[1], "enc")) {
        if (n % 0x10) {
            uint8_t pad = 0x10 - n % 0x10;
            while (n % 0x10) A[n++] = pad;
        }
        init_ctx(ctx, (void *)0x4D251F);
        set_iv(ctx, "12345678abcdefgh");
        stream_enc(ctx, &A, n);
        memcpy(&B, &A, 0x4000);
        init_ctx(ctx, (void *)0x4D251F);
        set_iv(ctx, "12345678abcdefgh");
        stream_dec(ctx, &B, n);
        // write(1, &B, n);
    } else if (!strcmp(argv[1], "crc")) {
        *(uint32_t *)&A[0xc] = 0;
        uint32_t res = crc32(0, &A, n);
        *(uint32_t *)&A[0xc] = res;
    }
    write(1, &A, n);

    return 0;
}
