# Nicolas DeGuglielmo
# 8/3/2021
import os
import json
import re
from past.builtins import raw_input
import textract

customreg = "(/ct[0-9]+)"


# checks if file exists, returns boolean
def doesFileExist(filename):
    # choice = os.path.join('inputs', filename + ".txt")
    # my_file = open(choice, "r")

    # text = text.replace('\u201C', '"')
    # text = text.replace('\u201c', '"')
    # text = text.replace('\u201D', '"')
    # text = text.replace('\u201d', '"')
    return ''
    # if text:
    #     print(text)
    #     return True
    # else:
    #     return False


# reads a custom file, returns
def readCustomFile(filename):

    filename = raw_input("Which file would you like to process? (include the extension, only .txt and .docx supported)\n")
    # saving name of custom word file
    if re.search("\.docx$", filename):
        # docx file
        cont = textract.process("inputs/" + filename)
        # supplement for the replacement function
        text = str(cont)
        text = text.replace("\\xe2\\x80\\x9c", '"')
        text = text.replace("\\xe2\\x80\\x9d", '"')
        text = text.replace('\\xe2\\x80\\x98', "\'")
        text = text.replace('\\xe2\\x80\\x99', "\'")
        cont = text
    elif re.search("\.txt$", filename):
        customfile = filename.replace('.txt', '_cts.txt')
        print(customfile)
        # reading main content file
        choice = os.path.join('inputs', filename)
        my_file = open(choice, "r")
        cont = my_file.read()
    else:
        print("file invalid")
        quit()



    #inputList = cont.split(" ")
    return cont


# checks string for custom words
def checkForCustomWords(madlib):

    return False


def quoteConverter(text):

    #print(text)
    text = text.replace('\u2018\u2018', '"')
    text = text.replace('\u2019\u2019', '"')
    text = text.replace('\u2018', "\'")
    text = text.replace('\u2019', "\'")
    text = text.replace('\u201C', '"')
    text = text.replace('\u201c', '"')
    text = text.replace('\u201D', '"')
    text = text.replace('\u201d', '"')

    return text


# Main function
def main():
    # Test 1
    d = doesFileExist('wordquotetest.docx')
    print("Test 1 Result: ", d)

    # Test 2
    c = readCustomFile('customtestin')
    print("Test 2 Result: ", c)

    # Test 3
    g = checkForCustomWords("")
    print("Test 3 Result: ", g)

    # Test 4
    h = quoteConverter("“Go /ct1_1! Shouted Mackey.”")
    print("Test 3 Result: ", h)


if __name__ == "__main__":
    main()
