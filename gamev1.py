# Game start button/type smth in terminal -> timer starts
# They do the game, play sfx
# They complete it or 5 minutes have passed -> timer ends
# Data is documented
# Repeat with other sfx
    
import time
import winsound
import threading

def play_sound():
    winsound.PlaySound("src/real_1.wav", winsound.SND_FILENAME)

ANSWER = "7*6=42"
TIME_LIMIT = 300  # 5 mins

numguesses = 0

def is_valid_equation(eq):
    if eq.count("=") != 1:
        return False
    left, right = eq.split("=")

    if left[0] in "+-*/" or right[0] in "+-*/":
        return False
    if left[-1] in "+-*/" or right[-1] in "+-*/":
        return False

    try:
        return eval(left) == eval(right)
    except:
        return False

def check_progress(guess, answer):
    correct_pos = []
    correct_wrong_pos = []

    for i in range(6):
        if guess[i] == answer[i]:
            correct_pos.append(True)
            correct_wrong_pos.append(False)
        elif guess[i] in answer:
            correct_pos.append(False)
            correct_wrong_pos.append(True)
        else:
            correct_pos.append(False)
            correct_wrong_pos.append(False)

    return correct_pos, correct_wrong_pos

input("Press enter to start the game...")
start_time = time.time()
progress = 0
guessed = False

while not guessed:
    if time.time() - start_time > TIME_LIMIT:
        print("Time's up!")
        passed_time = TIME_LIMIT
        break

    guess = input("Enter a 6-character equation: ")
    passed_time = time.time() - start_time
    numguesses += 1

    if len(guess) != 6:
        print("Must be exactly 6 characters.")
        continue

    if any(c not in "0123456789+-*/=" for c in guess):
        print("Invalid characters used.")
        continue

    if not is_valid_equation(guess):
        print("Invalid equation.")
        continue

    if guess == ANSWER:
        guessed = True
        print("Correct! You solved it.")
        break

    correct_pos, correct_wrong_pos = check_progress(guess, ANSWER)

    curprogress = sum(correct_pos)

    print()
    print("Progress:")
    # display the max number of correct positions
    # display ALL positions -> green yellow grey
    for i in range(6):
        if correct_pos[i]:
            print(f"Position {i+1}: correct ({guess[i]})")
        elif correct_wrong_pos[i]: # this is wrong for double letters but it doesn't matter if we use single letters only in equation
            print(f"Position {i+1}: wrong position but is in the equation somewhere else ({guess[i]})")

    if curprogress > progress:
        # play sfx here
        play_sound()
        progress = curprogress

# document & save now
print(f"Time taken: {passed_time - (numguesses - 1) * 2:.2f} seconds")
print(f"Number of guesses: {numguesses}")