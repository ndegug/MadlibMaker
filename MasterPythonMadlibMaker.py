import os
import re
import json

from pip._vendor.distlib.compat import raw_input

custom = {}

outlist = []

latlist = []

inputList = []

generic_words = {'/adj': 'Adjective', '/nou': 'Noun', '/pln': 'Plural noun',
                 '/ver': 'Verb', '/vng': 'Verb ending in \"ing\"', '/ved': 'Past tense verb',
                 '/ves': 'Verb ending in \"s\"', '/adv': 'adverb',
                 '/num': 'Number', '/nam': 'Name', '/cel': 'Celebrity',
                 '/per': 'Person', '/pir': 'Person in room', '/thi': 'Thing',
                 '/pla': 'Place', '/job': 'Job', '/ran': 'Random Word',
                 '/rex': 'Random Exclamation', '/tvs': 'TV Show', '/mov': 'Movie',
                 '/mtv': "Movie/TV show", '/ins': 'Insulting name', '/phr': 'Random Phrase',
                 '/fam': 'Family member (title)', '/foo': 'Food', '/ani': 'Animal',
                 '/fic': 'Fictional Character', '/act': 'Activity', '/bod': 'Body Part', '/flu': 'Fluid',
                 '/emo': 'Emotion', '/noi': 'noise', '/eve': 'Event', '/fos': 'Plural food', '/fur': 'Furniture'}
unnumbered = "(/...)"
numbered = "(/...[0-9]+)"
customreg = "(/ct[0-9]+)"
numcustcom = ".+\([0-9]+\)"
numcustreg = "(/ct[0-9]+_[0-9]+)"
tail = "(_[0-9])"

if not os.path.isdir(os.path.join(os.getcwd(), "inputs")):
    os.mkdir(os.path.join(os.getcwd(), "inputs"))
if not os.path.isdir(os.path.join(os.getcwd(), "outputs")):
    os.mkdir(os.path.join(os.getcwd(), "outputs"))


def quote_convert(text):
    text = text.replace('\u2018\u2018', '"')
    text = text.replace('\u2019\u2019', '"')
    text = text.replace('\u2018', "\'")
    text = text.replace('\u2019', "\'")
    text = text.replace('\u201C', '"')
    text = text.replace('\u201D', '"')
    return text


def invalid_html(ch, RK):
    if ch == 0:
        ch = raw_input(realkey + ' is not a valid key, did you want it to be?')
    elif ch == 1:
        ch = raw_input(realkey + ' is not configured, did you mean to do it?')
    if ch == 'yes':
        new = raw_input('What is the word\'s category?')
        latword = htmlsample.replace('underscript', new)
        final = word.replace(RK, latword, 1)
        latlist.append(final)
    elif ch == 'no' or ch == '':
        latlist.append(word)
    else:
        print(potato)
        exit()


def keywords(ind):
    base = re.findall(unnumbered, ind)
    base = ''.join(base)
    if base in generic_words.keys():
        print(generic_words[base] + ': ')
    elif re.findall(customreg, ind) and ind in custom:
        print(custom[ind] + ':')
    elif re.findall(customreg, ind) and ind not in custom:
        print(ind, "hasn't been configured, what would you like to replace it with?")
    else:
        print(ind, "is not a valid keyword, enter what to fill it with: ")


def file_write(name_of_file, ch):
    if ch == 0:  # normal write
        completeName = os.path.join(save_path, name_of_file + ".txt")
        f = open(completeName, "w")
        f.write(' '.join(inputList))
        f.close()
    elif ch == 1:  # custom write
        completeName = os.path.join('inputs', name_of_file + "_cts.txt")
        f = open(completeName, "w")
        f.write(str(custom))
        f.close()
    else:#todo add output write
        print("custom write bug, please report to github page")
        exit()


def cust_config():
    print("Custom words detected, enter each of your custom words, one by one, in order of appearance. Enter \"q\" to "
          "stop ")
    i = 1
    tempreg = "(/ct1+)"  # variable regular expression
    while re.findall(tempreg, content):  # todo account for people who use unconfigured doubles
        print("custom", i)
        ch = raw_input()
        custom["/ct" + str(i)] = ch
        i = i + 1
        tempreg = "(/ct" + str(i) + "+)"


potato = "What the hell is wrong with you? I give you a list of options and you decide to make your own?\nThat's not " \
         "how it works you moron! Get 'outa here!\n"
potato2 = "What the hell is wrong with you? I give you a \"yes\" or \"no\" question and THAT'S what you come up " \
          "with?\nThat's not how it works you moron! Get 'outa here!\n"

choice = raw_input(
    "Welcome to the Madlib Maker\nHere you can compose and fill in madlibs using our specialized syntax.\nTo begin, "
    "please select from the following menu options:\n1. Type madlib\n2. Use a madlib from the \"inputs\" folder.\n3. "
    "Instructions\n")
