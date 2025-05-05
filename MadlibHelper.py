# Nicolas DeGuglielmo
# 8/3/2021

# Function testing file, pay no attention

import os
import json
import re
from past.builtins import raw_input
import textract
import PySimpleGUI as sg
import tkinter as tk
from tkinter import scrolledtext
#root = tk.Tk()

generic_words = { # reminder: do not add any keywords that are the same as ignored words
                 '/adj': 'Adjective', '/nou': 'Noun', '/pln': 'Plural noun',
                 '/ver': 'Verb'}
ignored_words = ['/her', '/she', '/She']  # words that resemble generic words that will be ignored
numword_dic = {}
unnumbered = "(/...)"
numbered = "(/...[0-9]+)"
customreg = "(/ct[0-9]+)"
numcustcom = ".+\([0-9]+\)"
numcustreg = "(/ct[0-9]+_[0-9]+)"
tail = "(_[0-9])"
custom={}
def in_out(input):
    out = input
    return out
def Guitest():
    layout = [
        [sg.InputText(key='-NAME-')],
        [sg.Button('Submit')],
        [sg.Text('', key='-OUTPUT-')]
    ]

    window = sg.Window('Greeting', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Submit':
            window['-OUTPUT-'].update(f"Hello {values['-NAME-']}")

    window.close()
# checks if file exists, returns boolean
def doesFileExist(filename):
    # choice = os.path.join('inputs', filename + ".txt")
    # my_file = open(choice, "r")

    # text = text.replace('\u201C', '"')
    # text = text.replace('\u201c', '"')
    # text = text.replace('\u201D', '"')
    # text = text.replace('\u201d', '"')
    return ''
    # if text:
    #     print(text)
    #     return True
    # else:
    #     return False



class MadlibApp: #todo interface with fillmadlib
    def __init__(self, root):
        self.root = root #initializes a general widget (to be used in every element)
        self.root.title("Madlib Generator") #titles the window(s)
        self.userMadlib = []
        self.save_flag = False
        self.welcomeMenuHandler() #Opens the first window

    def cust_config(self, inlist):
        #print("Custom words detected, enter each of your custom words, one by one, in order of appearance. Enter \"q\" to stop ")
        for word in inlist:
            if re.findall(customreg, word):
                regkey = re.findall(customreg, word)
                realkey = ''.join(regkey)
                if realkey not in custom:
                    base = re.findall(customreg, word)
                    base = ''.join(base)
                    regnum = re.findall(r'\d+', base)
                    num = ''.join(regnum)
                    print("Custom " + str(num))
                    ch = raw_input()
                    custom[realkey] = ch
                else:
                    pass
            else:
                continue

        return custom
    def customWordsFilter(self, inputList, base_name, saveFileOverride):
        customfile = base_name + "_cts.txt"
        if os.path.exists(os.path.join('inputs', customfile)):
            choice = os.path.join('inputs', customfile)
            with open(choice) as f:
                data = f.read()
            local_custom = json.loads(data.replace("\'", "\""))
            f.close()
        elif not os.path.exists(os.path.join('inputs', customfile)) and re.search(customreg,
                                                                                  str(inputList)) is not None:
            local_custom = self.cust_config(inputList)
            if saveFileOverride:
                self.dummyscreen('filewrite()')
                #file_write(str(custom), base_name, 'inputs', '_cts.txt')
        else:
            custom = None
        custom=local_custom

    def advance_to_cust(self):
        self.customs_found = re.findall(customreg, self.input_entry.get())
        self.cust_itterate = iter(self.customs_found)
        self.dummyscreen('advance_to_cust')
    def cust_window(self):
        for widget in self.root.winfo_children(): widget.destroy() #clears previous window
        #define and create word prompts display
        self.display = scrolledtext.ScrolledText(self.root, width=80, height=10, font=("Arial", 12), bg="#9cc9e0", fg="black")
        self.display.pack(pady=10)
        self.display.insert(tk.END, f"Custom Words detected. Please configure them now.\n")
        # define and create entry field for user's entry for a word
        self.input_entry = tk.Entry(self.root, font=("Arial", 14), width=80, bg="#d0e7ff", fg="black")
        self.input_entry.bind("<Return>", lambda event: self.process_cust_entry) #allows the "enter" key to submit the keyword
        self.input_entry.pack(pady=10)
        self.input_entry.focus_set() #automatically puts the cursor into the entry field

        self.submit_btn = tk.Button(self.root, text="Submit",command=self.process_cust_entry, bg="#3b9dd3", fg="white")
        self.submit_btn.pack(pady=10)

        self.next_prompt()
    def advance_to_second(self): #advances from first screen to second
        self.userMadlib = re.findall(r'/\w+\d*|[^\s\w]|[\w]+', self.input_entry.get()) #finds the keyword ignoring surrounding punctuation
        #print(str(self.userMadlib))
        self.prompt_words = iter(self.userMadlib) #saves the words to prompt
        #print("Prompt words:", str(self.prompt_words))
        self.outlist = [] #starts the outlist
        self.second_window() #loads the second window
    def second_window(self):
        for widget in self.root.winfo_children(): widget.destroy() #clears previous window
        #define and create word prompts display
        self.display = scrolledtext.ScrolledText(self.root, width=80, height=10, font=("Arial", 12), bg="#9cc9e0", fg="black")
        self.display.pack(pady=10)
        # define and create entry field for user's entry for a word
        self.input_entry = tk.Entry(self.root, font=("Arial", 14), width=80, bg="#d0e7ff", fg="black")
        self.input_entry.bind("<Return>", lambda event: self.process_next_keyword()) #allows the "enter" key to submit the keyword
        self.input_entry.pack(pady=10)
        self.input_entry.focus_set() #automatically puts the cursor into the entry field

        self.submit_btn = tk.Button(self.root, text="Submit", command=self.process_next_keyword, bg="#3b9dd3", fg="white")
        self.submit_btn.pack(pady=10)

        self.next_prompt()
    def third_window(self):
        for widget in self.root.winfo_children(): widget.destroy()
        display = scrolledtext.ScrolledText(self.root, width=80, height=20, font=("Arial", 12), bg="#9cc9e0", fg="black")
        display.pack(pady=20)

        def smart_join(words):# removes spaces surrounding punctuation
            result = ""
            for i, word in enumerate(words):
                if i == 0:
                    result += word
                elif re.match(r"[.,!?;:]", word):  # If it's punctuation, don't add space
                    result += word
                else:
                    result += " " + word
            return result

        display.insert(tk.END, "\nFinal Madlib:\n" + smart_join(self.outlist))
    def next_cust(self):
        try:
            if re.findall(customreg, self.current_word):
                regkey = re.findall(customreg, self.current_word)
                realkey = ''.join(regkey)
                if realkey not in custom:
                    base = re.findall(customreg, self.current_word) #extracts the base custom word (ex /ct1)
                    base = ''.join(base)
                    regnum = re.findall(r'\d+', base) #extracts the ID number of the custom word (ex 1)
                    num = ''.join(regnum)
                    self.display.insert(tk.END, f"Custom "+str(num)+":\n")
                    return
                else:
                    pass
            else:
                pass
        except StopIteration:
            self.dummyscreen('done with custs')
            #self.current_word = next(custom)
        self.dummyscreen('nextcust()')
    def next_prompt(self):
        try:
            self.current_word = next(self.prompt_words)
            if re.findall(unnumbered, self.current_word) and not re.findall(numbered, self.current_word) and not re.findall(customreg, self.current_word):
                regkey = re.findall(unnumbered, self.current_word)
                realkey = ''.join(regkey)
                if realkey in generic_words:
                    self.display.insert(tk.END, f"{generic_words[realkey]}:\n")
                    return
                    #outlist.append(keyword_convert(realkey, self.current_word, 0, None))
                elif realkey in ignored_words:
                    #outlist.append(word)
                    return
                else:
                    self.display.insert(tk.END, f"{realkey} is not a valid keyword, what would you like to replace it with?:\n")
                    return
                    #outlist.append(keyword_convert(realkey, self.current_word, 6, None))

            elif re.findall(customreg, self.current_word) and not re.findall(numcustreg, self.current_word):
                # custom
                regkey = re.findall(customreg, self.current_word)
                realkey = ''.join(regkey)
                if realkey in custom:
                    base = re.findall(customreg, self.current_word)
                    base = ''.join(base)
                    self.display.insert(tk.END, f"{custom[realkey]}:\n")
                    return

                # outlist.append(keyword_convert(realkey, self.current_word, 3, custom))

                # HTML array
                elif realkey not in custom:
                    self.display.insert(tk.END, f"{realkey} hasn't been configured, what would you like to replace it with?:\n")
                    return
                    #outlist.append(keyword_convert(realkey, self.current_word, 5, custom))


            # html equivelent

            elif re.findall(numcustreg, self.current_word):
                # numberded custom

                regkey = re.findall(numcustreg, self.current_word)
                realkey = ''.join(regkey)

                base = re.findall(customreg, self.current_word)
                base = ''.join(base)

                tailkey = re.findall(tail, self.current_word)
                tailkey = ''.join(tailkey)
                regnum = re.findall(r'\d+', tailkey)
                num = ''.join(regnum)

                if realkey not in numword_dic:
                    # numbered cust unsaved
                    base = re.findall(customreg, self.current_word)
                    base = ''.join(base)
                    self.display.insert(tk.END, f"{custom[base]} :\n")#todo: fix unconfigged numbered customs
                    self.save_flag= True
                    self.save_key= realkey
                    return
                elif realkey in numword_dic:
                    print("I'm a saved word "+ str(realkey)+" "+str(numword_dic[realkey]))
                    self.current_word=numword_dic[realkey]
                    # numbered cust saved
                elif base not in custom:
                    # numbered cust unsaved
                    self.display.insert(tk.END, f"{realkey} hasn't been configured, what would you like to replace it with?:\n")
                    self.save_flag = True
                    self.save_key = realkey
                    return
                else:
                    # others
                    self.display.insert(tk.END,
                                        f"{realkey} is not a valid keyword, what would you like to replace it with?:\n")
                    return


            elif re.findall(numbered, self.current_word):
                # numbered
                regkey = re.findall(numbered, self.current_word)
                regkeyb = re.findall(unnumbered, self.current_word)
                realkey = ''.join(regkey)
                base = ''.join(regkeyb)
                regnum = re.findall(r'\d+', realkey)
                num = ''.join(regnum)
                if realkey not in numword_dic.keys() and base in generic_words.keys():
                    self.display.insert(tk.END, f"{generic_words[base]}:\n")
                    self.save_flag = True
                    self.save_key = realkey
                    return
                    # numbered unsaved
                    #outlist.append(keyword_convert(realkey, self.current_word, 1, None))
                elif realkey not in numword_dic.keys() and base not in generic_words.keys():
                    self.display.insert(tk.END,
                                        f"{realkey} is not a valid keyword, what would you like to replace it with?:\n")
                    return
                    #outlist.append(keyword_convert(realkey, self.current_word, 6, None))  # invalid
                elif realkey in numword_dic.keys():
                    self.current_word=numword_dic[realkey]
                    #outlist.append(keyword_convert(realkey, self.current_word, 2, None))  # numbered saved
            else:
                pass
                # none, just append
                #outlist.append(word)


            self.outlist.append(self.current_word)
            self.next_prompt()
        except StopIteration:
            self.third_window()

    def process_cust_entry(self, key):
        user_text = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        if user_text:
            custom[key]=self.current_word
        self.next_cust()
    def process_next_keyword(self):
        user_text = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        if user_text and self.save_flag == False:
            self.outlist.append(user_text)
        elif user_text and self.save_flag == True:
            self.outlist.append(user_text)
            numword_dic[self.save_key]=user_text
            #print("I'm saving ",str(self.save_key),' as ',str(self.current_word))
            self.save_flag=False
        else:
            pass
        self.next_prompt()
    # Returns file generated madlib

    def dummyscreen(self,name):
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        text = "This is the screen for " + str(name)
        w = tk.Label(self.root, text=text, width=80, height=10, bg="#d0e7ff", fg="black")
        w.pack(pady=10)
        self.root.mainloop()  # deploys the GUI screen till closed

    def welcomeMenuHandler(self):
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets

        # Welcome Menu
        # welcome text
        w = tk.Label(self.root, text='Hello, Welcome to the Madlib Maker', width=80, height=10, bg="#d0e7ff", fg="black")
        w.pack(pady=10)
        # buttons for Welcome menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        # manual input button
        btn = tk.Button(button_frame, command=lambda: self.first_window(), text="Manual Input", bg="#3b9dd3",
                        fg="white")  # defines each button with frame, todo: add argument: command= enterMadlibManual()
        btn.grid(row=1, column=0, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # Load inputs button
        btn = tk.Button(button_frame, command=lambda: self.dummyscreen('[new file read function]'), text="Load a Madlib",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame, todo: add argument: command= [file namer function]
        btn.grid(row=1, column=2, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # Instruction menu button
        btn = tk.Button(button_frame, command=lambda: self.dummyscreen('New Instructions'), text="Instructions",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame, todo: add argument: command= instructionsMenuHandler()
        btn.grid(row=1, column=3, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        self.root.mainloop()  # deploys the GUI screen till closed
    def first_window(self): # manual madlib entry screen
        for widget in self.root.winfo_children(): widget.destroy() #removes pre-existing widgets

        self.input_entry = tk.Entry(self.root, font=("Arial", 14), width=80, bg="#d0e7ff", fg="black") #defines the text input field, size, color of font and background
        self.input_entry.pack(pady=10)# sets the verticle spacing given between the input field and other successive elements
        self.input_entry.focus_set()  # This sets focus so the cursor appears in the field

        button_frame = tk.Frame(self.root) #defines the button frame
        button_frame.pack(pady=5)

        row = 0 #initializes row and column counters for button grid
        col = 0
        for key, label in generic_words.items(): #for every generic word. Grabs the key (/adj) and label (adjective)
            btn = tk.Button(button_frame, text=label, command=lambda k=key: self.insert_keyword(k), bg="#3b9dd3", fg="white") #defines each button with frame
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew") #defines the button's location on the grid ("ew" centers all buttons to their grid position)
            col += 1
            if col >= 10: #ten columns, then new row
                col = 0
                row += 1
        #define submit button, command to advance to next screen
        self.submit_btn = tk.Button(self.root, text="Submit", command=self.advance_to_second, bg="#3b9dd3", fg="white")
        self.submit_btn.pack(pady=10)
        #define display
        self.display = scrolledtext.ScrolledText(self.root, width=80, height=10, font=("Arial", 12), bg="#9cc9e0", fg="black")
        self.display.pack(pady=10)

        self.input_entry.bind("<KeyRelease>", self.sync_display) #syncs display on every key release

    def insert_keyword(self, keyword):
        #self.input_entry.insert(tk.END, keyword + " ") #inputs keyword to text with a space automatically after it
        self.input_entry.insert(tk.END, keyword) #inputs keyword without a space (do not have both lines active)
        self.sync_display() #adds the keyword to the display

    def sync_display(self, event=None): #syncs text between manual entry and display
        self.display.delete(1.0, tk.END) #clears the display before updating with current text (from row 1 char 0 to the end)
        self.display.insert(tk.END, self.input_entry.get()) #inserts text from the end (which is the start of the field after delete) to



# menuHandler returns the unprocessed user madlib or empty string to retry









# Main function
def main():
    global custom

    #welcomeMenuHandler()  # Call the function and unpack the return values
    root = tk.Tk()
    app = MadlibApp(root)
    root.mainloop()


    #print("userMadlib:", str(userMadlib))  # Print userMadlib as a string
    #print("custom:", str(custom))  # Print custom as a string
    # Test 1
    #d = doesFileExist('wordquotetest.docx')
    #print("Test 1 Result: ", d)

    # Test 2
  #  c = readCustomFile('customtestin')
    #print("Test 2 Result: ", c)

    # Test 3
   # g = checkForCustomWords("")
    #print("Test 3 Result: ", g)

    # Test 4
    #h = quoteConverter("“Go /ct1_1! Shouted Mackey.”")
    #print("Test 3 Result: ", h)


if __name__ == "__main__":
    main()
