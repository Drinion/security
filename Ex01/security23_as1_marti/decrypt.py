import Crypto.Cipher as cc
from Crypto.Random import get_random_bytes

class Decrypt:

    def start(self):
        self.file = file
        self.choose_decryption_algo()

    def decrypt_ecb(self):
        ecb_key = Encrypt.get(ecb_key)
        cipher = cc.AES.new(key, MODE_ECB)
        decrypted_file = cipher.decrypt(pad(self.file, 32))

        with open('decrypted_files/de_ecb.txt', 'w') as f:
            f.write(decrypted_file)

    def decrypt_ofb(self):
        ofb_key = Encryption.get(ofb_key)
        cipher = cc.AES.new(key, MODE_OFB)
        decrypted_file = cipher.decrypt(pad(self.file, 32))

        with open('decrypted_files/de_ofb.txt', 'w') as f:
            f.write(decrypted_file)

    global options
    options = {
            'ECB': decrypt_ecb,
            'OFB': decrypt_ofb
            }

    def choose_decryption_algo(self):
        chosen_algo = input("What algorithm should be used for the decryption? (enter ECB, OFB or RSA):")
        print(chosen_algo + " is a nice choice!")
        options.get(str(chosen_algo))
