#!/usr/bin/env python3

import subprocess
import glob


WORKING_DIR = "/home/pi/lightshowpi"
SONG_DIR = WORKING_DIR + "/music/"
PLAYLIST_DIR = WORKING_DIR + "/playlists/"
LIGHTS_SCRIPT = WORKING_DIR + "/py/synchronized_lights.py"


def numeric_choice_check(choice, start, end):
    if choice.isnumeric():
        return int(choice) in range(start, end+1)
    return False

def get_formatted_name(path_string, extension):
    filepath = path_string.split("/")
        
    filename = filepath[len(filepath)-1]

    #return filename.replace("-", " ")[:(-1 * len(extension))].title()
    return filename[:(-1 * len(extension))].title()

def print_file_list(files):

    GAP_LENGTH = 50
    
    for i in range((len(files) +0) // 2):

        i2 = i + (len(files) // 2)
        
        file1 = get_formatted_name(files[i], ".mp3")    

        gap = " " * (GAP_LENGTH - len(file1))
        
        if i < 9:
            file1 = " " + file1

        file2 = get_formatted_name(files[i2], ".mp3")

        print(str.format("{}. {}{}{}. {}", i+1, file1, gap, i2+1, file2))

    if (len(files) % 2 != 0):
        print(str.format("{}{}. {}", " " * (GAP_LENGTH + 4), len(files), get_formatted_name(files[len(files)-1], ".mp3")))


def play_song(path):
    return subprocess.Popen(["sudo", "python", LIGHTS_SCRIPT, "--file=" + path])

def play_playlist(path):
    return subprocess.Popen(["sudo", "python", LIGHTS_SCRIPT, "--playlist=" + path])

def get_song_choice(banner, songs):
    while True:
        print("Available choices:")
        print_file_list(songs)
        print()
        print(banner)
        
        choice = input(">>>")

        if numeric_choice_check(choice, 1, len(songs)):
            return songs[int(choice) - 1]

        print("Error: invalid choice")

def get_songs():
    return sorted(glob.glob(SONG_DIR + "*.mp3"))

def menu():
    print("---PyLightshow---")
    print(" 1. Play a song")
    print(" 2. Stop current")
    print(" 3. Refresh song list from disk")
    print(" 4. STOP AND EXIT")
    print("\nSelect one:")

    choice = input(">>>")

    if numeric_choice_check(choice, 1, 6):
        return int(choice)



# Code execution begins below
all_songs = get_songs()
running = True
now_playing = None
    

while running:
    mode = menu()

    if mode == 1:   
        choice = get_song_choice("Which song to play?", all_songs)

        if (now_playing != None):
            now_playing.terminate()
    
        now_playing = play_song(choice)
        
    elif mode == 2:
        if now_playing != None:
            now_playing.terminate()
        print("Stopped.")
    elif mode == 3:
        all_songs = get_songs()
        print("List updated.")
    elif mode == 4:
        if now_playing != None:
            now_playing.terminate()
        running = False

#GPIO.cleanup()
print("Goodbye!")


