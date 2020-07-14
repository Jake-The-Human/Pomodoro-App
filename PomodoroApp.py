import tkinter as tk
from datetime import datetime

WINDOW_WIDTH  = 250
WINDOW_HEIGHT = 250

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
		self.create_widgets()

	def create_widgets(self):
		self.master.columnconfigure(0,minsize=0)
		self.master.rowconfigure([0,1,2],minsize=0)

		# creating the timer height height
		circleWidth = WINDOW_WIDTH/2
		circleHeight = WINDOW_HEIGHT/3
		circleRadius = 75

		circleCanvas = tk.Canvas(self,w=WINDOW_WIDTH,height=circleHeight*2,bg="turquoise")

		createCircle(x=circleWidth, y=circleHeight, r=circleRadius, canvas=circleCanvas, fill="white")
		#this arc needs to redraw as the timer goes down
		createArc(x=circleWidth, y=circleHeight, r=circleRadius, canvas=circleCanvas, fill="red",start=90,extent=270)
		createCircle(x=circleWidth, y=circleHeight, r=33, canvas=circleCanvas, fill="white")
		circleCanvas.grid(row=0,column=0,sticky="nsew")

		# creating the text
		timerLabel = tk.Label(master=self, text="Focus!",font="Helvetica 18")
		timerLabel.grid(row=1,column=0,sticky="nsew")

		#create buttons
		self.currentTimeLabel = tk.Label(master=self, font="Helvetica 9")
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

	def update(self):

		#update time
		self.currentTimeLabel["text"] = datetime.now().strftime('%a %m/%d/%Y %I:%M')
		self.master.after(1000, self.update)
		
		return


def main():
	window = tk.Tk()
	window.title("Pomodoro")
	window.resizable(False, False)
	window.geometry(str(WINDOW_WIDTH)+'x'+str(WINDOW_HEIGHT))

	print("Running")

	app = Application(master=window)
	app.update()
	app.mainloop()

	print("Quiting")
	return

if __name__ == "__main__":
	main()