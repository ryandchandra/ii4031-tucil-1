from VigenereLib import *

def ExtendedEncrypt(plaintext,key):
    # Extended Vigenere Encrypt plaintext with key
    # Input : plaintext, key
    # Output : ciphertext
    
    # Prepare the key
    extended_key = GenerateVigenereKey(key,len(plaintext))

    # Encrypt
    result = ""
    for i in range(len(plaintext)):
        encrypted_char_num = (ord(plaintext[i]) + ord(extended_key[i]))%256
        result += chr(encrypted_char_num)        
    return result
    
def ExtendedDecrypt(ciphertext,key):
    # Extended Vigenere Decrypt ciphertext with key
    # Input : ciphertext, key
    # Output : plaintext
    
    # Prepare the key
    extended_key = GenerateVigenereKey(key,len(ciphertext))
    
    # Decrypt
    result = ""
    for i in range(len(ciphertext)):
        decrypted_char_num = (ord(ciphertext[i]) - ord(extended_key[i]))%256
        result += chr(decrypted_char_num)
        
    return result