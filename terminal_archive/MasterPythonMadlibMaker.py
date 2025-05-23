from terminal_archive.MadlibMakerHelpers import *
from terminal_archive.long_strings import *
from past.builtins import raw_input

custom = {}


def customWordsFilter(inputList, base_name, saveFileOverride):
    customfile = base_name + "_cts.txt"
    if os.path.exists(os.path.join('../inputs', customfile)):
        choice = os.path.join('../inputs', customfile)
        with open(choice) as f:
            data = f.read()
        custom = json.loads(data.replace("\'", "\""))
        f.close()
    elif not os.path.exists(os.path.join('../inputs', customfile)) and re.search(customreg, str(inputList)) is not None:
        custom = cust_config(inputList)
        if saveFileOverride:
            file_write(str(custom), base_name, '../inputs', '_cts.txt')
    else:
        custom = None
    return custom


def createHtmlMadlib(userMadlib):
    print("create madlib html")
    latlist = []
    for word in userMadlib:
        if re.findall(unnumbered, word) and not re.findall(numbered, word) and not re.findall(customreg, word):
            # unnumbered
            regkey = re.findall(unnumbered, word)
            realkey = ''.join(regkey)

            if realkey in generic_words.keys():
                latword = htmlsample.replace('underscript', generic_words[realkey])
                final = word.replace(realkey, latword, 1)
                latlist.append(final)
            elif realkey in ignored_words:
                latlist.append(word)
            elif realkey not in generic_words.keys():
                latlist.append(invalid_html(0, realkey, word))
        elif re.findall(customreg, word) and not re.findall(numcustreg, word):
            # custom
            regkey = re.findall(customreg, word)
            realkey = ''.join(regkey)
            if realkey in custom:
                # saved
                latword = htmlsample.replace('underscript', custom[realkey])
                final = word.replace(realkey, latword, 1)
                latlist.append(final)
            elif realkey not in custom:
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

            if base in generic_words.keys():
                latword = htmlsample.replace('underscript', generic_words[base] + ' (' + str(num) + ')')
                final = word.replace(realkey, latword, 1)
                latlist.append(final)
            if base not in generic_words.keys():
                latlist.append(invalid_html(0, realkey, word))
        else:
            # none, just append
            # #Latex array todo: rename all latex referances to HTML
            latlist.append(word)
    return latlist


def fillInMadlib(userMadlib, custom):
    outlist = []
    for word in userMadlib:
        if re.findall(unnumbered, word) and not re.findall(numbered, word) and not re.findall(customreg, word):
            regkey = re.findall(unnumbered, word)
            realkey = ''.join(regkey)
            if realkey in generic_words:
                outlist.append(keyword_convert(realkey, word, 0, None))
            elif realkey in ignored_words:
                outlist.append(word)
            else:
                outlist.append(keyword_convert(realkey, word, 6, None)) #todo: Should prompt invalid key, investigate if this should force edge case 7 instead of 6

        elif re.findall(customreg, word) and not re.findall(numcustreg, word):
            # custom
            regkey = re.findall(customreg, word)
            realkey = ''.join(regkey)
            if realkey in custom:
                outlist.append(keyword_convert(realkey, word, 3, custom))
            # HTML array
            elif realkey not in custom:
                outlist.append(keyword_convert(realkey, word, 5, custom))


        # html equivelent

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

            if realkey not in numword_dic:
                # numbered cust unsaved
                strIdx = 4
            elif realkey in numword_dic:
                # numbered cust saved
                strIdx = 2
            elif base not in custom:
                # numbered cust unsaved
                strIdx = 5
            else:
                # others
                strIdx = 6
            outlist.append(keyword_convert(realkey, word, strIdx, custom))

        elif re.findall(numbered, word):
            # numbered
            regkey = re.findall(numbered, word)
            regkeyb = re.findall(unnumbered, word)
            realkey = ''.join(regkey)
            base = ''.join(regkeyb)
            regnum = re.findall(r'\d+', realkey)
            num = ''.join(regnum)
            if realkey not in numword_dic.keys() and base in generic_words.keys():
                # numbered unsaved
                outlist.append(keyword_convert(realkey, word, 1, None))
            elif realkey not in numword_dic.keys() and base not in generic_words.keys():
                outlist.append(keyword_convert(realkey, word, 6, None))  # invalid
            elif realkey in numword_dic.keys():
                outlist.append(keyword_convert(realkey, word, 2, None))  # numbered saved
        else:
            # none, just append
            outlist.append(word)
    return outlist


