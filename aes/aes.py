import os
import base64
import argparse
from Crypto.Cipher import AES

# commandline arguments
ap = argparse.ArgumentParser()
ap.add_argument('-k', '--key', required=True, help='the key used in encryption and decryption')
ap.add_argument('-m', '--mode', default='enc',
                help='mode of encrypt or decrypt. default is enc. available value: enc|dec')
ap.add_argument('-i', '--input', help='input string you want to append to a file')
ap.add_argument('-f', '--file', help='file you want to append to or decrypt from.')
ap.add_argument('-e', '--encoding', default='utf8', help='encoding use in encryption and decryption. default is utf8')
args = vars(ap.parse_args())

if args['file'] is None:
    args['file'] = os.path.join(os.environ['HOME'], '.aes')


# if the text is not a multiple of 16, add some characters
# so that it become a multiple of 16
def multiple_of_16(text):
    while len(text) % 16 != 0:
        text += ' '
    return str.encode(text)


key_bin = multiple_of_16(args['key'])
aes = AES.new(key_bin, AES.MODE_ECB)  # init cipher


# encrypt a line into a encrypted line
def enc(line):
    encrypted_bin = aes.encrypt(multiple_of_16(line))
    encrypted_text = str(base64.encodebytes(encrypted_bin), encoding=args['encoding'])
    return encrypted_text


# decrypt a line into a decrypted line
def dec(line):
    to_decrypt_bin = base64.decodebytes(bytes(line, encoding=args['encoding']))
    decrypted_bin = aes.decrypt(to_decrypt_bin)
    decrypted_text = str(decrypted_bin.decode('utf8')).rstrip(' ')
    return decrypted_text


if args['mode'] == 'enc':
    assert args['input'] is not None, 'the input should not be none'
    with open(args['file'], 'a') as fh:
        fh.write(enc(args['input']))
elif args['mode'] == 'dec':
    assert os.path.exists(args['file']), 'the file does not exist'
    with open(args['file'], 'r') as fh:
        for line in fh:
            print(dec(line))
else:
    print('the mode should be enc or dec')
