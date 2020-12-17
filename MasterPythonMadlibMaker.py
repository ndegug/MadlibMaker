import os
import string
import re
from pip._vendor.distlib.compat import raw_input

custom = []

outlist = []

inputList = []

generic_words = {'/adj': 'Adjective', '/nou': 'Noun', '/pln': 'Plural noun',
                 '/ver': 'Verb', '/vng': 'Verb ending in \"ing\"', '/ved': 'Past tense verb', '/ves':'Verb ending in \"s\"',
                 '/num': 'Number', '/nam': 'Number', '/cel': 'Celebrity',
                 '/per': 'Person', '/pir': 'Person in room', '/thi': 'Thing',
                 '/pla': 'Place', '/job': 'Job', '/ran': 'Random Word',
                 '/rex': 'Random Exclamation', '/tvs': 'TV Show', '/mov': 'Movie',
                 '/mtv': "Movie/TV show", '/ins': 'Insult/Insulting name', '/phr': 'Random Phrase',
                 '/fam': 'Family member (title)', '/foo': 'Food', '/ani': 'Animal',
                 '/fic': 'Fictional Character','/act':'Activity','/bod':'Body Part'}
printable_words = []
if not os.path.isdir(os.path.join(os.getcwd(), "inputs")):
    os.mkdir(os.path.join(os.getcwd(), "inputs"))
if not os.path.isdir(os.path.join(os.getcwd(), "outputs")):
    os.mkdir(os.path.join(os.getcwd(), "outputs"))


def keywords(ind):
    if ind in generic_words.keys():
        print(generic_words[ind] + ': ')
    elif re.findall(customreg, ind) and (int(ind[3]) - 1) in custom:
        print(custom[int(ind[3]) - 1])
    elif re.findall(customreg, ind) and (int(ind[3]) - 1) not in custom:
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
    choice = 'inputs\\' + raw_input("Which file would you like to upload?\n") + ".txt"
    my_file = open(choice, "r")
    content = my_file.read()
    inputList = content.split(" ")
elif choice == "3":
    choice = raw_input("Which would you like to learn about: \n1. How to write, upload and save Madlibs\n2. "
                       "Syntax\n3. Custom Words\n") #todo finish instructions
    if choice == "1":
        print("Here in the Madlib Maker, you can either type your Madlib or upload a file you've already typed.\nFor "
              "each blank, you must type a keyword specific to the word category you desire.\nThese keywords follow "
              "the format of 3 letters preceded by a \"/\", for example,\ntyping the keyword \"/adj\" will prompt the "
              "program to ask the user for an \"Adjective.\"\n See the Syntax section for the full list of "
              "keywords.\n\nIf you wish to use a word that is not in this program's selection,\nyou may enter it as a "
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

        exit()
    elif choice == "3":
        print("Custom Words")
    else:
        print(potato)
        exit()

else:
    print(potato)
    exit()
numword_dic = {}
unnumbered="(/...)"
numbered="(/...[0-9]+)"
customreg="(/ct[0-9]+)"
regkey=""
realkey=""
choice = raw_input("Before you fill your madlib, would you configure your custom words?\n")
if choice == "yes":
    print("Enter each of your custom words, one by one, in order of appearance. Enter \"q\" to stop ")
    i = 1
    while choice != "q":
        if choice != "q":
            print("custom", i)
            choice = raw_input()
            custom.append(choice)
        i = i + 1
elif choice == "no" or choice=="":
        pass
else:
        print(potato2)
        exit()
for word in inputList:
    if re.findall(unnumbered, word) and not re.findall(numbered, word):
        #unnumbered
        regkey = str(re.findall(unnumbered, word))
        keywords(regkey[2]+regkey[3]+regkey[4]+regkey[5])#this is because that stupid re code puts out brakets and quotes for no reason
        new = raw_input()
        new = str(re.sub(unnumbered, new, word))
        outlist.append(new)
    elif re.findall(customreg, word):
        regkey = str(re.findall(unnumbered, word))
        keywords(regkey[2] + regkey[3] + regkey[4] + regkey[5])  # this is because that stupid re code puts out brakets and quotes for no reason
        new = raw_input()
        new = str(re.sub(unnumbered, new, word))
        outlist.append(new)
    elif re.findall(numbered, word):
        regkey = str(re.findall(unnumbered, word))
        realkey= regkey[2]+regkey[3]+regkey[4]+regkey[5]
        if realkey+regkey[6] not in numword_dic.keys():
            #numbered unsaved
            keywords(realkey)
            new = raw_input()
            numword_dic[realkey+regkey[6]] = new
            new=re.sub(numbered, new, word)
            outlist.append(new)
        elif realkey+regkey[6] in numword_dic.keys():
            new = re.sub(numbered, numword_dic[realkey+regkey[6]], word)
            outlist.append(new)
    else:
        #none, just append
        outlist.append(word)

filled = ' '.join(outlist)
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
    print("Have a good day!")
else:
    print(potato2)
# 3. Output string ist to a text file
# output name to whatever 'outputs/output1.txt'
