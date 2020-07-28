from time import sleep
import sys

import ConstValues as cv

UPDATE_TIME = 1

class Application():
    def __init__(self, workMin=None, breakMin=None, longBreakMin=None):
        def argCheck(arg, defaultValue, scaler=1):
            result = int(arg * scaler) if (arg is not None) else int(defaultValue)
            assert (result != 0), "Timer times must be at least 1 mintute"
            return result

        self.timers  = { 
            cv.Mode.WORK: argCheck(arg=workMin, defaultValue=cv.WORK_SECONDS, scaler=60),
            cv.Mode.SHORT_BREAK: argCheck(arg=breakMin, defaultValue=cv.BREAK_SECONDS, scaler=60),
            cv.Mode.LONG_BREAK: argCheck(arg=longBreakMin, defaultValue=cv.LONG_BREAK_SECONDS, scaler=60)
		}
        self.mode = cv.Mode.WORK
        return
    

    def run(self):
        print(
            "Study Time:", int(self.timers[cv.Mode.WORK]/60), "minutes,", 
			"Break Time:", int(self.timers[cv.Mode.SHORT_BREAK]/60), "minutes"
		)
		#" Long Break Time:",int(self.timers[cv.Mode.LONG_BREAK]))
        
        while True:
            print(cv.modeString(self.mode))
            # Progress bar/Timer
            for counter in range(self.timers[self.mode]):
                self.updateCMDLine(counter)
                sleep(UPDATE_TIME)

            self.changeMode()
            if not self.continueApp():
                break
        
        return

    
    def updateCMDLine(self, counter):
        numberOfChar = 75
        percentComplete = int((counter / self.timers[self.mode]) * numberOfChar)
        print(
            "|" + ("#" * percentComplete) + ("-" * (numberOfChar - percentComplete - 1)) + "|",
            end="\r",
            flush=True
        )
    

    def continueApp(self):
        userInput = input("\n-Nice Work! Continue? Y/N/S(Skip next timer): ").lower()
        if skip := (userInput == 's' or userInput == "skip"):
            self.changeMode()
        return userInput == 'y' or userInput == "yes" or skip
    

    def changeMode(self):
        self.mode = cv.Mode.SHORT_BREAK if (self.mode == cv.Mode.WORK) else cv.Mode.WORK
        cv.playSound()

        