from network.config import secrets, struct

class Prime:
    """Генерация простого числа с использованием теста Миллера-Рабина"""
    def __init__(self):
        self.k: int
        self.bits: int

    def is_prime(self): 
        """Тест Миллера-Рабина"""
        if self.prime <= 1:
            return False
        if self.prime <= 3:
            return True
        if self.prime % 2 == 0:
            return False
        
        # представление n-1 в виде 2^s * d
        r, s = 0, self.prime - 1
        while s % 2 == 0:
            r += 1
            s //= 2
        
        # k раундов теста Миллера-Рабина
        for _ in range(self.k):
            a = secrets.randbelow(self.prime - 3) + 2
            x = pow(a, s, self.prime)
            if x == 1 or x == self.prime - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, self.prime)
                if x == self.prime - 1:
                    break
            else:
                return False
        return True
    
    def generate_large_prime(self):
        """Генерация большого простого числа"""
        while True:
            self.prime = secrets.randbits(self.bits//2)
            if self.is_prime():
                return self.prime

class RSAcrypto(Prime):
    def __init__(self, k = 40, bits = 2048, e = 65539):
        self.k = k
        self.e = e
        self.bits = bits
        self.oaep = OAEP()

    # Шифрование сообщения с паддингом OAEP
    def encrypt(self, message, public_key):
        e, n = public_key
        n_len = (n.bit_length() + 7) // 8
        padded_message = self.oaep.pad(message, n_len)
        message_int = int.from_bytes(padded_message, 'big')
        encrypted_int = pow(message_int, e, n)
        return encrypted_int

    # Расшифрование сообщения с распаддингом OAEP
    def decrypt(self, encrypted_message, private_key):
        d, n = private_key
        decrypted_int = pow(encrypted_message, d, n)
        n_len = (n.bit_length() + 7) // 8
        decrypted_message = decrypted_int.to_bytes(n_len, 'big')
        message = self.oaep.unpad(decrypted_message)
        return message

    def gen_keys(self):
        """Генерация ключей RSA"""
        p = self.generate_large_prime()
        q = self.generate_large_prime()
        n = p * q
        phi = (p - 1) * (q - 1)
        # Вычисление d, обратного e по модулю phi
        d = pow(self.e, -1, phi)
        
        return (self.e, n), (d, n)

class Bits:
    @staticmethod
    def right_rotate(value, shift):
        """Вспомогательная функция для битовых операций"""
        return (value >> shift) | (value << (32 - shift)) & 0xFFFFFFFF
    
    @staticmethod
    def transform(h, k, w):
        """Вспомогательная функция для битовых операций"""
        for i in range(64):
            s1 = HASH.right_rotate(h[4], 6) ^ Bits.right_rotate(h[4], 11) ^ Bits.right_rotate(h[4], 25)
            ch = (h[4] & h[5]) ^ ((~h[4]) & h[6])
            temp1 = (h[7] + s1 + ch + k[i] + w[i]) & 0xFFFFFFFF
            s0 = Bits.right_rotate(h[0], 2) ^ Bits.right_rotate(h[0], 13) ^ Bits.right_rotate(h[0], 22)
            maj = (h[0] & h[1]) ^ (h[0] & h[2]) ^ (h[1] & h[2])
            temp2 = (s0 + maj) & 0xFFFFFFFF

            h = [
                (temp1 + temp2) & 0xFFFFFFFF,
                h[0],
                h[1],
                h[2],
                (h[3] + temp1) & 0xFFFFFFFF,
                h[4],
                h[5],
                h[6]
            ]

        return h    

class HASH(Bits):
    def  __init__(self):
        """Инициализация констант"""
        self.h = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]
        self.k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]
    
    @staticmethod
    def prepare(data):
        """Предобработка"""
        data = bytearray(data)
        original_length = len(data) * 8
        data.append(0x80)
        while (len(data) * 8) % 512 != 448:
            data.append(0)
        data += original_length.to_bytes(8, byteorder='big')
        return data

    def sha256(self, data):
        """Основная функция SHA-256"""
        data = self.prepare(data)

        """Обработка в 512-битных (64-байтных) блоках"""
        for i in range(0, len(data), 64):
            block = data[i:i+64]
            w = list(struct.unpack('>16L', block)) + [0] * 48

            for j in range(16, 64):
                s0 = self.right_rotate(w[j-15], 7) ^ self.right_rotate(w[j-15], 18) ^ (w[j-15] >> 3)
                s1 = self.right_rotate(w[j-2], 17) ^ self.right_rotate(w[j-2], 19) ^ (w[j-2] >> 10)
                w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFF

            h = self.transform(self.h, self.k, w)
            
        """Итоговое значение"""
        return b''.join(struct.pack('>I', i) for i in h)

class OAEP():
    def  __init__(self):
        self.hash = HASH()
    # Генерация псевдослучайной последовательности
    def mgf1(self, seed, length):
        counter = 0
        output = b""
        while len(output) < length:
            C = counter.to_bytes(4, byteorder='big')
            output += self.hash.sha256(seed + C)
            counter += 1
        return output[:length]

    # Паддинг OAEP
    def pad(self, message, n_len):
        message = message.encode()
        h_len = self.hash.sha256(b'').__len__()
        ps_len = n_len - len(message) - 2 * h_len - 2
        if ps_len < 0:
            raise ValueError("Message too long.")
        
        l_hash = self.hash.sha256(b'')
        ps = b'\x00' * ps_len
        db = l_hash + ps + b'\x01' + message
        seed = secrets.token_bytes(h_len)
        db_mask = self.mgf1(seed, len(db))
        masked_db = bytes(a ^ b for a, b in zip(db, db_mask))
        seed_mask = self.mgf1(masked_db, h_len)
        masked_seed = bytes(a ^ b for a, b in zip(seed, seed_mask))
        return b'\x00' + masked_seed + masked_db

    def unpad(self, padded_message):
        h_len = self.hash.sha256(b'').__len__()
        y, masked_seed, masked_db = padded_message[0], padded_message[1:h_len+1], padded_message[h_len+1:]
        seed_mask = self.mgf1(masked_db, h_len)
        seed = bytes(a ^ b for a, b in zip(masked_seed, seed_mask))
        db_mask = self.mgf1(seed, len(masked_db))
        db = bytes(a ^ b for a, b in zip(masked_db, db_mask))
        l_hash, rest = db[:h_len], db[h_len:]
        if l_hash != self.hash.sha256(b''):
            raise ValueError("Decryption error.")
        rest = rest.lstrip(b'\x00')
        if rest[0] != 1:
            raise ValueError("Decryption error.")
        return rest[1:].decode()


# Демонстрация работы алгоритма
def main(message = "Hello, RSA!"):

    rsa = RSAcrypto()
    public_key, private_key = rsa.gen_keys()  # Генерация ключей RSA
    
    encrypted_message = rsa.encrypt(message, public_key)   # Шифрование
    decrypted_message = rsa.decrypt(encrypted_message, private_key)  # Расшифрование

    print("Original message:", message)
    print("Encrypted message:", encrypted_message)
    print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
    # from config import secrets, struct
    main()