#!/usr/bin/env python

import subprocess
import os
import sys

# Colors
BOLD = '\033[1m'
END_FORMAT = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[36m'
RED_BOLD = BOLD + RED
GREEN_BOLD = BOLD + GREEN

SEPARATOR = "=================================================================="

HEADER_TEXT = \
    """
    ___________                           .__                 
    \\_   _____/__  ___ ___________   ____ |__| ______ _____   
     |    __)_\\  \\/  // __ \\_  __ \\_/ ___\\|  |/  ___//     \\  
     |        \\>    <\\  ___/|  | \\/\\  \\___|  |\\___ \\|  Y Y  \\ 
    /_______  /__/\\_ \\\\___  >__|    \\___  >__/____  >__|_|  / 
            \\/      \\/    \\/            \\/        \\/      \\/  
                  ___ ___                __    
                 /   |   \\  ____   ____ |  | __
                /    ~    \\/  _ \\ /  _ \\|  |/ /
                \\    Y    (  <_> |  <_> )    < 
                 \\___|_  / \\____/ \\____/|__|_ \\
                       \\/                    \\/
                   
                                       licenced GPLv3 by Phanatos\n"""

HEADER = CYAN + SEPARATOR + HEADER_TEXT + SEPARATOR + END_FORMAT + '\n\n'

# Commands
EXERCISM_SUBMIT_COMMAND = "exercism submit "
GIT_DIFF_COMMAND = "git diff --cached --name-only --diff-filter=ACM"
UTF8_ENC = "UTF-8"

# Messages
SUCCESS_MESSAGE = GREEN_BOLD + 'Success: ' + END_FORMAT
ERROR_MESSAGE = RED_BOLD + 'Error: ' + END_FORMAT

NO_FILES_MESSAGE = RED + \
                   "No files are being committed. " \
                   "Commit aborted from pre-commit hook" + \
                   END_FORMAT

INVALID_PARSE_MESSAGE = RED + \
                        "Couldn't find the language or exercise name. " \
                        "This usually means the script is not being run " \
                        "from the excercism root folder." + \
                        END_FORMAT


def hook():
    print(HEADER)

    cwd = os.getcwd()
    files = get_files()

    if len(files) == 0:
        print(NO_FILES_MESSAGE)
        return 1

    exercise_files = []
    prev_lang = None
    prev_exercise = None

    for file in files:
        try:
            exercise, lang = parse_file_name(file)
        except ValueError:
            print(INVALID_PARSE_MESSAGE)
            return 1

        if (lang != prev_lang or exercise != prev_exercise) and prev_lang:
            print(send_exercise(exercise_files))
            exercise_files = []

        exercise_files.append(os.path.join(cwd, file))

        prev_exercise = exercise
        prev_lang = lang

    print(send_exercise(exercise_files))

    print(CYAN + SEPARATOR)


def parse_file_name(file):
    lang, exercise = os.path.split(file)[:2]
    if not lang or not exercise:
        raise ValueError
    return exercise, lang


def get_files():
    return subprocess.check_output(GIT_DIFF_COMMAND,
                                   shell=True,
                                   stderr=subprocess.STDOUT) \
        .decode(UTF8_ENC).split()


def send_exercise(exercise_files):
    try:
        output = subprocess.check_output(EXERCISM_SUBMIT_COMMAND +
                                         ' '.join(exercise_files),
                                         shell=True,
                                         stderr=subprocess.STDOUT)

        output = SUCCESS_MESSAGE + output.decode(UTF8_ENC).split('\n')[0]

    except subprocess.CalledProcessError as e:
        output = ERROR_MESSAGE + e.output.decode(UTF8_ENC).split('\n')[0]

    return output


if __name__ == "__main__":
    sys.exit(hook())
