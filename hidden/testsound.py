import winsound
import threading

import os
print("Exists:", os.path.exists("piano.wav"))
print("Full path:", os.path.abspath("piano.wav"))

def play_sound():
    winsound.PlaySound("piano.wav", winsound.SND_FILENAME)
threading.Thread(target=play_sound, daemon=True).start()