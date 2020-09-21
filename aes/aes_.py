# Author: Hack Chyson
# [2018-12-20 11:27:27]

import sys
import base64
# package: cryptodome
from Crypto.Cipher import AES


# all the encrypt and decrypt operations is based on binary data
# this avoid many encoding problems
# base64 is used for human reading
# because you cannot copy a binary content in the console or somewhere else
# base64 can convert any character,
# so it is used between binary and character

# if the text is not a multiple of 16, add some characters
# so that it become a multiple of 16
def multiple_of_16(text):
    while len(text) % 16 != 0:
        text += ' '
    return str.encode(text)


# key = '123456'
# text = 'hello world'
mode = sys.argv[1]
key = sys.argv[2]
text = sys.argv[3]

# all the encryption and decryption are based on binary
key_bin = multiple_of_16(key)
text_bin = multiple_of_16(text)
aes = AES.new(key_bin, AES.MODE_ECB)  # init cipher



def encrypt():
    encrypted_bin = aes.encrypt(text_bin)
    encrypted_text = str(base64.encodebytes(encrypted_bin), encoding='utf8').rstrip('\n')  # ?
    return encrypted_text


def decrypt():
    to_decrypt_bin = base64.decodebytes(bytes(text, encoding='utf8'))
    decrypted_bin = aes.decrypt(to_decrypt_bin)
    decrypted_text = str(decrypted_bin.decode('utf8')).rstrip(' ')
    return decrypted_text


if 'enc' == mode or 'encrypt' == mode:
    print(encrypt())
elif 'dec' == mode or 'decrypt' == mode:
    print(decrypt())
else:
    print('usage: python aes.py enc|dec <key> <text>')
