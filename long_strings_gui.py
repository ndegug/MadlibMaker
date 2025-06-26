htmlhead = '<html><head></head><body><h1> heading </h1><style>h1 {text-align: center;}p.big {  line-height: ' \
           '2;}.tab { display: inline-block; margin-left: 80px;}  </style><p class="big"><span class="tab"></span>'
htmlhead_notitle = '<html><head></head><body><style>h1 {text-align: center;}p.big {  line-height: ' \
           '2;}.tab { display: inline-block; margin-left: 80px;}  </style><p class="big"><span class="tab"></span>'
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
#todo: insert return and tab characters where needed
how_to_play_madlibs = """
    In case you’ve never played the age-old game of Madlibs, here’s how the game is played:
    
    A Madlib is a story with missing words. Before reading the story, players are prompted with a word category like “adjective.” At which point, they must choose a word in that category to be written into the vacant space. Once all the blanks are filled, you read the result.
    
    Traditionally, Madlibs are done on paper. One player calls out the categories while others call out the words to fill in each blank. 
    
    This program is meant to help you write, share and play Madlibs written by you or your friends! Once you have a Madlib in our input format, we’ll let you play it and save the hilarious result! Want to play your Madlib the old fashion way with ink and paper? We can help you with that too! See “How to write a Madlib, Loading a Madlib” or “Printing Madlibs” for more details."""

loading_a_madlib = """
    If you wrote a Madlib in our input format or received one from a friend, simply place the file into the “inputs” folder that we’ve placed in the same directory as this program. Our input file is identifiable by distinct keywords such as “/adj” or “/ct1” to encode word entries. To learn more about these keywords, see “How to Write Madlibs.” To play it, select “Load Madlib” from the main menu and click the button with the filename of the Madlib you want to load. If you don’t see the file in the button grid, confirm that the file is in the “inputs” folder and click the “refresh” button.
    
    For more details on writing these input files, see “How to write Madlibs.”"""

how_to_write_a_madlib = """
    Here at the Madlib maker, you can write Madlibs with ease. Write your Madlibs here or your preferred text/documentation software. Write your story and insert one of our keywords. Keywords like “/adj” will be replaced by an “adjective” of the player’s choice. You can type these keywords yourself, or, if you’re typing your Madlib in-house, click the buttons on the keypad that correspond with the word category you want to place in your Madlib. For a full list of the native keywords, click “generic words.” 
    
    For long Madlibs, we recommend writing your Madlib outside of the program and then moving the file to the “inputs” folder to be loaded. We currently support Word Docx and Text files as inputs. Be aware that certain formatting choices in Word may not be supported and may lead to encoding errors. If something doesn’t look right, try turning off special Word characters such as “smart quotes” or converting your Madlib to plain text. See “Loading a Madlib” for more details.
    
    NOTE: Copying and pasting text from Word documents into a text file may not be sufficient to resolve these errors.
    
    If you'd like to add a title at the top of your Madlib, we recommend using our title tag to let the program know that it is there. Simply enter the following at the top of your file:
    
        <t>Your Title Here</t>
    
    Want to use a player’s word more than once? Want to add your own categories? Click on the items below to learn about our advanced keywords to help you do that!"""

generic_words_list = """
 Here is a list of all our natively supported categories and keys:

    '/adj': 'Adjective',     '/nou': 'Noun',     '/pln': 'Plural noun',
    '/ver': 'Verb',     '/vng': 'Verb ending in "ing"',     '/ved': 'Past tense verb',
    '/ves': 'Verb ending in "s"',     '/adv': 'adverb',
    '/num': 'Number',     '/nam': 'Name',     '/cel': 'Celebrity',
    '/per': 'Person',     '/pir': 'Person in room',     '/thi': 'Thing',
    '/pla': 'Place',     '/job': 'Job',     '/ran': 'Random Word',
    '/rex': 'Random Exclamation',     '/tvs': 'TV Show',     '/mov': 'Movie',
    '/mtv': "Movie/TV show",     '/ins': 'Insulting name',     '/phr': 'Random Phrase',
    '/fam': 'Family member (title)',     '/foo': 'Food',     '/ani': 'Animal',
    '/fic': 'Fictional Character',     '/act': 'Activity',     '/bod': 'Body Part',     '/flu': 'Fluid',
    '/emo': 'Emotion',     '/noi': 'noise',     '/eve': 'Event',     '/fos': 'Plural food',     '/fur': 'Furniture'

 If you’d like to add your own, see “Custom Words” for how to do that."""

