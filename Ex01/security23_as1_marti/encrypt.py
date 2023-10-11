#  import Crypto.Cipher as cc
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import rsa

class Encrypt:

    def start(self, file):
        self.file = file
        self.choose_encryption_algo()

    def encrypt_ecb(self):
        file_contents = bytes(self.file.read())
        key = get_random_bytes(32)

        with open('keys/ecb_key.bin', 'wb') as f:
            f.write(key)

        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_file = cipher.encrypt(pad(file_contents, 32))

        with open('encrypted_files/en_ecb.bin', 'wb') as f:
            f.write(encrypted_file)

    def encrypt_ofb(self):
        file_contents = bytes(self.file.read())
        key = get_random_bytes(32)

        with open('keys/ofb_key.bin', 'wb') as f:
            f.write(key)

        cipher = AES.new(key, AES.MODE_OFB)

        with open('keys/ofb_iv.bin', 'wb') as f:
            f.write(cipher.iv)

        encrypted_file = cipher.encrypt(pad(file_contents, 32))

        with open('encrypted_files/en_ofb.bin', 'wb') as f:
            f.write(encrypted_file)

    def encrypt_rsa(self):
        rsa.RSA(self.file).encrypt()
        #  sym_aead_key = rsa.symmetric_aead()
        #  encrypted_file = rsa.encrypt_file_with_aead(self.file)
        #  enc_sym_key = rsa.encrypt_sym_key("public_key.bin")
        #  rsa.append(encrypted_file, enc_sym_key)

    """
    TODO: options shouldn't be global. Change it.
    """
    global options
    options = {
            'ecb': encrypt_ecb,
            'ofb': encrypt_ofb,
            'rsa': encrypt_rsa
            }

    def choose_encryption_algo(self):
        chosen_algo = input("What algorithm should be used for the encryption? (enter ECB, OFB or RSA):")
        print(chosen_algo + " is a nice choice!")
        options[str(chosen_algo.lower())](self)
