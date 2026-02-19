# _ _ _ _ _ _

# 8*6=48

# _ _ _ = 4 _
# C: 6, 4
# I: 8, *


# Game start button/type smth in terminal -> timer starts
# They do the game, play sfx
# They complete it or 5 minutes have passed -> timer ends
# Data is documented
# Repeat with other sfx
    
import time

from click import getchar

# somehow load sfx

input("Type 1 to start the game...")
start_time = time.time()

eq1char1 = '8'
eq1char2 = '*'
eq1char3 = '6'
eq1char4 = '='
eq1char5 = '4'
eq1char6 = '8'

guessed = False

progress = 0

while not guessed:
    curprogress = 0
    guess = input("Type your guess for the equation, six characters with no spaces: ")
    if guess == eq1char1 + eq1char2 + eq1char3 + eq1char4 + eq1char5 + eq1char6:
        guessed = True
        print("Correct! You guessed the equation.")
        timer_end = time.time()
    elif len(guess) != 6:
        print("Incorrect guess. Please enter exactly six characters.")
    elif characters in the guess are invalid:
    elif invalid math equation:
    else:
        print ("Incorrect guess. Try again. Here is your progress:")
        # for each character, if the guess is exactly correct, print it
        # if the guess is in the wrong spot, print it
        # else, don't say anything
        # only do sfx if they have made more progress than last time
        if getchar(guess, i) == eq1char1:
            print("Character 1 is correct.")
            curprogress += 1
        elif ... 
        if curprogress > progress:
            # play sfx here
            progress = curprogress

# document & save now