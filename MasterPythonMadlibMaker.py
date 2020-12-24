import os
import re
from pip._vendor.distlib.compat import raw_input

custom = {}

outlist = []

latlist = []

inputList = []

generic_words = {'/adj': 'Adjective', '/nou': 'Noun', '/pln': 'Plural noun',
                 '/ver': 'Verb', '/vng': 'Verb ending in \"ing\"', '/ved': 'Past tense verb',
                 '/ves': 'Verb ending in \"s\"',
                 '/num': 'Number', '/nam': 'Name', '/cel': 'Celebrity',
                 '/per': 'Person', '/pir': 'Person in room', '/thi': 'Thing',
                 '/pla': 'Place', '/job': 'Job', '/ran': 'Random Word',
                 '/rex': 'Random Exclamation', '/tvs': 'TV Show', '/mov': 'Movie',
                 '/mtv': "Movie/TV show", '/ins': 'Insult/Insulting name', '/phr': 'Random Phrase',
                 '/fam': 'Family member (title)', '/foo': 'Food', '/ani': 'Animal',
                 '/fic': 'Fictional Character', '/act': 'Activity', '/bod': 'Body Part', '/flu': 'Fluid'}

printable_words = []  # todo figure out if we need this
if not os.path.isdir(os.path.join(os.getcwd(), "inputs")):
    os.mkdir(os.path.join(os.getcwd(), "inputs"))
if not os.path.isdir(os.path.join(os.getcwd(), "outputs")):
    os.mkdir(os.path.join(os.getcwd(), "outputs"))


def keywords(ind):
    if ind in generic_words.keys():
        print(generic_words[ind] + ': ')
    elif re.findall(customreg, ind) and ind in custom:
        print(custom[ind] + ':')
    elif re.findall(customreg, ind) and ind not in custom:
        print(ind, "hasn't been configured, what would you like to replace it with?")
    else:
        print(ind, "is not a valid keyword, enter what to fill it with: ")


potato = "What the hell is wrong with you? I give you a list of options and you decide to make your own?\nThat's not " \
         "how it works you moron! Goodbye!\n "
potato2 = "What the hell is wrong with you? It's a \"yes\" or \"no\" question and THAT'S what you come up " \
          "with?\nThat's not how it works you moron! Goodbye!\n "

choice = raw_input(
    "Welcome to the Madlib Maker\nHere you can compose and fill in madlibs using our specialized syntax.\nTo begin, "
    "please select from the following menu options:\n1. Type madlib \n2. Upload madlib from \"input\" folder.\n3. "
    "Instructions\n")
if choice == "1":
    # manual input
    content = raw_input("Enter the madlib below:\n")
    inputList = content.split(" ")
    choice = raw_input("Would you like to save your madlib to the inputs folder before filling it?\n")
    if choice == "yes":
        save_path = 'inputs'
        name_of_file = raw_input("What do you wish to name the file? (do not type the extension): ")
        completeName = os.path.join(save_path, name_of_file + ".txt")
        f = open(completeName, "w")
        f.write(' '.join(inputList))
        f.close()
        choice = raw_input("Your Madlib has been saved under the inputs folder, would you like to fill it in now?\n")
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
    filename = raw_input("Which file would you like to upload?\n") + ".txt"
    choice = os.path.join('inputs', filename)
    my_file = open(choice, "r")
    content = my_file.read()
    inputList = content.split(" ")
elif choice == "3":
    while choice != "q":
        choice = raw_input("Which would you like to learn about: \n1. How to write, upload and save Madlibs\n2. "
                           "Syntax\n3. Custom Words\nType \"q\" to quit\n") #todo: add inputs and outputs tutorial
        if choice == "1":
            print("Here in the Madlib Maker, you can either type your Madlib or upload a file you've already typed.\nFor "
                  "each blank, you must type a keyword specific to the word category you desire.\nThese keywords follow "
                  "the format of 3 letters preceded by a \"/\", for example,\ntyping the keyword \"/adj\" will prompt the "
                  "program to ask the user for an \"Adjective.\"\n See the Syntax section for the full list of "
                  "keywords.\n You can add a number at the end of any keyword in the databank to repeat it within the "
                  "same madlib.\n For example, if the input is:\n \"We have a pet /ani1, he's a good /ani1!\" \n and you "
                  "enter \"dog\" when prompted, the program will fill in both at the same time resulting in:\n \"We have "
                  "a pet dog, he's a good dog!\n\nIf you wish to use a word that is not in "
                  "this program's selection,\nyou may enter it as a"
                  "custom word. These custom words can be\nconfigured before writing the Madlib.\nSee the \"Custom Words\" "
                  "section for further details.")
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

        elif choice == "3":
            print("Custom words allow you to add your own word categories if they are not already stored in this "
                  "program's databanks.\n If you wanted the program to call out something obscure like \"Baseball player\" "
                  "or \"High school friend\", you can use this feature to do so.\n When questioned whether you wish to "
                  "configure the custom words, type \"yes\" "
                  "and enter these words sequentially. Once your custom words are configured, use the keyword sequence: "
                  "\"/ct1\" where the number indicates which sequential word you want to be called there.\n\n The current "
                  "version of the Maldib Maker does not yet support saved or numbered custom words, as of now they must "
                  "be configured each time the madlib is filled.\n If your Madlib "
                  "requires repeated custom words,it is reccomended you give them names such as \"High school friend ("
                  "1)\" to remind yourself to fill in the same word.")
        elif choice == "q":
            print("I hope these instructions helped, start the program again to give it a try!\n Have a good day!")
            exit()
        else:
            print(potato)
            exit()

