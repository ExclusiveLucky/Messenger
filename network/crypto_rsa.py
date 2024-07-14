# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_OAEP
# from Crypto.Util.Padding import pad, unpad
# from Crypto.Random import get_random_bytes


# def gen_keys(key_size=2048):
#     """
#     Генерирует пару ключей RSA с заданным размером ключа.
    
#     :param key_size: Размер ключа в битах
#     :return: Пара ключей (приватный и публичный)
#     """
#     key = RSA.generate(key_size)
#     private_key = key.export_key()
#     public_key = key.publickey().export_key()
#     return private_key, public_key

# def encrypt(message, public_key):
#     """
#     Шифрует сообщение с использованием публичного ключа RSA.
    
#     :param message: Сообщение для шифрования
#     :param public_key: Публичный ключ для шифрования
#     :return: Зашифрованное сообщение
#     """
#     recipient_key = RSA.import_key(public_key)
#     cipher_rsa = PKCS1_OAEP.new(recipient_key)
#     encrypted_message = cipher_rsa.encrypt(message)
#     return encrypted_message

# def decrypt(encrypted_message, private_key):
#     """
#     Расшифровывает сообщение с использованием приватного ключа RSA.
    
#     :param encrypted_message: Зашифрованное сообщение
#     :param private_key: Приватный ключ для расшифрования
#     :return: Расшифрованное сообщение
#     """
#     private_key = RSA.import_key(private_key)
#     cipher_rsa = PKCS1_OAEP.new(private_key)
#     decrypted_message = cipher_rsa.decrypt(encrypted_message)
#     return decrypted_message

# if __name__ == "__main__":
#     # Генерация ключей
#     private_key, public_key = gen_keys()
    
#     # Пример сообщения для шифрования
#     original_message = b'RSA'
    
#     # Шифрование сообщения
#     encrypted_message = encrypt(original_message, public_key)
#     print(f'Зашифрованное сообщение: {encrypted_message}')
    
#     # Расшифрование сообщения
#     decrypted_message = decrypt(encrypted_message, private_key)
#     print(f'Расшифрованное сообщение: {decrypted_message.decode()}')
