#!/usr/bin/env python3

import subprocess
import os

EXERCISM_SUBMIT_COMMAND = "exercism submit "
GIT_DIFF_COMMAND = "git diff --cached --name-only --diff-filter=ACM"
UTF8_ENC = "UTF-8"


def hook():
    print("============================================================")
    print("_________.__                           __                         ")
    print("\\_____   \\  |__ _____   _____  _____ _/  |_  ____  ______       ")
    print(" |    ___/  |  \\\\__  \\ /     \\ \\__  \\\\   __\\/  _ \\/  ___/")
    print(" |   |   |   Y  \\/ __ \\|   |  \\/ __  \\|  | (  <_> )___ \      ")
    print(" |___|   |___|  (____  /___|  (____   /__|  \____/____  >         ")
    print("               \/     \/     \/     \/                \/        \n")

    print("          Pre-commit hook for Exercism integration            \n\n")

    pwd = os.getcwd()
    files = subprocess.check_output(GIT_DIFF_COMMAND,
                                    shell=True,
                                    stderr=subprocess.STDOUT)\
        .decode(UTF8_ENC).split()

    if len(files) == 0:
        raise FileNotFoundError(
            "No files are being committed. Commit aborted from pre-commit hook")

    exercise_files = []
    prev_lang = None
    prev_exercise = None

    for file in files:
        lang, exercise = file.split(os.sep)[:2]

        if (lang != prev_lang or exercise != prev_exercise) and prev_lang:
            print(subprocess.check_output(EXERCISM_SUBMIT_COMMAND +
                                          ' '.join(exercise_files),
                                          shell=True,
                                          stderr=subprocess.STDOUT)
                  .decode(UTF8_ENC))

            exercise_files = []

        exercise_files.append(pwd + os.sep + file)

        prev_exercise = exercise
        prev_lang = lang

    print(subprocess.check_output(EXERCISM_SUBMIT_COMMAND
                                  + ' '.join(exercise_files),
                                  shell=True,
                                  stderr=subprocess.STDOUT)
          .decode(UTF8_ENC))

    print("============================================================\n")


if __name__ == "__main__":
    hook()
