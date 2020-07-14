import tkinter as tk
from datetime import datetime
from enum import Enum
import argparse

# NOTE: make a array of colors so each run of the timer will have a different color
# TODO: Add config file to set a default colors and time

# DEFAULT VALUES #
WINDOW_WIDTH  = 250
WINDOW_HEIGHT = 250

WORK_MINUTES = 25 * 60
BREAK_MINUTES = 5 * 60
LONG_BREAK = 30 * 60
#       -        #

class Mode(Enum):
	WORK_MINUTES = 0
	BREAK_MINUTES = 1
	LONG_BREAK = 2


def getCommandLineArgs():
	parser = argparse.ArgumentParser(description='Setup your Pomodoro Timer')
	parser.add_argument('Focus timer length', metavar='F_Time', type=int, nargs='?', help='The number of minutes you want to focus for')
	parser.add_argument('Break timer length', metavar='B_Time', type=int, nargs='?', help='The number of minutes you want to break for')
	parser.add_argument('Long break timer length', metavar='L_Time', type=int, nargs='?', help='The number of minutes you want to take a long break for')
	parser.add_argument('Window Width', metavar='w', type=int, nargs='?', help='Width')
	parser.add_argument('Window Height', metavar='h', type=int, nargs='?', help='Height')
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
		self.timers = { Mode.WORK_MINUTES:(lambda t : t*60 if (t != None) else WORK_MINUTES)(workMin),
						Mode.BREAK_MINUTES:(lambda t : t*60 if (t != None) else BREAK_MINUTES)(breakMin),
						Mode.LONG_BREAK:(lambda t : t*60 if (t != None) else LONG_BREAK)(longBreakMin) }
		self.mode = Mode.WORK_MINUTES
		self.numberOfPomodoro = 0

		self.master.bind("<Key>", self.handle_keypress)
		# DELETE ME: FOR debug #
		self.master.bind("<Escape>", lambda event : self.master.destroy())

		self.create_widgets()
		self.update()


	def create_widgets(self):
		self.master.columnconfigure(0,minsize=0)
		self.master.rowconfigure([0,1,2],minsize=0)

		self.circleCanvas = tk.Canvas(self,width=self.windowWidth,height=self.windowHeight*0.65,bg="turquoise")
		self.circleCanvas.grid(row=0,column=0,sticky="nsew")

		# creating the text
		self.timerLabel = tk.Label(master=self, text="Focus!",font="Helvetica 18")
		self.timerLabel.grid(row=1,column=0,sticky="nsew",pady=4)

		#create buttons
		self.currentTimeLabel = tk.Label(master=self, font="Helvetica 10")
		self.btn = tk.Button(master=self,text="Start",command=self.startButton)

		self.currentTimeLabel.grid(row=2,column=0,sticky="w", padx=10)
		self.btn.grid(row=2,column=0,sticky="e",padx=15,pady=10, ipadx=20)
		return


	def startButton(self):
		self.btn["text"] = "Pause" if (self.btn["text"] == "Start") else "Start"
		return


	def update(self):
		# Update Pomodoro Timer #
		if self.btn["text"] == "Pause":
			self.counter += 1

		if self.mode == Mode.WORK_MINUTES and self.counter == self.timers[Mode.WORK_MINUTES]:
			# Switch to take a break mode
			self.changeMode(newMode=Mode.BREAK_MINUTES,text="Break Time!")
		elif self.mode == Mode.BREAK_MINUTES and self.counter == self.timers[Mode.BREAK_MINUTES]:
			# Switch to focus mode
			self.changeMode(newMode=Mode.WORK_MINUTES,text="Focus!")
		elif self.mode == Mode.LONG_BREAK and self.counter == self.timers[Mode.LONG_BREAK]:
			pass

		# Update Graphics #
		# creating the timer dimensions
		circleWidth = self.windowWidth/2
		circleHeight = self.windowHeight/3
		bigCircleRadius = 75
		smallCircleRadius = 33
		startingArcAngle = 90

		circlePercent = (self.counter / self.timers[self.mode]) * 360
		# print(circlePercent) # DEBUG

		createCircle(x=circleWidth, y=circleHeight, r=bigCircleRadius, canvas=self.circleCanvas, fill="light green")
		#this arc needs to redraw as the timer goes down
		createArc(x=circleWidth, y=circleHeight, r=bigCircleRadius, canvas=self.circleCanvas, fill="coral", start=startingArcAngle, extent=circlePercent)
		createCircle(x=circleWidth, y=circleHeight, r=smallCircleRadius, canvas=self.circleCanvas, fill="dark grey")

		# Update Time #
		self.currentTimeLabel["text"] = datetime.now().strftime('%a %m/%d/%Y %I:%M')

		# Put window to sleep
		self.master.after(1000, self.update)
		return


	# Not sure if this is good idea
	def reset(self):
		self.counter = 0
		print("RESET THE TIMER!")
		return


	def handle_keypress(self, event):
		# print(event.char, end='') # DEBUG
		if event.char == ' ':
			self.startButton()
		elif event.char == 'r':
			self.reset()
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

	print("Study Time:",  (lambda t : t if (t != None) else WORK_MINUTES/60)(args['Focus timer length']), 
		  " Break Time:", (lambda t : t if (t != None) else BREAK_MINUTES/60)(args['Break timer length']),
		  " Long Break Time:", (lambda t : t if (t != None) else LONG_BREAK/60)(args['Long break timer length']))

	app = Application(master=window,
						windowWidth=args['Window Width'],
						windowHeight=args['Window Height'],
						workMin=args['Focus timer length'],
						breakMin=args['Break timer length'],
						longBreakMin=args['Long break timer length']
					)
	app.mainloop()

	print("Quiting")
	return 0


if __name__ == "__main__":
	main()