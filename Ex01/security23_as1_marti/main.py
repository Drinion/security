import encrypt
import decrypt


class Main:
    def __init__(self):
        self.start()

    def start(self):
        file_path = input("Hey! Please give me a file (enter filepath): ")
        file = open(file_path, 'rb')
        self.choose_encryption_or_decryption(file, file_path)

    def encrypt(self, file, file_path):
        encrypt.Encrypt(file, file_path).start()

    def decrypt(self, file, file_path):
        decrypt.Decrypt(file, file_path).start()

    def choose_encryption_or_decryption(self, file, file_path):
        choice = input("Would you like to encrypt or decrypt a file?")
        if choice.lower() == 'encrypt':
            self.encrypt(file, file_path)
        if choice.lower() == 'decrypt':
            self.decrypt(file, file_path)

main = Main()
main.start
