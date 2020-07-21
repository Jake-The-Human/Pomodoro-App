import tkinter as tk
from datetime import datetime
from enum import Enum
import argparse

# NOTE: make a array of colors so each run of the timer will have a different color
# TODO: Add config file to set a default colors and time
# TODO: Make GUI-less option

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
#STRINGS
GET_READY = "Get Ready!"
START = "Start"
PAUSE = "Pause"
FOCUS = "Focus!"
BREAK_TIME = "Break Time!"
#       --       #

class Mode(Enum):
	WORK = 0
	SHORT_BREAK = 1
	LONG_BREAK = 2


def getCommandLineArgs():
	parser = argparse.ArgumentParser(description='Setup your Pomodoro Timer')
	parser.add_argument(
		'Focus timer length', 
		metavar='F_Time',
		type=int,
		nargs='?',
		help='The number of minutes you want to focus for. Default: '+str(WORK_MINUTES)+' minutes'
	)
	parser.add_argument(
		'Break timer length',
		metavar='B_Time',
		type=int,
		nargs='?',
		help='The number of minutes you want to break for. Default: '+str(BREAK_MINUTES)+' minutes'
	)
	# parser.add_argument(
	# 	'Long break timer length',
	# 	metavar='L_Time',
	# 	type=int,
	# 	nargs='?',
	# 	help='The number of minutes you want to take a long break for'
	# )
	parser.add_argument(
		'Window Width',
		metavar='w',
		type=int,
		nargs='?',
		help='Width. Default:'+str(WINDOW_WIDTH)
	)
	parser.add_argument(
		'Window Height',
		metavar='h',
		type=int,
		nargs='?',
		help='Height. Default:'+str(WINDOW_HEIGHT)
	)
	return vars(parser.parse_args())


# x, y are the center of the circle
def createCircle(x, y, r, canvas, **kwargs):
	return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)


def createArc(x, y, r, canvas, **kwargs):
	return canvas.create_arc(x-r, y-r, x+r, y+r, **kwargs)


