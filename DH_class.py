import random

class DH_Endpoint(object):
    def __init__(self,client_public_key=None,server_public_key=None, private_key=None):
        if client_public_key==None:
            self.client_public_key = None
            self.server_public_key = None
            self.private_key = None
            self.full_key = None
        else:
            self.client_public_key = client_public_key
            self.server_public_key = server_public_key
            self.private_key = private_key
            self.full_key = None

    def generate_partial_key(self):
        partial_key = self.client_public_key ** self.private_key
        partial_key = partial_key % self.server_public_key
        return partial_key

    def generate_full_key(self, partial_key_client):
        full_key = partial_key_client ** self.private_key
        full_key = full_key % self.server_public_key
        self.full_key = full_key
        return full_key

    def encrypt_message(self, msg):
        encrypted_message = ""
        key = self.full_key
        for c in msg:
            encrypted_message += chr(ord(c) + key)
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        decrypted_message = ""
        key = self.full_key
        for c in encrypted_message:
            decrypted_message += chr(ord(c) - key)
        return decrypted_message

    def all_of_public_keys(self):
        self.private_key = int(input('Введите ваш персональный ключ (от 1 до 999):'))
        self.client_public_key = int(input('Введите ваш публичный ключ (от 1 до 999):'))
        self.server_public_key = random.randint(1,200) # Генерация публичного ключа клиента