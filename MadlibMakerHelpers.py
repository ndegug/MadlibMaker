from past.builtins import raw_input
import re
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

custom = {}

numword_dic = {}

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

#keyword say and replace function


def keyword_convert(ind, wrd):
    base = re.findall(unnumbered, wrd)
    base = ''.join(base)
    if base in generic_words.keys() and ind not in numword_dic.keys():
        print(generic_words[base] + ': ')
    elif ind in numword_dic.keys():
        new = numword_dic[ind]
        return re.sub(ind, new, wrd)
    elif re.findall(customreg, ind) and ind in custom:
        print(custom[ind] + ':')
    elif re.findall(customreg, ind) and ind not in custom:
        print(ind, "hasn't been configured, what would you like to replace it with?")
    else:
        print(ind, "is not a valid keyword, enter what to fill it with: ")
    new = raw_input()
    return re.sub(ind, new, wrd)

