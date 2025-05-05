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
root = tk.Tk()
customreg = "(/ct[0-9]+)"
custom={}
def in_out(input):
    out = input
    return out




def dummyscreen(name):
    for widget in root.winfo_children(): widget.destroy()  # removes pre-existing widgets
    text= "This is the screen for " + str(name)
    w = tk.Label(root, text=text, width=80, height=10, bg="#d0e7ff", fg="black")
    w.pack(pady=10)


# menuHandler returns the unprocessed user madlib or empty string to retry
def welcomeMenuHandler():
    #for widget in root.winfo_children(): widget.destroy()  # removes pre-existing widgets
    local_custom={}
    save_manual_file = True #assume autosave of custom words file will happen
    # print("User selects:", choice)

    #Welcome Menu
    #welcome text
    w = tk.Label(root, text='Hello, Welcome to the Madlib Maker', width=80, height=10, bg="#d0e7ff", fg="black")
    w.pack(pady=10)
    #buttons for Welcome menu selection
    button_frame = tk.Frame(root)  # defines the button frame
    button_frame.pack(pady=5) #for all button frames
    #manual input button
    btn = tk.Button(button_frame,  command=lambda: dummyscreen('enterMadlibManual()'), text="Manual Input", bg="#3b9dd3",
                    fg="white")  # defines each button with frame, todo: add argument: command= enterMadlibManual()
    btn.grid(row=1, column=0, padx=2, pady=2,
             sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
    #Load inputs button
    btn = tk.Button(button_frame, text="Load a Madlib", bg="#3b9dd3",
                    fg="white")  # defines each button with frame, todo: add argument: command= [file namer function]
    btn.grid(row=1, column=2, padx=2, pady=2,
             sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)

    root.mainloop()
    base_name = "" #declair string for name of file, no extension
    choice=0 #temporary
    #If structure will be replaced by each button
    if choice == "1":
        # print("Manual input")
        userMadlib = "pretend I got the madlib from enterMadlibManual()"
        savequest = raw_input("Would you like to save?\n")
        if savequest == "yes":
            base_name = raw_input("Enter your desired filename (without extention)\n")
            #file_write(' '.join(userMadlib), base_name, 'inputs', '.txt')
            #File write procedure
        elif savequest == "no":
            save_manual_file = False
        else:
            #print(potato)
            exit()
    elif choice == "2":
        # print("From file")
        filename = input("Enter a madlib filename with the extension:\n")
        base_name = os.path.splitext(filename)[0]
        #userMadlib = enterMadlibFile(filename)
    elif choice == "3":
        #instructionsMenuHandler()
        userMadlib = ""
    else:#not needed for GUI buttons
        # print("invalid entry")
        userMadlib = ""
        #print(potato)
        #exit()

    #if userMadlib is not "":
    #    local_custom = "pretend I got checked by customWordsFilter(userMadlib, base_name, save_manual_file)"
    return userMadlib, local_custom

# reads a custom file, returns



def GUImenu():
    #root = tk.Tk()
    w = tk.Label(root, text='This is a menu \n here\'s your output!',width=80, height=10, bg="#d0e7ff", fg="black")
    w.pack(pady=10)
    out = scrolledtext.ScrolledText(root, width=80, height=10, font=("Arial", 12), bg="#9cc9e0", fg="black")
    out.insert(tk.END,"out")
    out.pack(pady=10)
    root.mainloop()

# Main function
def main():
    global custom

    userMadlib, custom = welcomeMenuHandler()  # Call the function and unpack the return values
    print("userMadlib:", str(userMadlib))      # Print userMadlib as a string
    print("custom:", str(custom))              # Print custom as a string
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
