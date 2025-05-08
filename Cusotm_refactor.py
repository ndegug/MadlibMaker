import tkinter as tk
from tkinter import scrolledtext
import re
import os
generic_words = { # reminder: do not add any keywords that are the same as ignored words
                 '/adj': 'Adjective', '/nou': 'Noun', '/pln': 'Plural noun',
                 '/ver': 'Verb'}
ignored_words = ['/her', '/she', '/She']  # words that resemble generic words that will be ignored
numword_dic = {}
unnumbered = "(/...)"
numbered = "(/...[0-9]+)"
customreg = "(/ct[0-9]+)"
#numcustcom = ".+\([0-9]+\)" #todo remove if unneeded for numbered customs
numcustreg = "(/ct[0-9]+_[0-9]+)"
tail = "(_[0-9])"

class MadlibApp:
    def __init__(self, root):
        self.root = root
        self.custom = {}
        self.custom_keys = []
        self.custom_index = 0
        self.save_flag = False
        self.folders()
        self.welcomeMenuHandler()


    def folders(self):
        if not os.path.isdir(os.path.join(os.getcwd(), "inputs")):
            os.mkdir(os.path.join(os.getcwd(), "inputs"))
        if not os.path.isdir(os.path.join(os.getcwd(), "outputs")):
            os.mkdir(os.path.join(os.getcwd(), "outputs"))
    def dummyscreen(self,name):
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        text = "This is the screen for " + str(name)
        w = tk.Label(self.root, text=text, width=80, height=10, bg="#d0e7ff", fg="black")
        w.pack(pady=10)
        self.root.mainloop()  # deploys the GUI screen till closed

    def file_write(self, content, name_of_file, path, ext):
        completeName = os.path.join(path, name_of_file + ext)
        f = open(completeName, "w")
        f.write(content)
        f.close()
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
        btn = tk.Button(button_frame, command=lambda: self.setup_first_window(), text="Manual Input", bg="#3b9dd3",
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
    def setup_first_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.input_entry = tk.Entry(self.root, width=60)
        self.input_entry.pack(pady=20)

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
        self.submit_btn = tk.Button(self.root, text="Submit", command=self.advance_from_first, bg="#3b9dd3", fg="white")
        self.submit_btn.pack(pady=10)
        #define display
        self.display = scrolledtext.ScrolledText(self.root, width=80, height=10, font=("Arial", 12), bg="#9cc9e0", fg="black")
        self.display.pack(pady=10)

        self.input_entry.bind("<KeyRelease>", self.sync_display) #syncs display on every key release
        #tk.Button(self.root, text="Submit", command=self.advance_from_first).pack()

    def sync_display(self, event=None): #syncs text between manual entry and display
        self.display.delete(1.0, tk.END) #clears the display before updating with current text (from row 1 char 0 to the end)
        self.display.insert(tk.END, self.input_entry.get()) #inserts text from the end (which is the start of the field after delete) to
    def insert_keyword(self, keyword):
        #self.input_entry.insert(tk.END, keyword + " ") #inputs keyword to text with a space automatically after it
        self.input_entry.insert(tk.END, keyword) #inputs keyword without a space (do not have both lines active)
        self.sync_display() #adds the keyword to the display
    def advance_from_first(self):
        self.manual_in = self.input_entry.get()

        self.userMadlib = re.findall(r'/\w+\d*_[0-9]+|/\w+\d*|[^\s\w]|[\w]+', self.manual_in)
        self.prompt_words = iter(self.userMadlib)
        self.outlist = []

        # Extract and sort custom keys
        all_custom_matches = re.findall(r'/ct(\d+)(?:_\d+)?', self.manual_in)
        self.custom_keys = sorted(set(f"/ct{id}" for id in all_custom_matches), key=lambda x: int(x[3:]))

        if self.custom_keys:
            self.custom_configure_window()
        else:
            self.file_choice()
            self.next_prompt()

    def custom_configure_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.display = scrolledtext.ScrolledText(self.root, width=80, height=10, font=("Arial", 12), bg="#9cc9e0", fg="black")
        self.display.pack(pady=10)
        self.display.insert(tk.END, "Custom words detected, please configure them.\n")

        self.custom_entry = tk.Entry(self.root, width=40,font=("Arial", 12), bg="#d0e7ff", fg="black")
        self.custom_entry.bind("<Return>",
                               lambda event: self.save_custom_word())  # allows the "enter" key to submit the keyword
        self.custom_entry.pack(pady=10)
        self.custom_button = tk.Button(self.root, text="Enter",bg="#3b9dd3", fg="white", command=self.save_custom_word)
        self.custom_button.pack(pady=5)

        self.prompt_next_custom()

    def prompt_next_custom(self):
        if self.custom_index < len(self.custom_keys):
            current_key = self.custom_keys[self.custom_index]
            self.display.insert(tk.END, f"Custom {current_key[3:]}: ")
        else:
            print("No more Customs")
            self.file_choice()
            #self.second_window()
            #self.next_prompt()

    def save_custom_word(self):
        current_key = self.custom_keys[self.custom_index]
        user_input = self.custom_entry.get().strip()
        if user_input:
            self.custom[current_key] = user_input
            self.custom_entry.delete(0, tk.END)
            self.custom_index += 1
            self.display.insert(tk.END, f"{user_input}\n")
            self.prompt_next_custom()

    def second_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.display = scrolledtext.ScrolledText(self.root, width=80, height=10, font=("Arial", 12), bg="#9cc9e0",
                                                 fg="black")
        self.display.pack(pady=10)
        # define and create entry field for user's entry for a word
        self.input_entry = tk.Entry(self.root, font=("Arial", 14), width=80, bg="#d0e7ff", fg="black")
        self.input_entry.bind("<Return>",
                              lambda event: self.process_next_keyword())  # allows the "enter" key to submit the keyword
        self.input_entry.pack(pady=10)
        self.input_entry.focus_set()  # automatically puts the cursor into the entry field

        self.submit_btn = tk.Button(self.root, text="Submit", command=self.process_next_keyword, bg="#3b9dd3",
                                    fg="white")
        self.submit_btn.pack(pady=10)

    def next_prompt(self):
        try:
            self.current_word = next(self.prompt_words)
            if re.findall(unnumbered, self.current_word) and not re.findall(numbered,
                                                                            self.current_word) and not re.findall(
                    customreg, self.current_word):
                regkey = re.findall(unnumbered, self.current_word)
                realkey = ''.join(regkey)
                if realkey in generic_words:
                    self.display.insert(tk.END, f"{generic_words[realkey]}:\n")
                    return
                    # outlist.append(keyword_convert(realkey, self.current_word, 0, None))
                elif realkey in ignored_words:
                    # outlist.append(word)
                    return
                else:
                    self.display.insert(tk.END,
                                        f"{realkey} is not a valid keyword, what would you like to replace it with?:\n")
                    return
                    # outlist.append(keyword_convert(realkey, self.current_word, 6, None))

            elif re.findall(customreg, self.current_word) and not re.findall(numcustreg, self.current_word):
                # custom
                regkey = re.findall(customreg, self.current_word)
                realkey = ''.join(regkey)
                if realkey in self.custom:
                    base = re.findall(customreg, self.current_word)
                    base = ''.join(base)
                    self.display.insert(tk.END, f"{self.custom[realkey]}:\n")
                    return

                # outlist.append(keyword_convert(realkey, self.current_word, 3, custom))

                # HTML array
                elif realkey not in self.custom:
                    self.display.insert(tk.END,
                                        f"{realkey} hasn't been configured, what would you like to replace it with?:\n")
                    return
                    # outlist.append(keyword_convert(realkey, self.current_word, 5, custom))


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
                    self.display.insert(tk.END, f"{self.custom[base]} :\n")  # todo: fix unconfigged numbered customs
                    self.save_flag = True
                    self.save_key = realkey
                    return
                elif realkey in numword_dic:
                    print("I'm a saved word " + str(realkey) + " " + str(numword_dic[realkey]))
                    self.current_word = numword_dic[realkey]
                    # numbered cust saved
                elif base not in self.custom:
                    # numbered cust unsaved
                    self.display.insert(tk.END,
                                        f"{realkey} hasn't been configured, what would you like to replace it with?:\n")
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
                    # outlist.append(keyword_convert(realkey, self.current_word, 1, None))
                elif realkey not in numword_dic.keys() and base not in generic_words.keys():
                    self.display.insert(tk.END,
                                        f"{realkey} is not a valid keyword, what would you like to replace it with?:\n")
                    return
                    # outlist.append(keyword_convert(realkey, self.current_word, 6, None))  # invalid
                elif realkey in numword_dic.keys():
                    self.current_word = numword_dic[realkey]
                    # outlist.append(keyword_convert(realkey, self.current_word, 2, None))  # numbered saved
            else:
                pass
                # none, just append
                # outlist.append(word)
            self.outlist.append(self.current_word)
            self.next_prompt()
        except StopIteration:
            self.third_window()

    def in_file_name(self):
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        w = tk.Label(self.root, text='Enter the filename you\'d like to save to (no extension)', width=80, height=10, bg="#d0e7ff",
                     fg="black")
        w.pack(pady=10)
        # buttons for Welcome menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        self.input_entry = tk.Entry(self.root, font=("Arial", 14), width=80, bg="#d0e7ff", fg="black")
        self.input_entry.bind("<Return>",
                              lambda event: self.save_and_play())  # allows the "enter" key to submit the keyword
        self.input_entry.pack(pady=10)
        self.input_entry.focus_set()  # automatically puts the cursor into the entry field
        self.submit_btn = tk.Button(self.root, text="Submit", command=lambda: self.save_and_play(), bg="#3b9dd3", fg="white")
        self.submit_btn.pack(pady=10)

        self.root.mainloop()  # deploys the GUI screen till closed

    def save_and_play(self):
        base = self.input_entry.get().strip()
        self.file_write(self.manual_in+'\n'+str(self.custom), base, 'inputs','.txt')
        w = tk.Label(self.root, text='Your mandlib has been saved to: '+str(base)+ '.txt in your \"inputs\" folder.\nNow we can Play!',
                     width=80, height=10, bg="#d0e7ff",
                     fg="black")
        w.pack(pady=10)
        self.submit_btn = tk.Button(self.root, text="Let's Go", command=lambda: self.advance_to_second(), bg="#3b9dd3", fg="white")
        self.submit_btn.pack(pady=10)
    def advance_to_second(self):
        self.second_window()
        self.next_prompt()
    def file_choice(self):
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        w = tk.Label(self.root, text='Would you like to save your Madlib for future use or play without saving?', width=80, height=10, bg="#d0e7ff",
                     fg="black")
        w.pack(pady=10)
        # buttons for Welcome menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        #Yes button
        btn = tk.Button(button_frame, command=lambda: self.in_file_name(), text="Save", bg="#3b9dd3",
                        fg="white")  # defines each button with frame, todo: add argument: command= enterMadlibManual()
        btn.grid(row=1, column=0, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # no button
        btn = tk.Button(button_frame, command=lambda: self.advance_to_second(), text="Play without saving", bg="#3b9dd3",
                        fg="white")  # defines each button with frame, todo: add argument: command= enterMadlibManual()
        btn.grid(row=1, column=2, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        self.root.mainloop()  # deploys the GUI screen till closed
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

    def smart_join(self, words):  # removes spaces surrounding punctuation todo: evaluate if self.outlist can be integrated into this instead of passed to it
        result = ""
        prev_word = ""
        quote_flag = False  # indicates being part of a quote segment
        for i, word in enumerate(words):
            if i == 0:  # first word, no space before
                result += word
                if re.match(r"[\"]", word):  # if the first element is a quote, turn on quote flag
                    quote_flag = True
            elif re.match(r"[.,!?;:]", word):  # If it's punctuation, don't add space
                result += word
            elif re.match(r"[\"]", word) and quote_flag == False:  # Open quote, space before, turn on quote flag
                result += " " + word
                quote_flag = True
            elif re.match(r"[\"]", word) and quote_flag == True:  # close quote, no space before, turn off quote flag
                result += word
                quote_flag = False
            elif re.match(r"[\"]", prev_word) and quote_flag == True:  # word after open quote, no leading space
                result += word
            # elif re.match(r"[\"]", prev_word) and quote_flag==False: #word after close quote, no leading space, turn off quote flag
            #    result += " " + word

            else:
                result += " " + word
            prev_word = word
        return result



    def third_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        display = scrolledtext.ScrolledText(self.root, width=80, height=20, font=("Arial", 12), bg="#9cc9e0", fg="black")
        display.pack(pady=20)
        #final_output = re.sub(r'\s([.,!?;:])', r'\1', ' '.join(self.outlist))



        display.insert(tk.END, "\nFinal Madlib:\n" + self.smart_join(self.outlist))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Madlib App")
    app = MadlibApp(root)
    root.mainloop()
