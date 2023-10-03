import Crypto.Cipher as cc
from Crypto.Random import get_random_bytes

class Encrypt:

    def __init__(self):
        self.file = "blablabla"
        self.choose_encryption_algo()

    def encrypt_ecb(self):
        key = get_random_bytes(32)
        cipher = cc.AES.new(key, MODE_ECB)
        encrypted_file = cipher.encrypt(pad(self.file, 32))

        with open('encrypted_files/en_ecb.txt', 'w') as f:
            f.write(encrypted_file)

    def encrypt_ofb(self):
        key = get_random_bytes(32)
        cipher = cc.AES.new(key, MODE_OFB)
        encrypted_file = cipher.encrypt(pad(self.file, 32))

        with open('encrypted_files/en_ofb.txt', 'w') as f:
            f.write(encrypted_file)

    def encrypt_rsa(self):
        RSA.generate_keypairs()
        sym_aead_key = RSA.symmetric_aead()
        encrypted_file = RSA.encrypt_file_with_aead(self.file)
        enc_sym_key = RSA.encrypt_sym_key("public_key.txt")
        RSA.append(encrypted_file, enc_sym_key)

    """
    TODO: options shouldn't be global. Change it.
    """
    global options
    options = {
            'ECB': encrypt_ecb,
            'OFB': encrypt_ofb
            }

    def choose_encryption_algo(self):
        chosen_algo = input("What algorithm should be used for the encryption? (enter ECB or OFB):")
        print(chosen_algo + " is a nice choice!")
        options.get(str(chosen_algo))
encrypt = Encrypt()
