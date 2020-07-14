import tkinter as tk
from datetime import datetime

# NOTE: make a array of colors so each run of the timer will have a different color

# NOTE: Think about making thess optional cmd args size and times!
WINDOW_WIDTH  = 250
WINDOW_HEIGHT = 250

WORK_MINUTES = 25 * 60
BREAK_MINUTES = 5 * 60
LONG_BREAK = 30 * 60


# x, y are the center of the circle
def createCircle(x, y, r, canvas, **kwargs):
	return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)


def createArc(x, y, r, canvas, **kwargs):
	return canvas.create_arc(x-r, y-r, x+r, y+r, **kwargs)


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()

		self.master.bind("<Key>", self.handle_keypress)
		# DELETE ME: FOR debug #
		self.master.bind("<Escape>", lambda event : self.master.destroy())

		self.create_widgets()
		self.update()


	def create_widgets(self):
		self.master.columnconfigure(0,minsize=0)
		self.master.rowconfigure([0,1,2],minsize=0)

		self.circleCanvas = tk.Canvas(self,width=WINDOW_WIDTH,height=WINDOW_HEIGHT*0.65,bg="turquoise")
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
		text = self.btn["text"]
		if text == "Start":
			text = "Pause"
		else:
			text = "Start"

		self.btn["text"] = text
		return


	def update(self): # TODO: finish this function
		# Update Pomodoro Timer #

		# Update Graphics #
		# creating the timer dimensions
		circleWidth = WINDOW_WIDTH/2
		circleHeight = WINDOW_HEIGHT/3
		bigCircleRadius = 75
		smallCircleRadius = 33

		createCircle(x=circleWidth, y=circleHeight, r=bigCircleRadius, canvas=self.circleCanvas, fill="white")
		#this arc needs to redraw as the timer goes down
		createArc(x=circleWidth, y=circleHeight, r=bigCircleRadius, canvas=self.circleCanvas, fill="coral",start=90,extent=359)
		createCircle(x=circleWidth, y=circleHeight, r=smallCircleRadius, canvas=self.circleCanvas, fill="white")

		# Update Time #
		self.currentTimeLabel["text"] = datetime.now().strftime('%a %m/%d/%Y %I:%M')

		self.master.after(1000, self.update)
		return


	# Not sure if this is good idea
	def reset(self):
		print("RESET THE TIMER!")
		return

	def handle_keypress(self, event):
		# print(event.char, end='') # DEBUG
		switch = {
			' ': self.startButton,
			'r': self.reset
		}

		switch[event.char]()
		return


def main():
	window = tk.Tk()
	window.title("Pomodoro")
	window.resizable(False, False)
	window.geometry(str(WINDOW_WIDTH)+'x'+str(WINDOW_HEIGHT))

	print("Running")

	app = Application(master=window)
	app.mainloop()

	print("Quiting")

	return


if __name__ == "__main__":
	main()