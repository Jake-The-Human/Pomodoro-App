from enum import Enum
from sys import platform


# DEFAULT VALUES #
# Window WIDTH AND HEIGHT
WINDOW_WIDTH  = 250
WINDOW_HEIGHT = 300
# TIMER LENGTHS
WORK_MINUTES = int(25)
BREAK_MINUTES = int(5)
LONG_BREAK_MINUTES = int(30)

WORK_SECONDS = WORK_MINUTES * 60
BREAK_SECONDS = BREAK_MINUTES * 60
LONG_BREAK_SECONDS = LONG_BREAK_MINUTES * 60
# COLOR VALUES
BACKGROUND_COLOR = "turquoise"
TIMER_BG_COLOR = "light green"
TIMER_COLOR = "coral"
TIMER_CENTER_COLOR = "dark grey"
NUM_POMODORO_COLOR = "red"
# STRINGS
GET_READY = "Get Ready!"
START = "Start"
PAUSE = "Pause"
FOCUS = "Focus!"
BREAK_TIME = "Break Time!"
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
			print('\a\a', end='')

