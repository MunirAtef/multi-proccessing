
import numpy as np
import sympy as sp
from abc import abstractmethod

class EncryptionMethod:
    @staticmethod
    @abstractmethod
    def encrypt(text: str, key: str): pass

    @staticmethod
    @abstractmethod
    def decrypt(text: str, key: str): pass

class CaesarCipher(EncryptionMethod):
    @staticmethod
    def caesar_cipher(message: str, shift: int, is_encrypt: bool):
        result = ""
        letters = "abcdefghijklmnopqrstuvwxyz"

        for char in message.lower():
            if char.isalpha():
                idx = letters.index(char)
                idx = idx + shift if is_encrypt else idx - shift
                result += letters[idx % 26]
            else:
                result += char

        return result

    @staticmethod
    def encrypt(text: str, key: str):
        return CaesarCipher.caesar_cipher(text, int(key), is_encrypt=True)

    @staticmethod
    def decrypt(text: str, key: str):
        return CaesarCipher.caesar_cipher(text, int(key), is_encrypt=False)

class MonoAlphabetic(EncryptionMethod):
    @staticmethod
    def prepare_key(key: str):
        alphabet = list("abcdefghijklmnopqrstuvwxyz")
        for char in key.lower():
            alphabet.remove(char)
        print(key.lower() + "".join(alphabet))
        return key.lower() + "".join(alphabet)

    @staticmethod
    def encrypt(message: str, key: str):
        key = MonoAlphabetic.prepare_key(key)
        result = ""
        for char in message.lower():
            if char.isalpha():
                result += key[ord(char) - ord('a')]
            else:
                result += char
        return result

    @staticmethod
    def decrypt(ciphertext: str, key: str):
        key = MonoAlphabetic.prepare_key(key)
        result = ""
        for char in ciphertext.lower():
            if char.isalpha():
                idx = key.find(char)
                result += chr(ord('a') + idx)
            else:
                result += char
        return result

class RailFence(EncryptionMethod):
    @staticmethod
    def encrypt(text: str, key: str) -> str:
        key = int(key)
        rail: list[str] = ["" for _ in range(key)]
        dir_down = False
        row = 0

        for i in range(len(text)):
            if row == 0 or row == key - 1:
                dir_down = not dir_down

            rail[row] += text[i]

            if dir_down:
                row += 1
            else:
                row -= 1

        return "".join(rail)

    @staticmethod
    def decrypt(cipher: str, key: str) -> str:
        key = int(key)
        rail: list[list[str]] = [['\n' for _ in range(len(cipher))] for _ in range(key)]

        dir_down = False
        row, col = 0, 0

        for i in range(len(cipher)):
            if row == 0 or row == key - 1:
                dir_down = not dir_down

            rail[row][col] = '*'
            col += 1

            if dir_down:
                row += 1
            else:
                row -= 1

        index = 0
        for i in range(key):
            for j in range(len(cipher)):
                if rail[i][j] == '*':
                    rail[i][j] = cipher[index]
                    index += 1

        result = ""
        dir_down = False
        row, col = 0, 0
        for i in range(len(cipher)):
            if row == 0 or row == key - 1:
                dir_down = not dir_down

            if rail[row][col] != '*':
                result += rail[row][col]
                col += 1

            if dir_down:
                row += 1
            else:
                row -= 1

        return result

