import random
import os


def pick_word(file):
    f = open(file, 'r')
    ls = []
    for line in f:
        ls.append(line)

    f.close()

    if len(ls) == 0:
        print("No words in file")
        exit()
    else:
        word = ls[random.randint(0, len(ls))]

    return word


def get_correct_letters(word):
    d = {}
    for l in word:
        if l in d:
            d[l] = d[l] + 1
        else:
            d[l] = 1

    return d


def check_letter(letter, dictionary):
    if letter in dictionary:
        return True
    else:
        return False


def draw_board(hang_man, lives):
    print(hang_man[lives])
hang_man = [
    """
    +------|
    |      
    |     
    |	  
    |
    =========""",
    """
    +------|
    |      O
    |     
    |	  
    |
    =========""",

    """
    +------|
    |      O
    |      |
    |	   
    |
    =========""",
    """
    +------|
    |      O
    |     /|
    |	  
    |
    =========
    """,
    """
    +------|
    |      O
    |     /|\\
    |	  
    |
    =========
    """,
    """
    +------|
    |      O
    |     /|\\
    |     / 
    |
    =========""",
    """
    +------|
    |      O
    |     /|\\
    |     / \\
    |
    =========
    """
]


def user_won(correct_guesses, correct_letters):
    if (len(correct_guesses) == len(correct_letters) - 1):
        return True
    else:
        return False


def show_word(word, correct_guesses):
    for l in word:
        if l in correct_guesses:
            print(l, end=" ")
        else:
            print("_", end=" ")
    print("\n")


def game_loop():
    os.system('cls')
    print("======================================")
    print("          Welcome to hangman          ")
    print("======================================")
    print(" Rules:")
    print(" * Select weather you want to pick a \n  word or letter.")
    print(" * If you pick the wrong letter you lose one life.")
    print("======================================")
    print(" Scoring:")
    print(" * 1 point for each correct guess.")
    print(" * 10 extra points for each win.")
    print("======================================")

    f = input("Enter the name of the file containing a list of words: ")

    if ".txt" not in f:
        print("File must be a txt file")
        exit()
    else:
        lives = 0
        word_guesses = 2
        num_guesses = 0
        score = 0
        game_over = False
        chosen_word = pick_word(f)
        correct_letters = get_correct_letters(chosen_word)
        correct_guesses = dict()
        incorrect_guesses = set()
        messages = []
        game_exited = False

        while not game_exited:
            os.system('cls')

            # Check if player has won or died
            if (user_won(correct_guesses, correct_letters) or lives == 5):
                game_over = True

            # print out the options, board, and messages
            print("======================================")
            print(" Available Word Guesses:", word_guesses)
            print(" Incorrect Guesses", "{} " if len(incorrect_guesses) == 0 else incorrect_guesses)
            print(" Number of Guesses:", num_guesses)
            print(" Word Length:", len(chosen_word) - 1)
            print("\n Current Score:", score)
            print("======================================")

            draw_board(hang_man, lives)

            # print out each letter in the word
            word = str(chosen_word).strip()
            show_word(word, correct_guesses)

            if (len(messages) > 0):
                # print out any messages that were added from previous round
                print(messages[0], "\n")
                # remove all messages from queue after printing
                messages.clear()

            option = input("Options:\n1. Guess letter\n2. Guess word\n\nSelection: ")

            if (option == "1"):
                guess = input("Enter a letter: ")

                if (check_letter(guess.lower(), correct_letters) == 0):
                    if (check_letter(guess.lower(), incorrect_guesses) == 0):
                        num_guesses += 1
                        lives += 1
                        incorrect_guesses.add(guess)
                    else:
                        messages.append("You have already guessed " + guess.lower())
                else:
                    if (check_letter(guess.lower(), correct_guesses) == 0):
                        num_guesses += 1
                        # add the new message from this round
                        messages.append("\nThere are " + str(
                            correct_letters[guess.lower()]) + " " + guess.lower() + "'s in the word.")

                        # add current guess to correct guesses set and update score
                        correct_guesses[guess.lower()] = correct_letters[guess.lower()]
                        score += 1
                    else:
                        messages.append("You have already guessed " + guess.lower())


            elif (option == "2"):
                if (word_guesses > 0):
                    guess = input("Enter word: ")

                    word_guesses -= 1

                    if (guess.lower() == word):
                        for l in guess.lower():
                            if (check_letter(l, correct_guesses) == 0):
                                correct_guesses[l] = correct_letters[l]
                                score += 1
                        game_over = True
                    else:
                        messages.append(guess + " is not the chosen word")
                else:
                    messages.append("No more word guesses allowed")

            else:
                messages.append("Invalid option")

            if (game_over):
                os.system('cls')

                if (user_won(correct_guesses, correct_letters)):
                    score += 10
                    print("\nYOU WON!\n")
                    print("Your Word Was:", chosen_word)
                    print("Current Score:", score)
                else:
                    print("\nYOU LOSE!\n")
                    print("Your Word Was:", chosen_word)
                    print("Current Score:", score)
                option = input("\nWould you like to play again? [Y or N]: ")

                if (option.lower() == "y"):
                    game_over = False
                    num_guesses = 0
                    lives = 0
                    chosen_word = pick_word(f)
                    correct_letters = get_correct_letters(chosen_word)
                    incorrect_guesses.clear()
                    correct_guesses.clear()
                else:
                    os.system('cls')
                    print("======================================")
                    print(" Final Score", score)
                    print("======================================")
                    game_exited = True
                    exit()


if __name__ == "__main__":
    game_loop()
