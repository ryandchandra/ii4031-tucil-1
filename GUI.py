import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as fd
import random
import math
import pickle

from Components import *

from CommonLib import *
from VigenereLib import *
from PlayfairLib import *
from AffineLib import *
from FullVigenereLib import *
from ExtendedLib import *

class GUI:
    def __init__(self,parent):
        #--- init ---#
        self.parent = parent
        parent.title("Kriptografi")
        self.mode = "Vigenere"
        
        #--- define grid ---#
        parent.columnconfigure([0,1,2,3],weight=1)
        parent.rowconfigure([0,1,2],weight=1,minsize=100)
        
        #--- plaintext ---#
        self.plaintext = TextFrame(
            title="Plaintext",
            width=50,
            height=5
        )
        self.plaintext.frame.grid(row=0,column=0,columnspan=3)
        
        #--- encrypt button ---#
        self.encrypt_button = tk.Button(text="Encrypt",command=self.Encrypt)
        self.encrypt_button.grid(row=1,column=0,padx=10,pady=10)

        #--- keyframe ---#
        self.keyframe = KeyFrame(title="Key",width=34)
        self.keyframe.button.bind("<Button-1>",self.RandomizeKey)
        self.keyframe.frame.grid(row=1,column=1)
        
        #--- affinekeyframe ---#
        self.affinekeyframe = AffineKeyFrame(width=6)
        # is created only but not packed

        #--- decrypt button ---#
        self.decrypt_button = tk.Button(text="Decrypt",command=self.Decrypt)
        self.decrypt_button.grid(row=1,column=2,padx=10,pady=10)
        
        #--- ciphertext ---#
        self.ciphertext = TextFrame(
            title="Ciphertext",
            width=50,
            height=5
        )
        self.ciphertext.frame.grid(row=2,column=0,columnspan=3)
        
        #--- cipher method button list ---#
        cipher_method_list = ["Vigenere","Full Vigenere","Auto-Key Vigenere","Extended Vigenere","Playfair","Affine"]
        self.cipher_method_frame = ButtonListFrame(
            title = "Method : Vigenere",
            labels = cipher_method_list,
            width = 25
        )
        for button in self.cipher_method_frame.button_list:
            button.bind("<Button-1>",lambda event,mode=button["text"]: self.ChangeMode(event,mode))
        self.cipher_method_frame.frame.grid(row=0,column=3,rowspan=3,sticky="ns")
        
        #--- file frame ---#
        file_method_list = ["Open Plaintext TextFile","Open Ciphertext TextFile","Save Plaintext to TextFile","Save Ciphertext to TextFile","Binary File"]
        self.file_frame = ButtonListFrame(
            title = "File",
            labels = file_method_list,
            width = 25
        )
        self.file_frame.button_list[0].bind("<Button-1>",lambda event,text="plaintext": self.OpenFileText(event,text))
        self.file_frame.button_list[1].bind("<Button-1>",lambda event,text="ciphertext": self.OpenFileText(event,text))
        self.file_frame.button_list[2].bind("<Button-1>",lambda event,text="plaintext": self.SaveFileText(event,text))
        self.file_frame.button_list[3].bind("<Button-1>",lambda event,text="ciphertext": self.SaveFileText(event,text))
        self.file_frame.button_list[4].bind("<Button-1>",self.BinaryFileWindow)
        self.file_frame.frame.grid(row=2,column=3)
        
    def ChangeMode(self,event,mode):
        # Event handler when button in cipher button list is pressed
        # Change cipher mode and the text
        if (mode=="Affine" and self.mode!="Affine"): # Change to Affine from not Affine, change the frame
            self.keyframe.frame.grid_forget()
            self.affinekeyframe.frame.grid(row=1,column=1)
        elif (mode!="Affine" and self.mode=="Affine"): # Clicked not Affine from Affine, change the frame
            self.affinekeyframe.frame.grid_forget()
            self.keyframe.frame.grid(row=1,column=1)
        
        self.mode = mode
        self.cipher_method_frame.label["text"] = "Method : " + mode
        
    def RandomizeKey(self,event):
        # Create randomized key according to input length
        
        # Take input length
        length = self.keyframe.random_entry.get()
        
        if (len(length)==0): # No length is inputed
            self.AlertWindow("Please insert randomizer length")
        elif (not length.isnumeric()): # Inputted length is not a number
            self.AlertWindow("Please insert randomizer length in number")
        else:
            # Generate random string
            randomizer = ""
            for i in range(int(length)):
                randomizer += NumToChar(random.randint(0,26))
                
            self.keyframe.entry.delete(0,tk.END)
            self.keyframe.entry.insert(0,randomizer)
        
        
    def Encrypt(self):
        # Event handler when encrypt button is pressed
        # Encrypt plaintext and key
        
        if (self.mode!="Affine"): # for methods other than Affine
            # Take the plaintext and key from the field
            plaintext = self.plaintext.entry.get("1.0",tk.END)[:-1]
            key = self.keyframe.entry.get()
            
            # Check for validity
            if (len(plaintext)==0): # Empty plaintext
                self.AlertWindow("Please insert plaintext")
            elif (len(key)==0): # Empty key
                self.AlertWindow("Please insert key")
            else:
                # Encrypt
                if (self.mode=="Vigenere"): # Vigenere
                    ciphertext = VigenereEncrypt(plaintext,key)
                elif (self.mode=="Full Vigenere"): # Full Vigenere
                    ciphertext = FullVigenereEncrypt(plaintext,key)
                elif (self.mode=="Auto-Key Vigenere"): # Auto Key
                    ciphertext = AutoKeyVigenereEncrypt(plaintext,key)
                elif (self.mode=="Extended Vigenere"): # Extended
                    ciphertext = ExtendedEncrypt(plaintext,key)
                elif (self.mode=="Playfair"): # Playfair
                    ciphertext = PlayfairEncrypt(plaintext,key)
                
                # Insert into ciphertext field
                self.ciphertext.entry.delete("1.0",tk.END)
                self.ciphertext.entry.insert("1.0",ciphertext)
                
        else: # Affine
            # Take the plaintext and parameters from the field
            plaintext = self.plaintext.entry.get("1.0",tk.END)[:-1]
            multiple = self.affinekeyframe.multiple_entry.get()
            offset = self.affinekeyframe.offset_entry.get()
            
            # Check for validity
            if (len(plaintext)==0): # Empty plaintext
                self.AlertWindow("Please insert plaintext")
            elif (not multiple.isnumeric() or not offset.isnumeric()): # Non numeric multiple and offset
                self.AlertWindow("Multiple and offset is a number")
            else:
                # Encrypt
                multiple = int(multiple)
                offset = int(offset)
                if (math.gcd(multiple,26)!=1):
                    self.AlertWindow("Multiple is not relative prime of 26")
                else:
                    # Insert into ciphertext field
                    ciphertext = AffineEncrypt(plaintext,multiple,offset)
                    self.ciphertext.entry.delete("1.0",tk.END)
                    self.ciphertext.entry.insert("1.0",ciphertext)

            
    def Decrypt(self):
        # Event handler when decrypt button is pressed
        # Decrypt ciphertext and key
        
        if (self.mode!="Affine"): # for methods other than Affine
            # Take the ciphertext and key from the field
            key = self.keyframe.entry.get()
            ciphertext = self.ciphertext.entry.get("1.0",tk.END)[:-1]

            # Check for validity
            if (len(ciphertext)==0): # Empty ciphertext
                self.AlertWindow("Please insert ciphertext")
            elif (len(key)==0): # Empty key
                self.AlertWindow("Please insert key")
            else:
                # Decrypt
                if (self.mode=="Vigenere"): # Vigenere
                    plaintext = VigenereDecrypt(ciphertext,key)
                elif (self.mode=="Full Vigenere"): # Full Vigenere
                    plaintext = FullVigenereDecrypt(ciphertext,key)
                elif (self.mode=="Auto-Key Vigenere"): # Auto Key
                    plaintext = AutoKeyVigenereDecrypt(ciphertext,key)
                elif (self.mode=="Extended Vigenere"): # Extended
                    plaintext = ExtendedDecrypt(ciphertext,key)
                elif (self.mode=="Playfair"): # Playfair
                    plaintext = PlayfairDecrypt(ciphertext,key)

                # Insert into plaintext field
                self.plaintext.entry.delete("1.0",tk.END)
                self.plaintext.entry.insert("1.0",plaintext)
                
        else: # Affine
            # Take the plaintext and parameters from the field
            ciphertext = self.ciphertext.entry.get("1.0",tk.END)[:-1]
            multiple = self.affinekeyframe.multiple_entry.get()
            offset = self.affinekeyframe.offset_entry.get()
            
            # Check for validity
            if (len(ciphertext)==0): # Empty plaintext
                self.AlertWindow("Please insert plaintext")
            elif (not multiple.isnumeric() or not offset.isnumeric()): # Non numeric multiple and offset
                self.AlertWindow("Multiple and offset is a number")
            else:
                # Decrypt
                multiple = int(multiple)
                offset = int(offset)
                if (math.gcd(multiple,26)!=1):
                    self.AlertWindow("Multiple and is not relative prime of 26")
                else:
                    # Insert into ciphertext field
                    plaintext = AffineDecrypt(ciphertext,multiple,offset)
                    self.plaintext.entry.delete("1.0",tk.END)
                    self.plaintext.entry.insert("1.0",plaintext)
        
    def OpenFileText(self,event,text):
        # Open file using open file dialog
        
        # Take filename
        filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select " + text + " file",
            filetypes = [("Text files (.txt)","*.txt")]
        )
        
        if (filename!=""): # If filename is chosen
            file = open(filename,"rt")
            content = file.read()
                
            file.close()
            
            if (text=="plaintext"): # For plaintext, insert to plaintext field
                self.plaintext.entry.delete("1.0",tk.END)
                self.plaintext.entry.insert("1.0",content)
            elif (text=="ciphertext"): # For ciphertext, insert to ciphertext field
                self.ciphertext.entry.delete("1.0",tk.END)
                self.ciphertext.entry.insert("1.0",content)
        
        return "break"
        
    def SaveFileText(self,event,text):
        # Save file using save file dialog
        
        # Take filename
        filename = fd.asksaveasfilename(
            initialdir = "/",
            title = "Select " + text + " file",
            filetypes = [("Text files (.txt)","*.txt")],
            defaultextension = [("Text files (.txt)","*.txt")]
        )
        
        if (filename!=""): # If file name is chosen
            file = open(filename,"wt")
            if (text=="plaintext"): # For plaintext, insert the plaintext
                plaintext = self.plaintext.entry.get("1.0",tk.END)[:-1]
                file.write(plaintext)
            elif (text=="ciphertext"): # For ciphertext, insert the ciphertext
                ciphertext = self.ciphertext.entry.get("1.0",tk.END)[:-1]
                file.write(ciphertext)
                
            file.close()
        
        return "break"
        
    def AlertWindow(self,text):
        # Create new window for alert
        # Components : label with input text and dismiss button
        alert_window = tk.Toplevel(self.parent)
        alert_window.title("Alert")
        
        tk.Label(master=alert_window,text=text).pack(padx=120,pady=20)
        tk.Button(master=alert_window,text="OK",width=10,command=lambda:alert_window.destroy()).pack(pady=10)
        
        alert_window.grab_set()
        
    def BinaryFileWindow(self,event):
        # Create new window for file encrypt/decrypt
        # Components : label, key entry, and buttons
        new_window = tk.Toplevel(self.parent)
        new_window.title("Binary File")
        
        self.binary_file = ""

        self.file_label = tk.Label(master=new_window,text="File : " + self.binary_file)
        self.file_label.grid(row=0,column=0,columnspan=2,sticky="we",padx=120,pady=2)
        self.key_label = tk.Label(master=new_window,text="Key :")
        self.key_label.grid(row=1,column=0,columnspan=2,pady=2)
        self.key_entry = tk.Entry(master=new_window,width=15)
        self.key_entry.grid(row=2,column=0,columnspan=2,pady=2)
        tk.Button(master=new_window,text="Choose File",width=20,command=self.ChooseFileBinary).grid(row=3,column=0,columnspan=2,pady=2)
        tk.Button(master=new_window,text="Encrypt and Save",width=20,command=self.SaveEncryptedFile).grid(row=4,column=0,columnspan=2,pady=2)
        tk.Button(master=new_window,text="Decrypt and Save",width=20,command=self.SaveDecryptedFile).grid(row=5,column=0,columnspan=2,pady=2)
        tk.Button(master=new_window,text="Unselect File",width=20,command=self.UnselectFile).grid(row=6,column=0,columnspan=2,pady=2)

        new_window.grab_set()
        
    def ChooseFileBinary(self):
        # Take filename
        filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select  file",
            filetypes = [("Text files (.txt)","*.txt"),("Binary files (.bin)","*.bin"),("All files","*.*")],
        )
        
        if (filename!=""):
            self.file_label["text"] = "File : " + filename
            self.binary_file = filename
                
    def SaveEncryptedFile(self):
        # buka file di self.binary_file 
        if (self.binary_file==""):
            self.AlertWindow("Please choose a file")
        else:
            #encrypt
            key = self.key_entry.get()
            if (len(key)==0):
                self.AlertWindow("Please insert key")
            else:
                file = open(self.binary_file,"r")
                readPlaintext = file.read()
                encripChipertext = ExtendedEncrypt(readPlaintext, key)
                file.close()
                # save
                filename = fd.asksaveasfilename(
                    initialdir = "/",
                    title = "Save file",
                    filetypes = [("Binary files (.bin)","*.bin"),("All files","*.*")],
                    defaultextension = [("Binary files (.bin)","*.bin"),("All files","*.*")]
                )
                if (filename!=""):
                    output_file = open(filename, "wb")
                    pickle.dump(encripChipertext, output_file)
                    output_file.close()
        
        
    def SaveDecryptedFile(self):
        # buka file di self.binary_file 
        if (self.binary_file==""):
            self.AlertWindow("Please choose a file")
        else:
            # decrypt
            key = self.key_entry.get()
            if (len(key)==0):
                self.AlertWindow("Please insert key")
            else:
                if (self.binary_file[-4:]==".bin"):
                    file = open(self.binary_file,"rb")
                    readChipertext = pickle.load(file)
                    decripPlaintext = ExtendedDecrypt(readChipertext, key)
                    file.close()
                    # sama kayak atasnya
                    filename = fd.asksaveasfilename(
                        initialdir = "/",
                        title = "Save file",
                        filetypes = [("Text files (.txt)","*.txt"),("All files","*.*")],
                        defaultextension = [("Text files (.txt)","*.txt"),("All files","*.*")]
                    )
                    if (filename!=""):
                        output_file = open(filename, "w")
                        output_file.write(decripPlaintext)
                        output_file.close()
                else:
                    self.AlertWindow("Ekstensi file yang mau didekripsi harus .bin")
    
    def UnselectFile(self):
        self.binary_file = ""
        self.file_label["text"] = "File : " + self.binary_file
