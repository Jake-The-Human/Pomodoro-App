import tkinter as tk
from datetime import datetime

import ConstValues

# use this for debugging controlls the app's timer
COUNTER = 1

#  x, y are the center of the circle
def createCircle(x, y, r, canvas, **kwargs):
    return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)


def createArc(x, y, r, canvas, **kwargs):
    return canvas.create_arc(x-r, y-r, x+r, y+r, **kwargs)


class Application(tk.Frame):
    def __init__(self, master=None, windowWidth=None, windowHeight=None, workMin=None, breakMin=None, longBreakMin=None):
        if master is None:
            master = tk.Tk()

        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky="nsew")

        self.master = master
        self.master.title("Pomodoro")
        self.master.resizable(False, False)

        def argCheck(arg, defaultValue, scaler=1):
            result = int(arg * scaler) if (arg is not None) else int(defaultValue)
            assert result != 0, "Timer times must be at least 1 mintute"
            return result

        windowWidth = argCheck(arg=windowWidth, defaultValue=ConstValues.WINDOW_WIDTH)
        windowHeight = argCheck(arg=windowHeight, defaultValue=ConstValues.WINDOW_HEIGHT)
        windowDimensions = str(windowWidth) + 'x' + str(windowHeight)
        self.master.geometry(windowDimensions)

        self.counter = 0
        self.timers = {
            ConstValues.Mode.WORK: argCheck(arg=workMin, defaultValue=ConstValues.WORK_SECONDS, scaler=60),
            ConstValues.Mode.SHORT_BREAK: argCheck(arg=breakMin, defaultValue=ConstValues.BREAK_SECONDS, scaler=60),
            ConstValues.Mode.LONG_BREAK: argCheck(arg=longBreakMin, defaultValue=ConstValues.LONG_BREAK_SECONDS, scaler=60)
        }
        self.mode = ConstValues.Mode.WORK
        self.numberOfPomodoro = 0
        self.numberOfFocusPom = 0

        self.master.bind("<Key>", self.handle_keypress)
        # NOTE DELETE ME: FOR debug #
        self.master.bind("<Escape>", lambda event: self.master.destroy())

        self.create_widgets(windowWidth=windowWidth, windowHeight=windowHeight)
        self.updateCounter()
        self.updateGui()

    def create_widgets(self, windowWidth, windowHeight):
        self.circleCanvas = tk.Canvas(
            master=self,
            width=windowWidth,
            height=windowHeight * 0.65,
        )
        self.circleCanvas.grid(row=0, column=0, sticky="nsew")

        # creating the text
        self.timerLabel = tk.Label(
            master=self,
            text=ConstValues.GET_READY,
            font=("Helvetica", int(windowWidth * 0.072), "underline")
        )
        self.timerLabel.grid(row=1, column=0, sticky="nsew", pady=4)

        #create buttons
        self.currentTimeLabel = tk.Label(master=self, font=("Helvetica", int(windowWidth * 0.04)))
        self.btn = tk.Button(
            master=self,
            text=ConstValues.START,
            font=("Helvetica", int(windowWidth * 0.04)),
            command=self.startButton
        )

        self.currentTimeLabel.grid(row=2, column=0, sticky="nsw", padx=2)
        self.btn.grid(row=2, column=0, sticky="nse", padx=12, ipadx=20)

        self.label = tk.Label(
            master=self,
            font=("Helvetica", int(windowWidth * 0.035)),
            text="Study Time: " +
            str(int(self.timers[ConstValues.Mode.WORK] / 60)) +
            " minutes,  Break Time: " +
            str(int(self.timers[ConstValues.Mode.SHORT_BREAK] / 60)) +
            " minutes"
        )
        self.label.grid(row=3, column=0, sticky="nesw", padx=2, pady=2)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure([0,1,2,3], weight=1)
        return

    def startButton(self):
        self.btn["text"] = ConstValues.PAUSE if (self.btn["text"] == ConstValues.START) else ConstValues.START
        if self.timerLabel["text"] == ConstValues.GET_READY:
            self.timerLabel["text"] = ConstValues.FOCUS
        return

    def updateCounter(self):
        # Update Pomodoro Timer #
        if self.btn["text"] == ConstValues.PAUSE:
            self.counter += COUNTER
        # Put updateCounter to sleep for one second
        return self.master.after(1000, self.updateCounter)

    def updateGui(self, setNextUpdate = True):
        # Updates the mode
        if self.mode == ConstValues.Mode.WORK and self.counter >= self.timers[ConstValues.Mode.WORK]:
            # Switch to take a break mode
            self.changeMode(newMode=ConstValues.Mode.SHORT_BREAK, text=ConstValues.BREAK_TIME)
        elif self.mode == ConstValues.Mode.SHORT_BREAK and self.counter >= self.timers[ConstValues.Mode.SHORT_BREAK]:
            # Switch to focus mode
            self.changeMode(newMode=ConstValues.Mode.WORK, text=ConstValues.FOCUS)
        elif self.mode == ConstValues.Mode.LONG_BREAK and self.counter >= self.timers[ConstValues.Mode.LONG_BREAK]:
            pass

        # Update Graphics #
        # creating the timer dimensions
        windowWidth = self.circleCanvas.winfo_width()
        windowHeight = self.circleCanvas.winfo_height()

        circleXPos = windowWidth / 2
        circleYPos = windowHeight / 2
        bigCircleRadius = windowWidth * 0.3
        smallCircleRadius = windowWidth * 0.14
        startingArcAngle = 90.0

        circlePercent = (self.counter / self.timers[self.mode]) * 360.0

        self.circleCanvas.create_rectangle(
            0,
            0,
            windowWidth,
            windowHeight,
            fill=ConstValues.BACKGROUND_COLOR
        )
        createCircle(
            x=circleXPos,
            y=circleYPos,
            r=bigCircleRadius,
            canvas=self.circleCanvas,
            fill=ConstValues.TIMER_BG_COLOR,
            width=2
        )
        #  this arc needs to redraw as the timer goes down
        createArc(
            x=circleXPos,
            y=circleYPos,
            r=bigCircleRadius - 0.5,
            canvas=self.circleCanvas,
            fill=ConstValues.TIMER_COLOR,
            start=startingArcAngle,
            extent=circlePercent,
            width=2
        )
        createCircle(
            x=circleXPos,
            y=circleYPos,
            r=smallCircleRadius,
            canvas=self.circleCanvas,
            fill=ConstValues.TIMER_CENTER_COLOR,
            width=2
        )

        numberOfPomodoroGUIOffsetX = windowWidth * 0.1
        numberOfPomodoroGUIOffsetY = windowHeight * 0.1
        numberOfPomodoroGUIRadius = windowWidth * 0.04

        createCircle(
            x=numberOfPomodoroGUIOffsetX,
            y=numberOfPomodoroGUIOffsetY,
            r=numberOfPomodoroGUIRadius,
            canvas=self.circleCanvas,
            fill=ConstValues.NUM_POMODORO_COLOR if (self.numberOfFocusPom >= 1) else ConstValues.BACKGROUND_COLOR,
            width=2
        )
        createCircle(
            x=numberOfPomodoroGUIOffsetX,
            y=windowHeight-numberOfPomodoroGUIOffsetY,
            r=numberOfPomodoroGUIRadius,
            canvas=self.circleCanvas,
            fill=ConstValues.NUM_POMODORO_COLOR if (self.numberOfFocusPom >= 2) else ConstValues.BACKGROUND_COLOR,
            width=2
        )
        createCircle(
            x=windowWidth-numberOfPomodoroGUIOffsetX,
            y=windowHeight-numberOfPomodoroGUIOffsetY,
            r=numberOfPomodoroGUIRadius,
            canvas=self.circleCanvas,
            fill=ConstValues.NUM_POMODORO_COLOR if (self.numberOfFocusPom >= 3) else ConstValues.BACKGROUND_COLOR,
            width=2
        )
        createCircle(
            x=windowWidth-numberOfPomodoroGUIOffsetX,
            y=numberOfPomodoroGUIOffsetY,
            r=numberOfPomodoroGUIRadius,
            canvas=self.circleCanvas,
            fill=ConstValues.NUM_POMODORO_COLOR if (self.numberOfFocusPom >= 4) else ConstValues.BACKGROUND_COLOR,
            width=2
        )

        # Update Time #
        self.currentTimeLabel["text"] = datetime.now().strftime('%a %m/%d/%Y %I:%M')  # for am pm use %p

        # Put updateGui to sleep for one second
        if(setNextUpdate):
            return self.master.after(1000, self.updateGui)

    # Not sure if this is good idea
    def reset(self, keypress=False):
        self.counter = 0
        self.btn["text"] = ConstValues.START
        self.timerLabel["text"] = ConstValues.GET_READY
        self.numberOfPomodoro -= 1 if (self.numberOfPomodoro != 0 and keypress) else 0
        self.updateGui(setNextUpdate=False)
        ConstValues.playSound(play=not keypress)
        return

    def handle_keypress(self, event):
        # print(event.char, end='') # DEBUG
        if event.char == ConstValues.KEY_PAUSE:
            self.startButton()
        elif event.char == ConstValues.KEY_RESET:
            self.reset(keypress=True)
        return

    def changeMode(self, newMode, text):
        self.reset()
        if self.mode == ConstValues.Mode.WORK:
            self.numberOfPomodoro += 1
        self.mode = newMode
        self.timerLabel["text"] = text

        if self.numberOfPomodoro == 4 and newMode == ConstValues.Mode.WORK:
            self.numberOfFocusPom = 0
        elif newMode == ConstValues.Mode.SHORT_BREAK:
            self.numberOfFocusPom += 1
        return
