welcome = (
    "Welcome to the Madlib Maker\nHere you can compose and fill in madlibs using our specialized syntax.\n")
makeSelection = (
    "Please select from the following menu options\n(enter the corresponding number):\n1. Type madlib\n2. Use a madlib "
    "from the \"inputs\" folder.\n3. "
    "Instructions\n")
instruct0 = ("Which would you like to learn about:\n1. How to write Madlibs\n2. "
             "Syntax\n3. Using premade madlibs\n4. Custom Words\n5. Saving and printing madlibs\nType \"q\" to return to the menu.\n")
instruct1 = ("Here in the Madlib Maker, you can write a Madlib directly or process a file you've already "
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
instruct3 = (
    "Valid input files can be made from within or outside this program, simply type\nyour madlib with the supported "
    "keywords into a supported file and move said file into the \"inputs\"\nfolder that was created when you first "
    "ran the program.\n\nIf you have perchance received a madlib from a firend, ensure that you transfer "
    "any\nassociated custom file of the same name to the inputs folder. Custom files have the same filename as the "
    "madlib\nas the madlib for which it was creted but have the extension \"_cts.txt\".\n\nThis program currently "
    "supports txt and docx files.\n\nWARNING: Do not copy/paste your madlib from the .docx file to the text file "
    "unlesss you have turned\ncurly punctuation and other unsupported characters off.")
instruct4 = (
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
instruct5 = ("After writing a madlib, you can save it to the \"inputs\" folder for later use.\nThis is usefull "
             "if you have a lengthy madlib that you wish to fill in later or multiple times.\nIf you wish to "
             "type a madlib outside of this program, note that the current build accepts text and docx files only and "
             "refrain from adding a title/heading in word"
             "as it will be entered later in the program.\nReview the \"Syntax\" section of the instructions for "
             "the proper syntax of an input file.\n\nWith a madlib typed or selected, you may chose to fill it "
             "within the program or\nprint it as a traditional unfilled maldib on paper.\nOutputs of either "
             "nature will be saved to the \"outputs\" folder.\nThe filled madlibs will be saved as a text file "
             "while traditional madlibs will be converted into\nHTML files designed to display the heading and "
             "blanks with word categories underneath. Drag the\nHTML file into any web browser to view it in "
             "the traditional madlib format, then use the respective\nbrowser's print feature to print a "
             "physical copy of the madlib.")

