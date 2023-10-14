import encrypt
import decrypt


class Main:
    def __init__(self):
        self.start()

    def start(self):
        file_path = input("Hey! Please give me a file (enter filepath): ")
        global file
        file = open(file_path, 'rb')
        self.choose_encryption_or_decryption()

    def encrypt(self):
        encrypt.Encrypt(file, file_path).start()

    def decrypt(self):
        decrypt.Decrypt(file, file_path).start()

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