class Application(tk.Frame):
	def __init__(self, master=None, windowWidth=None, windowHeight=None, workMin=None, breakMin=None, longBreakMin=None):
		if master is None:
			master = tk.Tk()

		super().__init__(master)

		self.columnconfigure(0,weight=1)
		self.rowconfigure([0,1,2],weight=1)
		self.grid(sticky="nsew")

		self.master = master
		self.master.title("Pomodoro")
		self.master.resizable(False, False)

		def argCheck(arg, defaultValue, scaler=1):
			result = int(arg*scaler) if (arg is not None) else int(defaultValue)
			assert result != 0, "Timer times must be at least 1 mintute"
			return result

		windowWidth = argCheck(arg=windowWidth,defaultValue=WINDOW_WIDTH)
		windowHeight = argCheck(arg=windowHeight,defaultValue=WINDOW_HEIGHT)
		self.master.geometry(str(windowWidth)+'x'+str(windowHeight))

		self.counter = 0
		self.timers = { 
			Mode.WORK:argCheck(arg=workMin,defaultValue=WORK_SECONDS,scaler=60),
			Mode.SHORT_BREAK:argCheck(arg=breakMin,defaultValue=BREAK_SECONDS,scaler=60),
			Mode.LONG_BREAK:argCheck(arg=longBreakMin,defaultValue=LONG_BREAK_SECONDS,scaler=60)
		}
		self.mode = Mode.WORK
		self.numberOfPomodoro = 0
		self.numberOfFocusPom = 0

		self.master.bind("<Key>", self.handle_keypress)
		# NOTE DELETE ME: FOR debug #
		self.master.bind("<Escape>", lambda event : self.master.destroy())

		self.create_widgets(windowWidth=windowWidth,windowHeight=windowHeight)
		self.updateCounter()
		self.updateGui()


	def create_widgets(self, windowWidth, windowHeight):
		self.circleCanvas = tk.Canvas(
			master=self,
			width=windowWidth,
			height=windowHeight*0.65,
		)
		self.circleCanvas.grid(row=0,column=0,sticky="nsew")

		# creating the text
		self.timerLabel = tk.Label(
			master=self,
			text=GET_READY,
			font=("Helvetica",int(windowWidth*0.072),"underline")
		)
		self.timerLabel.grid(row=1,column=0,sticky="nsew",pady=4)

		#create buttons
		self.currentTimeLabel = tk.Label(master=self, font=("Helvetica",int(windowWidth * 0.04)))
		self.btn = tk.Button(
			master=self,
			text=START,
			font=("Helvetica",int(windowWidth * 0.04)),
			command=self.startButton
		)

		self.currentTimeLabel.grid(row=2,column=0,sticky="nsw", padx=2)
		self.btn.grid(row=2,column=0,sticky="nse",padx=12, ipadx=20)

		self.master.columnconfigure(0,weight=1)
		self.master.rowconfigure([0,1,2],weight=1)
		return


	def startButton(self):
		self.btn["text"] = PAUSE if (self.btn["text"] == START) else START
		if self.timerLabel["text"] == GET_READY:
			self.timerLabel["text"] = FOCUS
		return


	def updateCounter(self):
		# Update Pomodoro Timer #
		if self.btn["text"] == PAUSE:
			self.counter += 1
		# Put updateCounter to sleep for one second
		return self.master.after(1000, self.updateCounter)


	def updateGui(self, setNextUpdate = True):
		if self.mode == Mode.WORK and self.counter >= self.timers[Mode.WORK]:
			# Switch to take a break mode
			self.changeMode(newMode=Mode.SHORT_BREAK,text=BREAK_TIME)
		elif self.mode == Mode.SHORT_BREAK and self.counter >= self.timers[Mode.SHORT_BREAK]:
			# Switch to focus mode
			self.changeMode(newMode=Mode.WORK,text=FOCUS)
		elif self.mode == Mode.LONG_BREAK and self.counter >= self.timers[Mode.LONG_BREAK]:
			pass

		# Update Graphics #
		# creating the timer dimensions
		windowWidth = self.circleCanvas.winfo_width()
		windowHeight = self.circleCanvas.winfo_height()

		circleXPos = windowWidth/2
		circleYPos = windowHeight/2
		bigCircleRadius  = windowWidth * 0.3
		smallCircleRadius = windowWidth * 0.14
		startingArcAngle = 90.0

		circlePercent = (self.counter / self.timers[self.mode]) * 360.0

		self.circleCanvas.create_rectangle(0,0,windowWidth,windowHeight,fill=BACKGROUND_COLOR)
		createCircle(
			x=circleXPos,
			y=circleYPos,
			r=bigCircleRadius,
			canvas=self.circleCanvas,
			fill=TIMER_BG_COLOR,
			width=2
		)
		#this arc needs to redraw as the timer goes down
		createArc(x=circleXPos, y=circleYPos, r=bigCircleRadius-0.5,
			canvas=self.circleCanvas,
			fill=TIMER_COLOR,
			start=startingArcAngle,
			extent=circlePercent,
			width=2
		)
		createCircle(
			x=circleXPos,
			y=circleYPos,
			r=smallCircleRadius,
			canvas=self.circleCanvas,
			fill=TIMER_CENTER_COLOR,
			width=2
		)

		numberOfPomodoroGUIOffsetX = windowWidth * 0.1
		numberOfPomodoroGUIOffsetY = windowHeight * 0.1
		numberOfPomodoroGUIRadius  = windowWidth * 0.04

		createCircle(
			x=numberOfPomodoroGUIOffsetX,
			y=numberOfPomodoroGUIOffsetY,
			r=numberOfPomodoroGUIRadius,
			canvas=self.circleCanvas,
			fill=NUM_POMODORO_COLOR if (self.numberOfFocusPom >= 1) else BACKGROUND_COLOR,
			width=2
		)
		createCircle(
			x=numberOfPomodoroGUIOffsetX,
			y=windowHeight-numberOfPomodoroGUIOffsetY,
			r=numberOfPomodoroGUIRadius,
			canvas=self.circleCanvas,
			fill=NUM_POMODORO_COLOR if (self.numberOfFocusPom >= 2) else BACKGROUND_COLOR,
			width=2
		)
		createCircle(
			x=windowWidth-numberOfPomodoroGUIOffsetX,
			y=windowHeight-numberOfPomodoroGUIOffsetY,
			r=numberOfPomodoroGUIRadius,
			canvas=self.circleCanvas,
			fill=NUM_POMODORO_COLOR if (self.numberOfFocusPom >= 3) else BACKGROUND_COLOR,
			width=2
		)
		createCircle(
			x=windowWidth-numberOfPomodoroGUIOffsetX,
			y=numberOfPomodoroGUIOffsetY,
			r=numberOfPomodoroGUIRadius,
			canvas=self.circleCanvas,
			fill=NUM_POMODORO_COLOR if (self.numberOfFocusPom >= 4) else BACKGROUND_COLOR,
			width=2
		)

		# Update Time #
		self.currentTimeLabel["text"] = datetime.now().strftime('%a %m/%d/%Y %I:%M') # for am pm use %p

		# Put updateGui to sleep for one second
		if(setNextUpdate):
			return self.master.after(1000, self.updateGui)


	# Not sure if this is good idea
	def reset(self, keypress=False):
		self.counter = 0
		self.btn["text"] = START
		self.timerLabel["text"] = GET_READY
		self.numberOfPomodoro -= 1 if (self.numberOfPomodoro != 0 and keypress) else 0
		self.updateGui(setNextUpdate=False)
		# print("Timer was reset!", "Number of Pomodoros so far:"+str(self.numberOfPomodoro))
		return


	def handle_keypress(self, event):
		# print(event.char, end='') # DEBUG
		if event.char == ' ':
			self.startButton()
		elif event.char == 'r':
			self.reset(keypress=True)
		return


	def changeMode(self, newMode, text):
		self.reset()
		if self.mode == Mode.WORK:
			self.numberOfPomodoro += 1
		self.mode = newMode
		self.timerLabel["text"] = text

		if self.numberOfPomodoro == 4 and newMode == Mode.WORK:
			self.numberOfFocusPom = 0
		elif newMode == Mode.SHORT_BREAK:
			self.numberOfFocusPom += 1
		return


def main():
	args = getCommandLineArgs()

	print("Running")

	print("Study Time:",  int((lambda t : t if (t != None) else WORK_MINUTES)(args['Focus timer length'])), "minutes,", 
		  " Break Time:", int((lambda t : t if (t != None) else BREAK_MINUTES)(args['Break timer length'])),  "minutes")
		  #" Long Break Time:", (lambda t : t if (t != None) else LONG_BREAK/60)(args['Long break timer length']))

	app = Application(  
		windowWidth=args['Window Width'],
		windowHeight=args['Window Height'],
		workMin=args['Focus timer length'],
		breakMin=args['Break timer length'],
		#longBreakMin=args['Long break timer length']
	)
	app.mainloop()

	print("Quiting")
	return 0


if __name__ == "__main__":
	main()