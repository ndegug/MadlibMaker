import os

from MadlibMakerHelpers import *

from pip._vendor.distlib.compat import raw_input

outlist = []

latlist = []



if not os.path.isdir(os.path.join(os.getcwd(), "inputs")):
    os.mkdir(os.path.join(os.getcwd(), "inputs"))
if not os.path.isdir(os.path.join(os.getcwd(), "outputs")):
    os.mkdir(os.path.join(os.getcwd(), "outputs"))





choice = raw_input(
    "Welcome to the Madlib Maker\nHere you can compose and fill in madlibs using our specialized syntax.\nTo begin, "
    "please select from the following menu options:\n1. Type madlib\n2. Use a madlib from the \"inputs\" folder.\n3. "
    "Instructions\n")
if choice == "1":
    # manual input
    cont = raw_input("Enter the madlib below:\n")
    inputList = cont.split(" ")
    if re.search(customreg, str(inputList)) is not None:
        cust_config()
    else:
        pass
    choice = raw_input("Would you like to save your madlib to the inputs folder before filling it?\n")
    if choice == "yes":
        filename = raw_input("What do you wish to name the file? (do not type the extension): ")
        # main content file
        file_write(' '.join(inputList), filename, 'inputs', '.txt')
        # custom words file
        if re.search(customreg, str(inputList)) is not None:
            file_write(str(custom), filename, 'inputs', '_cts.txt')
        else:
            pass
        choice = raw_input("Your Madlib has been saved under the inputs folder, would you like to process it in now?\n")
        if choice == "yes":
            print("")
        elif choice == "no":
            print("Have a good day")
            exit()
        else:
            print(potato2)
            exit()
    elif choice == "no" or choice == "":
        pass
    else:
        print(potato2)
        exit()
elif choice == "2":
    # file base name
    file_read()
    # filename = raw_input("Which file would you like to process? (type the name with no extension)\n")
    # # saving name of custom word file
    # customfile = filename + "_cts.txt"
    # # reading main content file
    # choice = os.path.join('inputs', filename + ".txt")
    # my_file = open(choice, "r")
    # cont = my_file.read()
    # inputList = cont.split(" ")
    # if os.path.exists(os.path.join('inputs', customfile)):
    #     choice = os.path.join('inputs', customfile)
    #     with open(choice) as f:
    #         data = f.read()
    #     custom = json.loads(data.replace("\'", "\""))
    #     f.close()
    # elif not os.path.exists(os.path.join('inputs', customfile)) and re.search(customreg, str(inputList)) is not None:
    #     cust_config()
    #     file_write(str(custom), filename, 'inputs', '_cts.txt')
    # else:
    #     pass
