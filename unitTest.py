# unit test for madlib function
# 12/13/2020
import os
import string
from pip._vendor.distlib.compat import raw_input
def functionA(test):
    return test
generic_words = {'/adj': 'Adjective', '/nou': 'Noun', '/pln': 'Plural noun',
                 '/ver': 'Verb', '/vng': 'Verb ending in \"ing\"', '/ved': 'Past tense verb',
                 '/num': 'Number', '/nam': 'Number', '/cel': 'Celebrity',
                 '/per': 'Person', '/pir': 'Person in room', '/thi': 'Thing',
                 '/pla': 'Place', '/job': 'Job', '/ran': 'Random Word',
                 '/rex': 'Random Exclamation', '/tvs': 'TV Show', '/mov': 'Movie',
                 '/mtv': "Movie/TV show", '/ins': 'Insult/Insulting name', '/phr': 'Random Phrase',
                 '/fam': 'Family member (title)', '/foo': 'Food', '/ani': 'Animal',
                 '/fic': 'Fictional Character','/act':'Activity','/bod':'Body Part'}
def keywords(ind):
    if ind in generic_words.keys():
        print(generic_words[ind] + ': ')
    elif ind[1] == "c" and ind[2] == "t" and ind[3].isdigit and ind[3] not in string.punctuation:
        print(custom[int(ind[3]) - 1])
    else:
        print(ind, "is not a valid keyword, enter what to fill it with: ")
numword_dic = {}
word = "\"/adj1.\""
i=0
final= ""
wordfilled=0
while i<len(word):
    print("first",word[i])
    print("final",final)
    if word[i] == "/":
        if not word[i+4].isdigit#todo, make the code collect the whole keyword before asking for a replacement
            #slash found, not numbered
            keywords(word[i] + word[i+1] + word[i+2] + word[i+3])
            new = raw_input()
            final=final+new
            wordfilled=1
            i=i+4
        elif word[i+4].isdigit and (word[i]+word[i+1] + word[i+2] + word[i+3]+word[i+4]) not in numword_dic.keys():
            keywords(word[i] + word[i + 1] + word[i + 2] + word[i + 3])
            new = raw_input()
            numword_dic[word[i] + word[i + 1] + word[i + 2] + word[i + 3] + word[i + 4]] = new
            i = i + 1
    elif word[i] == "/" and word[i+4].isdigit and (word[i]+word[i+1] + word[i+2] + word[i+3]+word[i+4]) not in numword_dic.keys():
        #slash found, numbered unsaved
        keywords(word[i] + word[i+1] + word[i+2] + word[i+3])
        new = raw_input()
        numword_dic[word[i] + word[i+1] + word[i+2] + word[i+3]+word[i+4]] = new
        i=i+1
    elif  word[i] == "/" and word[i+4].isdigit and (word[i+1] + word[i+2] + word[i+3]) not in numword_dic.keys():
        #slash found, numbered saved
        new = numword_dic[word[i] + word[i+1] + word[i+2] + word[i+3] + word[i+4]]
        final = final + new
        i=i+4
    else:
        #punctuation
        final=final+word[i]
        i=i+1
wordfilled=0
print(final)
