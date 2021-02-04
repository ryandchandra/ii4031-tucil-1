from CommonLib import *

def AffineEncrypt(plaintext,multiple,offset):
    # Affine Encrypt
    # Input : plaintext, multiple, offset
    # Output : ciphertext

    # Prepare the plaintext
    prepared_plaintext = PrepareText(plaintext)
    
    # Encrypt
    result = ""
    for i in range(len(prepared_plaintext)):
        encrypted_char_num = (multiple*CharToNum(prepared_plaintext[i]) + offset)%26
        result += NumToChar(encrypted_char_num)
        if (i%5==4): # Set ciphertext to blocks of 5 characters
            result += " "
        
    return result.upper()
    
def AffineDecrypt(ciphertext,multiple,offset):
    # Affine Decrypt
    # Input : ciphertext, multiple, offset
    # Output : plaintext

    # Prepare the ciphertext
    prepared_ciphertext = PrepareText(ciphertext)
    
    # Find modulo inverse
    for i in range(1,26):
        if ((multiple*i)%26==1):
            inverse_modulo = i
            break    
    
    # Decrypt
    result = ""
    for i in range(len(prepared_ciphertext)):
        encrypted_char_num = inverse_modulo*(CharToNum(prepared_ciphertext[i]) - offset)%26
        result += NumToChar(encrypted_char_num)
        
    return result