class Hill(EncryptionMethod):
    @staticmethod
    def encrypt(message, key):
        key_matrix = np.array([[int(char) for char in row] for row in key.split()])
        key_det = int(np.linalg.det(key_matrix)) % 26  # Ensure invertible key
        if key_det == 0:
            raise ValueError("Key is not invertible.")

        ciphertext = ""
        for i in range(0, len(message), len(key_matrix)):
            block = np.array([ord(char) - ord('A') for char in message[i:i + len(key_matrix)]])
            encrypted_block = np.dot(block, key_matrix) % 26
            ciphertext += "".join(chr(x + ord('A')) for x in encrypted_block)

        return ciphertext

    @staticmethod
    def decrypt(ciphertext, key):
        """Decrypts a ciphertext using the Hill cipher."""
        key_matrix = np.array([[int(char) for char in row] for row in key.split()])
        key_inv = np.linalg.inv(key_matrix) % 26  # Modular inverse for decryption

        plaintext = ""
        for i in range(0, len(ciphertext), len(key_matrix)):
            block = np.array([ord(char) - ord('A') for char in ciphertext[i:i + len(key_matrix)]])
            decrypted_block = np.dot(block, key_inv) % 26
            plaintext += "".join(chr(x + ord('A')) for x in decrypted_block)

        return plaintext

    @staticmethod
    def encrypt3(plaintext: str, key: str):
        plaintext = plaintext.replace(' ', '').upper()
        n = len(key)
        plaintext += 'X' * (len(plaintext) % n)
        ciphertext = ''

        for i in range(0, len(plaintext), n):
            chunk = plaintext[i:i + n]
            chunk_indices = [ord(char) - ord('A') for char in chunk]
            transformed_chunk = np.dot(key, chunk_indices) % 26
            ciphertext += ''.join(chr(index + ord('A')) for index in transformed_chunk)

        return ciphertext

    @staticmethod
    def mod_inverse(a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    @staticmethod
    def decrypt3(ciphertext: str, key: str):
        det = int(np.round(np.linalg.det(key)))  # Calculate the determinant of the key matrix
        print(det)
        # Ensure the determinant is relatively prime to 26
        if np.gcd(det, 26) != 1:
            print("Key is not invertible. Decryption not possible!")
            return

        n = len(key)
        inverse_det = Hill.mod_inverse(det, 26)

        adjugate = sp.Matrix(key).adjugate()
        adjugate = np.array(adjugate.tolist(), dtype=int)

        # Perform matrix multiplication: det * adjugate
        inverse_key = (inverse_det * adjugate) % 26

        plaintext = ''
        for i in range(0, len(ciphertext), n):
            chunk = ciphertext[i:i+n]
            chunk_indices = [ord(char) - ord('A') for char in chunk]
            transformed_chunk = np.dot(inverse_key, chunk_indices) % 26
            plaintext += ''.join(chr(index + ord('A')) for index in transformed_chunk)

        return plaintext

class OnTimePad(EncryptionMethod):
    @staticmethod
    def vernam(plain, key, flag):
        result = ""
        for i in range(len(plain)):
            char_msg = ord(plain[i].lower()) - ord('a')
            char_key = ord(key[i % len(key)].lower()) - ord('a')

            if flag:
                result += chr((char_msg ^ char_key) % 26 + ord('a'))
            else:
                result += chr((char_msg ^ char_key) % 26 + ord('a'))

        return result

    @staticmethod
    def encrypt(message: str, pad: str):
        return OnTimePad.vernam(message, pad, True)

    @staticmethod
    def decrypt(encrypted_message: str, pad: str):
        return OnTimePad.vernam(encrypted_message, pad, False)

class PlayFair(EncryptionMethod):
    @staticmethod
    def prepare_input(text):
        text = text.replace(" ", "").upper()
        text = text.replace("J", "I")
        return text

    @staticmethod
    def generate_key(key):
        key = PlayFair.prepare_input(key)

        playfair_matrix = [['' for _ in range(5)] for _ in range(5)]
        key_set = set()

        i, j = 0, 0
        for letter in key:
            if letter not in key_set:
                playfair_matrix[i][j] = letter
                key_set.add(letter)
                j += 1
                if j == 5:
                    i += 1
                    j = 0

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for letter in alphabet:
            if letter != "J" and letter not in key_set:
                playfair_matrix[i][j] = letter
                key_set.add(letter)
                j += 1
                if j == 5:
                    i += 1
                    j = 0

        return playfair_matrix

    @staticmethod
    def find_char_position(matrix, char):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == char:
                    return i, j

    @staticmethod
    def encrypt(plaintext: str, key: str):
        matrix = PlayFair.generate_key(key)
        plaintext = PlayFair.prepare_input(plaintext)
        cipher_text = ""

        i = 0
        while i < len(plaintext):
            if i == len(plaintext) - 1:
                plaintext += "X"
            elif plaintext[i] == plaintext[i + 1]:
                plaintext = plaintext[:i + 1] + "X" + plaintext[i + 1:]
            i += 2

        for i in range(0, len(plaintext), 2):
            char1, char2 = plaintext[i], plaintext[i + 1]
            row1, col1 = PlayFair.find_char_position(matrix, char1)
            row2, col2 = PlayFair.find_char_position(matrix, char2)

            if row1 == row2:
                cipher_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                cipher_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                cipher_text += matrix[row1][col2] + matrix[row2][col1]

        return cipher_text


    @staticmethod
    def decrypt(ciphertext: str, key: str):
        matrix = PlayFair.generate_key(key)
        ciphertext = PlayFair.prepare_input(ciphertext)
        plaintext = ""

        for i in range(0, len(ciphertext), 2):
            char1, char2 = ciphertext[i], ciphertext[i + 1]
            row1, col1 = PlayFair.find_char_position(matrix, char1)
            row2, col2 = PlayFair.find_char_position(matrix, char2)

            if row1 == row2:
                plaintext += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                plaintext += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                plaintext += matrix[row1][col2] + matrix[row2][col1]

        # Clean up any extra 'X' added during encryption for padding
        plaintext = plaintext.replace("X", "")

        return plaintext

