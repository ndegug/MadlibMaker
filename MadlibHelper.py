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

# Returns file generated madlib



def madlibMainMenuHandler(choice, userMadlib, custom):
    #print("user choice:", choice)
    filledMadlib = None
    if choice == "1":
        print("Fill in")
        filledMadlib = fillInMadlib(userMadlib, custom)
        print(' '.join(filledMadlib))
        choice = raw_input("Would you like to save this filled madlib to the \"outputs\" folder?\n")
        if choice == 'yes':
            filename = raw_input("What do you wish to name the file? (do not type the extension): ")
            file_write(' '.join(filledMadlib), filename, 'outputs', '.txt')
            print("Your filled madlib has been saved to the outputs folder, have a good day!")
        elif choice == 'no' or choice == '':
            print("Have a good day!")
        else:
            print(potato2)
            exit()
    elif choice == "2":
        print("print physical")
        htmlList = createHtmlMadlib(userMadlib)
        latfill = ' '.join(htmlList)
        head = raw_input("What would you like to title this madlib?\n")
        latfill = htmlhead.replace('heading', head, 1) + latfill + ' </p></body></html>'
        filename = raw_input("What do you wish to name the file? (do not type the extension):\n")
        file_write(latfill, filename, 'outputs', '.html')
        print("An HTML coded version of your unfilled madlib has been saved to the outputs folder, "
              "drag the file into your browser to view it. Print the file using your respective browser's print "
              "feature.\n "
              "Have a good day!")
    elif choice == "3":
        print("Have a good day!")
    else:
        # print(potato)
        print("Invalid instruction choice:", choice, "Please try again...")
    return filledMadlib


def instructionsMenuHandler():
    choice = ""
    while choice != "q":
        choice = raw_input(instruct0)
        if choice == "1":  # todo add a "process pre-made file" instructions
            print(instruct1) # How to write madlibs
        elif choice == "2":
            print("The default keys and word categories are as follows:")
            printCleanColumns(generic_words) # generic words list
        elif choice == "3":
            print(instruct3) # custom words
        elif choice == "4":
            print(instruct4) # outputs
        elif choice == "5":
            print(instruct5) # outputs
        elif choice == "q":
            return
        else:
            # print(potato)
            print("Invalid instruction choice:", choice, "Please try again...")
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
    btn = tk.Button(button_frame,command=lambda: dummyscreen('[new file read function]'), text="Load a Madlib", bg="#3b9dd3",
                    fg="white")  # defines each button with frame, todo: add argument: command= [file namer function]
    btn.grid(row=1, column=2, padx=2, pady=2,
             sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
    #Instruction menu button
    btn = tk.Button(button_frame, command=lambda: dummyscreen('instructionsMenuHandler()'), text="Instructions",
                    bg="#3b9dd3",
                    fg="white")  # defines each button with frame, todo: add argument: command= instructionsMenuHandler()
    btn.grid(row=1, column=3, padx=2, pady=2,
             sticky="ew")  # defines the button's location on the grid ("ew" centers all buttons to their grid position)
    root.mainloop() #deploys the GUI screen till closed
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
            print(potato)
            exit()
    elif choice == "2":
        # print("From file")
        filename = input("Enter a madlib filename with the extension:\n")
        base_name = os.path.splitext(filename)[0]
        #userMadlib = enterMadlibFile(filename)
    elif choice == "3":
        instructionsMenuHandler()
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



# checks string for custom words
def checkForCustomWords(madlib):

    return False


def quoteConverter(text):

    #print(text)
    print('\\\\xc2\\\\xa0')

    return text
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
    print("userMadlib:", str(userMadlib))  # Print userMadlib as a string
    print("custom:", str(custom))  # Print custom as a string
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
