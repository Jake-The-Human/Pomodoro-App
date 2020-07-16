import tkinter as tk
from datetime import datetime
from enum import Enum
import argparse

# NOTE: make a array of colors so each run of the timer will have a different color
# TODO: Add config file to set a default colors and time

# DEFAULT VALUES #
# Window WIDTH AND HEIGHT
WINDOW_WIDTH  = 250
WINDOW_HEIGHT = 250
# TIMER LENGTHS
WORK_MINUTES = 25
BREAK_MINUTES = 5
LONG_BREAK_MINUTES = 30

WORK_SECONDS = WORK_MINUTES * 60
BREAK_SECONDS = BREAK_MINUTES * 60
LONG_BREAK_SECONDS = LONG_BREAK_MINUTES * 60
# COLOR VALUES
BACKGROUND_COLOR = "turquoise"
TIMER_BG_COLOR = "light green"
TIMER_COLOR = "coral"
TIMER_CENTER_COLOR = "dark grey"
#STRINGS
GET_READY = "Get Ready!"
START = "Start"
PAUSE = "Pause"
FOCUS = "Focus!"
BREAK_TIME = "Break Time!"
#       -        #

class Mode(Enum):
	WORK = 0
	SHORT_BREAK = 1
	LONG_BREAK = 2


def getCommandLineArgs():
	parser = argparse.ArgumentParser(description='Setup your Pomodoro Timer')
	parser.add_argument('Focus timer length', metavar='F_Time', type=int, nargs='?', help='The number of minutes you want to focus for. Default: '+str(WORK_MINUTES)+' minutes')
	parser.add_argument('Break timer length', metavar='B_Time', type=int, nargs='?', help='The number of minutes you want to break for. Default: '+str(BREAK_MINUTES)+' minutes')
	#Sparser.add_argument('Long break timer length', metavar='L_Time', type=int, nargs='?', help='The number of minutes you want to take a long break for')
	parser.add_argument('Window Width', metavar='w', type=int, nargs='?', help='Width. Default:'+str(WINDOW_WIDTH))
	parser.add_argument('Window Height', metavar='h', type=int, nargs='?', help='Height. Default:'+str(WINDOW_HEIGHT))
	return vars(parser.parse_args())


# x, y are the center of the circle
def createCircle(x, y, r, canvas, **kwargs):
	return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)


def createArc(x, y, r, canvas, **kwargs):
	return canvas.create_arc(x-r, y-r, x+r, y+r, **kwargs)


class Application(tk.Frame):
	def __init__(self, master=None, windowWidth=None, windowHeight=None, workMin=None, breakMin=None, longBreakMin=None):
		super().__init__(master)

		self.master = master

		self.master.title("Pomodoro")
		self.master.resizable(False, False)

		self.windowWidth = (lambda w : w if (w != None) else WINDOW_WIDTH)(windowWidth)
		self.windowHeight = (lambda h : h if (h != None) else WINDOW_HEIGHT)(windowHeight)
		self.master.geometry(str(self.windowWidth)+'x'+str(self.windowHeight))
		self.pack()

		self.counter = 0
		self.timers = { Mode.WORK:(lambda t : t*60 if (t != None) else WORK_SECONDS)(workMin),
						Mode.SHORT_BREAK:(lambda t : t*60 if (t != None) else BREAK_SECONDS)(breakMin),
						Mode.LONG_BREAK:(lambda t : t*60 if (t != None) else LONG_BREAK_SECONDS)(longBreakMin) }
		self.mode = Mode.WORK
		self.numberOfPomodoro = 0

		self.master.bind("<Key>", self.handle_keypress)
		# NOTE DELETE ME: FOR debug #
		self.master.bind("<Escape>", lambda event : self.master.destroy())

		self.create_widgets()
		self.updateCounter()
		self.updateGui()


	def create_widgets(self):
		self.master.columnconfigure(0,minsize=self.windowWidth)
		self.master.rowconfigure([0,1,2],minsize=1)

		self.circleCanvas = tk.Canvas(self,width=self.windowWidth,height=self.windowHeight*0.65,bg=BACKGROUND_COLOR)
		self.circleCanvas.grid(row=0,column=0,sticky="nsew")

		# creating the text
		self.timerLabel = tk.Label(master=self, text=GET_READY,font="Helvetica 18 underline")
		self.timerLabel.grid(row=1,column=0,sticky="nsew",pady=4)

		#create buttons
		self.currentTimeLabel = tk.Label(master=self, font="Helvetica 10")
		self.btn = tk.Button(master=self,text=START,command=self.startButton)

		self.currentTimeLabel.grid(row=2,column=0,sticky="w", padx=10)
		self.btn.grid(row=2,column=0,sticky="e",padx=15,pady=10, ipadx=20)
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
		circleXPos = self.windowWidth/2
		circleYPos = self.windowHeight/3
		bigCircleRadius = 75.0
		smallCircleRadius = 33.0
		startingArcAngle = 90.0

		circlePercent = (self.counter / self.timers[self.mode]) * 360.0
		# print(circlePercent) # DEBUG

		createCircle(x=circleXPos, y=circleYPos, r=bigCircleRadius, canvas=self.circleCanvas, fill=TIMER_BG_COLOR, width=2)
		#this arc needs to redraw as the timer goes down
		createArc(x=circleXPos, y=circleYPos, r=bigCircleRadius-0.5,
				canvas=self.circleCanvas,
				fill=TIMER_COLOR,
				start=startingArcAngle,
				extent=circlePercent,
				width=2
			)
		createCircle(x=circleXPos, y=circleYPos, r=smallCircleRadius, canvas=self.circleCanvas, fill=TIMER_CENTER_COLOR, width=2)

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
		print("Timer was reset!", "Number of Pomodoros so far:",self.numberOfPomodoro)
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
		self.mode = newMode
		self.timerLabel["text"] = text
		self.numberOfPomodoro += 1
		return


def main():
	args = getCommandLineArgs()
	window = tk.Tk()

	print("Running")

	print("Study Time:",  (lambda t : t if (t != None) else WORK_MINUTES)(args['Focus timer length']), 
		  " Break Time:", (lambda t : t if (t != None) else BREAK_MINUTES)(args['Break timer length']))
		  #" Long Break Time:", (lambda t : t if (t != None) else LONG_BREAK/60)(args['Long break timer length']))

	app = Application(master=window,
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