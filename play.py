import random
import time
import os
import itertools
import sys

MIN_NUM_PLAYERS = 2
MIN_NUM_CHAMELEONS = 0
NUM_SECONDS_BETWEEN_PLAYERS = 3

def play_game(words, default_words, user_input_number_of_chameleons=False,
              test=False):
    """
    plays a single game. asks for number of players

    :param words: the list of words to choose from

    :return:
    the word that was chosen and a boolean representing if the game
    should restart
    """

    num_players = input("how many players? enter here: ")
    int_num_players = int(num_players)

    player_list = [player for player in range(int_num_players)]

    # randomly choose a number of chameleons bounded below by the
    # minimum number of chameleons and bounded above by the maximum number
    # of chameleons
    # equal probability of choosing any number of chameleons
    if user_input_number_of_chameleons is True:
        num_cham = int(input(f"how many chameleons would you like to play with? (number between 0 and {int_num_players}): "))
        while num_cham > int_num_players:
            num_cham = int(input(f"try again; number must be between 0 and {int_num_players}: "))
    else:
        max_num_cham = int(input(f"what is the maximum number of chameleons? (number between 0 and {int_num_players-2}): "))
        num_cham = random.randint(MIN_NUM_CHAMELEONS, max_num_cham)

    # given a number of chameleons, choose a random combination of players to
    # be the chameleon
    chameleon_combos = list(itertools.combinations(player_list, num_cham))
    rand_int = random.randint(0, len(chameleon_combos)-1)
    chameleon_nums = chameleon_combos[rand_int]
    if test:
        print(f"chameleons: {chameleon_nums}")

    # choose a random word from the list of words
    rand_word = words[random.randint(0, len(words))]

    for i in range(int_num_players):
        print(f"player {i+1}:")
        if i in chameleon_nums:
            print("lol YOU are the chameleon")
        else:
            print(f"the word is: {rand_word}")

        if i+1 == int_num_players:
            print("play on!")
            time.sleep(NUM_SECONDS_BETWEEN_PLAYERS*3)
        else:
            isReady = None
            while isReady != "y":
                isReady = input(f"when you are ready type 'y' and hit enter... ")

        if not test:
            os.system('clear')
            print(f"changing in {NUM_SECONDS_BETWEEN_PLAYERS} seconds ... ")
            time.sleep(NUM_SECONDS_BETWEEN_PLAYERS)

    if default_words == True:
        delete_word_str = input(f"was ~~{rand_word}~~ a bad word? should it be removed permanately from the default word list? (y/n) ")
        if "y" in delete_word_str:
            delete_word(rand_word)

    play_again_str = input("would you like to play again? (y/n) ")

    if "y" in play_again_str:
        play_again = True
    else:
        play_again = False

    return play_again, rand_word

def read_words(f_in):
    """
    turns a txt file into a list

    :param f_in: location of the input file

    :return:
    an error, if its unreadable, or the list of words
    """
    try:
        with open(f_in) as input_file:
            contents = input_file.readlines()
        words = [x.strip() for x in contents]
        return words
    except:
        print("~~ERROR~~ with the input file!! try again")

def delete_word(word, f_in="default_words.txt"):
    """
    delets a word from the default txt file

    :param f_in: location of the input file

    :return:
    an error if it didn't work and a 1 if it did
    """
    try:
        with open(f_in, 'r') as input_file:
            lines = []
            for line in input_file:
                lines.append(str(line.replace("\n", "")))
            lines.remove(word)
            input_file.close()

        with open(f_in, 'w') as input_file:
            for line in lines:
                input_file.write(line)
                input_file.write("\n")
            input_file.close()
    except e:
        print("~~ERROR~~ with the input file!! try again")

    print(f"removed word was: {word}")
    return 1

if __name__ == "__main__":

    if len(sys.argv) > 1:
        print(f"using words in text file: {sys.argv[1]}")
        words = read_words(f_in=sys.argv[1])
        default_words = False

    else:
        words = read_words("default_words.txt")
        default_words = True

    playing = True
    while playing:
        print(f"MINIMUM NUMBER OF PLAYERS: {MIN_NUM_PLAYERS}")
        print(f"MINIMUM NUMBER OF CHAMELEONS: {MIN_NUM_CHAMELEONS}")
        user_num_cham_str = input("would you like to specify the number of chameleons? (otherwise it will be random) (y/n) ")
        if "y" in user_num_cham_str:
            playing, word = play_game(words, default_words, user_input_number_of_chameleons=True)
        else:
            playing, word = play_game(words, default_words)
        words.remove(word)
    print("\n\nGame Over")
