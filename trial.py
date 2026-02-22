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
import os
import threading

# Primary player (supports many formats if available)
try:
    from playsound3 import playsound
    _HAS_PLAYSOUND3 = True
except Exception:
    _HAS_PLAYSOUND3 = False

# Lightweight reliable WAV player fallback
try:
    import simpleaudio as sa
    _HAS_SIMPLEAUDIO = True
except Exception:
    _HAS_SIMPLEAUDIO = False

# Optional GUI picker (not used in hardcoded mode, kept if you want to switch)
try:
    import tkinter as tk
    from tkinter import filedialog
    _HAS_TK = True
except Exception:
    _HAS_TK = False

ANSWER = "8*6=48"
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

input("Type 1 to start the game...")
start_time = time.time()
progress = 0
guessed = False

# Hardcode the sound file path here (relative or absolute)
# If you run the script from the folder containing the file, a relative name like "piano.wav" works.
# Example (change to your file):
sfx_path = "/Users/inesuriarte/Documents/UofT/03Second_year/Winter/MIE/guessing-game-1/piano.mp3"

def play_for_seconds(path, seconds=2):
    """Play the given file nonblocking and stop after `seconds` where possible."""
    if not path:
        return

    # Debug info
    print("DEBUG: sfx_path:", path)
    print("DEBUG: exists:", os.path.exists(path))

    # Try playsound3 first (returns a handle with stop() when block=False)
    if _HAS_PLAYSOUND3:
        try:
            handle = playsound(path, block=False)
            print("DEBUG: playsound3 started, handle:", handle)
            def stop_handle_after_delay(h, delay):
                time.sleep(delay)
                try:
                    h.stop()
                    print("DEBUG: playsound3 stopped")
                except Exception as e:
                    print("DEBUG: playsound3 stop error:", repr(e))
            threading.Thread(target=stop_handle_after_delay, args=(handle, seconds), daemon=True).start()
            return
        except Exception as e:
            print("DEBUG: playsound3 error:", repr(e))

    # Fallback to simpleaudio for WAV files
    if _HAS_SIMPLEAUDIO and path.lower().endswith(".wav"):
        try:
            wave_obj = sa.WaveObject.from_wave_file(path)
            play_obj = wave_obj.play()
            print("DEBUG: simpleaudio started, play_obj:", play_obj)
            def stop_simpleaudio_after_delay(pobj, delay):
                time.sleep(delay)
                try:
                    pobj.stop()
                    print("DEBUG: simpleaudio stopped")
                except Exception as e:
                    print("DEBUG: simpleaudio stop error:", e)
            threading.Thread(target=stop_simpleaudio_after_delay, args=(play_obj, seconds), daemon=True).start()
            return
        except Exception as e:
            print("DEBUG: simpleaudio error:", e)

    # Last resort: try blocking playsound (will block main thread briefly)
    if _HAS_PLAYSOUND3:
        try:
            print("DEBUG: fallback blocking playsound for short duration (will block).")
            playsound(path, block=True)
        except Exception as e:
            print("DEBUG: final playsound error:", repr(e))
    else:
        print("DEBUG: No suitable audio backend available. Install playsound3 or simpleaudio and retry.")

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

    print("Progress:")
    for i in range(6):
        if correct_pos[i]:
            print(f"Position {i+1}: correct ({guess[i]})")
        elif correct_wrong_pos[i]:
            print(f"Position {i+1}: wrong position ({guess[i]})")

    if curprogress > progress:
        # play sfx here (nonblocking where possible, stops after ~2 seconds)
        if sfx_path:
            play_for_seconds(sfx_path, seconds=2)

        progress = curprogress

# document & save now
print(f"Time taken: {passed_time:.2f} seconds")
print(f"Number of guesses: {numguesses}")