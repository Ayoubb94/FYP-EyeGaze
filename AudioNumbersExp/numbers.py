""" This module generates an audio file with random numbers uttered every 2 seconds. """

import os
import sys
import random
from pydub import AudioSegment


def check_files(dir_path):
    # This function checks if the audio files meet the requirements
    numbers = dir_path + "/numbers"
    if os.path.isdir(numbers): # Check if numbers directory exists
        pass
    else:
        print("Folder 'numbers' containing audio files doesn't exist!")
        sys.exit()
    if len(os.listdir(numbers)) != 10: # Check if there are 10 audio files there
        print("Make sure there are 10 audio files in the folder!")
        sys.exit()
    else:
        for file in os.listdir(numbers): # Check all audio files are mp3
            if file.lower().endswith(".mp3"):
                if file[:-4].isdigit(): # Check if all audio files are names in digits
                    pass
                else:
                    Print("Make sure filenames are numbers!")
                    sys.exit()
            else:
                print("Make sure all audio files are mp3!")
                sys.exit()


def generate_random():
    # Generate a random integer between 0 and 9
    r = str(random.randint(0, 9)) + ".mp3"
    return r


def generate_file(dir_path):
    # Generate the audio file
    numbers = dir_path + "/numbers"
    pause = AudioSegment.silent(duration=2000)
    r = str(random.randint(0, 9)) + ".mp3"
    first = AudioSegment.from_mp3(numbers + "/" + r)
    for i in range(180):
        first = first + pause + AudioSegment.from_mp3(numbers + "/" + generate_random())
    save_file(first, dir_path)


def save_file(audio, dir_path):
    # Save the audio file
    if not os.path.exists("results"):
        os.makedirs("results")
    audio.export(dir_path + "/results/audio.mp3", format="mp3")


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    check_files(dir_path)
    generate_file(dir_path)