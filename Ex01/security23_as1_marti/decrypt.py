from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad, pad
import encrypt

class Decrypt:

    def start(self, file):
        self.file = file
        self.choose_decryption_algo()

    def decrypt_ecb(self):
        file_contents = self.file.read()

        with open('keys/ecb_key.bin', 'rb') as f:
            ecb_key = f.read()

        cipher = AES.new(ecb_key, AES.MODE_ECB)
        decrypted_text = unpad(cipher.decrypt(file_contents), 32)

        with open('decrypted_files/de_ecb.bin', 'wb') as f:
            f.write(decrypted_text)

    def decrypt_ofb(self):
        file_contents = self.file.read()

        with open('keys/ofb_key.bin', 'rb') as f:
            ofb_key = f.read()
        with open('keys/ofb_iv.bin', 'rb') as f:
            iv = f.read()

        cipher = AES.new(ofb_key, AES.MODE_OFB, iv=iv)
        decrypted_text = unpad(cipher.decrypt(file_contents), 32)

        with open('decrypted_files/de_ofb.bin', 'wb') as f:
            f.write(decrypted_text)

    global options
    options = {
            'ECB': decrypt_ecb,
            'OFB': decrypt_ofb
            }

    def choose_decryption_algo(self):
        chosen_algo = input("What algorithm should be used for the decryption? (enter ECB, OFB or RSA):")
        print(chosen_algo + " is a nice choice!")
        options[str(chosen_algo)](self)
