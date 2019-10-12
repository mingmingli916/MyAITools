import base64
# package: cryptodome
from Crypto.Cipher import AES
import optparse

parser = optparse.OptionParser()
parser.set_usage("%prog inputfile outputfile [options]")
parser.add_option("-m", "--mode", dest="mode",
                  help="available values: encrypt|enc|decrypt|dec [default: %default]")
parser.add_option('-k', '--key', dest='key',
                  help='the key for encryption and decryption [default: %default')
parser.set_defaults(mode="enc", key='123456')
opts, args = parser.parse_args()

inputfile = args[0]
outputfile = args[1]
mode = opts.mode
key = opts.key


# if the text is not a multiple of 16, add some characters
# so that it become a multiple of 16
def multiple_of_16(text):
    while len(text) % 16 != 0:
        text += ' '
    return str.encode(text)


# all the encryption and decryption are based on binary
key_bin = multiple_of_16(key)
aes = AES.new(key_bin, AES.MODE_ECB)  # init cipher

input_file = open(inputfile, "r")
output_file = open(outputfile, "w")


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
    print('usage: python aes.py <inputfile> <outputfile>')
