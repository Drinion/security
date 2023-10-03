import encrypt
import decrypt

class Main:

    def __init__(self):
        self.start()

    def start(self):
        file_path = input("Hey! Before we start, please give me a file to either en- or decrypt (enter filepath): ")
        global file
        file = open(file_path, 'r')
        self.choose_encryption_or_decryption()

    def encrypt(self):
        encrypt.Encrypt().start(file)

    def decrypt(self):
        decrypt.Decrypt().start()

    global options
    options = {
            'encrypt': encrypt,
            'decrypt': decrypt
            }

    def choose_encryption_or_decryption(self):
        choice = input("Would you like to encrypt or decrypt a file?")
        options[str(choice)](self)

main = Main()
main.start

