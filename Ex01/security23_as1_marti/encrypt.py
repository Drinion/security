#  import Crypto.Cipher as cc
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import rsa


class Encrypt:

    def __init__(self, file, file_path):
        self.file = file
        self.file_path = file_path

    def start(self):
        self.choose_encryption_algo()

    def encrypt_ecb(self):
        file_contents = bytes(self.file.read())
        key = (300).to_bytes(16, 'little')

        with open('keys/ecb_key.bin', 'wb') as f:
            f.write(key)

        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_file = cipher.encrypt(pad(file_contents, 32))
        with open('encrypted_files/en_ecb.bin', 'wb') as f:
            f.write(encrypted_file)
        print("Encrypted file stored at 'encrypted_files/en_ecb.bin'")

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

    def encrypt_rsa(self, file_path):
        rsa.RSA(self.file, self.file_path).encrypt()

    global options
    options = {
            'ecb': encrypt_ecb,
            'ofb': encrypt_ofb,
            'rsa': encrypt_rsa
            }

    def choose_encryption_algo(self):
        chosen_algo = input("Choose encryption algorithm (ECB, OFB or RSA):")
        options[str(chosen_algo.lower())](self)