numbered_words = """
    Numbered words are used to repeat a user’s entry more than once. Simply add a sequence number at the end of the generic word and all keywords of that type and number will be filled in with the first entry. 

    Let’s look at this example:

    The man was so /adj1 and /adj2, he decided that he’d never be /adj2 or /adj1 again!

    Here, the program would ask the player for two adjectives, one after the other. If the player chooses “dirty” and “ugly” for those adjectives, the result would be:

    The man was so dirty and ugly, he decided that he’d never be ugly or dirty again!

    Use this whenever something in the story needs to be repeated."""

custom_words_basics = """
    If there is a category not listed in our generic words that you’d like to add your own, use Custom Words. Basic custom words take the form: “/ct1” where the number following the “ct” is the ID number.

    When the program finds that you’ve added custom word keys, it will ask you to configure them, so remember which number you want your custom category to correspond with. If you are writing your Madlibs externally, 

    Here’s an example:

        “My car sprayed /ct1 all over the /ct2!”

    The program will first ask you to configure these custom words. Enter the word categories when prompted, then you’ll be able to start using them in your Madlib. Suppose you configured the categories to be: “Fluid” and “Thing outside.” When the Madlib is played, the user will be asked for a word in each of these categories and it may result in:

        “My car sprayed apple juice all over the grass!”"""

numbered_custom_words = """
    Custom words can also be numbered in the sequence “/ct1_1” where the first number is the ID number and the second number is the sequence number. 

    Let’s look at another example with the same custom words:

        “My car sprayed /ct1_1 and /ct1_2 all over the place! The /ct1_2 covered the /ct2_1 and the /ct1_1 covered the /ct2_2!”

    In this example, with the same configuration as the lesson in “custom words basics,” the program will ask for words in the following sequence:

        Fluid
        Fluid
        Thing outside
        Thing outside

    When prompted, the user responds with: 
    
        Apple juice 
        Orange juice
        Grass
        Beach ball

    The result:
        “My car sprayed Apple juice and Orange juice all over the place! The Orange juice covered the grass and the Apple juice covered the beach ball!”
    Noticed how each word got carried over to matching sequence numbers (after the underscore). Keep this in mind when writing Madlibs with your own custom categories."""

prewriting_custom_configurations = """
    When writing Madlibs to send to a friend, you’ll want to include your custom words pre-configured so that neither you, nor the recipient will be required to configure them again. To do this, you’ll need to type a custom dictionary.
    
    At the end of the Madlib you wrote, add the following to your next line:
    
        <C>{'/ct1': ‘your first custom here’, '/ct2': 'your second custom here'}
    
    Repeat the sequence above within the curly braces for each of your custom words. 
    
    DO NOT include sequence numbers as in the numbered custom key “/ct1_1!” Simply configure “/ct1” and all the keys that begin with it will prompt that word and distribute the player’s entry across the sequence number. See “Numbered custom words” if you haven’t already.
    
    If you find this procedure overwhelming, simply load your Madlib without the custom dictionary, configure them in the program when prompted, save the input file, and the program will add a custom dictionary to the file for you!"""

printing_madlibs= """
    The Madlib maker can convert your Madlib from its input format to a file that will allow you to print a traditionally styled Madlib on paper with real blanks.
    
    After composing or loading a Madlib input, select "Print Physical" when prompted. If the Madlib input does not have a title, you will be asked if you want to add one.
    
    If you choose to save your file when prompted, you will be asked to compose a filename. Once confirmed, your Madlib will be saved to the "outputs" folder and will have the extension ".html" Do this for long Madlibs that you'd like to reuse later.
    
    Whether you decide to save the file or not, the program will open your file into your default browser. Use said browser's print feature to print your Madlib. This is typically done by entering the menu on the top right and selecting "Print" 
    
    Enjoy the original, authentic experience of filling in a Madlib together with your friends!"""