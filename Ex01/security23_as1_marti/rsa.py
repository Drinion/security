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
    
    def gcd(self, a, b):
        if (b == 0):
            return a
        else:
            return self.gcd(b, a % b)

    #  def generate_e(self, n):
        #  found = False
        #  k = random.choice(range(1, n-1))
        #  while ~found:
            #  if math.gcd(n, k) == 1:
#                found = False
                #  return k
            #  k = random.choice(range(1, n-1))

    def generate_e(self, n):
        while (True):
            e = random.randrange(2, n)

            if (self.gcd(e, n) == 1):
                return e

    def generate_d(self, e, n):
        x, old_x = 0, 1
        y, old_y = 1, 0

        while (n != 0):
            quotient = e // n
            e, n = n, e - quotient * n
            old_x, x = x, old_x - quotient * x
            old_y, y = y, old_y - quotient * y

        return e, old_x, old_y

    #  def isPrime(self, n):
        #  for i in range(2, int(n/2)+1):
            #  if n % i == 0:
                #  return False
            #  return True

    #  def generate_primes(self):
        #  lbound = 10000000
        #  ubound = 1000000000000000
#
        #  return [i for i in range(lbound,ubound) if self.isPrime(i)]

    def generate_keys(self):
        p = 11
        q = 23
        N = p*q
        phi_N = (p-1)*(q-1)
        e = self.generate_e(phi_N)
        gcd, x, y = self.generate_d(e, phi_N)

        if (x < 0):
            d = x + phi_N
        else:
            d = x

        with open('keys/public_key.bin', 'w') as f:
            dictionary = { "e": e, "N": N }
            json.dump(dictionary, f)

        with open('keys/private_key.bin', 'w') as f:
            dictionary = { "d": d, "N": N }
            json.dump(dictionary, f)

        return e, N

    def get_private_key_values(self):
        with open('keys/private_key.bin', 'r') as f:
            json_file = json.load(f)

        return json_file['d'], json_file['N']

    def encrypt_file_with_aes_gcm(self):
        key = b"1000100010001000"
        cipher = AES.new(key, AES.MODE_GCM)
        #  nonce = cipher.nonce
        encrypted_file, tag = cipher.encrypt_and_digest(pad(self.file.read(), 16))

        with open("keys/gcm_nonce.bin", "wb") as f:
            f.write(tag)


        return encrypted_file, key

    def encrypt_sym_key(self, aes_gcm_key, e, n):
        sym_key_encrypted = pow(int.from_bytes(aes_gcm_key, 'little'), e) % n

        return sym_key_encrypted

    def append(self, file, key):
        with open('files/aead_encrypted.json', 'w') as f:
            dictionary = { "file": int.from_bytes(file, 'little'), "key": key }
            json.dump(dictionary, f)

        print("Encrypted file stored as 'files/aead_encrypted.json'")

    def extract_sym_key(self, file):
        json_file = json.load(file)

        return json_file['key'], json_file['file']

    #  def extract_file_content(self, file):
        #  json_file = json.load(file)
    #
        #  return json_file['file']

    def decrypt_sym_key(self, c, d, N):
        decrypted_key = pow(c, d) % N

        return decrypted_key

    def decrypt_file_with_aes_gcm(self, key, file):
        with open("keys/gcm_nonce.bin", "rb") as f:
            tag = f.read()
        test_key = b"1000100010001000"
        cipher = AES.new(test_key, AES.MODE_GCM)
        #  decrypted_file = cipher.decrypt_and_verify(int(file).to_bytes(file.bit_length(), 'little'), 16)
        decrypted_file = cipher.decrypt(file.to_bytes(file.bit_length() + 7 // 8, 'little'), tag)

        return decrypted_file

    def save_decrypted_file(self, file):
        with open('files/aead_decrypted.json', 'w') as f:
            f.write(file)

    def encrypt(self):
        e, N = self.generate_keys()
        encrypted_file, sym_key = self.encrypt_file_with_aes_gcm()
        encrypted_sym_key = self.encrypt_sym_key(sym_key,e,N)
        self.append(encrypted_file, encrypted_sym_key)

    def decrypt(self):
        sym_key, file_content = self.extract_sym_key(self.file)
        d, N = self.get_private_key_values()
        decrypted_sym_key = self.decrypt_sym_key(sym_key, d, N)
        decrypted_file = self.decrypt_file_with_aes_gcm(bytes(decrypted_sym_key), file_content)
        self.save_decrypted_file(decrypted_file)