def printCleanColumns(inputWords):
    i = 0
    for pair in inputWords.items():
        i = i + 1
        if i < 3:
            print(pair, end='\t')
        else:
            print(pair, end='\n')
            i = 0
    print("\n")


# Returns manually entered madlib
def enterMadlibManual():
    print("User has selected to manually enter madlib")
    cont = raw_input("Enter the madlib below:\n")
    inputList = cont.split(" ")
    return inputList


# Returns file generated madlib
def enterMadlibFile(filename):
    custom = None
    if re.search("\.docx$", filename):
        # docx file
        customfile = filename.replace('.docx', '_cts.txt') #todo: investigate greyed variables
        base_name = filename.replace('.docx', '')
        cont = textract.process("inputs/" + filename)
        cont = quote_convert(str(cont))  # converts all instances of curly punctuaton in word
        cont = cont[2:len(cont) - 1]  # temporary solution that removes the body markers from word

    elif re.search("\.txt$", filename):
        customfile = filename.replace('.txt', '_cts.txt')
        base_name = filename.replace('.txt', '')
        # reading main content file
        choice = os.path.join('../inputs', filename)
        my_file = open(choice, "r", encoding="utf8") # new comma case
        cont = my_file.read()
    else:
        cont = ''
        customfile = ''
        base_name = ''
        print("file invalid")
        print(potato)
        quit()
    inputList = cont.split(" ")
    return inputList


def madlibMainMenuHandler(choice, userMadlib, custom):
    #print("user choice:", choice)
    filledMadlib = None
    if choice == "1":
        print("Fill in")
        filledMadlib = fillInMadlib(userMadlib, custom)
        print(str(filledMadlib))
        print(' '.join(filledMadlib))
        choice = raw_input("Would you like to save this filled madlib to the \"outputs\" folder?\n")
        if choice == 'yes':
            filename = raw_input("What do you wish to name the file? (do not type the extension): ")
            file_write(' '.join(filledMadlib), filename, '../outputs', '.txt')
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
        file_write(latfill, filename, '../outputs', '.html')
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


# menuHandler returns the unprocessed user madlib or empty string to retry
def welcomeMenuHandler(choice):
    #custom={} #todo: test all custom word functions with this commented. Independent testing broke return "custom"
    save_manual_file = True
    # print("User selects:", choice)
    base_name = ""
    if choice == "1":
        # print("Manual input")
        userMadlib = enterMadlibManual()
        savequest = raw_input("Would you like to save?\n")
        if savequest == "yes":
            base_name = raw_input("Enter your desired filename (without extention)\:\n")
            file_write(' '.join(userMadlib), base_name, '../inputs', '.txt')
        elif savequest == "no":
            save_manual_file = False
        else:
            print(potato)
            exit()
    elif choice == "2":
        # print("From file")
        filename = input("Enter a madlib filename with the extension:\n")
        base_name = os.path.splitext(filename)[0]
        userMadlib = enterMadlibFile(filename)
    elif choice == "3":
        instructionsMenuHandler()
        userMadlib = ""
    else:
        # print("invalid entry")
        userMadlib = ""
        print(potato)
        exit()
    if userMadlib is not "":
        custom = customWordsFilter(userMadlib, base_name, save_manual_file)
    return userMadlib, custom


# Madlib maker main execution
def main():
    global custom
    print("welcome")
    # create input and output folders
    if not os.path.isdir(os.path.join(os.getcwd(), "inputs")):
        os.mkdir(os.path.join(os.getcwd(), "inputs"))
    if not os.path.isdir(os.path.join(os.getcwd(), "outputs")):
        os.mkdir(os.path.join(os.getcwd(), "outputs"))

    # userMadlib determines whether we re-enter first menuHandler
    userMadlib = ""
    while userMadlib is "":
        # Initial user input
        choice = raw_input(makeSelection)  # welcome and first decision
        userMadlibAndCustom = welcomeMenuHandler(choice)
        custom = userMadlibAndCustom[1]
        userMadlib = userMadlibAndCustom[0]
    # print("User's unfilled madlib is:", userMadlib)
    # At this point we have an unprocessed user madlib regardless of where it came from

    # Save and quit, play or print
    choice2 = raw_input("Do you wish to:\n1. Fill in your madlib now\n2. Print a physical version\n3. Quit\n")
    madlibMainMenuHandler(choice2, userMadlib, custom)
    # if filledMadlib is not None:
    #     print("Your madlib:", ' '.join(filledMadlib))

if __name__ == "__main__": #executes the main fucntion
    main()
    # test()
