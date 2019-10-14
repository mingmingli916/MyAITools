import os
import base64
import argparse
from Crypto.Cipher import AES
import sys

default_file = os.path.sep.join([os.environ['HOME'], 'notes', '.aes'])

# commandline arguments
ap = argparse.ArgumentParser(description='Encrypt or decrypt to save or display something that is secret.')
group = ap.add_mutually_exclusive_group()
group.add_argument('-i', '--input', help='input string you want to encrypt or decrypt')
group.add_argument('-f', '--file', help='file you want to encrypt')

ap.add_argument('-k', '--key', default='123456', help='the key used in encryption and decryption')
ap.add_argument('-m', '--mode', default='enc', help='mode of encrypt or decrypt')
ap.add_argument('-d', '--database', default=default_file, help='file used to save encrypted thing')
ap.add_argument('-e', '--encoding', default='utf8', help='encoding use in encryption and decryption')
ap.add_argument('-v', '--verbose', action='store_true', help='show verbose information')
ap.add_argument('-o', '--overwrite', default='a', action='store_const', const='w',
                help='overwrite the content in database')
args = vars(ap.parse_args())

if args['verbose']:
    print('default file is {}'.format(default_file))
    print('default key is 123456')
    print('default mode is enc. Available value: enc or dec')
    print('default encoding is utf8')

    print("""
    example1: python aes.py -i 'hello world' # encrypt 'hello world' into database;
    example2: python aes.py -m dec # decrypt the content in database;
    example3: python aes.py -i my_file -k 111 # encrypt my_file with key 111 and save to database; 
    """)
    sys.exit(0)


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
    line = line.strip('\n') + '\n'
    encrypted_bin = aes.encrypt(multiple_of_16(line))
    encrypted_text = str(base64.encodebytes(encrypted_bin), encoding=args['encoding'])
    return encrypted_text


# decrypt a line into a decrypted line
def dec(line):
    to_decrypt_bin = base64.decodebytes(bytes(line, encoding=args['encoding']))
    decrypted_bin = aes.decrypt(to_decrypt_bin)
    decrypted_text = str(decrypted_bin.decode('utf8')).rstrip(' ').rstrip('\n')
    return decrypted_text


def dec_file(path):
    with open(path, 'r') as fh:
        for line in fh:
            print(dec(line))


if args['mode'] == 'enc':
    with open(args['database'], args['overwrite']) as fh:
        if args['input'] is not None:
            fh.write(enc(args['input']))
        elif args['file'] is not None:
            assert os.path.exists(args['file']), 'the file does not exist'
            with open(args['file']) as f:
                for line in f:
                    fh.write(enc(line))
        else:
            print('Either of input or file should not be None.')

elif args['mode'] == 'dec':
    if args['input'] is not None:
        print(dec(args['input']), sep='')
    else:
        dec_file(args['database'])

else:
    print('the mode should be enc or dec')
