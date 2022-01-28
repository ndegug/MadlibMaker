
import re
import os
import json
import textract
from past.builtins import raw_input

custom = {}
inputList = []
numword_dic = {}

htmlhead = '<html><head></head><body><h1> heading </h1><style>h1 {text-align: center;}p.big {  line-height: ' \
           '2;}.tab { display: inline-block; margin-left: 80px;}  </style><p class="big"><span class="tab"></span>'

potato = "What the hell is wrong with you? I give you a list of options and you decide to make your own?\nThat's not " \
         "how it works you moron! Get 'outa here!\n"
potato2 = "What the hell is wrong with you? I give you a \"yes\" or \"no\" question and THAT'S what you come up " \
          "with?\nThat's not how it works you moron! Get 'outa here!\n"

htmlsample = '<span class="nowrap" style="display: none; display: inline-block; vertical-align: top; text-align: ' \
             'center;"><span style="display: block; padding: 0 0.2em;">__________</span><span style="display: block; ' \
             'font-size: 70%; line-height: 1em; padding: 0 0.2em;"><span style="position: relative; line-height: 1em; ' \
             'margin-top: -.2em; top: -.2em;">underscript</span></span></span>'

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

def customWordsFilter(inputList, base_name):
    # inputList = quote_convert(inputList)
    customfile = base_name + "_cts.txt"
    if os.path.exists(os.path.join('inputs', customfile)):
        choice = os.path.join('inputs', customfile)
        with open(choice) as f:
            data = f.read()
        custom = json.loads(data.replace("\'", "\""))
        f.close()
    elif not os.path.exists(os.path.join('inputs', customfile)) and re.search(customreg, str(inputList)) is not None:
        custom = cust_config(inputList)
        file_write(str(custom), base_name, 'inputs', '_cts.txt')
    else:
        custom = None
    return custom


def createHtmlMadlib(userMadlib):
    print("create madlib html")
    latlist=[]
    for word in userMadlib:
        if re.findall(unnumbered, word) and not re.findall(numbered, word) and not re.findall(customreg, word):
            # unnumbered
            regkey = re.findall(unnumbered, word)
            realkey = ''.join(regkey)

            if realkey in generic_words.keys():
                latword = htmlsample.replace('underscript', generic_words[realkey])
                final = word.replace(realkey, latword, 1)
                latlist.append(final)
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
            # #Latex array
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
            else:
                outlist.append(keyword_convert(realkey, word, 6, None))

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
                # numbered cust saved
                strIdx = 5
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


def hasCustomWords(userMadlib):
    return False

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
    custom=None
    if re.search("\.docx$", filename):
        # docx file
        customfile = filename.replace('.docx', '_cts.txt')
        base_name=filename.replace('.docx', '')
        cont = textract.process("inputs/" + filename)
        cont = quote_convert(str(cont))#converts all instances of curly punctuaton in word
        cont = cont[2:len(cont)-1] #temporary solution that removes the body markers from word
        #todo: find and extract body rather than just remove start and finish
    elif re.search("\.txt$", filename):
        customfile = filename.replace('.txt', '_cts.txt')
        base_name = filename.replace('.txt', '')
        # reading main content file
        choice = os.path.join('inputs', filename)
        my_file = open(choice, "r")
        cont = my_file.read()
    else:
        cont=''
        customfile =''
        base_name=''
        print("file invalid")
        print(potato)
        quit()
    inputList = cont.split(" ")
    return inputList

def madlibMainMenuHandler(choice, userMadlib, custom):
    print("user choice:",choice)
    filledMadlib=None
    if choice == "1":
        print("Fill in")
        filledMadlib = fillInMadlib(userMadlib, custom)
        print(filledMadlib)
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
              "drag the file into your browser to view it. Print the file using your respective browser's print feature.\n"
              "Have a good day!")
    elif choice == "3":
        print("quit")
    else:
        # print(potato)
        print("Invalid instruction choice:", choice, "Please try again...")
    return filledMadlib

def instructionsMenuHandler():
    choice = ""
    while choice != "q":
        choice = raw_input(instruct0)
        if choice == "1":  # todo add a "process pre-made file" instructions
            print(instruct1)
        elif choice == "2":
            print("The default keys and word categories are as follows:")
            printCleanColumns(generic_words)
        elif choice == "3":
            print(instruct3)
        elif choice == "4":
            print(instruct4)
        elif choice == "q":
            return
        else:
            #print(potato)
            print("Invalid instruction choice:",choice,"Please try again...")

