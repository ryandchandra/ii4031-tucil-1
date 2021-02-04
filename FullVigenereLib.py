from CommonLib import *
from VigenereLib import *

def MatrixFullVigenere(key):
    arr_key = []
    for i in range(len(key)):
        num_key = CharToNum(key[i])
        arr_key.append(i)

    abjadUrut = []
    for i in range(26):
        abjadUrut.append(i)

    X = 0
    tempAbjad = abjadUrut.copy()
    matVig = []
    for i in range(26):
        rowVig = []
        for j in range(25):
            X = X + arr_key[j%len(arr_key)]
            X = X%len(tempAbjad)
            rowVig.append(tempAbjad[X])
            tempAbjad.pop(X)
            X = tempAbjad[0]
        rowVig.append(tempAbjad[0])
        tempAbjad.pop(0)
        tempAbjad = rowVig.copy()
        matVig.append(rowVig)
    return matVig

def FullVigenereEncrypt(plaintext,key):
    # Vigenere Encrypt plaintext with key
    # Input : plaintext, key
    # Output : ciphertext
    
    # Prepare the plaintext, key, and matrix
    prepared_plaintext = PrepareText(plaintext)
    extended_key = GenerateVigenereKey(key,len(prepared_plaintext))
    matrixVig = MatrixFullVigenere(key)

    # Encrypt
    result = ""
    for i in range(len(prepared_plaintext)):
        num_plaintext = CharToNum(prepared_plaintext[i])
        num_extended_key = CharToNum(extended_key[i])
        encrypted_char_num = matrixVig[num_extended_key][num_plaintext]
        result += NumToChar(encrypted_char_num)
        if (i%5==4): # Set ciphertext to blocks of 5 characters
            result += " "
    return result.upper()
    
def FullVigenereDecrypt(ciphertext,key):
    # Vigenere Decrypt ciphertext with key
    # Input : ciphertext, key
    # Output : plaintext
    
    # Prepare the ciphertext, key, and matrix
    prepared_ciphertext = PrepareText(ciphertext)
    extended_key = GenerateVigenereKey(key,len(prepared_ciphertext))
    matrixVig = MatrixFullVigenere(key)
    
    # Decrypt
    result = ""
    for i in range(len(prepared_ciphertext)):
        num_ciphertext = CharToNum(prepared_ciphertext[i])
        num_extended_key = CharToNum(extended_key[i])
        idx = matrixVig[num_extended_key].index(num_ciphertext)
        decrypted_char_num = idx
        result += NumToChar(decrypted_char_num)
        
    return result 