elif choice == "3":
    while choice != "q":
        choice = raw_input("Which would you like to learn about:\n1. How to write Madlibs\n2. "
                           "Syntax\n3. Custom Words\n4. Saving and printing madlibs\nType \"q\" to quit\n")
        if choice == "1":  # todo add a "process pre-made file" instructions
            print("Here in the Madlib Maker, you can write a Madlib directly or process a file you've already "
                  "typed.\nFor "
                  "each blank, you must type a keyword specific to the word category you desire.\nThese keywords "
                  "typically follow "
                  "the syntax of 3 letters preceded by a \"/\", for example,\ntyping the keyword \"/adj\" will prompt "
                  "the "
                  "program to ask the user for an \"Adjective.\"\nSee the Syntax section for the full list of "
                  "keywords.\nYou can add a number at the end of any keyword in the program's dictionary to repeat it "
                  "within\nthe "
                  "same madlib.\n\nFor example, if the input is:\n\"We have a pet /ani1, he's a good /ani1!\"\nand "
                  "you "
                  "enter \"dog\" when prompted, the program will fill in both at the same time resulting in:\n\"We "
                  "have "
                  "a pet dog, he's a good dog!\"\n\nIf you wish to use a word that is not in "
                  "this program's selection,\nyou may enter it as a "
                  "custom word. These custom words can be\nconfigured before writing the Madlib.\nSee the \"Custom "
                  "Words\" "
                  "section for further details.\n")
        elif choice == "2":
            print("The default keys and word categories are as follows:")
            i = 0
            for pair in generic_words.items():
                i = i + 1
                if i < 3:
                    print(pair, end='\t')
                else:
                    print(pair, end='\n')
                    i = 0
            print("\n")

        elif choice == "3":
            print(
                "Custom words allow you to add your own word categories if they are not already stored in this "
                "program's dictionary.\nIf you wanted the program to call out something obscure like \"Baseball "
                "player\" "
                "or \"High school friend\", you can use this feature to do so.\nWhen questioned whether you wish to "
                "configure the custom words, type \"yes\""
                "and enter these words sequentially. Once your custom words are configured,\nuse the keyword "
                "sequence: "
                "\"/ct1\" where the number indicates which sequential word you want to be called there.\n\nIf you "
                "want a specific custom word entry to automatically entered several times, use a numbered\ncustom "
                "word key such as:\"/ct1_1.\" This key will be interperated as a numbered word (see the \"How\nto "
                "write Maldibs\" instructions section "
                "for more details) and any word that is used to replace it will then replace all other\nwords "
                "with that same key")
        elif choice == "4":
            print("After writing a madlib, you can save it to the \"inputs\" folder for later use.\nThis is usefull "
                  "if you have a lengthy madlib that you wish to fill in later or multiple times.\nIf you wish to "
                  "type a madlib outside of this program, note that the current build accepts text files only and "
                  "refrain from adding a title/heading "
                  "as it will be entered later in the program.\nReview the \"Syntax\" section of the instructions for "
                  "the proper syntax of an input file.\n\nWith a madlib typed or selected, you may chose to fill it "
                  "within the program or\nprint it as a traditional unfilled maldib on paper.\nOutputs of either "
                  "nature will be saved to the \"outputs\" folder.\nThe filled madlibs will be saved as a text file "
                  "while traditional madlibs will be converted into\nHTML files designed to display the heading and "
                  "blanks with word categories underneath. Drag the\nHTML file into any web browser to view it in "
                  "the traditional madlib format, then use the respective\nbrowser's print feature to print a "
                  "physical copy of the madlib.")
        elif choice == "q":
            print("I hope these instructions helped, start the program again to give it a try!\nHave a good day!")
            exit()
        else:
            print(potato)
            exit()

else:
    print(potato)
    exit()


regkey = ""
realkey = ""

htmlhead = '<html><head></head><body><h1> heading </h1><style>h1 {text-align: center;}p.big {  line-height: ' \
           '2;}.tab { display: inline-block; margin-left: 80px;}  </style><p class="big"><span class="tab"></span>'

choice2 = raw_input("Do you wish to:\n1. Fill in your madlib now\n2. Print a physical version\n3. Quit\n")
if choice2 == "1" or choice2 == "2":
    pass
elif choice2 == "3":
    print("Have a good day!")
    exit()
else:
    print(potato2)
    exit()
