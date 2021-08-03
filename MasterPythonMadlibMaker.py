from MadlibMakerHelpers import *
from long_strings import *
from past.builtins import raw_input
outlist = []
#custom = {}
latlist = []

if not os.path.isdir(os.path.join(os.getcwd(), "inputs")):
    os.mkdir(os.path.join(os.getcwd(), "inputs"))
if not os.path.isdir(os.path.join(os.getcwd(), "outputs")):
    os.mkdir(os.path.join(os.getcwd(), "outputs"))
# def cust_config():
#     print("Custom words detected, enter each of your custom words, one by one, in order of appearance. Enter \"q\" to "
#           "stop ")
#     for word in inputList:
#         if re.findall(customreg, word):
#             regkey = re.findall(customreg, word)
#             realkey = ''.join(regkey)
#             if realkey not in custom:
#                 base = re.findall(customreg, word)
#                 base = ''.join(base)
#                 regnum = re.findall(r'\d+', base)
#                 num = ''.join(regnum)
#                 print("Custom " + str(num))
#                 ch = raw_input()
#                 custom[realkey] = ch
#             else:
#                 pass
#         else:
#             pass
# def file_read():
#     filename = raw_input("Which file would you like to process? (type the name with no extension)\n")
#     # saving name of custom word file
#     customfile = filename + "_cts.txt"
#     # reading main content file
#     choice = os.path.join('inputs', filename + ".txt")
#     my_file = open(choice, "r")
#     cont = my_file.read()
#     inputList = cont.split(" ")
#     if os.path.exists(os.path.join('inputs', customfile)):
#         choice = os.path.join('inputs', customfile)
#         with open(choice) as f:
#             data = f.read()
#         custom = json.loads(data.replace("\'", "\""))
#         f.close()
#     elif not os.path.exists(os.path.join('inputs', customfile)) and re.search(customreg, str(inputList)) is not None:
#         cust_config()
#         file_write(str(custom), filename, 'inputs', '_cts.txt')
#     else:
#         pass
choice = raw_input(welcome)
if choice == "1":
    # manual input
    cont = raw_input("Enter the madlib below:\n")
    inputList = cont.split(" ")
    if re.search(customreg, str(inputList)) is not None:
        cust_config()
    else:
        pass
    choice = raw_input("Would you like to save your madlib to the inputs folder before filling it?\n")
    if choice == "yes":
        filename = raw_input("What do you wish to name the file? (do not type the extension): ")
        # main content file
        file_write(' '.join(inputList), filename, 'inputs', '.txt')
        # custom words file
        if re.search(customreg, str(inputList)) is not None:
            file_write(str(custom), filename, 'inputs', '_cts.txt')
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
    file_read()
    from MadlibMakerHelpers import inputList
    from MadlibMakerHelpers import custom
elif choice == "3":
    while choice != "q":
        choice = raw_input(instruct0)
        if choice == "1":  # todo add a "process pre-made file" instructions
            print(instruct1)
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
            print(instruct3)
        elif choice == "4":
            print(instruct4)
        elif choice == "q":
            print("I hope these instructions helped, start the program again to give it a try!\nHave a good day!")
            exit()
        else:
            print(potato)
            exit()

else:
    print(potato)
    exit()

regkey = ""
realkey = ""

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
        if choice2 == "1" and realkey in generic_words:
            outlist.append(keyword_convert(realkey, word, 0))
        elif choice2 == "1" and realkey not in generic_words:
            outlist.append(keyword_convert(realkey, word, 6))
        elif choice2 == "2" and realkey in generic_words.keys():
            latword = htmlsample.replace('underscript', generic_words[realkey])
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
        elif choice2 == "2" and realkey not in generic_words.keys():
            latlist.append(invalid_html(0, realkey, word))
    elif re.findall(customreg, word) and not re.findall(numcustreg, word):
        # custom
        regkey = re.findall(customreg, word)
        realkey = ''.join(regkey)
        if choice2 == "1" and realkey in custom:
            outlist.append(keyword_convert(realkey, word, 3))
        # latex array
        elif choice2 == "1" and realkey not in custom:
            outlist.append(keyword_convert(realkey, word, 5))
        elif choice2 == "2" and realkey in custom:
            # saved
            latword = htmlsample.replace('underscript', custom[realkey])
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
        elif choice2 == "2" and realkey not in custom:
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

        if choice2 == "1" and realkey not in numword_dic:
            # numbered cust unsaved
            outlist.append(keyword_convert(realkey, word, 4))
        elif choice2 == "1" and realkey in numword_dic:
            # numbered cust saved
            outlist.append(keyword_convert(realkey, word, 2))
        elif choice2 == "1" and base not in custom:
            # numbered cust saved
            outlist.append(keyword_convert(realkey, word, 5))
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
        if choice2 == "1" and realkey not in numword_dic.keys() and base in generic_words.keys():
            # numbered unsaved
            outlist.append(keyword_convert(realkey, word, 1))
        elif choice2 == "1" and realkey not in numword_dic.keys() and base not in generic_words.keys():
            outlist.append(keyword_convert(realkey, word, 6))  # invalid
        elif choice2 == "1" and realkey in numword_dic.keys():
            outlist.append(keyword_convert(realkey, word, 2))  # numbered saved
        elif choice2 == "2" and base in generic_words.keys():
            latword = htmlsample.replace('underscript', generic_words[base] + ' (' + str(num) + ')')
            final = word.replace(realkey, latword, 1)
            latlist.append(final)
        elif choice2 == "2" and base not in generic_words.keys():
            latlist.append(invalid_html(0, realkey, word))
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
        filename = raw_input("What do you wish to name the file? (do not type the extension): ")
        file_write(filled, filename, 'outputs', '.txt')
        print("Your filled madlib has been saved to the outputs folder, have a good day!")
    elif choice == 'no' or choice == '':
        print("Have a good day!")
    else:
        print(potato2)
        exit()
elif choice2 == '2':
    head = raw_input("What would you like to title this madlib?\n")
    latfill = htmlhead.replace('heading', head, 1) + latfill + ' </p></body></html>'
    filename = raw_input("What do you wish to name the file? (do not type the extension):\n")
    file_write(latfill, filename, 'outputs', '.html')
    print("An HTML coded version of your unfilled madlib has been saved to the outputs folder, "
          "drag the file into your browser to view it. Print the file using your respective browser's print feature.\n"
          "Have a good day!")
elif choice == 'no' or choice == '':
    print("Have a good day!")
else:
    print(potato2)
    exit()