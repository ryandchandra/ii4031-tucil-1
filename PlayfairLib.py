from CommonLib import *

def GeneratePlayfairKeyMatrix(key):
    # Create Playfair Key Matrix
    # Input : key(string)
    # Output : Playfair Key Matrix from key
    
    result = ""
    
    # delete non alphabet characters and 'j'
    for c in key.lower():
        if ((c not in result) and (c!='j') and (c.isalpha())):
            result+=c
    
    # extend the key with the other characters not in string according to alphabet order (except 'j')
    for c in range(ord('a'),ord('z')+1):
        if ((chr(c) not in result) and (chr(c)!='j')):
            result+=chr(c)
            
    # create the matrix
    result_matr = []
    for i in range(5):
        new_array = []
        for j in range(5):
            new_array.append(result[i*5+j])
        result_matr.append(new_array)
        
    return result_matr
    
def PlayfairPlaintextBigram(plaintext):
    # Create bigram from plaintext
    # Input : plaintext
    # Output : array of playfair bigrams
    
    # Prepare the plaintext
    prepared_plaintext = PrepareText(plaintext)

    # Replace j with i
    replaced_plaintext = ""
    for c in prepared_plaintext:
        if (c=='j'):
            replaced_plaintext += 'i'
        else:
            replaced_plaintext += c
    
    # Create the bigram array
    bigram_array = []
    i = 0
    while (i<len(replaced_plaintext)):
        if (i==(len(replaced_plaintext)-1)): # for the last character with no pair, add 'x'
            bigram = replaced_plaintext[i] + 'x'
            i = i + 1
        elif (replaced_plaintext[i]==replaced_plaintext[i+1]): # for bigram with same characters, set 'x' as the first character pair
            bigram = replaced_plaintext[i] + 'x'
            i = i + 1
        else: # create bigram with the next character
            bigram = replaced_plaintext[i] + replaced_plaintext[i+1]
            i = i + 2
        
        bigram_array.append(bigram)
        
    return bigram_array
    
def PlayfairCiphertextBigram(ciphertext):
    # Create bigram from ciphertext
    # Input : ciphertext
    # Output : array of playfair bigrams
    
    # Prepare the ciphertext
    prepared_ciphertext = PrepareText(ciphertext)
    
    # Create the bigram array
    bigram_array = []
    i = 0
    while (i<len(prepared_ciphertext)):
        # pair every two characters
        # for playfair ciphertext length, it is always expected to have even length
        bigram = prepared_ciphertext[i] + prepared_ciphertext[i+1]
        bigram_array.append(bigram)
        i = i + 2
        
    return bigram_array
    
def FindPlayfairIndex(bigram,key_matr):
    # Find bigram index position in key matrix
    # Input : bigram to be searched, key matrix
    # Output : (x,y) index of bigram characters
    found0 = False
    found1 = False
    for i in range(5):
        for j in range(5):
            if (key_matr[i][j]==bigram[0]):
                x0 = j
                y0 = i
                found0 = True
            if (key_matr[i][j]==bigram[1]):
                x1 = j
                y1 = i
                found1 = True
            if ((found0) and (found1)):
                break
        if ((found0) and (found1)):
            break
            
    return x0,y0,x1,y1
    
def PlayfairEncrypt(plaintext,key):
    # Playfair Encrypt plaintext with key
    # Input : plaintext, key
    # Output : ciphertext
    
    # Prepare the bigram and key matrix
    plaintext_bigram = PlayfairPlaintextBigram(plaintext)
    playfair_key = GeneratePlayfairKeyMatrix(key)
    
    # Encrypt
    encrypted_text = ""
    for bigram in plaintext_bigram:
        x0,y0,x1,y1 = FindPlayfairIndex(bigram,playfair_key)
        if (x0==x1): # same row -> take the next characters
            encrypted_bigram = playfair_key[(y0+1)%5][x0] + playfair_key[(y1+1)%5][x1]
        elif (y0==y1): # same column -> take the next characters
            encrypted_bigram = playfair_key[y0][(x0+1)%5] + playfair_key[y1][(x1+1)%5]
        else: # different row and column -> take the rectangle angle characters
            encrypted_bigram = playfair_key[y0][x1] + playfair_key[y1][x0]
        
        encrypted_text += encrypted_bigram
    
    # Split into blocks of 5 characters
    result = ""
    for i in range(len(encrypted_text)):
        result += encrypted_text[i].upper()
        if (i%5==4):
            result += ' '
            
    return result
    
def PlayfairDecrypt(ciphertext,key):
    # Playfair Decrypt ciphertext with key
    # Input : ciphertext, key
    # Output : plaintext
    
    # Prepare the bigram and key matrix
    ciphertext_bigram = PlayfairCiphertextBigram(ciphertext)
    playfair_key = GeneratePlayfairKeyMatrix(key)
    
    # Decrypt    
    decrypted_text = ""
    for bigram in ciphertext_bigram:
        x0,y0,x1,y1 = FindPlayfairIndex(bigram,playfair_key)
        if (x0==x1): # same row -> take the previous character
            decrypted_bigram = playfair_key[(y0-1)%5][x0] + playfair_key[(y1-1)%5][x1]
        elif (y0==y1): # same column -> take the previous character
            decrypted_bigram = playfair_key[y0][(x0-1)%5] + playfair_key[y1][(x1-1)%5]
        else: # different row and column -> take the rectangle angle characters
            decrypted_bigram = playfair_key[y0][x1] + playfair_key[y1][x0]
        
        decrypted_text += decrypted_bigram
    
    # Delete the inserted 'x'
    result = ""
    for i in range(len(decrypted_text)):
        if (decrypted_text[i]=='x'):
            if (i==(len(decrypted_text)-1)): # skip the last 'x' character
                pass
            elif (decrypted_text[i-1]==decrypted_text[i+1]): # skip the 'x' character between two same characters
                pass
            else:
                result += decrypted_text[i]
        else:
            result += decrypted_text[i]
            
    return result