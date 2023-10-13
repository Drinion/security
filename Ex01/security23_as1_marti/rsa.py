import random, math, json
from struct import pack
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class RSA:

    def __init__(self, file, file_path):
        self.file = file
        self.file_path = file_path

    def generate_e(self, n):
        while (True):
            e = random.randrange(2, n)
            if (math.gcd(e, n) == 1):
                return e

    def generate_gcd(self, e, n):
        x, old_x = 0, 1
        y, old_y = 1, 0

        while (n != 0):
            quotient = e // n
            e, n = n, e - quotient * n
            old_x, x = x, old_x - quotient * x
            old_y, y = y, old_y - quotient * y

        return e, old_x, old_y

    def save_public_key(self, e, N):
        with open('keys/public_key.bin', 'w') as f:
            dictionary = { "e": e, "N": N }
            json.dump(dictionary, f)

    def save_private_key(self, d, N):
        with open('keys/private_key.bin', 'w') as f:
            dictionary = { "d": d, "N": N }
            json.dump(dictionary, f)

    def compute_d(self, x, phi_N):
        if (x < 0):
            d = x + phi_N
        else:
            d = x
        return d


    def generate_keys(self):
        p = 23
        q = 91
        N = p*q
        phi_N = (p-1)*(q-1)
        e = self.generate_e(phi_N)
        gcd, x, y = self.generate_gcd(e, phi_N)
        d = self.compute_d(x, phi_N)
        self.save_public_key(e, N)
        self.save_private_key(d, N)

        return e, N

    def get_private_key_values(self):
        with open('keys/private_key.bin', 'r') as f:
            json_file = json.load(f)

        return json_file['d'], json_file['N']

    def encrypt_file_with_aes_gcm(self):
        key = (3).to_bytes(16, 'little')
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce
        encrypted_file = cipher.encrypt(self.file.read(), output=None)

        with open("keys/gcm_nonce.bin", "wb") as f:
            f.write(nonce)

        return encrypted_file, key

    def encrypt_sym_key(self, aes_gcm_key, e, n):
        sym_key_encrypted = pow(int.from_bytes(aes_gcm_key, 'little'), e) % n

        return sym_key_encrypted

    def append(self, file, key):
        file_name = self.file_path.split("/")[-1].split(".")[0]
        with open('files/' + file_name + '_encrypted.json', 'w') as f:
            dictionary = { "file": int.from_bytes(file, 'little'), "key": key }
            json.dump(dictionary, f)

        print("Encrypted file stored as 'files/"+ file_name + "_encrypted.json'")

    def extract_sym_key(self, file):
        json_file = json.load(file)

        return json_file['key'], json_file['file']

    def decrypt_sym_key(self, c, d, N):
        decrypted_key = pow(c, d) % N

        return decrypted_key

    def decrypt_file_with_aes_gcm(self, key, file):
        with open("keys/gcm_nonce.bin", "rb") as f:
            nonce = f.read()
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted_file = cipher.decrypt(file.to_bytes(file.bit_length(), 'little'), output=None)

        return decrypted_file

    def save_decrypted_file(self, file):
        file_name = self.file_path.split("/")[-1].split(".")[0]
        text_first = str(file).split('#')[0].split("b\'")[1]

        with open('decrypted_files/' + file_name + '_decrypted.bin', 'w') as f:
            f.write(text_first + '#')

    def encrypt(self):
        e, N = self.generate_keys()
        encrypted_file, sym_key = self.encrypt_file_with_aes_gcm()
        encrypted_sym_key = self.encrypt_sym_key(sym_key,e,N)
        self.append(encrypted_file, encrypted_sym_key)

    def decrypt(self):
        encrypted_sym_key, file_content = self.extract_sym_key(self.file)
        d, N = self.get_private_key_values()
        decrypted_sym_key = self.decrypt_sym_key(encrypted_sym_key, d, N)
        decrypted_file = self.decrypt_file_with_aes_gcm(decrypted_sym_key.to_bytes(16, 'little'), file_content)
        self.save_decrypted_file(decrypted_file)
