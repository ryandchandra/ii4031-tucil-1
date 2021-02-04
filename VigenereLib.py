from CommonLib import *

def GenerateVigenereKey(key,length):
    # Generate key for Vigenere Cipher according to desired length
    # Input : key, desired length
    # Output : Vigenere Cipher key with desired length
    if (len(key)>=length): # key is longer than desired length -> take only the front characters
        return key[0:length]
    else: # key is shorter, duplicate the key
        multiple = length//len(key)
        remainder = length%len(key)
        
        return key*multiple + key[0:remainder]

def VigenereEncrypt(plaintext,key):
    # Vigenere Encrypt plaintext with key
    # Input : plaintext, key
    # Output : ciphertext
    
    # Prepare the plaintext and key
    prepared_plaintext = PrepareText(plaintext)
    extended_key = GenerateVigenereKey(PrepareText(key),len(prepared_plaintext))

    # Encrypt
    result = ""
    for i in range(len(prepared_plaintext)):
        encrypted_char_num = (CharToNum(prepared_plaintext[i]) + CharToNum(extended_key[i]))%26
        result += NumToChar(encrypted_char_num)
        if (i%5==4): # Set ciphertext to blocks of 5 characters
            result += " "
        
    return result.upper()
    
def VigenereDecrypt(ciphertext,key):
    # Vigenere Decrypt ciphertext with key
    # Input : ciphertext, key
    # Output : plaintext
    
    # Prepare the ciphertext and key
    prepared_ciphertext = PrepareText(ciphertext)
    extended_key = GenerateVigenereKey(PrepareText(key),len(prepared_ciphertext))
    
    # Decrypt
    result = ""
    for i in range(len(prepared_ciphertext)):
        decrypted_char_num = (CharToNum(prepared_ciphertext[i]) - CharToNum(extended_key[i]))%26
        result += NumToChar(decrypted_char_num)
        
    return result
    
def GenerateVigenereAutoKey(plaintext,key):
    # Generate auto key for Vigenere Cipher according to plaintext
    # Input : plaintext, key
    # Output : Auto Key Vigenere
    if (len(key)>=len(plaintext)): # key is longer than desired length -> take only the front key characters
        return key[0:len(plaintext)]
    else: # key is shorter, extend with plaintext
        return key + plaintext[0:len(plaintext)-len(key)]
    
def AutoKeyVigenereEncrypt(plaintext,key):
    # Auto Key Vigenere Encrypt plaintext with key
    # Input : plaintext, key
    # Output : ciphertext
    
    # Prepare the plaintext and key
    prepared_plaintext = PrepareText(plaintext)
    extended_key = GenerateVigenereAutoKey(prepared_plaintext,PrepareText(key))
    
    # Encrypt
    result = ""
    for i in range(len(prepared_plaintext)):
        encrypted_char_num = (CharToNum(prepared_plaintext[i]) + CharToNum(extended_key[i]))%26
        result += NumToChar(encrypted_char_num)
        if (i%5==4): # Set ciphertext to blocks of 5 characters
            result += " "
        
    return result.upper()
    
def AutoKeyVigenereDecrypt(ciphertext,key):
    # Auto Key Vigenere Decrypt ciphertext with key
    # Input : ciphertext, key
    # Output : plaintext
    
    # Prepare the ciphertext
    prepared_ciphertext = PrepareText(ciphertext)
    key = PrepareText(key)
    
    # Decrypt
    result = ""
    # For the first key-length characters, decrypt with the key
    for i in range(len(key)):
        decrypted_char_num = (CharToNum(prepared_ciphertext[i]) - CharToNum(key[i]))%26
        result += NumToChar(decrypted_char_num)

    # For the next characters, decrypt starting from the first decrypted character
    for i in range(len(key),len(prepared_ciphertext)):
        decrypted_char_num = (CharToNum(prepared_ciphertext[i]) - CharToNum(result[i-len(key)]))%26
        result += NumToChar(decrypted_char_num)
        
    return result