# menuHandler returns the unprocessed user madlib or empty string to retry
def welcomeMenuHandler(choice):
    userMadlib=""
    print("User selects:",choice)
    if choice =="1":
        print("Manual")
        userMadlib = enterMadlibManual()
    elif choice == "2":
        print("From file")
        filename = input("Enter a madlib filename with extension:")
        base_name = os.path.splitext(filename)[0]
        userMadlib = enterMadlibFile(filename)
    elif choice == "3":
        instructionsMenuHandler()
        userMadlib = ""
    else:
        print("invalid entry")
        userMadlib = ""
    if userMadlib is not "":
        custom = customWordsFilter(userMadlib,base_name)
    return userMadlib, custom

def quote_convert(text):
    text = text.replace("\\xe2\\x80\\x9c", '"')
    text = text.replace("\\xe2\\x80\\x9d", '"')
    text = text.replace('\\xe2\\x80\\x98', "\'")
    text = text.replace('\\xe2\\x80\\x99', "\'")
    return text


def invalid_html(ch, RK, wrd):
    if ch == 0:
        ch = raw_input(RK + ' is not a valid key, did you want it to be?')
    elif ch == 1:
        ch = raw_input(RK + ' is not configured, did you mean to do it?')
    if ch == 'yes':
        new = raw_input('What is the word\'s category?')
        latword = htmlsample.replace('underscript', new)
        final = wrd.replace(RK, latword, 1)
        return final
    elif ch == 'no' or ch == '':
        return wrd
    else:
        print(potato2)
        exit()



def file_write(content, name_of_file, path, ext):
    completeName = os.path.join(path, name_of_file + ext)
    f = open(completeName, "w")
    f.write(content)
    f.close()
def cust_config(inlist):
    print("Custom words detected, enter each of your custom words, one by one, in order of appearance. Enter \"q\" to "
          "stop ")
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
            pass

    return custom

def file_read():
    global custom
    global inputList
    filename = raw_input("Which file would you like to process? (include extension)\n")
    # saving name of custom word file
    # # reading main content file
    # choice = os.path.join('inputs', filename + ".txt")
    # my_file = open(choice, "r")
    # cont = my_file.read()
    if re.search("\.docx$", filename):
        # docx file
        customfile = filename.replace('.docx', '_cts.txt')
        base_name=filename.replace('.docx', '')
        cont = textract.process("inputs/" + filename)
        cont = quote_convert(str(cont))#converts all instances of curly punctuaton in word
        cont = cont[2:len(cont)-1] #temporary solution that removes the body markers from word
        #todo: find and extract body rather than just remove start and finish
    elif re.search("\.txt$", filename):
        customfile = filename.replace('.txt', '_cts.txt')
        base_name = filename.replace('.txt', '')
        # reading main content file
        choice = os.path.join('inputs', filename)
        my_file = open(choice, "r")
        cont = my_file.read()
    else:
        cont=''
        customfile =''
        base_name=''
        print("file invalid")
        print(potato)
        quit()

    inputList = cont.split(" ")
    #inputList = quote_convert(inputList)
    if os.path.exists(os.path.join('inputs', customfile)):
        choice = os.path.join('inputs', customfile)
        with open(choice) as f:
            data = f.read()
        custom = json.loads(data.replace("\'", "\""))
        f.close()
    elif not os.path.exists(os.path.join('inputs', customfile)) and re.search(customreg, str(inputList)) is not None:
        cust_config(inputList)
        file_write(str(custom), base_name, 'inputs', '_cts.txt')
    else:
        pass


# keyword say and replace function


def keyword_convert(ind, wrd, ca, custom):
    base = re.findall(unnumbered, wrd)
    base = ''.join(base)
    if ca == 0:
        print(generic_words[ind] + ': ')
    elif ca == 1:
        print(generic_words[base] + ': ')
        new = raw_input()
        numword_dic[ind] = new
        return re.sub(ind, new, wrd)
    elif ca == 2:
        new = numword_dic[ind]
        return re.sub(ind, new, wrd)
    elif ca == 3:
        print(custom[base] + ':')
    elif ca == 4:
        print(custom[base] + ': ')
        new = raw_input()
        numword_dic[ind] = new
        return re.sub(ind, new, wrd)
    elif ca == 5:
        print(ind, "hasn't been configured, what would you like to replace it with?")
    else:
        print(ind, "is not a valid keyword, enter what to fill it with: ")
    new = raw_input()
    return re.sub(ind, new, wrd)