if choice == "1":
    # manual input
    content = raw_input("Enter the madlib below:\n")
    inputList = content.split(" ")
    if re.search(customreg, str(inputList)) is not None:
        cust_config()
    else:
        pass
    choice = raw_input("Would you like to save your madlib to the inputs folder before filling it?\n")
    if choice == "yes":
        save_path = 'inputs'
        filename = raw_input("What do you wish to name the file? (do not type the extension): ")
        # main content file
        file_write(filename, 0)
        # custom words file
        if re.search(customreg, str(inputList)) is not None:
            file_write(filename, 1)
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
    filename = raw_input("Which file would you like to process? (type the name with no extension)\n")
    # saving name of custom word file
    customfile = filename + "_cts.txt"
    # adding extention to main file name
    filename = filename + ".txt"
    # reading main content file
    choice = os.path.join('inputs', filename)
    my_file = open(choice, "r")
    content = my_file.read()
    inputList = content.split(" ")
    if os.path.exists(os.path.join('inputs', customfile)):
        choice = os.path.join('inputs', customfile)
        with open(choice) as f:
            data = f.read()
        custom = json.loads(data.replace("\'", "\""))
        f.close()
    elif not os.path.exists(os.path.join('inputs', customfile)) and re.search(customreg, str(inputList)) is not None:
        cust_config()
        file_write(filename, 1)
    else:
        pass
elif choice == "3":
    while choice != "q":
        choice = raw_input("Which would you like to learn about:\n1. How to write Madlibs\n2. "
                           "Syntax\n3. Custom Words\n4. Saving and printing madlibs\nType \"q\" to quit\n")
        if choice == "1":#todo add a "process pre-made file" instructions
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
numword_dic = {}
numcust_dic = {}
regkey = ""
realkey = ""
htmlsample = '<span class="nowrap" style="display: none; display: inline-block; vertical-align: top; text-align: ' \
             'center;"><span style="display: block; padding: 0 0.2em;">__________</span><span style="display: block; ' \
             'font-size: 70%; line-height: 1em; padding: 0 0.2em;"><span style="position: relative; line-height: 1em; ' \
             'margin-top: -.2em; top: -.2em;">underscript</span></span></span>'
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
for word in inputList:
    if re.findall(unnumbered, word) and not re.findall(numbered, word) and not re.findall(customreg, word):
        # unnumbered
        regkey = re.findall(unnumbered, word)
        realkey = ''.join(regkey)
        if choice2 == "1":
            keywords(realkey)  # this is because that stupid re code puts out brakets and quotes for no reason
            new = raw_input()
            new = str(re.sub(unnumbered, new, word))
            outlist.append(new)
        elif choice2 == "2" and realkey in generic_words.keys():
            latword = htmlsample.replace('underscript', generic_words[realkey])
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
        elif choice2 == "2" and realkey not in generic_words.keys():
            invalid_html(0, realkey)
    elif re.findall(customreg, word) and not re.findall(numcustreg, word):
        # custom
        regkey = re.findall(customreg, word)
        realkey = ''.join(regkey)
        if choice2 == "1":
            keywords(realkey)  # this is because that stupid re code puts out brakets and quotes for no reason
            new = raw_input()
            new = str(re.sub(unnumbered, new, word))
            outlist.append(new)
        # latex array
        elif choice2 == "2" and realkey in custom:
            # saved
            latword = htmlsample.replace('underscript', custom[realkey])
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
        elif choice2 == "2" and realkey not in custom:
            invalid_html(1, realkey)
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

        if choice2 == "1" and realkey not in numcust_dic:
            # numbered cust unsaved
            keywords(base)
            new = raw_input()
            numcust_dic[realkey] = new
            new = re.sub(numcustreg, new, word)
            outlist.append(new)
        elif choice2 == "1" and realkey in numcust_dic:
            # numbered cust saved
            new = re.sub(numcustreg, numcust_dic[realkey], word)
            outlist.append(new)
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
        if choice2 == "1" and realkey not in numword_dic.keys():
            # numbered unsaved

            keywords(realkey)
            new = raw_input()
            numword_dic[realkey] = new
            new = re.sub(numbered, new, word)
            outlist.append(new)
        elif choice2 == "1" and realkey in numword_dic.keys():
            new = re.sub(numbered, numword_dic[realkey], word)
            outlist.append(new)
        elif choice2 == "2" and base in generic_words.keys():
            latword = htmlsample.replace('underscript', generic_words[base] + ' (' + str(num) + ')')
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
        elif choice2 == "2" and base not in generic_words.keys():
            invalid_html(0, realkey)
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
        save_path = 'outputs'
        filename = raw_input("What do you wish to name the file? (do not type the extension): ")
        completeName = os.path.join(save_path, filename + ".txt")
        f = open(completeName, "w")
        f.write(filled)
        f.close()
        print("Your filled madlib has been saved to the outputs folder, have a good day!")
    elif choice == 'no' or choice == '':
        print("Have a good day!")
    else:
        print(potato2)
        exit()
elif choice2 == '2':
    head = raw_input("What would you like to title this madlib?\n")
    latfill = htmlhead.replace('heading', head, 1) + latfill + ' </p></body></html>'
    save_path = 'outputs'
    filename = raw_input("What do you wish to name the file? (do not type the extension):\n")
    completeName = os.path.join(save_path, filename + ".html")
    f = open(completeName, "w")
    f.write(latfill)
    f.close()
    print("An HTML coded version of your unfilled madlib has been saved to the outputs folder, "
          "drag the file into your browser to view it. Print the file using your respective browser's print feature.\n"
          "Have a good day!")
elif choice == 'no' or choice == '':
    print("Have a good day!")
else:
    print(potato2)
    exit()
