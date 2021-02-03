def CharToNum(char):
    # Changes a character to its nominal value, relative to 'a'
    # Ex : 'a' -> 0, 'b' -> 1, 'c' -> 2, ..., 'z' -> 25
    # Expected input : lowercase character char
    # Output : number(0-25)
    return ord(char.lower()) - ord('a')

def NumToChar(num):
    # Changes a number to the corresponding character
    # Ex : 0 -> 'a', 1 -> 'b', 2 -> 'c', ..., 25 -> 'z'
    # Expected input : number(0-25)
    # Output : lowercase character
    return chr(ord('a')+num%26)

def PrepareText(text):
    # Preparing a text before encrypt/decrypt
    # delete all non-alphabet characters (space,marks,number,etc.) and turning the alphabets to lowercase characters
    # Expected input : mixed string
    # Output : alphabet string
    result = ""
    for char in text:
        if (char.isalpha()):
            result += char.lower()
            
    return result