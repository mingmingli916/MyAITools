# Author: Hack Chyson
# [2018-12-20 11:38:15]


import sys
import base64
# package: cryptodome
from Crypto.Cipher import AES

mode = sys.argv[1]
key = sys.argv[2]
input_filename = sys.argv[3]
output_filename = sys.argv[4]


# if the text is not a multiple of 16, add some characters
# so that it become a multiple of 16
def multiple_of_16(text):
    while len(text) % 16 != 0:
        text += ' '
    return str.encode(text)


# all the encryption and decryption are based on binary
key_bin = multiple_of_16(key)
aes = AES.new(key_bin, AES.MODE_ECB)  # init cipher

input_file = open(input_filename, "r")
output_file = open(output_filename, "w")


def encrypt():
    for line in input_file:
        encrypted_bin = aes.encrypt(multiple_of_16(line))
        encrypted_text = str(base64.encodebytes(encrypted_bin), encoding='utf8')  
        output_file.write(encrypted_text)
    input_file.close()
    output_file.close()


def decrypt():
    for line in input_file:
        to_decrypt_bin = base64.decodebytes(bytes(line, encoding='utf8'))
        decrypted_bin = aes.decrypt(to_decrypt_bin)
        decrypted_text = str(decrypted_bin.decode('utf8')).rstrip(' ')
        output_file.write(decrypted_text)


if 'enc' == mode or 'encrypt' == mode:
    encrypt()
elif 'dec' == mode or 'decrypt' == mode:
    decrypt()
else:
    print('usage: python aes.py enc|dec <key> <input path> <output path>')
