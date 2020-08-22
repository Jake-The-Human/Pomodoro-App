from enum import Enum
from sys import platform

import json


try:
    with open('config.json') as f:
        appConfig = json.load(f)
except IOError:
    appConfig = None


# This func let the program still run if there is no config file
def defaultValuesFromFile(config, key, defaultValues):
    if config is not None and (value := config.get(key, False)):
        results = defaultValues
        counter = 0
        for k, v in value.items():
            results[counter] = (v if (k is not None) else defaultValues.at(counter))
            counter += 1
        return results
    else:
        print("Something went wrong with config file.")
        return defaultValues


def setupLang(config, lang, defualtValues):
    if config is not None and (value := config.get('lang', False)):
        return defaultValuesFromFile(value, lang, defualtValues)
    else:
        print("Something went wrong with config file.")
        return defualtValues

# DEFAULT VALUES #
# Window WIDTH AND HEIGHT
WINDOW_WIDTH, WINDOW_HEIGHT = defaultValuesFromFile(appConfig, 'window_size', [250, 300])

# TIMER LENGTHS
WORK_MINUTES, BREAK_MINUTES, LONG_BREAK_MINUTES = defaultValuesFromFile(appConfig, 'time', [25, 5, 30])

WORK_SECONDS = WORK_MINUTES * 60
BREAK_SECONDS = BREAK_MINUTES * 60
LONG_BREAK_SECONDS = LONG_BREAK_MINUTES * 60

# COLOR VALUES
BACKGROUND_COLOR, TIMER_BG_COLOR, TIMER_COLOR, TIMER_CENTER_COLOR, NUM_POMODORO_COLOR = defaultValuesFromFile(
    appConfig,
    'color',
    ["turquoise", "light green", "coral", "dark grey", "red"]
)
# KEY BINDINGS
KEY_RESET, KEY_PAUSE = defaultValuesFromFile(appConfig, 'keyboard_shortcuts', ["r", " "])

# STRINGS
CURRENT_LANG = 'english'
GET_READY, START, PAUSE, FOCUS, BREAK_TIME = setupLang(
    appConfig,
    CURRENT_LANG,
    ["Get Ready!", "Start", "Pause", "Focus!", "Break Time!"]
)

# OS
WINDOWS = platform == 'win32' or platform == 'cygwin'
MAC = platform == 'darwin'
LINUX = platform == 'linux'
#       --       #


class Mode(Enum):
    WORK = 0
    SHORT_BREAK = 1
    LONG_BREAK = 2


def modeString(mode):
    return FOCUS if (mode == Mode.WORK) else BREAK_TIME


def playSound(play=True):
    if play:
        if WINDOWS:
            import winsound
            winsound.Beep(frequency=440, duration=400)
            winsound.Beep(frequency=440, duration=400)
        elif MAC or LINUX:
            import sys
            print('\a\a', end='\r', file=sys.stdout)
    return
