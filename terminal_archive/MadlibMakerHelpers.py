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

potato = "We're sorry, but that command is invalid. You cannot make up an answer.\nThat's not " \
         "how it works, sorry!\n"
potato2 = "You were asked a \"yes\" or \"no\" question and ignored the options " \
          "\nThis will not be tolerated, goodbye!\n"

htmlsample = '<span class="nowrap" style="display: none; display: inline-block; vertical-align: top; text-align: ' \
             'center;"><span style="display: block; padding: 0 0.2em;">__________</span><span style="display: block; ' \
             'font-size: 70%; line-height: 1em; padding: 0 0.2em;"><span style="position: relative; line-height: 1em; ' \
             'margin-top: -.2em; top: -.2em;">underscript</span></span></span>'

generic_words = { # reminder: do not add any keywords that are the same as ignored words
                 '/adj': 'Adjective', '/nou': 'Noun', '/pln': 'Plural noun',
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
ignored_words = ['/her', '/she', '/She']  # words that resemble generic words that will be ignored

unnumbered = "(/...)"
numbered = "(/...[0-9]+)"
customreg = "(/ct[0-9]+)"
numcustcom = ".+\([0-9]+\)"
numcustreg = "(/ct[0-9]+_[0-9]+)"
tail = "(_[0-9])"


def quote_convert(text): #todo: quotes in MCM word madlib have an extra backslash
    text = text.replace("\\xe2\\x80\\x9c", '"')
    text = text.replace("\\xe2\\x80\\x9d", '"')
    text = text.replace('\\xe2\\x80\\x98', "'")
    text = text.replace('\\xe2\\x80\\x99', "'")
    text = text.replace('\\xe2\\x80\\xa6', "...") #todo resolve space syntax in "steven madlib 1 mlm.docx"
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
            continue

    return custom


def file_read():
    global custom
    global inputList
    filename = raw_input("Which file would you like to process? (include extension)\n")
    if re.search("\.docx$", filename):
        # docx file
        customfile = filename.replace('.docx', '_cts.txt')
        base_name = filename.replace('.docx', '')
        cont = textract.process("inputs/" + filename)
        cont = quote_convert(str(cont))  # converts all instances of curly punctuaton in word
        cont = cont[2:len(cont) - 1]  # temporary solution that removes the body markers from word
    elif re.search("\.txt$", filename):
        customfile = filename.replace('.txt', '_cts.txt')
        base_name = filename.replace('.txt', '')
        # reading main content file
        choice = os.path.join('../inputs', filename)
        my_file = open(choice, "r")
        cont = my_file.read()
    else:
        cont = ''
        customfile = ''
        base_name = ''
        print("file invalid")
        print(potato)
        quit()

    inputList = cont.split(" ")
    if os.path.exists(os.path.join('../inputs', customfile)):
        choice = os.path.join('../inputs', customfile)
        with open(choice) as f:
            data = f.read()
        custom = json.loads(data.replace("\'", "\""))
        f.close()
    elif not os.path.exists(os.path.join('../inputs', customfile)) and re.search(customreg, str(inputList)) is not None:
        cust_config(inputList)
        file_write(str(custom), base_name, '../inputs', '_cts.txt')
    else:
        pass


# keyword say and replace function


def keyword_convert(ind, wrd, ca, custom):#todo: verify all numbered keys 10 and over
    base = re.findall(unnumbered, wrd)
    base = ''.join(base)#todo: invesitgate potential duplicate of ind and base
    if ca == 0:  # Generic word unnumbered
        print(generic_words[ind] + ': ')
        new = raw_input()
    elif ca == 1:  # generic word numbered unsaved
        print(generic_words[base] + ': ')
        new = raw_input()
        numword_dic[ind] = new  # saves entry for numbered word
        # return re.sub(ind, new, wrd)
    elif ca == 2:  # Numbered word previously saved
        new = numword_dic[ind]  # pulls word directly from numbered words dictionary
        # return re.sub(ind, new, wrd)
    elif ca == 3:
        base = re.findall(customreg, wrd)
        base = ''.join(base)
        print(custom[base] + ':')
        new = raw_input()
    elif ca == 4:
        base = re.findall(customreg, wrd)
        base = ''.join(base)
        print(custom[base] + ': ')
        new = raw_input()
        numword_dic[ind] = new
        # return re.sub(ind, new, wrd)
    elif ca == 5:
        print(ind, "hasn't been configured, what would you like to replace it with?")
        new = raw_input()
    elif ca == 6: # invalid numbered word
        print(ind, "is not a valid keyword, enter what to fill it with: ")
        new = raw_input()
        numword_dic[ind] = new  # saves entry for numbered word
    else:
        print(ind, "is not a valid keyword, enter what to fill it with: ")
        new = raw_input()
    return re.sub(ind, new, wrd)  # todo inspect for issues "return statement" changes introduces
