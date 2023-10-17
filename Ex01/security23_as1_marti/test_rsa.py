import os
import pytest
import rsa
import encrypt
import decrypt


def test_key_deciphered_equals_seed_key():
    test_file = open('files/test_file.txt', 'rb')
    RSA = rsa.RSA(test_file, 'files/test_file.txt')
    seed_key = (23).to_bytes(16, 'little')
    e, N = RSA.generate_keys()
    encrypted_sym_key = RSA.encrypt_sym_key(seed_key, e, N)
    private_key, N = RSA.get_private_key_values()
    decrypted_sym_key = RSA.decrypt_sym_key(encrypted_sym_key, private_key, N)

    assert 23 == decrypted_sym_key


def test_decrypted_message_equals_encrypted_message():
    test_file = open('files/test_file.txt', 'rb')
    rsa_encrypt = encrypt.Encrypt(test_file, 'files/test_file.txt')
    rsa_encrypt.encrypt_rsa('files/test_file.txt')
    encrypted_file = open('encrypted_files/test_file_encrypted.bin', 'rb')
    rsa_decrypt = decrypt.Decrypt(encrypted_file, 'encrypted_files/test_file_encrypted.bin')
    rsa_decrypt.decrypt_rsa('encrypted_files/test_file_encrypted.bin')
    decrypted_file = open('decrypted_files/test_file_decrypted.bin', 'rb')
    with open('files/test_file.txt', 'r') as f:
        message = f.read()
    with open('decrypted_files/test_file_decrypted.bin', 'rb') as f:
        decrypted_message = f.read().decode('ascii')

    assert decrypted_message == message.split('\n')[0]
