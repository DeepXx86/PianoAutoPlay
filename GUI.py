import pyautogui as pau
import time as t
import keyboard
import tkinter as tk
from threading import Thread


stop_playing = False


def press_key(keys, duration=0.3, delay_between_keys=0.1):
    if stop_playing:
        return
    if isinstance(keys, list):
        for key in keys:
            keyboard.press(key)
        t.sleep(duration)
        for key in keys:
            keyboard.release(key)
    else:
        keyboard.press(keys)
        t.sleep(duration)
        keyboard.release(keys)
    t.sleep(delay_between_keys)  


def parse_song(song_text):
    parsed_song = []
    i = 0
    while i < len(song_text):
        if stop_playing:
            break
        if song_text[i] == '[':
            end_idx = song_text.find(']', i)
            keys = list(song_text[i+1:end_idx])
            parsed_song.append(keys)
            i = end_idx + 1
        elif song_text[i] == ' ':
            i += 1  
        else:
            parsed_song.append(song_text[i])
            i += 1
    return parsed_song


def play_song(song_text, delay_between_keys=0.05):
    song = parse_song(song_text)
    for keys in song:
        if stop_playing:
            break
        press_key(keys, delay_between_keys=delay_between_keys)  


def start_playing():
    global stop_playing
    stop_playing = False
    song_text = song_entry.get("1.0", tk.END).strip()
    delay = float(delay_entry.get())
    t.sleep(2)  
    play_thread = Thread(target=play_song, args=(song_text, delay))
    play_thread.start()


def stop_playing_song(e=None):
    global stop_playing
    stop_playing = True


root = tk.Tk()
root.title("Roblox Piano Auto Play")


song_entry = tk.Text(root, height=20, width=80)
song_entry.pack(pady=10)


delay_label = tk.Label(root, text="Delay between key (seconds):")
delay_label.pack(pady=5)
delay_entry = tk.Entry(root)
delay_entry.pack(pady=5)
delay_entry.insert(0, "0.05")  


play_button = tk.Button(root, text="Play Song", command=start_playing)
play_button.pack(pady=10)


root.bind('t', stop_playing_song)


root.mainloop()
