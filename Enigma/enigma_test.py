import random

class Enigma:
    def __init__(self, rotor_count=3, rotor_config='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        self.rotors = []
        for i in range(rotor_count):
            rotor = list(rotor_config)
            random.shuffle(rotor)
            self.rotors.append(rotor)
        
    def encrypt(self, message, rotor_config='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        encrypted_message = ''
        for char in message:
            encrypted_char = char
            for rotor in self.rotors:
                encrypted_char = rotor[ord(encrypted_char) - ord(rotor_config[0])]
            encrypted_message += encrypted_char
        return encrypted_message
    
    def decrypt(self, encrypted_message, rotor_config='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        message = ''
        for char in encrypted_message:
            decrypted_char = char
            for rotor in self.rotors:
                decrypted_char = rotor_config[rotor.index(decrypted_char)]
            message += decrypted_char
        return message

enigma = Enigma()

# Encrypt a message
message = input("Enter a message to encrypt: ")
encrypted_message = enigma.encrypt(message)
print("Encrypted message:", encrypted_message)

# Decrypt an encrypted message
decrypted_message = enigma.decrypt(input("Enter a message to decrypt: "))
print("Decrypted message:", decrypted_message)