print(custom)
for word in inputList:
    if re.findall(unnumbered, word) and not re.findall(numbered, word) and not re.findall(customreg, word):
        # unnumbered
        regkey = re.findall(unnumbered, word)
        realkey = ''.join(regkey)
        if choice2 == "1" and realkey in generic_words:
            outlist.append(keyword_convert(realkey, word, 0))
        elif choice2 == "1" and realkey not in generic_words:
            outlist.append(keyword_convert(realkey, word, 6))
        elif choice2 == "2" and realkey in generic_words.keys():
            latword = htmlsample.replace('underscript', generic_words[realkey])
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
        elif choice2 == "2" and realkey not in generic_words.keys():
            latlist.append(invalid_html(0, realkey, word))
    elif re.findall(customreg, word) and not re.findall(numcustreg, word):
        # custom
        regkey = re.findall(customreg, word)
        realkey = ''.join(regkey)
        if choice2 == "1" and realkey in custom:
            outlist.append(keyword_convert(realkey, word, 3))
        # latex array
        elif choice2 == "1" and realkey not in custom:
            outlist.append(keyword_convert(realkey, word, 5))
        elif choice2 == "2" and realkey in custom:
            # saved
            latword = htmlsample.replace('underscript', custom[realkey])
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
        elif choice2 == "2" and realkey not in custom:
            latlist.append(invalid_html(1, realkey, word))
        else:
            # html equivelent

            latword = htmlsample.replace('underscript', 'Undefined')

            final = word.replace(realkey, latword, 1)
            latlist.append(final)
    elif re.findall(numcustreg, word):
        # numberded custom

        regkey = re.findall(numcustreg, word)
        realkey = ''.join(regkey)

        base = re.findall(customreg, word)
        base = ''.join(base)

        tailkey = re.findall(tail, word)
        tailkey = ''.join(tailkey)
        regnum = re.findall(r'\d+', tailkey)
        num = ''.join(regnum)

        if choice2 == "1" and realkey not in numword_dic:
            # numbered cust unsaved
            outlist.append(keyword_convert(realkey, word, 4))
        elif choice2 == "1" and realkey in numword_dic:
            # numbered cust saved
            outlist.append(keyword_convert(realkey, word, 2))
        elif choice2 == "1" and base not in custom:
            # numbered cust saved
            outlist.append(keyword_convert(realkey, word, 5))
        elif choice2 == "2":
            latword = htmlsample.replace('underscript', custom[base] + ' (' + str(num) + ')')
            final = word.replace(realkey, latword, 1)
            latlist.append(final)

    elif re.findall(numbered, word):
        # numbered
        regkey = re.findall(numbered, word)
        regkeyb = re.findall(unnumbered, word)
        realkey = ''.join(regkey)
        base = ''.join(regkeyb)
        regnum = re.findall(r'\d+', realkey)
        num = ''.join(regnum)
        if choice2 == "1" and realkey not in numword_dic.keys() and base in generic_words.keys():
            # numbered unsaved
            outlist.append(keyword_convert(realkey, word, 1))
        elif choice2 == "1" and realkey not in numword_dic.keys() and base not in generic_words.keys():
            outlist.append(keyword_convert(realkey, word, 6))#invalid
        elif choice2 == "1" and realkey in numword_dic.keys():
            outlist.append(keyword_convert(realkey, word, 2))#numbered saved
        elif choice2 == "2" and base in generic_words.keys():
            latword = htmlsample.replace('underscript', generic_words[base] + ' (' + str(num) + ')')
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
        elif choice2 == "2" and base not in generic_words.keys():
            latlist.append(invalid_html(0, realkey, word))
    else:
        # none, just append
        if choice2 == "1":
            outlist.append(word)
        # #Latex array
        latlist.append(word)

filled = ' '.join(outlist)
latfill = ' '.join(latlist)
filled = quote_convert(filled)
latfill = quote_convert(latfill)
if choice2 == "1":
    print(filled)
    choice = raw_input("Would you like to save this filled madlib to the \"outputs\" folder?\n")
    if choice == 'yes':
        filename = raw_input("What do you wish to name the file? (do not type the extension): ")
        file_write(filled, filename, 'outputs', '.txt')
        print("Your filled madlib has been saved to the outputs folder, have a good day!")
    elif choice == 'no' or choice == '':
        print("Have a good day!")
    else:
        print(potato2)
        exit()
elif choice2 == '2':
    head = raw_input("What would you like to title this madlib?\n")
    latfill = htmlhead.replace('heading', head, 1) + latfill + ' </p></body></html>'
    filename = raw_input("What do you wish to name the file? (do not type the extension):\n")
    file_write(latfill, filename, 'outputs', '.html')
    print("An HTML coded version of your unfilled madlib has been saved to the outputs folder, "
          "drag the file into your browser to view it. Print the file using your respective browser's print feature.\n"
          "Have a good day!")
elif choice == 'no' or choice == '':
    print("Have a good day!")
else:
    print(potato2)
    exit()