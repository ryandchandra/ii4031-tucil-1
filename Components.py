import tkinter as tk
import tkinter.scrolledtext as st

class TextFrame:
    def __init__(self,title,width=50,height=5):
        # Constructor for text frame
        # Components : title and input field (big text)
        # Input : 
        #           title(string) for title
        #           width(int) and height(int) for input field dimensions
        self.frame = tk.Frame()

        self.label = tk.Label(master=self.frame,text=title)
        self.label.pack()

        self.entry = st.ScrolledText(master=self.frame,width=width,height=height)
        self.entry.pack()
        
class KeyFrame:
    def __init__(self,title,width=30):
        # Constructor for key frame
        # Components : title, entry, randomizer
        # Input : 
        #           title(string) for title
        #           width(int) for input field width
        self.frame = tk.Frame()

        self.label = tk.Label(master=self.frame,text=title)
        self.label.pack()

        self.entry = tk.Entry(master=self.frame,width=width)
        self.entry.pack()
        
        self.random_label = tk.Label(master=self.frame,text="Randomizer length")
        self.random_label.pack(padx=2,pady=2,side="left",anchor="center")
        
        self.random_entry = tk.Entry(master=self.frame,width=4)
        self.random_entry.pack(padx=2,pady=2,side="left",anchor="center")
        
        self.button = tk.Button(master=self.frame,width=10,text="Randomize")
        self.button.pack(padx=2,pady=2,side="left",anchor="center")
        
class AffineKeyFrame:
    def __init__(self,width=10):
        # Constructor for affine key frame
        # Components : two titles and two input fields (one line)
        # Input : 
        #           width(int) for input field width
        self.frame = tk.Frame()

        self.multiple_label = tk.Label(master=self.frame,text="Multiple (m)")
        self.multiple_label.pack(padx=2,pady=2,side="left")
        
        self.multiple_entry = tk.Entry(master=self.frame,width=width)
        self.multiple_entry.pack(padx=2,pady=2,side="left")
        
        self.offset_label = tk.Label(master=self.frame,text="Offset (b)")
        self.offset_label.pack(padx=2,pady=2,side="left")
        
        self.offset_entry = tk.Entry(master=self.frame,width=width)
        self.offset_entry.pack(padx=2,pady=2,side="left")
        
class ButtonListFrame:
    def __init__(self,title,labels,width=20):
        # Constructor for list of buttons frame
        # Components : title and button list
        # Input : 
        #           title(string) for title
        #           labels(list of strings) for button label
        #           width(int) for button width
        self.frame = tk.Frame()

        self.label = tk.Label(master=self.frame,text=title)
        self.label.pack()

        self.button_list = []
        for label in labels:
            new_button = tk.Button(master=self.frame,text=label,width=width)
            new_button.pack(padx=2,pady=2)
            self.button_list.append(new_button)