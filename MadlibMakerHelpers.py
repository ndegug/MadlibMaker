from past.builtins import raw_input
import re
import os
import json

custom = {}
inputList = []
numword_dic = {}

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


def quote_convert(text):
    text = text.replace('\u2018\u2018', '"')
    text = text.replace('\u2019\u2019', '"')
    text = text.replace('\u2018', "\'")
    text = text.replace('\u2019', "\'")
    text = text.replace('\u201C', '"')
    text = text.replace('\u201D', '"')
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


def file_read():
    global custom
    global inputList
    filename = raw_input("Which file would you like to process? (type the name with no extension)\n")
    # saving name of custom word file
    customfile = filename + "_cts.txt"
    # reading main content file
    choice = os.path.join('inputs', filename + ".txt")
    my_file = open(choice, "r")
    cont = my_file.read()
    inputList = cont.split(" ")
    if os.path.exists(os.path.join('inputs', customfile)):
        choice = os.path.join('inputs', customfile)
        with open(choice) as f:
            data = f.read()
        custom = json.loads(data.replace("\'", "\""))
        f.close()
    elif not os.path.exists(os.path.join('inputs', customfile)) and re.search(customreg, str(inputList)) is not None:
        cust_config()
        file_write(str(custom), filename, 'inputs', '_cts.txt')
    else:
        pass


# keyword say and replace function


def keyword_convert(ind, wrd, ca):
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
