import random
import math
import json
import codecs
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class RSA:

    def __init__(self, file):
        self.file = file
        self.encrypt()

    def generate_e(self, n):
        found = False
        k = random.choice(range(1, n-1))
        while ~found:
            if math.gcd(n, k) == 1:
                #  found = False
                return k
            k = random.choice(range(1, n-1))

    def generate_d(self, e, n):
        if e == 0:
            return n,0,1

        gcd,x_1,y_1 = self.generate_d(n%e, e)
        x = y_1 - (n//e)*x_1
        y = x_1
        
        return 1,x,y

    def isPrime(self, n):
        for i in range(2, int(n/2)+1):
            if n % i == 0:
                return False
            return True

    def generate_primes(self):
        lbound = 0
        ubound = 10000

        return [i for i in range(lbound,ubound) if self.isPrime(i)]
        
    def generate_keys(self):
        primes = self.generate_primes()
        p = random.choice(primes)
        q = random.choice(primes)
        N = p*q
        phi_N = (p-1)*(q-1)
        e = self.generate_e(phi_N)
        d = self.generate_d(e, phi_N)

        with open('keys/public_key.bin', 'w') as f:
            dictionary = { "e": e, "N": N }
            json.dump(dictionary, f)

        with open('keys/private_key.bin', 'w') as f:
            dictionary = { "d": d, "N": N }
            json.dump(dictionary, f)

        return e, N

    def encrypt_file_with_aes_gcm(self):
        key = get_random_bytes(32)
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce
        encrypted_file = cipher.encrypt(pad(self.file.read(), 32))
        
        return encrypted_file, key

    def encrypt_sym_key(self, aes_gcm_key, e, n):
        sym_key_encrypted = ((int.from_bytes(aes_gcm_key, 'little'))^e) % n

        return sym_key_encrypted

    def append(self, file, key):
        with open('files/aead_encrypted.txt', 'wb') as f:
            f.write(file)
            f.write(bytes(key))

        print("Encrypted file stored as 'files/aead_encrypted.txt'")

    def extract_sym_key(self, file):
        lines = file.readlines()

        return lines[1]
    
    def extract_file_content(self, file):
        message = json.loads(file)

        return message['content']

    def decrypt_sym_key(self, sym_key):
        decrypted_key = c^d % N

        return decrypted_key

    def decrypt_file_with_aes_gcm(self, key):
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted_file = cipher.decrypt(pad(self.file, 32))
        
        return decrypted_file

    def save_decrypted_file(self, file):
        with open('files/aead_decrypted.txt', 'w') as f:
            f.write(file)

    def encrypt(self):
        e, N = self.generate_keys()
        encrypted_file, sym_key = self.encrypt_file_with_aes_gcm()
        encrypted_sym_key = self.encrypt_sym_key(sym_key,e,N)
        self.append(encrypted_file, encrypted_sym_key)

    def decrypt(self):
        sym_key = extract_sym_key(file)
        file_content = extract_file_content(file)
        decrypted_sym_key = decrypt_sym_key(sym_key)
        decrypted_file = decrypt_file_with_aes_gcm(file, sym_key)
        save_decrypted_file(decrypted_file)
