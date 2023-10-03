import random
import json
from Crypto.Cipher import AES

class RSA:

    def __init__(self, file):
        self.file = file
        self.encrypt()

    def encrypt(self.file):
        e, N = generate_keys()
        encrypted_file, sym_key = encrypt_file_with_aes_gcm(self.file)
        encrypted_sym_key = encrypt_symmetric_key(sym_key,e,N)
        append(encrypted_file, encrypted_sym_key)

    def decrypt(self.file):
        sym_key = extract_sym_key(file)
        file_content = extract_file_content(file)
        decrypted_sym_key = decrypt_sym_key(sym_key)
        decrypted_file = decrypt_file_with_aes_gcm(file, sym_key)
        save_decrypted_file(decrypted_file)

    def generate_e(int N):
        found = false
        k = random.choice([1..N-1])
        while found == false:
            if math.gcd(N, k) == 1:
                found = true
                return k
            k = random.choice([1..N-1])

    def generate_d(int e, int N):
        if e == 0:
            return N,0,1

        gcd,x_1,y_1 = generate_d(N%e, e)
        x = y_1 - (N//e)*x_1
        y = x_1
        
        return x
        
    def generate_keys(self):
        primes = generate_primes()
        p = random.choice(primes)
        q = random.choice(primes)
        N = p*q
        phi_N = (p-1)*(q-1)
        e = generate_e(phi_N)
        d = generate_d(e, phi_N)

        with open('keys/public_key.txt', 'w') as f:
            f.write("e:" +  e + "\n" + "N:" + N)
        with open('keys/private_key.txt', 'w') as f:
            f.write("d:" +  d + "\n" + "N:" + N)

        return e, N

    def isPrime(n):
        for i in len(int(n/2)):
            if n % i == 0:
                return false
            return true

    def generate_primes():
        lbound = 0
        ubound = 10000

        return [i for i in range(lbound,ubound) if isPrime(i)]

    def encrypt_file_with_aes_gcm(self):
        key = get_random_bytes(32)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        encrypted_file = cipher.encrypt(pad(self.file, 32))
        
        return encrypted_file, key

    def encrypt_sym_key(int aes_gcm_key, int e, int N):
        sym_key_encrypted = (aead_key^e) % N

        return sym_key_encrypted

    def append(file, key):
        with open('files/aead_encrypted.txt', 'w') as f:
            dictionary = { content: file.content, key: key }
            json.dump(dictionary, f)

        print("Encrypted file stored as 'files/aead_encrypted.txt'")

    def extract_sym_key(file):
        message = json.loads(file)

        return message['key']
    
    def extract_file_content(file):
        message = json.loads(file)

        return message['content']

    def decrypt_sym_key(sym_key):
        decrypted_key = c^d % N

        return decrypted_key

    def decrypt_file_with_aes_gcm(self, key):
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        encrypted_file = cipher.decrypt(pad(self.file, 32))
        
        return decrypted_file

    def save_decrypted_file(file):
        with open('files/aead_decrypted.txt', 'w') as f:
            f.write(file.content)
