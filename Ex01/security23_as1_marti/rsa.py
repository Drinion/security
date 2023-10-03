import random
from Crypto.Cipher import AES

class RSA:

    def __init__(self):
        self.generate_keys()

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

    def isPrime(n):
        for i in len(int(n/2)):
            if n % i == 0:
                return false
            return true

    def generate_primes():
        lbound = 0
        ubound = 10000

        return [i for i in range(lbound,ubound) if isPrime(i)]

    def symmetric_aes_gcm():
        key = get_random_bytes(32)
        """
        Generate aead keypairs.
        """

    def encrypt_file_with_aes_gcm(self):
        key = get_random_bytes(32)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        encrypted_file = cipher.encrypt
        """
        Encrypt file with AEAD.
        """

    def encrypt_sym_key(int aes_gcm_key, int e, int N):
        sym_key_encrypted = (aead_key^e) % N

        return sym_key_encrypted
        """
        Encrypt the symmetric aead key with RSA.
        """

    def append(file, key):
        """
        Append key to body of file. Save it as well.
        """
