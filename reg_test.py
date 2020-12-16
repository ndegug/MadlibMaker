#nick 12/15/2020
#testing the goddamn regex feature

import re

def regex_example(word):
    unnumbered="(/...)"
    numbered="(/...[0-9]+)"
    # Define a string
    print(re.match(numbered, word))
    if re.findall(unnumbered, word) and not re.findall(numbered, word):
        print("replace the unnumbered word")
    elif re.findall(numbered, word):
        print("replace the numbered word")
    else:
        print("not a keyword, just append")

    # Replace the string
    new="sunny"
    repStr = re.sub(unnumbered, new, word)

    # Print the replaced string
    print(repStr)
    return 0



regex_example("/adj")