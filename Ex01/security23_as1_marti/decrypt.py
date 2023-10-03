from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad, pad
import encrypt

class Decrypt:

    def start(self, file):
        self.file = file
        self.choose_decryption_algo()

    def decrypt_ecb(self):
        print('file_contents:', self.file.read())
        file_contents = self.file.read()

        with open('keys/ecb_key.txt', 'rb') as f:
            ecb_key = f.read()

        cipher = AES.new(ecb_key, AES.MODE_ECB)
        print('decrypted: ', cipher.decrypt(file_contents))
        decrypted_text = unpad(cipher.decrypt(file_contents), 32)

        with open('decrypted_files/de_ecb.txt', 'wb') as f:
            f.write(decrypted_text)

    def decrypt_ofb(self):
        ofb_key = Encryption.get(ofb_key)
        cipher = AES.new(key, AES.MODE_OFB)

        decrypted_file = (cipher.decrypt(self.file, 32))

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
        options[str(chosen_algo)](self)
