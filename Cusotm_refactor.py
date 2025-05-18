import tkinter as tk
from tkinter import scrolledtext, messagebox
import webbrowser
import tempfile
import re
import os
from long_strings_gui import *
import json
from docx import Document

numword_dic = {}
unnumbered = "(/...)"
numbered = "(/...[0-9]+)"
customreg = "(/ct[0-9]+)"
#numcustcom = ".+\([0-9]+\)" #todo remove if unneeded for numbered customs
numcustreg = "(/ct[0-9]+_[0-9]+)"
tail = "(_[0-9])"
htmlsample = '<span class="nowrap" style="display: none; display: inline-block; vertical-align: top; text-align: ' \
             'center;"><span style="display: block; padding: 0 0.2em;">__________</span><span style="display: block; ' \
             'font-size: 70%; line-height: 1em; padding: 0 0.2em;"><span style="position: relative; line-height: 1em; ' \
             'margin-top: -.2em; top: -.2em;">underscript</span></span></span>'
class MadlibApp:
    def __init__(self, root):
        self.root = root
        self.reset()
    def reset(self):
        self.custom = {}
        self.custom_keys = []
        self.custom_index = 0
        self.save_flag = False
        self.folders()
        self.outlist = []
        self.htlist = []
        self.title = ''
        self.mode = 0  # decides mode (0=write or 1=load) todo: change to true/false if binary
        self.welcomeMenuHandler()
    def load_input_file(self):
        # Clear existing widgets if necessary
        for widget in self.root.winfo_children():
            widget.destroy()
        self.mode = 1
        label = tk.Label(self.root, text="Select a file to load:", font=("Arial", 14))
        label.pack(pady=10)

        inputs_path = os.path.join(os.getcwd(), "inputs")

        if not os.path.exists(inputs_path):
            os.makedirs(inputs_path)

        files = [f for f in os.listdir(inputs_path) if f.endswith('.txt') or f.endswith('.docx')]

        if not files:
            no_files_label = tk.Label(self.root, text="No input files found in the 'inputs' folder.",
                                      font=("Arial", 12))
            no_files_label.pack(pady=10)
            return

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        row = 0  # initializes row and column counters for button grid
        col = 0
        for filename in files:
            full_path = os.path.join(inputs_path, filename)
            btn = tk.Button(button_frame, text=filename, font=("Arial", 12),
                            command=lambda path=full_path: self.process_input_file_3(path), bg="#3b9dd3",
                        fg="white")
            btn.grid(row=row, column=col, padx=2, pady=2,
                     sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
            col += 1
            if col >= 10:  # ten columns, then new row
                col = 0
                row += 1
    def load_input_file_old(self): #todo: remove unless load bugs are found
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.mode=1
        # Get all .txt and .docx files from "inputs" folder

        input_dir = os.path.join(os.path.dirname(__file__), "inputs")
        files = [f for f in os.listdir(input_dir) if f.endswith(('.txt', '.docx'))]

        # Display available files
        tk.Label(self.root, text="Available input files:", font=("Arial", 12, "bold")).pack()
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        #for file in files:
        #    tk.Label(self.root, text=file).pack()
        row = 0  # initializes row and column counters for button grid
        col = 0
        fileID=0
        for file in files:  # for every generic word. Grabs the key (/adj) and label (adjective)
            btn = tk.Button(button_frame, command=lambda: self.dummyscreen(str(files[fileID])), text=file,
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame
            btn.grid(row=row, column=col, padx=2, pady=2,
                     sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
            col += 1
            fileID += 1
            if col >= 10:  # ten columns, then new row
                col = 0
                row += 1
        # Prompt user
        tk.Label(self.root, text="Please type the name of the file you'd like to load including the extension:").pack()
        self.file_entry = tk.Entry(self.root)
        self.file_entry.pack(pady=5)

        # Enter button
        #enter_button = tk.Button(self.root, text="Enter", command=self.process_input_file_3())
        #enter_button.pack(pady=10)

    def process_input_file_3(self, path): #todo remove other process_input_file methods if this works
        madlib_text = ""
        custom_dict = {}
        title_text = ""
        #filename = self.file_entry.get()
        file_path = path
        try:
            # Read file content
            if file_path.endswith(".txt"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif file_path.endswith(".docx"):
                doc = Document(file_path)
                content = "\n".join([p.text for p in doc.paragraphs])
            else:
                messagebox.showerror("Unsupported Format", "Only .txt and .docx files are supported.")
                return

            # Extract title if present
            if "<t>" in content and "</t>" in content:
                start = content.index("<t>") + len("<t>")
                end = content.index("</t>")
                title_text = content[start:end].strip()

                # Remove title from content
                content = content[:content.index("<t>")] + content[end + len("</t>"):]

            # Extract custom dictionary
            if "<C>" in content:
                c_index = content.index("<C>")
                madlib_text = content[:c_index].strip()
                dict_text = content[c_index + len("<C>"):].strip()
                try:
                    custom_dict = eval(dict_text)
                except Exception as e:
                    messagebox.showerror("Custom Dict Error", f"Failed to parse custom dictionary:\n{e}")
                    return
            else:
                madlib_text = content.strip()

            self.title = title_text
            self.custom = custom_dict
            self.raw_in=madlib_text
            self.advance_from_first()

        except Exception as e:
            messagebox.showerror("File Error", f"Could not read file:\n{e}")
    def process_input_file_2(self): #todo: decide between orignal and this one
        filename = self.file_entry.get()
        file_path = os.path.join(os.path.dirname(__file__), "inputs", filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                import docx
                doc = docx.Document(file_path)
                content = '\n'.join([para.text for para in doc.paragraphs])
            except Exception as e:
                messagebox.showerror("Error", f"Could not read DOCX file: {e}")
                return

        # Extract custom dictionary
        custom_start = content.find("<C>")
        if custom_start != -1:
            custom_text = content[custom_start + 3:].strip()
            try:
                self.custom = eval(custom_text)
            except Exception as e:
                #messagebox.showerror("Error", f"Could not parse custom dictionary: {e}")
                return
            madlib_text = content[:custom_start].strip()
        else:
            madlib_text = content.strip()

        # Extract title if present
        title_start = content.find("<t>")
        title_end = content.find("</t>")
        if title_start != -1 and title_end != -1 and title_end > title_start:
            self.title = content[title_start + 3:title_end].strip()
        else:
            self.title = ""

        self.raw_in=madlib_text
        self.advance_from_first()
    def process_input_file(self):
        filename = self.file_entry.get()
        input_path = os.path.join(os.path.dirname(__file__), "inputs", filename)

        if not os.path.exists(input_path):
            messagebox.showerror("File Error", f"File '{filename}' not found.")
            return

        try:
            # Read file content
            if filename.endswith('.txt'):
                with open(input_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            elif filename.endswith('.docx'):
                doc = Document(input_path)
                lines = [para.text for para in doc.paragraphs]
            else:
                messagebox.showerror("Format Error", "Unsupported file type.")
                return

            # Split lines into madlib and custom dictionary
            madlib_lines = []
            custom_dict_str = ""
            found_c_marker = False

            for line in lines:
                if line.strip().startswith("<C>"):
                    found_c_marker = True
                    custom_dict_str = line.strip()[3:].strip()  # Remove "<C>"
                    continue
                if not found_c_marker:
                    madlib_lines.append(line.strip())

            #if not found_c_marker:
            #    messagebox.showerror("Format Error", "No <C> marker found for custom dictionary.")
            #    return

            madlib_text = ' '.join(madlib_lines)
            self.raw_in = madlib_text

            try:
                self.custom = eval(custom_dict_str)
                if not isinstance(self.custom, dict):
                    raise ValueError("Parsed custom dictionary is not a valid dict.")
            except Exception as e:
                #messagebox.showerror("Parsing Error", f"Could not parse dictionary: {e}")
                #return
                pass

            messagebox.showinfo("Success", "File loaded successfully!")
            self.advance_from_first()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

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
    def escape(self):
        return
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
        btn = tk.Button(button_frame, command=lambda: self.load_input_file(), text="Load a Madlib",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame, todo: add argument: command= [file namer function]
        btn.grid(row=1, column=2, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # Instruction menu button
        btn = tk.Button(button_frame, command=lambda: self.instruct_main(), text="Instructions",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame, todo: add argument: command= instructionsMenuHandler()
        btn.grid(row=1, column=3, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        self.root.mainloop()  # deploys the GUI screen till closed
    def instruct_main(self):
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets

        # Welcome Menu
        # welcome text
        w = tk.Label(self.root, text='What would you like to learn about?', width=80, height=10, bg="#d0e7ff", fg="black")
        w.pack(pady=10)
        # buttons for Welcome menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        # How to play instruct
        btn = tk.Button(button_frame, command=lambda: self.end_instructions(how_to_play_madlibs, False), text="How to play Madlibs", bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=0, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # Load inputs button todo: integrate all other instruction menus
        btn = tk.Button(button_frame, command=lambda: self.write_instructions_menu(), text="How to write madlibs",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=2, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # Instruction menu button
        btn = tk.Button(button_frame, command=lambda: self.end_instructions(loading_a_madlib,False), text="Loading a madlib",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=3, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        btn = tk.Button(button_frame, command=lambda: self.end_instructions(printing_madlibs,False), text="Printing madlibs",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=4, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        self.root.mainloop()  # deploys the GUI screen till closed #todo: test if needed
    def write_instructions_menu(self):
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        self.display = scrolledtext.ScrolledText(self.root, width=80, height=10, font=("Arial", 12), bg="#9cc9e0",
                                                 fg="black", wrap=tk.WORD)
        self.display.pack(pady=10)
        self.display.insert(tk.END, how_to_write_a_madlib)
        #self.display.insert(tk.END, content.replace("\\n", "\n"))
        self.display.config(state='disabled')  # Make it read-only
        # buttons for Welcome menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        # Generic words
        btn = tk.Button(button_frame, command=lambda: self.end_instructions(generic_words_list,True), text="Generic words",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=0, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        #numbered words
        btn = tk.Button(button_frame, command=lambda: self.end_instructions(numbered_words,True),
                        text="Numbered words",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=1, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # Custom words
        btn = tk.Button(button_frame, command=lambda: self.end_instructions(custom_words_basics,True),
                        text="Custom words basics",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=2, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # numbered custom words
        btn = tk.Button(button_frame, command=lambda: self.end_instructions(numbered_custom_words,True),
                        text="Numbered custom words",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=3, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # Custom dic
        btn = tk.Button(button_frame, command=lambda: self.end_instructions(prewriting_custom_configurations,True),
                        text="Preconfiguring custom words",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=4, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # back button

        btn = tk.Button(button_frame, command=lambda: self.instruct_main(), text="< Back to Instructions",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=2, column=1, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        #back to menu button
        btn = tk.Button(button_frame, command=lambda: self.reset(), text="<< Back to main menu",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=2, column=3, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
    def end_instructions(self,content,lv):#generic window for instructions at the end of the instruction tree.
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        self.display = scrolledtext.ScrolledText(self.root, width=80, height=10, font=("Arial", 12), bg="#9cc9e0",
                                                 fg="black", wrap=tk.WORD)
        self.display.pack(pady=10)
        self.display.insert(tk.END, content)
        #self.display.insert(tk.END, content.replace("\\n", "\n"))
        self.display.config(state='disabled')  # Make it read-only
        # buttons for Welcome menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames

        if lv==True: #second level of menus, currently only used in specifics of writing madlibs, change to an int if more are added
            btn = tk.Button(button_frame, command=lambda: self.write_instructions_menu(), text="< Back to writing madlibs",
                            bg="#3b9dd3", fg="white")
            btn.grid(row=1, column=1, padx=2, pady=2,
                     sticky="ew")
            btn = tk.Button(button_frame, command=lambda: self.instruct_main(), text="<< Back to Instructions",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
            btn.grid(row=1, column=2, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
            btn = tk.Button(button_frame, command=lambda: self.reset(), text="<<< Back to main menu",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
            btn.grid(row=1, column=3, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        else: #normal end instructions
            btn = tk.Button(button_frame, command=lambda: self.instruct_main(), text="< Back to Instructions",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
            btn.grid(row=1, column=1, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
            btn = tk.Button(button_frame, command=lambda: self.reset(), text="<< Back to main menu",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
            btn.grid(row=1, column=3, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
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
        if self.mode==0:#manual input
            self.raw_in = self.input_entry.get()
        elif self.mode==1: #from file
            pass
        else:
            self.dummyscreen('Invalid mode for advance_from_first()')

        #self.userMadlib = re.findall(r'/\w+\d*_[0-9]+|/\w+\d*|[^\s\w]|[\w]+', self.raw_in)
        self.userMadlib= self.raw_in.split(' ') #todo: try and make all splits like this and integrate previous version's solution to quote problems
        self.prompt_words = iter(self.userMadlib)
        #self.outlist = []
        # Extract and sort custom keys
        all_custom_matches = re.findall(r'/ct(\d+)(?:_\d+)?', self.raw_in)
        self.custom_keys = sorted(set(f"/ct{id}" for id in all_custom_matches), key=lambda x: int(x[3:]))


        if self.custom_keys and self.custom=={}:

            self.custom_configure_window() #configure customs, file_choice will be executted as well
        else: #if manual input and no others are needed
            self.title_check()
            #self.file_choice()
        #else:
        #    self.advance_to_second()

    def title_check(self):
        if self.title:
            self.file_choice()
        else:
            print("no title")
            self.title_write()
    def title_write(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Would you like to title your Madlib?\n Type it here and click enter or \"skip\" to skip this step.", font=("Arial", 12, "bold")).pack()
        self.input_entry = tk.Entry(self.root, font=("Arial", 14), width=80, bg="#d0e7ff", fg="black")
        self.input_entry.bind("<Return>",
                              lambda event: self.title_saver())
        self.input_entry.pack(pady=10)
        self.input_entry.focus_set()  # automatically puts the cursor into the entry field
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        # Yes button
        btn = tk.Button(button_frame, command=lambda: self.title_saver(), text="Submit", bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=0, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # no button
        btn = tk.Button(button_frame, command=lambda: self.file_choice(), text="Skip",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=2, padx=2, pady=2,
                 sticky="ew")
        #self.root.mainloop()  # deploys the GUI screen till closed
    def title_saver(self):
        self.title = self.input_entry.get().strip()
        self.file_choice()
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
        self.root.mainloop()  # deploys the GUI screen till closed

    def prompt_next_custom(self):
        if self.custom_index < len(self.custom_keys):
            current_key = self.custom_keys[self.custom_index]
            self.display.insert(tk.END, f"Custom {current_key[3:]}: ")
        else:
            #print("No more Customs")
            self.title_check()
            #self.file_choice()
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
                self.save_key = realkey
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
                self.save_key = realkey
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
                num = ''.join(re.findall(r'_(\d+)', self.current_word))
                #tailkey = re.findall(tail, self.current_word) #todo: restore if numcustwords have issues
                #tailkey = ''.join(tailkey)
                #regnum = re.findall(r'\d+', tailkey)
                #num = ''.join(regnum)
                self.save_key = realkey
                if realkey not in numword_dic:# todo: fix unconfigged numbered customs, try adding "and base in self.custom"
                    # numbered cust unsaved
                    base = re.findall(customreg, self.current_word)
                    base = ''.join(base)
                    self.display.insert(tk.END, f"{self.custom[base]} :\n")
                    self.save_flag = True
                    #self.save_key = realkey
                    return
                elif realkey in numword_dic:
                    print("I'm a saved word " + str(realkey) + " " + str(numword_dic[realkey]))
                    self.current_word = re.sub(realkey, numword_dic[realkey], self.current_word)
                    # numbered cust saved
                elif base not in self.custom:
                    # numbered cust unsaved
                    self.display.insert(tk.END,
                                        f"{realkey} hasn't been configured, what would you like to replace it with?:\n")
                    self.save_flag = True
                    #self.save_key = realkey
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
                self.save_key = realkey
                if realkey not in numword_dic.keys() and base in generic_words.keys():
                    self.display.insert(tk.END, f"{generic_words[base]}:\n")
                    self.save_flag = True
                    #self.save_key = realkey
                    return
                    # numbered unsaved
                    # outlist.append(keyword_convert(realkey, self.current_word, 1, None))
                elif realkey not in numword_dic.keys() and base not in generic_words.keys():
                    self.display.insert(tk.END,
                                        f"{realkey} is not a valid keyword, what would you like to replace it with?:\n")
                    return
                    # outlist.append(keyword_convert(realkey, self.current_word, 6, None))  # invalid
                elif realkey in numword_dic.keys():
                    self.current_word =  re.sub(realkey, numword_dic[realkey], self.current_word)
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
        # buttons for file naming menu selection
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
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        self.file_write(self.raw_in+'\n'+'<C>'+str(self.custom), base, 'inputs','.txt')#todo: add title
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
        print(self.title)
        display = scrolledtext.ScrolledText(self.root, width=80, height=20, font=("Arial", 12), bg="#9cc9e0",
                                            fg="black")
        display.pack(pady=20)
        # final_output = re.sub(r'\s([.,!?;:])', r'\1', ' '.join(self.outlist))
        display.insert(tk.END, "\nHere is your Madlib:\n" + self.raw_in)
        w = tk.Label(self.root, text='What would you like to do with it?', width=40, height=5, bg="#d0e7ff",
                     fg="black")
        w.pack(pady=5)
        # buttons for Welcome menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        #Yes button
        btn = tk.Button(button_frame, command=lambda: self.in_file_name(), text="Save", bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=0, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # no button
        btn = tk.Button(button_frame, command=lambda: self.advance_to_second(), text="Play without saving", bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=2, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        btn = tk.Button(button_frame, command=lambda: self.advance_to_html(), text="Print HTML",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=4, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        self.root.mainloop()  # deploys the GUI screen till closed
    def process_next_keyword(self): #todo: use self.display.insert(tk.END, f"{user_input}\n") to show recorded word
        user_text = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        if user_text and self.save_flag == False:
            self.outlist.append(re.sub(self.save_key, user_text, self.current_word))
        elif user_text and self.save_flag == True:
            self.outlist.append(re.sub(self.save_key, user_text, self.current_word))
            numword_dic[self.save_key]=user_text
            #print("I'm saving ",str(self.save_key),' as ',str(self.current_word))
            self.save_flag=False
        else:
            pass
        self.next_prompt()

    def normalize_quotes(self, text):
        return text.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
    def smart_join(self, words):  # removes spaces surrounding punctuation
        result = ""
        prev_word = ""
        quote_flag = False  # indicates being part of a quote segment
        for i, word in enumerate(words):
            word=self.normalize_quotes(word)
            if i == 0:  # first word, no space before
                result += word
                if word=="\"":  # if the first element is a quote, turn on quote flag
                    quote_flag = True
            elif re.match(r"[.,!?;:\']", word) or re.match(r"[\']", prev_word):  # If it's punctuation, don't add space
                result += word
            elif word=="\"" and quote_flag == False:  # Open quote, space before, turn on quote flag
                result += " " + word
                quote_flag = True
            elif word=="\"" and quote_flag == True:  # close quote, no space before, turn off quote flag
                result += word
                quote_flag = False
            elif prev_word=="\"" and quote_flag == True:  # word after open quote, no leading space
                result += word
            # elif re.match(r"[\"]", prev_word) and quote_flag==False: #word after close quote, no leading space, turn off quote flag
            #    result += " " + word

            else:
                result += " " + word
            prev_word = word
        return result



    def third_window(self):  #decide whether to save filled output
        for widget in self.root.winfo_children():
            widget.destroy()
        display = scrolledtext.ScrolledText(self.root, width=80, height=20, font=("Arial", 12), bg="#9cc9e0", fg="black")
        display.pack(pady=20)
        self.filled = re.sub(r'\s([.,!?;:])', r'\1', ' '.join(self.outlist))

        if self.title:
            self.filled=self.title+"\n\n"+self.filled

        display.insert(tk.END, "\nHere is your filled Madlib:\n" + self.filled)
        w = tk.Label(self.root, text='What would you like to do with it?', width=40, height=5, bg="#d0e7ff",
                     fg="black")
        w.pack(pady=5)
        # buttons for Welcome menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        # Yes button
        btn = tk.Button(button_frame, command=lambda: self.plain_file_name(), text="Save", bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=0, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # no button
        btn = tk.Button(button_frame, command=lambda: self.reset(), text="Return to menu",
                        bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=2, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)

    def plain_file_name(self):
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        w = tk.Label(self.root, text='Enter the filename you\'d like to save to (no extension)', width=80, height=10,
                     bg="#d0e7ff",
                     fg="black")
        w.pack(pady=10)
        # buttons for file naming menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        self.input_entry = tk.Entry(self.root, font=("Arial", 14), width=80, bg="#d0e7ff", fg="black")
        self.input_entry.bind("<Return>",
                              lambda event: self.output_save(0))  # allows the "enter" key to submit the keyword
        self.input_entry.pack(pady=10)
        self.input_entry.focus_set()  # automatically puts the cursor into the entry field
        self.submit_btn = tk.Button(self.root, text="Submit", command=lambda: self.output_save(0), bg="#3b9dd3",
                                    fg="white")
        self.submit_btn.pack(pady=10)

    def invalid_html_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.display = scrolledtext.ScrolledText(self.root, width=80, height=10, font=("Arial", 12), bg="#9cc9e0",
                                                 fg="black")
        self.display.pack(pady=10)
        # define and create entry field for user's entry for a word
        self.input_entry = tk.Entry(self.root, font=("Arial", 14), width=80, bg="#d0e7ff", fg="black")
        self.input_entry.bind("<Return>",
                              lambda event: self.process_invalid_html())  # allows the "enter" key to submit the keyword
        self.input_entry.pack(pady=10)
        self.input_entry.focus_set()  # automatically puts the cursor into the entry field

        self.submit_btn = tk.Button(self.root, text="Submit", command=self.process_invalid_html, bg="#3b9dd3",
                                    fg="white")
        self.submit_btn.pack(pady=10)

    def html_replace_C(self): #todo: decide between original (had length bugs) and "_C." if "_C" then refactor keyword replacement to match this
        try:
            while True:
                self.current_word = next(self.html_words)
                final = '[undefined]'
                if re.findall(unnumbered, self.current_word) and not re.findall(numbered,
                                                                                self.current_word) and not re.findall(
                        customreg, self.current_word):
                    regkey = re.findall(unnumbered, self.current_word)
                    realkey = ''.join(regkey)
                    self.save_key=realkey
                    if realkey in generic_words:
                        htword = htmlsample.replace('underscript', generic_words[realkey])
                        final = self.current_word.replace(realkey, htword, 1)
                    elif realkey in ignored_words:
                        final = self.current_word
                    else:
                        self.display.insert(tk.END, f"{realkey} is not a valid keyword, what is it?:\n")
                        return

                elif re.findall(customreg, self.current_word) and not re.findall(numcustreg, self.current_word):
                    regkey = re.findall(customreg, self.current_word)
                    realkey = ''.join(regkey)
                    if realkey in self.custom:
                        htword = htmlsample.replace('underscript', self.custom[realkey])
                        final = self.current_word.replace(realkey, htword, 1)
                    else:
                        self.display.insert(tk.END, f"{realkey} is not a valid keyword, what is it?:\n")
                        return

                elif re.findall(numcustreg, self.current_word):
                    regkey = re.findall(numcustreg, self.current_word)
                    realkey = ''.join(regkey)
                    base = ''.join(re.findall(customreg, self.current_word))
                    num = ''.join(re.findall(r'_(\d+)', self.current_word))
                    #num = ''.join(re.findall(r'\d+', self.current_word))
                    htword = htmlsample.replace('underscript', self.custom[base] + ' (' + num + ')')
                    final = self.current_word.replace(realkey, htword, 1)

                elif re.findall(numbered, self.current_word):
                    regkey = re.findall(numbered, self.current_word)
                    regkeyb = re.findall(unnumbered, self.current_word)
                    realkey = ''.join(regkey)
                    base = ''.join(regkeyb)
                    num = ''.join(re.findall(r'\d+', realkey))
                    self.save_key = realkey
                    if base in generic_words:
                        htword = htmlsample.replace('underscript', generic_words[base] + ' (' + num + ')')
                        final = self.current_word.replace(realkey, htword, 1)
                    else:
                        self.display.insert(tk.END, f"{realkey} is not a valid keyword, what is it?:\n")
                        return
                else:
                    final = self.current_word

                self.htlist.append(final)

        except StopIteration:
            self.html_post_process()

    def advance_to_html(self):
        #user_input = self.raw_in
        #self.userMadlib = re.findall(r'/\w+\d*_[0-9]+|/\w+\d*|[^\s\w]|[\w]+', user_input)
        self.userMadlib=self.raw_in.split(' ')
        self.html_words = iter(self.userMadlib)
        self.invalid_html_window()
        self.html_replace_C()

    def process_invalid_html(self):
        user_text = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)
        user_ht = htmlsample.replace('underscript', user_text)
        self.htlist.append(user_ht)
        self.html_replace_C()
    def html_post_process(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        #self.html_out=self.smart_join(self.htlist)
        self.html_out = re.sub(r'\s([.,!?;:])', r'\1', ' '.join(self.htlist))
        if self.title:
            self.html_out = htmlhead.replace('heading', self.title, 1) + self.html_out + ' </p></body></html>'
        else:
            self.html_out = htmlhead_notitle + self.html_out + ' </p></body></html>'
        self.html_file_choice()

    def html_file_choice(self):
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        w = tk.Label(self.root, text='Before we print your Madlib, would you like to save it?', width=80, height=10, bg="#d0e7ff",
                     fg="black")
        w.pack(pady=10)
        # buttons for Welcome menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        #Yes button
        btn = tk.Button(button_frame, command=lambda: self.html_file_name(), text="Save", bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=0, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        # no button
        btn = tk.Button(button_frame, command=lambda: self.html_view(), text="Print without saving", bg="#3b9dd3",
                        fg="white")  # defines each button with frame,
        btn.grid(row=1, column=2, padx=2, pady=2,
                 sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
        self.root.mainloop()  # deploys the GUI screen till closed

    def html_file_name(self):
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        w = tk.Label(self.root, text='Enter the filename you\'d like to save to (no extension)', width=80, height=10,
                     bg="#d0e7ff",
                     fg="black")
        w.pack(pady=10)
        # buttons for file naming menu selection
        button_frame = tk.Frame(self.root)  # defines the button frame
        button_frame.pack(pady=5)  # for all button frames
        self.input_entry = tk.Entry(self.root, font=("Arial", 14), width=80, bg="#d0e7ff", fg="black")
        self.input_entry.bind("<Return>",
                              lambda event: self.output_save(1))  # allows the "enter" key to submit the keyword
        self.input_entry.pack(pady=10)
        self.input_entry.focus_set()  # automatically puts the cursor into the entry field
        self.submit_btn = tk.Button(self.root, text="Submit", command=lambda: self.output_save(1), bg="#3b9dd3",
                                    fg="white")
        self.submit_btn.pack(pady=10)
    def output_save(self,md):
        base = self.input_entry.get().strip()
        for widget in self.root.winfo_children(): widget.destroy()  # removes pre-existing widgets
        if md==0: #plain save
            self.file_write(self.normalize_quotes(self.filled), base, 'outputs', '.txt')  # todo: add title
            w = tk.Label(self.root, text='Your filled mandlib has been saved to: ' + str(
                base) + '.txt in your \"outputs\" folder.\nWe hope you liked it!',
                         width=80, height=10, bg="#d0e7ff",
                         fg="black")
            w.pack(pady=10)
            self.submit_btn = tk.Button(self.root, text="Back to menu", command=lambda: self.reset(), bg="#3b9dd3",
                                        fg="white")
            self.submit_btn.pack(pady=10)
        elif md==1: #html save
            
            self.file_write(self.html_out, base, 'outputs',
                            '.html')  # todo: include selected (or loaded) title and formatting from terminal version
            w = tk.Label(self.root, text='Your mandlib has been saved to: ' + str(
                base) + '.html in your \"outputs\" folder.\nNow let\'s print it!',
                         width=80, height=10, bg="#d0e7ff",
                         fg="black")
            w.pack(pady=10)
            self.submit_btn = tk.Button(self.root, text="Let's Go", command=lambda: self.html_view(), bg="#3b9dd3",
                                        fg="white")
            self.submit_btn.pack(pady=10)
        else: #plain and all invalids
            
            self.file_write(self.html_out, base, 'outputs',
                            '.txt')  # todo: include selected (or loaded) title and formatting from terminal version
            w = tk.Label(self.root, text='Invalid save case found, please contact the developer.\n In the meantime, your mandlib has been saved to: ' + str(
                base) + '.txt in your \"outputs\" folder.',
                         width=80, height=10, bg="#d0e7ff",
                         fg="black")
            w.pack(pady=10)
            self.submit_btn = tk.Button(self.root, text="Ok", command=lambda: self.html_view(), bg="#3b9dd3",
                                        fg="white")
            self.submit_btn.pack(pady=10)
    def html_view(self):

        self.root.destroy()  # closes the gui entirely todo: decide whether to quit the window here
        messagebox.showinfo("Thank you.", "We'll uploaded your madlib to your browser, you can print it from there.")
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html") as f:
            f.write(self.html_out)
            webbrowser.open(f.name)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Madlib App")
    app = MadlibApp(root)
    root.mainloop()