else:
    print(potato)
    exit()
numword_dic = {}
unnumbered = "(/...)"
numbered = "(/...[0-9]+)"
customreg = "(/ct[0-9]+)"
regkey = ""
realkey = ""
choice = raw_input("Wourld you like to configure your custom words?\n")
if choice == "yes":
    print("Enter each of your custom words, one by one, in order of appearance. Enter \"q\" to stop ")
    i = 1
    while choice != "q":
        if choice != "q":
            print("custom", i)
            choice = raw_input()
            custom["/ct" + str(i)] = choice
        i = i + 1
elif choice == "no" or choice == "":
    pass
else:
    print(potato2)
    exit()
choice2 = raw_input("Do you wish to:\n1. Fill in your madlib now\n2. Print a physical version\n")
if choice2 == "1" or choice2 == "2":
    pass
else:
    print("you are here")
    print(potato2)
    exit()
for word in inputList:
    if re.findall(unnumbered, word) and not re.findall(numbered, word) and not re.findall(customreg, word):
        # unnumbered
        regkey = str(re.findall(unnumbered, word))
        realkey = regkey[2] + regkey[3] + regkey[4] + regkey[5]
        if choice2 == "1":
            keywords(realkey)  # this is because that stupid re code puts out brakets and quotes for no reason
            new = raw_input()
            new = str(re.sub(unnumbered, new, word))
            outlist.append(new)
        # #latex array
        latword_sub = generic_words[realkey].replace(" ", "\\ ")
        latword = '$\\underset{' + latword_sub + '}{\\rule{2.5cm}{0.15mm}}$'
        # latword
        final = word.replace(realkey, latword, 1)
        latlist.append(final)
    elif re.findall(customreg, word):
        # custom
        regkey = str(re.findall(unnumbered, word))
        realkey = regkey[2] + regkey[3] + regkey[4] + regkey[5]
        if choice2 == "1":
            keywords(realkey)  # this is because that stupid re code puts out brakets and quotes for no reason
            new = raw_input()
            new = str(re.sub(unnumbered, new, word))
            outlist.append(new)
        # latex array
        if realkey in custom:
            # saved
            latword_sub = custom[realkey].replace(" ", "\\ ")
            latword = '$\\underset{' + latword_sub + '}{\\rule{2.5cm}{0.15mm}}$'
            # latword
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
        else:
            latword = '$\\underset{Undefined}{\\rule{2.5cm}{0.15mm}}$'
            # latword
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
    elif re.findall(numbered, word):
        # numbered
        regkey = str(re.findall(numbered, word))
        realkey = regkey[2] + regkey[3] + regkey[4] + regkey[5]
        if realkey + regkey[6] not in numword_dic.keys():
            # numbered unsaved
            if choice2 == "1":
                keywords(realkey)
                new = raw_input()
                numword_dic[realkey + regkey[6]] = new
                new = re.sub(numbered, new, word)
                outlist.append(new)
        elif realkey + regkey[6] in numword_dic.keys():
            if choice2 == "1":
                new = re.sub(numbered, numword_dic[realkey + regkey[6]], word)
                outlist.append(new)
            # #latex array
        latword_sub = generic_words[realkey].replace(' ', '\\ ')
        latword = '$\\underset{' + latword_sub + '\\ (' + regkey[6] + ')}{\\rule{2.5cm}{0.15mm}}$'
        # latword
        final = word.replace(realkey, latword, 1)
        latlist.append(final)
    else:
        # none, just append
        if choice2 == "1":
            outlist.append(word)
        # #Latex array
        latlist.append(word)

filled = ' '.join(outlist)
latfill = ' '.join(latlist)

if choice2 == "1":
    print(filled)
    choice = raw_input("Would you like to save this filled madlib to the \"outputs\" folder? \n")
    if choice == 'yes':
        save_path = 'outputs'
        name_of_file = raw_input("What do you wish to name the file? (do not type the extension): ")
        completeName = os.path.join(save_path, name_of_file + ".txt")
        f = open(completeName, "w")
        f.write(filled)
        f.close()
        print("Your filled madlib has been saved to the outputs folder, have a good day!")
    elif choice == 'no' or choice == '':
        pass
    else:
        print(potato2)
        exit()
    choice = raw_input("Would you like to make a physical copy of the madlib?\n")
if choice == 'yes' or choice2 == '2':
    save_path = 'outputs'
    name_of_file = raw_input("What do you wish to name the file? (do not type the extension): ")
    completeName = os.path.join(save_path, name_of_file + ".txt")
    f = open(completeName, "w")
    f.write("\\documentclass{article}\n\\usepackage{amsmath}\n\\begin{document}\n" + latfill + "\n\\end{document}")
    f.close()
    print("A Latex coded version of your unfilled madlib has been saved to the outputs folder, run it in a latex "
          "compiler and save the result as a PDF, \nan online compiler can be found here: "
          "https://cocalc.com/doc/latex-editor.html \n"
          "have a good day!")
elif choice == 'no' or '':
    print("Have a good day!")
else:
    print(potato2)
    exit()
# 3. Output string ist to a text file
# output name to whatever 'outputs/output1.txt'
