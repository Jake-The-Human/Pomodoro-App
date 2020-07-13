import tkinter as tk

def createApp(window):
	window.columnconfigure(0,minsize=250)
	window.rowconfigure([0,1,2],minsize=50)

	
	return

def main():
	window = tk.Tk()

	print("Running")

	createApp(window=window)
	window.mainloop()

	print("Quiting")
	return

if __name__ == "__main__":
	main()